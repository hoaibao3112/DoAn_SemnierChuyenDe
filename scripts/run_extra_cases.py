import os
import sys
import json

# Ensure repo root is on sys.path so imports like `preprocess` and `nlp` resolve
repo_root = os.path.dirname(os.path.dirname(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from preprocess import normalize_vi
from nlp import predict_sentiment


def load_cases(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    repo_root = os.path.dirname(os.path.dirname(__file__))
    cases_path = os.path.join(repo_root, "tests", "test_cases_extra.json")
    cases = load_cases(cases_path)

    total = len(cases)
    passed = 0

    print(f"Running {total} extra test cases:\n")
    for i, case in enumerate(cases, start=1):
        text = case["text"]
        expected = case["expected"]
        normalized = normalize_vi(text, use_tokenize=True)
        pred, score = predict_sentiment(normalized, neutral_threshold=0.50)

        ok = pred == expected
        if ok:
            passed += 1

        print(f"{i:2d}. Text: {text!r}")
        print(f"    Normalized: {normalized!r}")
        print(f"    Expected: {expected}, Predicted: {pred}, Score: {score:.3f} -> {'OK' if ok else 'FAIL'}\n")

    acc = passed / total if total else 0.0
    print(f"Summary: {passed}/{total} passed. Accuracy: {acc:.2%}")


if __name__ == "__main__":
    main()
