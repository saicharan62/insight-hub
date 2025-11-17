import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import SessionLocal
from app.models.insight import Insight
from app.models.embedding import InsightEmbedding
from app.core.clustering import generate_embedding

db = SessionLocal()

insights = db.query(Insight).all()
for ins in insights:
    # skip if embedding already exists
    exists = db.query(InsightEmbedding).filter(InsightEmbedding.insight_id == ins.id).first()
    if exists:
        continue
    text = ins.summary or ins.content
    vec = generate_embedding(text)
    emb = InsightEmbedding(insight_id=ins.id, vector=vec, cluster_id=None)
    db.add(emb)
    db.commit()
    print("Backfilled embedding for insight", ins.id)

db.close()
