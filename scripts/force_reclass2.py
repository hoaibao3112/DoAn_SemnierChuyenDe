"""
Force-reclassify all rows in sentiments.db using the current pipeline.
This variant ensures the project root is on sys.path so `from nlp import predict_sentiment` works
when executed from the scripts/ directory.

Run from project root (venv active):
  python .\scripts\force_reclass2.py

This script creates a backup `sentiments.db.bak` and prints a per-row diff + summary.
"""
import sys
import shutil
import sqlite3
from pathlib import Path

# Insert project root into sys.path so imports work when running this script directly
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from nlp import predict_sentiment
except Exception as e:
    print("Failed to import predict_sentiment from nlp.py:", e)
    raise

DB_PATH = ROOT / "sentiments.db"
BACKUP_PATH = ROOT / "sentiments.db.bak"

if not DB_PATH.exists():
    raise SystemExit(f"Database not found at {DB_PATH}")

# Make a backup
shutil.copy2(DB_PATH, BACKUP_PATH)
print(f"Backup created: {BACKUP_PATH}")

conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()

cur.execute("SELECT id, text, sentiment, score FROM sentiments ORDER BY id ASC")
rows = cur.fetchall()
print(f"Found {len(rows)} rows to reclassify")

updated = 0
unchanged = 0
errors = 0

for r in rows:
    id_, text, old_label, old_score = r
    try:
        res = predict_sentiment(text, neutral_threshold=0.50)
        if isinstance(res, (tuple, list)):
            new_label, new_score = res[0], float(res[1])
        elif isinstance(res, dict):
            new_label = res.get("label") or res.get("sentiment")
            new_score = float(res.get("score", 0.0))
        else:
            print(f"Row {id_}: unexpected predict_sentiment return type: {type(res)}")
            errors += 1
            continue

        if isinstance(new_label, str):
            new_label = new_label.strip().upper()

        need_update = (str(old_label).upper() != str(new_label)) or (abs(float(old_score) - float(new_score)) > 1e-6)
        if need_update:
            cur.execute(
                "UPDATE sentiments SET sentiment = ?, score = ? WHERE id = ?",
                (new_label, float(new_score), id_),
            )
            conn.commit()
            print(f"Updated id={id_}: {old_label} ({old_score}) -> {new_label} ({new_score:.6f}) | text: {text}")
            updated += 1
        else:
            unchanged += 1
    except Exception as exc:
        print(f"Error processing id={id_} text={text!r}: {exc}")
        errors += 1

print("\nSummary:")
print(f"  Total rows: {len(rows)}")
print(f"  Updated:    {updated}")
print(f"  Unchanged:  {unchanged}")
print(f"  Errors:     {errors}")

conn.close()
print("Done. Re-run `python .\scripts\eval_db.py --limit 50` to verify results.")
