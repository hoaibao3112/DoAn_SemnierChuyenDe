"""
Detailed evaluation printing confusion matrix for each threshold.
"""
import json
from collections import defaultdict
from nlp import predict_sentiment
from preprocess import normalize_vi


def load_tests(path="tests/test_cases.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


LABELS = ["POSITIVE","NEUTRAL","NEGATIVE"]


def evaluate(threshold, tests):
    confusion = {e: {p:0 for p in LABELS} for e in LABELS}
    correct = 0
    for case in tests:
        text = case["text"]
        expected = case["expected"]
        norm = normalize_vi(text)
        pred, score = predict_sentiment(norm, neutral_threshold=threshold)
        confusion[expected][pred] += 1
        if pred == expected:
            correct += 1
    return correct, len(tests), confusion


def print_confusion(confusion):
    print("Expected -> Predicted")
    print("\t" + "\t".join(LABELS))
    for e in LABELS:
        row = [str(confusion[e][p]) for p in LABELS]
        print(f"{e}\t" + "\t".join(row))


def main():
    tests = load_tests()
    thresholds = [0.50, 0.45, 0.40, 0.35, 0.30]
    for t in thresholds:
        correct, total, confusion = evaluate(t, tests)
        acc = correct/total*100
        print("="*40)
        print(f"Threshold={t:.2f} -> {acc:.1f}% ({correct}/{total})")
        print_confusion(confusion)

if __name__ == '__main__':
    main()
