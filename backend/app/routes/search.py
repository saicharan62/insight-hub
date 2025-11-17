from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.core.deps import get_current_user
from app.models.insight import Insight
import numpy as np

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/")
def semantic_search(
    q: str = Query(..., description="Search query"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # 1. Convert query text → embedding
    query_vector = generate_embedding(q)

    # 2. Fetch all insights for the user
    insights = db.query(Insight).filter(Insight.user_id == current_user.id).all()

    if not insights:
        return {"results": []}

    # 3. Collect embeddings from DB
    results = []
    for ins in insights:
        if not ins.embedding:
            continue

        vec = np.array(ins.embedding.vector)
        score = np.dot(query_vector, vec) / (
            np.linalg.norm(query_vector) * np.linalg.norm(vec)
        )

        results.append({
            "id": ins.id,
            "summary": ins.summary,
            "score": float(score)
        })

    # 4. Sort by similarity score
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return {"query": q, "results": results}
