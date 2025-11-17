from app.db import engine

with engine.connect() as conn:
    print("PostgreSQL Connected")