import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from preprocess import normalize_vi
from nlp import predict_sentiment
from db import add_record

EXTRA_PATH = ROOT / 'tests' / 'test_cases_extra.json'

def main():
    cases = json.loads(EXTRA_PATH.read_text(encoding='utf-8'))
    print(f"Inserting {len(cases)} extra cases into DB with current pipeline predictions...")
    for i, c in enumerate(cases, 1):
        text = c['text']
        norm = normalize_vi(text, use_tokenize=True)
        pred, score = predict_sentiment(norm)
        add_record(text=norm, sentiment=pred, score=score)
        print(f"{i:2d}. {text!r} -> {pred} ({score:.2f})")
    print("Done.")

if __name__ == '__main__':
    main()
