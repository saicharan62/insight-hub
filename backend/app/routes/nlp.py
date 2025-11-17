from fastapi import APIRouter
from app.core.nlp import analyze_text

router = APIRouter(prefix="/nlp", tags=["NLP"])

@router.post("/analyze")
def analyze_route(payload: dict):
    text = payload.get("text", "")
    return analyze_text(text)
