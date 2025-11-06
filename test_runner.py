# Copilot Directives:
# - Load tests/test_cases.json (text, expected).
# - Run normalize_vi + predict_sentiment.
# - Print accuracy as percentage with 1 decimal place.
# - Print compact confusion matrix counts (expected -> predicted).
# - Exit code 0 if accuracy >= 0.65 else 1 (useful for CI).

import json
import sys
from collections import defaultdict
from preprocess import normalize_vi
from nlp import predict_sentiment

def load_test_cases(file_path: str = "tests/test_cases.json"):
    """Load test cases from JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_tests():
    """Run all test cases and compute metrics."""
    print("=" * 60)
    print("Vietnamese Sentiment Assistant - Test Runner")
    print("=" * 60)
    
    # Load test cases
    try:
        test_cases = load_test_cases()
    except FileNotFoundError:
        print("❌ Error: tests/test_cases.json not found!")
        sys.exit(1)
    
    print(f"\nRunning {len(test_cases)} test cases...\n")
    
    # Run predictions
    results = []
    confusion_matrix = defaultdict(lambda: defaultdict(int))
    
    for i, case in enumerate(test_cases, 1):
        text = case["text"]
        expected = case["expected"]
        
        # Preprocess and predict
        normalized = normalize_vi(text)
        predicted, score = predict_sentiment(normalized, neutral_threshold=0.50)
        
        # Store result
        is_correct = predicted == expected
        results.append(is_correct)
        confusion_matrix[expected][predicted] += 1
        
        # Print result
        status = "✓" if is_correct else "✗"
        print(f"{status} Test {i:2d}: {text[:50]:50s} | Expected: {expected:8s} | Predicted: {predicted:8s} ({score:.2f})")
    
    # Calculate accuracy
    accuracy = sum(results) / len(results)
    accuracy_pct = accuracy * 100
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"ACCURACY: {accuracy_pct:.1f}% ({sum(results)}/{len(results)})")
    print("=" * 60)
    
    # Print confusion matrix
    print("\nConfusion Matrix (Expected → Predicted):")
    print("-" * 60)
    labels = ["POSITIVE", "NEUTRAL", "NEGATIVE"]
    
    # Header
    print(f"{'Expected':12s} | ", end="")
    for label in labels:
        print(f"{label:8s}", end=" ")
    print("\n" + "-" * 60)
    
    # Rows
    for expected in labels:
        print(f"{expected:12s} | ", end="")
        for predicted in labels:
            count = confusion_matrix[expected][predicted]
            print(f"{count:8d}", end=" ")
        print()
    
    print("=" * 60)
    
    # Exit with appropriate code
    if accuracy >= 0.65:
        print("\n✅ PASS: Accuracy >= 65%")
        sys.exit(0)
    else:
        print(f"\n❌ FAIL: Accuracy < 65% (got {accuracy_pct:.1f}%)")
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
