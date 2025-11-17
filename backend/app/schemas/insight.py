# app/schemas/insight.py
from pydantic import BaseModel
from typing import Optional

class InsightCreate(BaseModel):
    title: str
    content: str
    tags: Optional[str] = None

class InsightUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None

class InsightResponse(BaseModel):
    id: int
    summary: Optional[str] = None
    sentiment: Optional[str] = None
    keywords: Optional[str] = None
    user_id: int

    class Config:
        from_attributes = True
