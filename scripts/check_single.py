from preprocess import normalize_vi
from nlp import predict_sentiment, HAS_TRANSFORMERS, get_sentiment_pipeline
import sqlite3, sys
s = 'Mệt mỏi quá hôm nay'
norm = normalize_vi(s, use_tokenize=True)
print('normalized:', norm)
print('python exe:', sys.executable)
print('HAS_TRANSFORMERS:', HAS_TRANSFORMERS)
try:
    p = get_sentiment_pipeline()
    print('pipeline repr:', type(p), repr(p)[:200])
except Exception as e:
    print('pipeline error:', e)
pred,score = predict_sentiment(norm)
print('predict_sentiment ->', pred, f'({score:.2f})')
# Query DB for matching text
conn = sqlite3.connect('sentiments.db')
c = conn.cursor()
# Use simple LIKE matching on normalized text
c.execute("SELECT id, text, sentiment, score, timestamp FROM sentiments ORDER BY id DESC LIMIT 10")
rows = c.fetchall()
print('last 10 rows count:', len(rows))
for r in rows:
    print(r)
conn.close()