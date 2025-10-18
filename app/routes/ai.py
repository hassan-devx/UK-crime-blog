from flask import Blueprint
from textblob import TextBlob

ai_bp = Blueprint('ai_bp', __name__)

def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.2:
        return 'positive'
    elif polarity < -0.2:
        return 'negative'
    else:
        return 'neutral'
    

def summarize_post(text):
    lines = text.strip().split('.')
    summary = '. '.join(lines[:2]) + '.' if len(lines) >= 2 else text
    return summary
