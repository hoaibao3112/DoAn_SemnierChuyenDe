"""
Reset the sentiments database and seed it with test cases.

Usage (from project root with venv active):
  python .\scripts\reset_and_seed_db.py

What it does:
- Creates a timestamped backup copy of `sentiments.db` if it exists
- Removes the original `sentiments.db`
- Recreates the DB schema via `db.init_db()`
- Loads test cases from `tests/test_cases.json` and `tests/test_cases_extra.json`
  and for each case runs `nlp.predict_sentiment()` and inserts the (normalized) text,
  final sentiment and score into the DB via `db.add_record()`.

This gives you a clean DB containing exactly the test cases and their current
predictions so the Streamlit UI will show the same numbers as `test_runner.py`.
"""
import sys
import shutil
from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from nlp import predict_sentiment
    from preprocess import normalize_vi
    import db
except Exception as e:
    print("Failed to import project modules. Run this from the project root with the venv active.")
    print(e)
    raise

DB_FILE = ROOT / "sentiments.db"

# Backup existing DB if present
if DB_FILE.exists():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = ROOT / f"sentiments.db.backup.{ts}.bak"
    shutil.copy2(DB_FILE, bak)
    print(f"Backed up existing DB to: {bak}")
    # Remove the DB file so we start fresh
    DB_FILE.unlink()
    print("Removed original DB file to start fresh.")

# Re-initialize DB schema
db.init_db()
print("Initialized database schema.")

# Load test cases
cases = []
for fname in (ROOT / "tests" / "test_cases.json", ROOT / "tests" / "test_cases_extra.json"):
    if fname.exists():
        with open(fname, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                cases.extend(data)
                print(f"Loaded {len(data)} cases from {fname.name}")
            except Exception as ex:
                print(f"Failed to read {fname}: {ex}")
    else:
        print(f"Test file not found: {fname}")

if not cases:
    print("No test cases found to seed. Exiting.")
    sys.exit(0)

# Seed DB
added = 0
for c in cases:
    text = c.get("text") if isinstance(c, dict) else str(c)
    if not text:
        continue
    # Normalize text for storage (matches other parts of the project)
    norm = normalize_vi(text, use_tokenize=True)
    # Run prediction on the normalized text
    try:
        res = predict_sentiment(norm, neutral_threshold=0.50)
        if isinstance(res, (tuple, list)):
            label, score = res[0], float(res[1])
        elif isinstance(res, dict):
            label = res.get("label") or res.get("sentiment")
            score = float(res.get("score", 0.0))
        else:
            print(f"Unexpected predict_sentiment return for text={text!r}: {res}")
            continue
        # Normalize label to uppercase for DB
        if isinstance(label, str):
            label = label.strip().upper()

        db.add_record(norm, label, float(score))
        added += 1
    except Exception as e:
        print(f"Error predicting/seeding for text={text!r}: {e}")

print(f"\nSeeding complete. Added {added} records to the database.")
print("You can run: python .\\scripts\\eval_db.py --limit 200")
print("Then restart Streamlit to refresh the UI: streamlit run app.py")
