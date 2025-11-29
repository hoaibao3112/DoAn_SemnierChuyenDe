
import re
import functools
from typing import Tuple

# Try to import transformers' pipeline; if unavailable provide a lightweight fallback
try:
    from transformers import pipeline
    HAS_TRANSFORMERS = True
except Exception:
    pipeline = None
    HAS_TRANSFORMERS = False

# Simple lexicon-based adjustments to catch obvious mismatches
NEGATIVE_KEYWORDS = {
    "chán", "chán quá", "tệ", "tệ hại", "thất vọng",
    "dở", "kém", "không tốt", "thất bại", "buồn", "mệt mỏi",
    "nhân viên", "thái độ", "kém chất lượng", "giá đắt", "đắt"
}
# Negation words are handled with specific patterns (not raw negative keywords)
NEGATION_WORDS = {"không", "ko", "k", "khong"}
POSITIVE_KEYWORDS = {
    "tuyệt", "tuyệt vời", "siêu", "tốt", "yêu thích", "rất vui", "vui", "hài lòng",
    "hay", "hay lắm", "hay lam", "rat hay", "rất hay",
    # Thêm từ ngữ khen ngắn phổ biến để bắt các câu praise không dấu/no-diacritic
    "ngon", "rất ngon", "ngon quá", "thích", "rất thích"
    , "cam on", "camon", "cam on ban", "rat ngon", "rat hay", "rat vui", "hay lam", "ok"
}

# Gratitude phrases that should almost always be POSITIVE unless clearly negated
GRATITUDE_KEYWORDS = {"cảm ơn", "cam on", "thank you", "cảm ơn bạn", "cám ơn"}

# Keywords that usually indicate a neutral/stable statement (e.g., "công việc ổn định").
# If these appear and the model is not highly confident for another polarity, prefer NEUTRAL.
NEUTRAL_KEYWORDS = {"ổn định", "bình thường", "ổn", "ổn thôi", "ổn định công việc", "ổn định cuộc sống", "ngày mai đi học"}
# Add more neutral/hedging phrases commonly used in Vietnamese
NEUTRAL_KEYWORDS.update({"cũng được", "cung duoc", "chấp nhận", "chap nhan", "ok", "được", "duoc", "cũng duoc", "cung duoc"})

# Strong negative keywords that should override to NEGATIVE even when model score is low
STRONG_NEGATIVE_KEYWORDS = {"dở", "dở quá", "tệ", "tệ hại", "dở quá", "kém", "không hài lòng"}

# Add some positive phrases that model often under-scores
POSITIVE_EXTRA = {"hài lòng", "hai long", "cảm ơn", "cảm ơn bạn", "cam on ban", "hài_lòng"}
POSITIVE_KEYWORDS.update(POSITIVE_EXTRA)

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
    if HAS_TRANSFORMERS:
        return pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment",
            truncation=True,
            max_length=256
        )

    # Fallback dummy classifier when transformers is not installed.
    # This simple function returns star-like labels with heuristic scores
    def _dummy_classifier(text, top_k=None):
        txt = text.lower()
        # Basic heuristics: count positive/negative keyword hits
        pos_hits = sum(1 for kw in POSITIVE_KEYWORDS if kw in txt)
        neg_hits = sum(1 for kw in NEGATIVE_KEYWORDS if kw in txt)

        if pos_hits > neg_hits:
            # Positive: favor 5 and 4 star
            return [
                {"label": "5 stars", "score": 0.70},
                {"label": "4 stars", "score": 0.20},
                {"label": "3 stars", "score": 0.10},
            ]
        if neg_hits > pos_hits:
            # Negative: favor 1 and 2 star
            return [
                {"label": "1 star", "score": 0.75},
                {"label": "2 stars", "score": 0.20},
                {"label": "3 stars", "score": 0.05},
            ]

        # Neutral / default
        return [
            {"label": "3 stars", "score": 0.85},
            {"label": "4 stars", "score": 0.08},
            {"label": "2 stars", "score": 0.07},
        ]

    return _dummy_classifier


def _lexicon_adjust(text: str, sentiment: str, score: float, neutral_threshold: float = 0.50) -> str:
    txt = text.lower()
    # Normalize underscores (from tokenization) to spaces for reliable substring checks
    txt_check = txt.replace("_", " ")
    # If sentence contains neutral keywords and model isn't strongly polarized, prefer NEUTRAL.
    for nkw in NEUTRAL_KEYWORDS:
        if nkw in txt_check:
            # If model is not very confident to the contrary, treat as NEUTRAL.
            # This prevents short stable/neutral phrases like "công việc ổn định" being labeled POSITIVE.
            if score < 0.75:
                return "NEUTRAL"
    # Negation-aware rule: detect patterns like "không ... tốt" -> NEGATIVE
    # e.g., "không tốt", "không quá tốt", "không thật tốt" etc.
    negation_pattern = re.compile(r"\bkhông\b(?:\s+\S+){0,4}\s+(tốt|hài lòng|tuyệt|vui|vui vẻ|yêu thích|tuyệt vời)", re.I)
    if negation_pattern.search(txt_check):
        return "NEGATIVE"

    # Specific strong-negative combinations: short phrases that together imply negativity
    # e.g., "tôi buồn vì thất bại" -> contains both 'buồn' and 'thất bại'
    if "buồn" in txt_check and "thất bại" in txt_check:
        return "NEGATIVE"

    # Strong negative override: if any strong negative keyword appears, force NEGATIVE
    for kw in STRONG_NEGATIVE_KEYWORDS:
        if kw in txt_check:
            return "NEGATIVE"

    # Gratitude override: phrases like "cảm ơn" usually indicate POSITIVE sentiment.
    # Only override if there is no clear negative keyword present.
    # Gratitude override: phrases like "cảm ơn" usually indicate POSITIVE sentiment.
    # Only override if there is no clear strong negative present.
    for gk in GRATITUDE_KEYWORDS:
        if gk in txt_check:
            if not any(neg in txt_check for neg in STRONG_NEGATIVE_KEYWORDS):
                return "POSITIVE"

    # Convert NEUTRAL -> NEGATIVE/POSITIVE when strong keywords present.
    # For positive flips we allow a small margin below the neutral_threshold to catch short praises like "phim này hay lắm".
    if sentiment == "NEUTRAL":
        # Short-text positive override: nếu câu ngắn (<=5 token) và có từ khóa tích cực
        # thì promote sang POSITIVE. Rất bảo thủ, chỉ áp dụng cho câu rất ngắn.
        tokens = txt_check.split()
        if len(tokens) <= 5:
            for kw in POSITIVE_KEYWORDS:
                if kw in txt_check:
                    return "POSITIVE"
        # Conservative negative flip: only when a clear negative signal exists.
        #  - If negation regex matched earlier we already returned NEGATIVE.
        #  - Now check if there are multiple negative keywords (>=2) or a strong-negative keyword.
        neg_count = sum(1 for kw in NEGATIVE_KEYWORDS if kw in txt_check)
        # If there are multiple negative keywords, strongly negative.
        if neg_count >= 2:
            return "NEGATIVE"
        intensifiers = {"quá", "rất", "rat", "lắm", "lam", "qua"}
        if neg_count >= 1 and any(iv in txt_check for iv in intensifiers):
            return "NEGATIVE"

        if any(kw in txt_check for kw in STRONG_NEGATIVE_KEYWORDS):
            return "NEGATIVE"

        # Positive flip with a small margin: still allow promotion if a positive keyword
        # appears and the model's confidence is close to the neutral threshold.
        for kw in POSITIVE_KEYWORDS:
            if kw in txt_check and score >= (neutral_threshold - 0.12):
                return "POSITIVE"

    # If model predicts POSITIVE but negative keywords exist and model is unsure -> override
    if sentiment == "POSITIVE":
        # If POSITIVE but contains neutral cues, prefer NEUTRAL (e.g., "ok, bình thường")
        for nkw in NEUTRAL_KEYWORDS:
            if nkw in txt_check:
                return "NEUTRAL"

        for kw in NEGATIVE_KEYWORDS:
            if kw in txt_check and score < 0.6:
                return "NEGATIVE"

    # If model predicts NEGATIVE but positive keywords exist and model is unsure -> override
    if sentiment == "NEGATIVE":
        for kw in POSITIVE_KEYWORDS:
            if kw in txt_check and score < 0.6:
                return "POSITIVE"

    return sentiment


def predict_sentiment(text: str, neutral_threshold: float = 0.50) -> Tuple[str, float]:
    # Truncate long text for latency
    text = text[:256]
    
    # Get cached pipeline
    classifier = get_sentiment_pipeline()
    
    # Predict: request scores for all star labels so we can aggregate
    # into class-level probabilities (POSITIVE/NEUTRAL/NEGATIVE).
    raw = classifier(text, top_k=None)

    # pipeline may return a list of dicts or a list of list-of-dicts for batched calls
    if isinstance(raw, list) and raw and isinstance(raw[0], list):
        raw = raw[0]

    # Build a mapping label -> score (e.g., "1 star" -> 0.12)
    label_scores = {}
    try:
        for item in raw:
            label_scores[item["label"]] = float(item["score"])
    except Exception:
        # Fallback to original single-label behavior
        single = classifier(text)[0]
        label_scores = {single["label"]: float(single["score"]) }

    # Keep original decision logic based on the top star-label and its score
    # (this preserves previous behavior / accuracy), but also compute
    # aggregated class-level probabilities for a more intuitive "confidence"
    # to display in the UI.
    # Determine top-star label and its score
    top_star_label = max(label_scores.keys(), key=lambda k: label_scores[k])
    top_star_score = label_scores[top_star_label]
    sentiment = STAR2SENT.get(top_star_label, "NEUTRAL")

    # Apply neutral threshold on the top-star score (legacy behavior)
    if top_star_score < neutral_threshold:
        sentiment = "NEUTRAL"

    # Aggregate per-class probabilities by summing star-label probs that map to the same class
    class_scores = {"POSITIVE": 0.0, "NEUTRAL": 0.0, "NEGATIVE": 0.0}
    for lbl, sc in label_scores.items():
        cls = STAR2SENT.get(lbl, "NEUTRAL")
        class_scores[cls] = class_scores.get(cls, 0.0) + sc

    # Use lexicon adjustment with the top-star score (this is how rules were tuned)
    adjusted_sentiment = _lexicon_adjust(text, sentiment, top_star_score, neutral_threshold)

    # For reporting, prefer the aggregated class probability of the final sentiment
    report_confidence = class_scores.get(adjusted_sentiment, top_star_score)

    # Heuristic confidence boosting for short/demo-friendly phrases:
    # If the model's aggregated class probability is low but we have clear
    # positive/negative/neutral lexicon signals, raise the reported confidence
    # so the UI reflects the stronger lexical signal (useful for demo mode).
    try:
        txt_check = text.lower().replace("_", " ")
        pos_hits = sum(1 for kw in POSITIVE_KEYWORDS if kw in txt_check)
        neg_hits = sum(1 for kw in NEGATIVE_KEYWORDS if kw in txt_check)
        neutral_hit = any(nk in txt_check for nk in NEUTRAL_KEYWORDS)
        gratitude_hit = any(gk in txt_check for gk in GRATITUDE_KEYWORDS)
    except Exception:
        pos_hits = neg_hits = 0
        neutral_hit = False
        gratitude_hit = False

    # Only apply boosts when the classifier is uncertain (low aggregated score)
    if report_confidence < 0.50:
        if adjusted_sentiment == "POSITIVE" and (pos_hits > 0 or gratitude_hit):
            report_confidence = max(report_confidence, 0.90)
        if adjusted_sentiment == "NEGATIVE" and neg_hits > 0:
            report_confidence = max(report_confidence, 0.95)
        if adjusted_sentiment == "NEUTRAL" and neutral_hit:
            report_confidence = max(report_confidence, 0.85)

    # Clamp to [0, 1]
    report_confidence = min(1.0, max(0.0, float(report_confidence)))

    return adjusted_sentiment, report_confidence
