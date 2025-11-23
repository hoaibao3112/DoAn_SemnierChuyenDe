import os
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters.img import ImageFormatter


FIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "figures")
os.makedirs(FIG_DIR, exist_ok=True)

STEP1 = '''# Bước 1 — Tiền xử lý
def preprocess(text: str) -> str:
    """Chuẩn hóa: lowercase, sửa lỗi gõ đơn giản, gom khoảng trắng, giới hạn 200 ký tự."""
    t = text.lower()
    # ví dụ sửa lỗi gõ phổ biến (có thể mở rộng)
    t = t.replace('hom', 'hôm').replace('mon', 'món')
    # gom khoảng trắng
    t = ' '.join(t.split())
    # giới hạn độ dài
    return t[:200]

# Ví dụ sử dụng
raw = "Hom   nay   mon an    rat  ngon  "
print(preprocess(raw))
'''

STEP2 = '''# Bước 2 — Dự đoán cảm xúc (transformers pipeline)
from transformers import pipeline

classifier = pipeline(
    'sentiment-analysis',
    model='nlptown/bert-base-multilingual-uncased-sentiment',
    truncation=True,
    max_length=256
)

def predict(text: str, neutral_threshold: float = 0.35):
    # Gọi model (top_k=None để lấy tất cả labels)
    raw = classifier(text, top_k=None)
    # raw là list of dicts: [{"label": "1 star", "score": 0.12}, ...]
    label_scores = {item['label']: item['score'] for item in raw}
    # Lấy nhãn sao có score cao nhất
    top_star = max(label_scores, key=label_scores.get)
    top_score = label_scores[top_star]

    # Mapping 1-2 -> NEGATIVE, 3 -> NEUTRAL, 4-5 -> POSITIVE
    star = int(top_star.split()[0])
    if top_score < neutral_threshold:
        sentiment = 'NEUTRAL'
    else:
        if star <= 2:
            sentiment = 'NEGATIVE'
        elif star == 3:
            sentiment = 'NEUTRAL'
        else:
            sentiment = 'POSITIVE'
    return sentiment, top_score

# Ví dụ
print(predict('hôm nay món ăn rất ngon'))
'''

STEP3 = '''# Bước 3 — Mapping nhãn + Threshold + Lưu & Hiển thị
def map_star_to_sentiment(label_scores: dict, neutral_threshold: float = 0.35):
    """label_scores: {'1 star': 0.1, '2 stars': 0.05, ...}
       Trả về (sentiment, report_score)"""
    # Convert star-labels to numeric and sum class probs
    star_to_class = {1: 'NEGATIVE', 2: 'NEGATIVE', 3: 'NEUTRAL', 4: 'POSITIVE', 5: 'POSITIVE'}
    class_scores = {'NEGATIVE': 0.0, 'NEUTRAL': 0.0, 'POSITIVE': 0.0}
    for lbl, sc in label_scores.items():
        try:
            star = int(lbl.split()[0])
        except Exception:
            continue
        cls = star_to_class.get(star, 'NEUTRAL')
        class_scores[cls] += sc

    # Determine top-star label and its score for historical behavior
    top_star = max(label_scores.keys(), key=lambda k: label_scores[k])
    top_score = label_scores[top_star]
    top_star_num = int(top_star.split()[0])

    # Apply threshold: if top_score < neutral_threshold, return NEUTRAL
    if top_score < neutral_threshold:
        final = 'NEUTRAL'
    else:
        final = star_to_class.get(top_star_num, 'NEUTRAL')

    # For reporting we prefer the aggregated class probability
    report_score = class_scores.get(final, top_score)
    return final, report_score

# Ví dụ kết hợp với output của pipeline
example_label_scores = {'1 star': 0.02, '2 stars': 0.03, '3 stars': 0.10, '4 stars': 0.30, '5 stars': 0.55}
print(map_star_to_sentiment(example_label_scores, neutral_threshold=0.35))
'''


def render(code: str, out_path: str):
    # Try multiple monospaced fonts (Windows common fallback to Consolas)
    fonts_to_try = ["DejaVu Sans Mono", "Consolas", "Courier New", "Liberation Mono"]
    last_err = None
    for fname in fonts_to_try:
        try:
            formatter = ImageFormatter(font_name=fname, font_size=16, line_numbers=True)
            data = highlight(code, PythonLexer(), formatter)
            with open(out_path, 'wb') as f:
                f.write(data)
            return
        except Exception as e:
            last_err = e
            # try next font
            continue
    # If no font worked, raise the last error for visibility
    raise last_err


if __name__ == '__main__':
    render(STEP1, os.path.join(FIG_DIR, 'code_step1.png'))
    render(STEP2, os.path.join(FIG_DIR, 'code_step2.png'))
    render(STEP3, os.path.join(FIG_DIR, 'code_step3.png'))
    print('Wrote figures:', os.path.join(FIG_DIR, 'code_step1.png'), os.path.join(FIG_DIR, 'code_step2.png'))
