from transformers import pipeline
from keybert import KeyBERT

summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0, torch_dtype="auto")
sentiment_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest", device=0, torch_dtype="auto")
kw_model = KeyBERT()

def analyze_text(text: str):
    #summarization
    try:
        summary = summarizer(text, max_length=1000, min_length=15, do_sample=False)[0]['summary_text']
    except Exception:
        summary = "Summary unavailable."
    
    #keywords
    try:
        keywords = [kw[0] for kw in kw_model.extract_keywords(text, top_n=5)]
    except Exception:
        keywords = []
    #sentiment
    try:
        sentiment = sentiment_analyzer(text[:512])[0]['label']
    except Exception:
        sentiment = "neutral"
    
    return {
        "summary": summary,
        "sentiment": sentiment,
        "keywords": keywords
    } 


