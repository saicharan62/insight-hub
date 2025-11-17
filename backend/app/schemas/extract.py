# app/schemas/extract.py
from typing import List
from pydantic import BaseModel

class InsightExtractionRequest(BaseModel):
    title: str | None = None
    content: str
    tags: str | None = None

class InsightExtractionResponse(BaseModel):
    key_points: List[str]
    action_items: List[str]
    questions: List[str]
    tone: str
    tags: List[str]
