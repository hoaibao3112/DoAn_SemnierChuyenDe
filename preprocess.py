
import re
import functools
@functools.lru_cache(maxsize=2048)
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
    if not isinstance(text, str):
        text = str(text or "")
    text = text.strip().lower()

    # Quick cleanup: normalize punctuation and repeated spaces
    text = re.sub(r"[\t\n\r]+", " ", text)
    text = re.sub(r"[""'”“‘’]+", "", text)
    text = re.sub(r"[\-_=+*/\\]+", " ", text)

    # Helper: replace whole words using word boundaries to avoid substring mistakes
    def replace_words(s: str, mapping: dict) -> str:
        for k, v in mapping.items():
            pattern = r"\b" + re.escape(k) + r"\b"
            s = re.sub(pattern, v, s)
        return s

    # Mapping for common abbreviations / no-diacritic tokens -> corrected forms
    nodiac_map = {
        "hom": "hôm",
        "hnay": "hôm nay",
        "hn": "hôm nay",
        "rat": "rất",
        "rat nhieu": "rất nhiều",
        "ratnhieu": "rất nhiều",
        "rat nhieu": "rất nhiều",
        "ratnhieu": "rất nhiều",
        "troi": "trời",
        "ratvui": "rất vui",
        "rat vui": "rất vui",
        "buon": "buồn",
        "that bai": "thất bại",
        "thatbai": "thất bại",
        "met moi": "mệt mỏi",
        "metmoi": "mệt mỏi",
        "cam on": "cảm ơn",
        "camon": "cảm ơn",
        "cam on ban": "cảm ơn bạn",
        "toi": "tôi",
        "ban": "bạn",
        "khong": "không",
        "ko": "không",
        "k": "không",
        "dk": "được",
        "dc": "được",
        "ngon": "ngon",
        "tot": "tốt",
        "dep": "đẹp",
        "xau": "xấu",
        "tuyet": "tuyệt",
        "tuyet voi": "tuyệt vời",
        "tuyetvoi": "tuyệt vời",
        "te": "tệ",
        "dang": "đang",
        "chu": "chưa",
        "bt": "bình thường",
        "binh thuong": "bình thường",
        "mon an": "món ăn",
        "monan": "món ăn",
        "dich vu": "dịch vụ",
        "dichvu": "dịch vụ",
        "san pham": "sản phẩm",
        "sanpham": "sản phẩm",
        "nhan vien": "nhân viên",
        "thai do": "thái độ",
        "chat luong": "chất lượng",
        "rat vui": "rất vui",
        "rất vui": "rất vui",
    }

    # More general typo fixes (including spaced variants)
    typo_map = {
        "rat ": "rất ",
        " hom ": " hôm ",
        " hnay ": " hôm nay ",
        " h nay ": " hôm nay ",
        " dc ": " được ",
        " ko ": " không ",
        " k ": " không ",
        " kh ": " không ",
        " khong ": " không ",
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
        " j ": " gì ",
        " gi ": " gì ",
        " lam ": " làm ",
        " dk ": " được ",
        " ms ": " mới ",
        " nua ": " nữa ",
        " thi ": " thì ",
        " cuc ": " cực ",
        " sieu ": " siêu ",
        " tuyet ": " tuyệt ",
        " that vong ": " thất vọng ",
        " hai long ": " hài lòng ",
        " kem ": " kém ",
        " nhan vien ": " nhân viên ",
        " thai do ": " thái độ ",
        " chat luong ": " chất lượng ",
        " san pham ": " sản phẩm ",
        " dich vu ": " dịch vụ ",
        " mon an ": " món ăn ",
        " binh thuong ": " bình thường ",
        " bt ": " bình thường ",
    }

    # If text contains no Vietnamese diacritics, apply nodiac_map first
    if not re.search(r"[\u00C0-\u1EF9]", text):
        text = replace_words(text, nodiac_map)

    # Apply general typo corrections
    text = replace_words(text, typo_map)
    
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
