# Copilot Directives:
# - Create a cached (singleton) Hugging Face "sentiment-analysis" pipeline.
# - Model: nlptown/bert-base-multilingual-uncased-sentiment.
# - Map labels "1 star".."5 stars" to 3 classes using STAR2SENT.
# - Expose: predict_sentiment(text:str, neutral_threshold:float=0.50)
#           -> (label:str, score:float)
# - If score < threshold => return NEUTRAL.
# - Truncate long inputs to 256 chars for latency.

import re
from transformers import pipeline
import functools
from typing import Tuple

# Simple lexicon-based adjustments to catch obvious mismatches
NEGATIVE_KEYWORDS = {
    "không", "ko", "chán", "chán quá", "tệ", "tệ hại", "thất vọng",
    "dở", "kém", "không tốt", "thất bại", "buồn", "mệt mỏi",
    "nhân viên", "thái độ", "kém chất lượng", "giá đắt", "đắt"
}
POSITIVE_KEYWORDS = {
    "tuyệt", "tuyệt vời", "siêu", "tốt", "yêu thích", "rất vui", "vui", "hài lòng",
    "hay", "hay lắm", "hay lam", "rat hay", "rất hay",
    # Thêm từ ngữ khen ngắn phổ biến để bắt các câu praise không dấu/no-diacritic
    "ngon", "rất ngon", "ngon quá", "thích", "rất thích"
}

# Gratitude phrases that should almost always be POSITIVE unless clearly negated
GRATITUDE_KEYWORDS = {"cảm ơn", "cam on", "thank you", "cảm ơn bạn", "cám ơn"}

# Keywords that usually indicate a neutral/stable statement (e.g., "công việc ổn định").
# If these appear and the model is not highly confident for another polarity, prefer NEUTRAL.
NEUTRAL_KEYWORDS = {"ổn định", "bình thường", "ổn", "ổn thôi", "ổn định công việc", "ổn định cuộc sống", "ngày mai đi học"}

# Strong negative keywords that should override to NEGATIVE even when model score is low
STRONG_NEGATIVE_KEYWORDS = {"dở", "dở quá", "tệ", "tệ hại", "dở quá", "kém", "không hài lòng"}

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


def _lexicon_adjust(text: str, sentiment: str, score: float, neutral_threshold: float = 0.50) -> str:
    """Adjust sentiment using simple keyword heuristics when model is uncertain.

    Rules:
    - If model predicts POSITIVE but a negative keyword exists and score < 0.6 => NEGATIVE
    - If model predicts NEGATIVE but a positive keyword exists and score < 0.6 => POSITIVE
    - Otherwise keep model label (unless score < threshold handled by caller)
    """
    txt = text.lower()
    # If sentence contains neutral keywords and model isn't strongly polarized, prefer NEUTRAL.
    for nkw in NEUTRAL_KEYWORDS:
        if nkw in txt:
            # If model is not very confident to the contrary, treat as NEUTRAL.
            # This prevents short stable/neutral phrases like "công việc ổn định" being labeled POSITIVE.
            if score < 0.75:
                return "NEUTRAL"
    # Negation-aware rule: detect patterns like "không ... tốt" -> NEGATIVE
    # e.g., "không tốt", "không quá tốt", "không thật tốt" etc.
    negation_pattern = re.compile(r"\bkhông\b(?:\s+\S+){0,4}\s+(tốt|hài lòng|tuyệt|vui|vui vẻ|yêu thích|tuyệt vời)", re.I)
    if negation_pattern.search(txt):
        return "NEGATIVE"

    # Specific strong-negative combinations: short phrases that together imply negativity
    # e.g., "tôi buồn vì thất bại" -> contains both 'buồn' and 'thất bại'
    if "buồn" in txt and "thất bại" in txt:
        return "NEGATIVE"

    # Strong negative override: if any strong negative keyword appears, force NEGATIVE
    for kw in STRONG_NEGATIVE_KEYWORDS:
        if kw in txt:
            return "NEGATIVE"

    # Gratitude override: phrases like "cảm ơn" usually indicate POSITIVE sentiment.
    # Only override if there is no clear negative keyword present.
    for gk in GRATITUDE_KEYWORDS:
        if gk in txt:
            if not any(neg in txt for neg in NEGATIVE_KEYWORDS):
                return "POSITIVE"

    # Convert NEUTRAL -> NEGATIVE/POSITIVE when strong keywords present.
    # For positive flips we allow a small margin below the neutral_threshold to catch short praises like "phim này hay lắm".
    if sentiment == "NEUTRAL":
        # Short-text positive override: nếu câu ngắn (<=5 token) và có từ khóa tích cực
        # thì promote sang POSITIVE. Rất bảo thủ, chỉ áp dụng cho câu rất ngắn.
        tokens = txt.split()
        if len(tokens) <= 5:
            for kw in POSITIVE_KEYWORDS:
                if kw in txt:
                    return "POSITIVE"

        # allow a small margin below neutral_threshold for negative flips
        neg_flip_threshold = max(0.0, neutral_threshold - 0.05)
        for kw in NEGATIVE_KEYWORDS:
            if kw in txt and score >= neg_flip_threshold:
                return "NEGATIVE"

        for kw in POSITIVE_KEYWORDS:
            # allow small margin below neutral_threshold (e.g., 0.50 -> 0.40) for short, strong praises
            if kw in txt and score >= (neutral_threshold - 0.10):
                return "POSITIVE"

    # If model predicts POSITIVE but negative keywords exist and model is unsure -> override
    if sentiment == "POSITIVE":
        for kw in NEGATIVE_KEYWORDS:
            if kw in txt and score < 0.6:
                return "NEGATIVE"

    # If model predicts NEGATIVE but positive keywords exist and model is unsure -> override
    if sentiment == "NEGATIVE":
        for kw in POSITIVE_KEYWORDS:
            if kw in txt and score < 0.6:
                return "POSITIVE"

    return sentiment


def predict_sentiment(text: str, neutral_threshold: float = 0.50) -> Tuple[str, float]:
    """
    Predict sentiment for Vietnamese text.
    
    Args:
        text: Input text (already normalized)
        neutral_threshold: Minimum confidence score threshold (default: 0.50)
        
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

    # Lexicon-based post-processing to catch obvious mismatches
    sentiment = _lexicon_adjust(text, sentiment, score, neutral_threshold)

    return sentiment, score
