from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from app.db import Base

class InsightEmbedding(Base):
    __tablename__ = "insight_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    insight_id = Column(Integer, ForeignKey("insights.id", ondelete="CASCADE"), nullable=False)
    vector = Column(ARRAY(Float), nullable=False)
    cluster_id = Column(Integer, index=True)