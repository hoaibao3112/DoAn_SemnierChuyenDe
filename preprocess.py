# Copilot Directives:
# - Implement normalize_vi(text, use_tokenize=False): lowercase, strip,
#   replace vulgar typos (rat->rất, hom->hôm, hnay->hôm nay...), optional underthesea.
# - Keep it deterministic and fast; limit length to 200 chars.

def normalize_vi(text: str, use_tokenize: bool = False) -> str:
    """
    Normalize Vietnamese text for sentiment analysis.
    
    Args:
        text: Raw input text
        use_tokenize: Whether to use underthesea word tokenization (optional)
        
    Returns:
        Normalized text (lowercase, typos fixed, trimmed)
    """
    # Basic normalization
    text = text.strip().lower()
    
    # Common Vietnamese typo corrections
    typo_map = {
        " rat ": " rất ",
        " hom ": " hôm ",
        " hnay ": " hôm nay ",
        " dc ": " được ",
        " ko ": " không ",
        " k ": " không ",
        " cx ": " cũng ",
        " vs ": " với ",
        " voi ": " với ",
        " wa ": " quá ",
        " qua ": " quá ",
        " ntn ": " như thế nào ",
        " trc ": " trước ",
        " sau ": " sau ",
        " tot ": " tốt ",
        " dep ": " đẹp ",
        " xau ": " xấu ",
        " te ": " tệ ",
        " j ": " gì ",
        " gi ": " gì ",
        " lam ": " làm ",
        " dk ": " được ",
        " ms ": " mới ",
        " nua ": " nữa ",
        " thi ": " thì ",
    }
    
    # Apply typo corrections (with word boundaries)
    for typo, correct in typo_map.items():
        text = text.replace(typo, correct)
    
    # Handle start/end typos
    start_typo_map = {
        "rat ": "rất ",
        "hom ": "hôm ",
        "ko ": "không ",
        "k ": "không ",
        "dc ": "được ",
        "wa ": "quá ",
        "qua ": "quá ",
        "tot ": "tốt ",
        "dep ": "đẹp ",
        "xau ": "xấu ",
        "te ": "tệ ",
    }
    
    for typo, correct in start_typo_map.items():
        if text.startswith(typo):
            text = correct + text[len(typo):]
    
    # Optional: use underthesea for word tokenization
    if use_tokenize:
        try:
            from underthesea import word_tokenize
            text = word_tokenize(text, format="text")
        except ImportError:
            pass  # Skip if underthesea not installed
    
    # Limit length to 200 chars
    text = text[:200]
    
    # Final cleanup
    text = " ".join(text.split())  # Remove extra whitespace

    return text
