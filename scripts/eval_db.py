"""
Simple DB inspector: prints sentiment distribution and latest N rows from sentiments.db

Usage:
    python scripts/eval_db.py [--limit N]

This helps verify that the reclassify step updated stored labels.
"""
import sqlite3
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=20, help="How many latest rows to show")
    args = parser.parse_args()

    conn = sqlite3.connect("sentiments.db")
    cur = conn.cursor()

    # Distribution
    cur.execute("SELECT sentiment, COUNT(*) FROM sentiments GROUP BY sentiment")
    rows = cur.fetchall()
    print("Sentiment distribution:")
    for sentiment, count in rows:
        print(f"  {sentiment}: {count}")

    print("\nLatest rows:")
    cur.execute("SELECT id, text, sentiment, score, timestamp FROM sentiments ORDER BY id DESC LIMIT ?", (args.limit,))
    for r in cur.fetchall():
        print(r)

    conn.close()


if __name__ == '__main__':
    main()
