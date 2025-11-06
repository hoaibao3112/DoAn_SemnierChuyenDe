# Copilot Directives:
# - Create a cached (singleton) Hugging Face "sentiment-analysis" pipeline.
# - Model: nlptown/bert-base-multilingual-uncased-sentiment.
# - Map labels "1 star".."5 stars" to 3 classes using STAR2SENT.
# - Expose: predict_sentiment(text:str, neutral_threshold:float=0.50)
#           -> (label:str, score:float)
# - If score < threshold => return NEUTRAL.
# - Truncate long inputs to 256 chars for latency.

from transformers import pipeline
import functools

# Star rating to sentiment mapping
STAR2SENT = {
    "1 star": "NEGATIVE",
    "2 stars": "NEGATIVE",
    "3 stars": "NEUTRAL",
    "4 stars": "POSITIVE",
    "5 stars": "POSITIVE"
}

# Cache the pipeline (singleton pattern)
@functools.lru_cache(maxsize=1)
def get_sentiment_pipeline():
    """
    Load and cache the Hugging Face sentiment analysis pipeline.
    This ensures the model is loaded only once.
    """
    return pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment",
        truncation=True,
        max_length=256
    )


def predict_sentiment(text: str, neutral_threshold: float = 0.50) -> tuple[str, float]:
    """
    Predict sentiment for Vietnamese text.
    
    Args:
        text: Input text (already normalized)
        neutral_threshold: Minimum confidence score threshold
        
    Returns:
        Tuple of (label, score) where:
        - label: POSITIVE, NEUTRAL, or NEGATIVE
        - score: Confidence score (0.0 to 1.0)
    """
    # Truncate long text for latency
    text = text[:256]
    
    # Get cached pipeline
    classifier = get_sentiment_pipeline()
    
    # Predict
    result = classifier(text)[0]
    star_label = result["label"]
    score = result["score"]
    
    # Map star rating to sentiment
    sentiment = STAR2SENT.get(star_label, "NEUTRAL")
    
    # Apply neutral threshold
    if score < neutral_threshold:
        sentiment = "NEUTRAL"
    
    return sentiment, score
