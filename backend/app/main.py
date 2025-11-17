# app/main.py
from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.insight import router as insight_router
from app.db import engine
from app.models.user import Base as UserBase
from app.models.insight import Base as InsightBase
from app.models.embedding import InsightEmbedding  # ensures model import for Alembic / create_all
from fastapi.middleware.cors import CORSMiddleware

# create tables if missing (safe in dev)
UserBase.metadata.create_all(bind=engine)
InsightBase.metadata.create_all(bind=engine)
# InsightEmbedding is imported above but create_all needs the right Base; if your Base is same object, it's fine.

app = FastAPI(title="InsightHub API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(insight_router)  # router already has prefix /insights
