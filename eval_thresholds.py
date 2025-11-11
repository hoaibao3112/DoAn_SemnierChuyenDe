"""
Evaluate test cases at different neutral_threshold values to see effect on accuracy.
"""
import json
from nlp import predict_sentiment
from preprocess import normalize_vi


def load_tests(path="tests/test_cases.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate(threshold, tests):
    correct = 0
    total = len(tests)
    for case in tests:
        text = case["text"]
        expected = case["expected"]
        norm = normalize_vi(text)
        pred, score = predict_sentiment(norm, neutral_threshold=threshold)
        if pred == expected:
            correct += 1
    return correct, total


def main():
    tests = load_tests()
    thresholds = [0.50, 0.45, 0.40, 0.35, 0.30]
    print("Threshold -> Accuracy")
    for t in thresholds:
        correct, total = evaluate(t, tests)
        acc = correct / total * 100
        print(f"{t:.2f} -> {acc:.1f}% ({correct}/{total})")

if __name__ == '__main__':
    main()
