# app/routes/insight.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.insight import Insight
from app.schemas.insight import InsightCreate, InsightResponse, InsightUpdate
from app.core.deps import get_current_user
from app.core.nlp import analyze_text
from app.models.embedding import InsightEmbedding
from app.schemas.cluster import ClusterResponse
from app.core.clustering import generate_embedding, cluster_texts
from app.schemas.extract import InsightExtractionRequest, InsightExtractionResponse
from app.core.insight_extractor import extract_insights


router = APIRouter(prefix="/insights", tags=["Insights"])

@router.post("/", response_model=InsightResponse)
def create_insight(
    data: InsightCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    analysis = analyze_text(data.content)

    new_insight = Insight(
        title=data.title,
        content=data.content,
        tags=data.tags,
        user_id=current_user.id,
        summary=analysis.get("summary"),
        keywords=",".join(analysis.get("keywords", [])),
        sentiment=analysis.get("sentiment")
    )

    db.add(new_insight)
    db.commit()
    db.refresh(new_insight)

    # compute cluster for all user's insights (interactive)
    insights = db.query(Insight).filter(Insight.user_id == current_user.id).all()
    texts = [ins.summary or "" for ins in insights]
    ids = [ins.id for ins in insights]

    clusters = cluster_texts(texts, insight_ids=ids)

    # delete old embeddings for user's insights and write fresh ones
    db.query(InsightEmbedding).filter(InsightEmbedding.insight_id.in_(ids)).delete(synchronize_session=False)
    db.commit()

    for ins in insights:
        vec = generate_embedding(ins.summary or "")
        # find cluster id
        assigned = None
        for c in clusters:
            if ins.id in c['insight_ids']:
                assigned = c['cluster_id']
                break
        entry = InsightEmbedding(insight_id=ins.id, vector=vec, cluster_id=assigned)
        db.add(entry)
    db.commit()

    return new_insight


@router.get("/", response_model=list[InsightResponse])
def get_insights(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Insight).filter(Insight.user_id == current_user.id).all()


@router.patch("/{insight_id}", response_model=InsightResponse)
def update_insight(
    insight_id: int,
    data: InsightUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    insight = db.query(Insight).filter(Insight.id == insight_id).first()
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    if insight.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this insight.")

    if data.title is not None:
        insight.title = data.title
    if data.content is not None:
        insight.content = data.content
    if data.tags is not None:
        insight.tags = data.tags

    db.commit()
    db.refresh(insight)
    return insight


@router.delete("/{insight_id}")
def delete_insight(
    insight_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    insight = db.query(Insight).filter(Insight.id == insight_id).first()
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found.")
    if insight.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this insight.")

    db.delete(insight)
    db.commit()
    return {"message": "Deleted successfully"}


@router.get("/clusters")
def get_clusters(db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    insights = db.query(Insight).filter(Insight.user_id == current_user.id).all()
    if not insights:
        return {"clusters": []}

    texts = [i.summary for i in insights]
    ids = [i.id for i in insights]

    clusters = cluster_texts(texts, ids)
    return {"clusters": clusters}

@router.post("/extract", response_model=InsightExtractionResponse)
def extract_from_raw(
    payload: InsightExtractionRequest,
    current_user = Depends(get_current_user)
):
    """
    Take raw note content, run NLP + extraction, return structured insights.
    Does NOT save anything to DB.
    """
    analysis = analyze_text(payload.content)

    extracted = extract_insights(
        text=payload.content,
        summary=analysis["summary"],
        sentiment=analysis["sentiment"],
        keywords=analysis["keywords"],
    )

    return extracted

@router.get("/{insight_id}/extract", response_model=InsightExtractionResponse)
def extract_from_saved(
    insight_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Load an existing insight by ID, then run extraction on its summary/content.
    """
    ins = (
        db.query(Insight)
        .filter(Insight.id == insight_id, Insight.user_id == current_user.id)
        .first()
    )

    if not ins:
        raise HTTPException(status_code=404, detail="Insight not found")

    # if summary already exists, we use it; else fall back to content
    base_text = ins.summary or ins.content or ""
    # keywords stored as comma string
    kw_list = (ins.keywords.split(",") if ins.keywords else [])

    extracted = extract_insights(
        text=base_text,
        summary=ins.summary,
        sentiment=ins.sentiment,
        keywords=kw_list,
    )

    return extracted
