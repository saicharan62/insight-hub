import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import SessionLocal
from app.models.benchmark import BenchmarkResult

db = SessionLocal()

print("\n📊 Benchmark Results in DB:\n" + "-"*50)
for b in db.query(BenchmarkResult).order_by(BenchmarkResult.id.desc()).limit(5).all():
    print(f"ID: {b.id} | Model: {b.model_name} | Device: {b.device} | "
          f"Avg Time: {b.avg_time}s | VRAM Used: {b.vram_used_gb}GB | Date: {b.run_date}")

db.close()
