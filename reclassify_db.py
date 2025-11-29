from db import list_latest, init_db
import sqlite3
from preprocess import normalize_vi
from nlp import predict_sentiment
from typing import Optional

DB_FILE = "sentiments.db"


def reclassify_all(limit: int = 5000) -> int:
    init_db()
    updated = 0
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, text FROM sentiments ORDER BY id ASC LIMIT ?", (limit,))
        rows = cursor.fetchall()

        for _id, text in rows:
            normalized = normalize_vi(text)
            sentiment, score = predict_sentiment(normalized)
            cursor.execute("UPDATE sentiments SET sentiment=?, score=? WHERE id=?", (sentiment, score, _id))
            updated += 1
        conn.commit()

    return updated


if __name__ == '__main__':
    n = reclassify_all(limit=5000)
    print(f'Reclassification done. Updated {n} records.')
