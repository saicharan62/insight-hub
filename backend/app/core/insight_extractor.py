# app/core/insight_extractor.py
from typing import List, Dict
import re

def split_sentences(text: str) -> List[str]:
    # very lightweight splitter
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p.strip() for p in parts if p.strip()]

def extract_insights(
    text: str,
    summary: str | None = None,
    sentiment: str | None = None,
    keywords: list[str] | None = None,
) -> Dict:
    """
    Rule-based insight extraction on top of NLP outputs.
    Returns:
      - key_points: important sentences
      - action_items: 'do' style lines
      - questions: explicit questions
      - tone: mapped from sentiment
      - tags: from keywords
    """
    raw_summary = summary or text
    sents = split_sentences(raw_summary)

    # key points = top 3–5 sentences from summary
    key_points = sents[:5]

    # simple action-item detector
    action_items: List[str] = []
    question_items: List[str] = []

    for s in sents:
        lower = s.lower()
        if "?" in s:
            question_items.append(s)
        # rough heuristic for “do something” style sentences
        if any(
            word in lower
            for word in ["should", "need to", "must", "plan to", "will ", "let's ", "decided to"]
        ):
            action_items.append(s)

    # fallback: if no key points, at least return full summary
    if not key_points and raw_summary:
        key_points = [raw_summary]

    # tone mapping from sentiment label
    sentiment = (sentiment or "neutral").lower()
    if "pos" in sentiment:
        tone = "optimistic / constructive"
    elif "neg" in sentiment:
        tone = "concerned / risky"
    else:
        tone = "neutral / observational"

    return {
        "key_points": key_points,
        "action_items": action_items,
        "questions": question_items,
        "tone": tone,
        "tags": keywords or [],
    }
