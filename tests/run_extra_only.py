import json
import sys
from pathlib import Path

# Ensure project root is on sys.path so imports like `preprocess` work
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from preprocess import normalize_vi
from nlp import predict_sentiment


def load_cases(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == '__main__':
    cases = load_cases("tests/test_cases_extra.json")
    print("Running 10 extra test cases:\n")
    ok = 0
    for i, c in enumerate(cases, 1):
        text = c['text']
        expected = c.get('expected')
        norm = normalize_vi(text, use_tokenize=True)
        pred, score = predict_sentiment(norm, neutral_threshold=0.50)
        correct = pred == expected
        mark = '✓' if correct else '✗'
        if correct:
            ok += 1
        print(f"{mark} {i:2d}. {text!r:40s} -> {pred:8s} ({score:.2f}) | expected: {expected}")

    print(f"\nSummary: {ok}/{len(cases)} correct")
