from pathlib import Path
import sys
sys.path.insert(0, str(Path('.').resolve()))
import nlp
from preprocess import normalize_vi

cases = [
"Hôm nay tôi rất vui",
"Món ăn này dở quá",
"Thời tiết bình thường",
"Rat vui hom nay",
"Công việc ổn định",
"Phim này hay lắm",
"Tôi buồn vì thất bại",
"Ngày mai đi học",
"Cảm ơn bạn rất nhiều",
"Mệt mỏi quá hôm nay",
]
print('HAS_TRANSFORMERS =', getattr(nlp, 'HAS_TRANSFORMERS', None))
print('get_sentiment_pipeline() =>', type(nlp.get_sentiment_pipeline()))
print('\nPredictions:')
for t in cases:
    norm = normalize_vi(t, use_tokenize=True)
    pred, score = nlp.predict_sentiment(norm)
    print(f"{t!r} -> {pred} ({score:.2f}) | norm={norm!r}")
