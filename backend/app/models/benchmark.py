from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.db import Base

class BenchmarkResult(Base):
    __tablename__ = "benchmark_results"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False)
    device = Column(String, nullable=False)   # 'CPU' or 'GPU'
    avg_time = Column(Float, nullable=False)
    vram_used_gb = Column(Float)
    vram_total_gb = Column(Float)
    run_date = Column(DateTime(timezone=True), server_default=func.now())
