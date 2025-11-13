import os
import json
import pytest

from preprocess import normalize_vi
from nlp import predict_sentiment


def load_cases(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


BASE = load_cases(os.path.join(os.path.dirname(__file__), "test_cases.json"))
EXTRA = load_cases(os.path.join(os.path.dirname(__file__), "test_cases_extra.json"))
ALL = BASE + EXTRA


@pytest.mark.parametrize("case", ALL)
def test_predict_matches_expected(case):
    text = case["text"]
    expected = case["expected"]

    # Use tokenization if available for more accurate token matching
    normalized = normalize_vi(text, use_tokenize=True)
    pred, score = predict_sentiment(normalized, neutral_threshold=0.50)

    assert pred == expected, (
        f"Mismatch: text={text!r}, normalized={normalized!r}, expected={expected}, got={pred} ({score:.2f})"
    )
