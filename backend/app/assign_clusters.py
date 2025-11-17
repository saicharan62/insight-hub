import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import SessionLocal
from app.models.embedding import InsightEmbedding
from app.models.insight import Insight
from app.core.clustering import generate_embedding, find_cluster

db = SessionLocal()

# load all embeddings and assign cluster ids by simple sequential clustering
all_embs = db.query(InsightEmbedding).all()
vectors = [e.vector for e in all_embs]

for i, emb in enumerate(all_embs):
    if emb.cluster_id:
        continue
    # cluster against other vectors (excluding self for initial pass)
    others = [v for idx, v in enumerate(vectors) if idx != i]
    cluster_index = find_cluster(emb.vector, others, threshold=0.65)
    # map to cluster id: if cluster_index <= len(others) -> assign existing index+1
    # simple heuristic:
    emb.cluster_id = cluster_index
    db.add(emb)
db.commit()
db.close()
print("Reassigned cluster ids")
