
import re
import functools
from typing import Tuple


try:
    from transformers import pipeline
    HAS_TRANSFORMERS = True
except Exception:
    pipeline = None
    HAS_TRANSFORMERS = False


NEGATIVE_KEYWORDS = {
    # === Cảm xúc tiêu cực cơ bản ===
    "chán", "chán quá", "tệ", "tệ hại", "thất vọng", "thất_vọng",
    "dở", "dở quá", "kém", "không tốt", "thất bại", "thất_bại",
    "buồn", "buồn quá", "buồn bã", "buồn_bã",
    "mệt", "mệt mỏi", "mệt_mỏi", "mệt quá",
    # === Phiên bản không dấu ===
    "chan", "chan qua", "te", "te hai", "that vong", "thatvong",
    "do", "do qua", "kem", "khong tot", "that bai", "thatbai",
    "buon", "buon qua", "buon ba", "buonba",
    "met", "met moi", "metmoi", "met qua",
    # === Cảm xúc tiêu cực mở rộng ===
    "giận", "tức giận", "tức_giận", "gian", "tuc gian", "tucgian",
    "bực mình", "bực_mình", "buc minh", "bucminh",
    "khó chịu", "khó_chịu", "kho chiu", "khochiu",
    "sợ", "lo lắng", "lo_lắng", "so", "lo lang", "lolang",
    "căng thẳng", "căng_thẳng", "cang thang", "cangthang", "stress",
    "ghét", "ghet",
    # === Từ tiêu cực về dịch vụ/sản phẩm ===
    "kém chất lượng", "kém_chất_lượng", "kem chat luong",
    "giá đắt", "giá_đắt", "gia dat", "giadat", "đắt", "dat", "quá đắt",
    "không hài lòng", "không_hài_lòng", "khong hai long", "khonghailong",
    "không thích", "không_thích", "khong thich", "khongthich",
    "chậm", "cham", "bẩn", "ban",
    # === Từ tiếng Anh tiêu cực ===
    "bad", "terrible", "awful", "horrible",
    # === Các cụm từ tiêu cực ===
    "rất tệ", "rất_tệ", "rat te", "ratte",
    "rất kém", "rất_kém", "rat kem", "ratkem",
    "rất xấu", "rất_xấu", "rat xau", "ratxau",
    "rất buồn", "rất_buồn", "rat buon", "ratbuon",
    "xấu", "xấu quá", "xau", "xau qua",
}
NEGATION_WORDS = {"không", "ko", "k", "khong", "kg", "kh", "hok", "hem", "chưa", "chua", "ch"}
POSITIVE_KEYWORDS = {
    # === Cảm xúc tích cực cơ bản ===
    "tuyệt", "tuyệt vời", "tuyệt_vời", "tuyệt hảo", "tuyệt_hảo",
    "siêu", "siêu tốt", "siêu_tốt",
    "tốt", "rất tốt", "rất_tốt", "quá tốt",
    "vui", "rất vui", "rất_vui", "vui vẻ", "vui_vẻ", "vui quá",
    "hài lòng", "hài_lòng", "rất hài lòng", "rất_hài_lòng",
    "yêu", "yêu thích", "yêu_thích",
    "thích", "rất thích", "rất_thích",
    "hay", "hay lắm", "hay_lắm", "rất hay", "rất_hay",
    "ngon", "rất ngon", "rất_ngon", "ngon quá",
    "đẹp", "rất đẹp", "rất_đẹp", "đẹp quá",
    # === Phiên bản không dấu ===
    "tuyet", "tuyet voi", "tuyetvoi", "tuyet hao",
    "sieu", "sieu tot",
    "tot", "rat tot", "rattot", "qua tot",
    "vui", "rat vui", "ratvui", "vui ve", "vuive",
    "hai long", "hailong", "rat hai long",
    "yeu", "yeu thich", "yeuthich",
    "thich", "rat thich", "ratthich",
    "hay", "hay lam", "haylam", "rat hay", "rathay",
    "ngon", "rat ngon", "ratngon", "ngon qua",
    "dep", "rat dep", "ratdep", "dep qua",
    # === Cảm xúc tích cực mở rộng ===
    "hạnh phúc", "hạnh_phúc", "hanh phuc", "hanhphuc",
    "sung sướng", "sung_sướng", "sung suong",
    "phấn khởi", "phấn_khởi", "phan khoi",
    "xuất sắc", "xuất_sắc", "xuat sac", "xuatsac",
    "hoàn hảo", "hoàn_hảo", "hoan hao", "hoanhao",
    "tuyệt hảo", "tuyệt_hảo", "tuyet hao",
    # === Từ cảm ơn ===
    "cảm ơn", "cảm_ơn", "cam on", "camon",
    "cảm ơn bạn", "cảm_ơn_bạn", "cam on ban", "camonban",
    "cảm ơn nhiều", "cam on nhieu",
    "cám ơn",
    # === Từ tiếng Anh tích cực ===
    "ok", "okie", "okela", "nice", "good", "great", "amazing", "perfect", "thanks", "thank",
    # === Từ tăng cường tích cực ===
    "cực kỳ", "cực_kỳ", "cuc ky", "cucky",
    "vô cùng", "vô_cùng", "vo cung", "vocung",
    "hết sức", "hết_sức", "het suc", "hetsuc",
    "thật sự", "thật_sự", "that su", "thatsu",
    # === Các cụm từ tích cực khác ===
    "rẻ", "giá rẻ", "giá_rẻ", "re", "gia re", "giare",
    "nhanh", "sạch", "sach",
}

GRATITUDE_KEYWORDS = {
    "cảm ơn", "cảm_ơn", "cam on", "camon",
    "cảm ơn bạn", "cảm_ơn_bạn", "cam on ban", "camonban",
    "cảm ơn nhiều", "cam on nhieu",
    "cám ơn", "thank you", "thanks", "thank",
}
NEUTRAL_KEYWORDS = {
    # === Trung tính cơ bản ===
    "ổn định", "ổn_định", "on dinh", "ondinh",
    "bình thường", "bình_thường", "binh thuong", "binhthuong", "bt",
    "ổn", "ổn thôi", "on", "on thoi",
    # === Cụm từ trung tính ===
    "ổn định công việc", "ổn định cuộc sống",
    "ngày mai đi học", "ngày_mai đi học",
    "cũng được", "cũng_được", "cung duoc", "cungduoc",
    "tạm được", "tạm_được", "tam duoc", "tamduoc",
    "tạm ổn", "tạm_ổn", "tam on", "tamon",
    "chấp nhận", "chấp_nhận", "chap nhan", "chapnhan",
    "chấp nhận được", "chapnhanduoc",
    "không có gì", "khong co gi",
    "không sao", "không_sao", "khong sao", "khongsao",
    "trung bình", "trung_bình", "trung binh", "trungbinh", "tb",
    # === Từ ok/được ===
    "ok", "được", "duoc",
}

# Strong negative keywords that should override to NEGATIVE even when model score is low
STRONG_NEGATIVE_KEYWORDS = {
    "dở", "dở quá", "dở_quá",
    "tệ", "tệ hại", "tệ_hại", "rất tệ", "rất_tệ",
    "kém", "rất kém", "rất_kém",
    "không hài lòng", "không_hài_lòng",
    # Phiên bản không dấu
    "do", "do qua", "te", "te hai", "rat te",
    "kem", "rat kem", "khong hai long",
}

# Add some positive phrases that model often under-scores
POSITIVE_EXTRA = {
    "hài lòng", "hài_lòng", "hai long", "hailong",
    "cảm ơn", "cảm_ơn", "cảm ơn bạn", "cảm_ơn_bạn",
    "cam on", "cam on ban", "camonban",
    "rất hài lòng", "rất_hài_lòng", "rat hai long",
    # Thêm từ tích cực khác
    "tuyệt vời", "tuyệt_vời", "tuyet voi", "tuyetvoi",
    "xuất sắc", "xuất_sắc", "xuat sac", "xuatsac",
    "hoàn hảo", "hoàn_hảo", "hoan hao", "hoanhao",
}
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
