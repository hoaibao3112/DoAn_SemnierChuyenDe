import os
import json
from textwrap import wrap
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

# Ensure repo root on path for imports
import sys
repo_root = os.path.dirname(os.path.dirname(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from preprocess import normalize_vi
from nlp import predict_sentiment


TESTS_PATH = os.path.join(repo_root, "tests", "test_cases.json")
OUT_DIR = os.path.join(repo_root, "figures")
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, "test_results.png")


def load_tests(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def make_lines(cases):
    lines = []
    header = f"Test results generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    lines.append(header)
    lines.append("")
    for i, case in enumerate(cases, start=1):
        text = case["text"]
        expected = case.get("expected", "")
        normalized = normalize_vi(text, use_tokenize=True)[:200]
        pred, score = predict_sentiment(normalized, neutral_threshold=0.50)
        status = "OK" if pred == expected else "FAIL"
        # Prepare a short block per test
        lines.append(f"{i}. Text: {text}")
        lines.append(f"   Normalized: {normalized}")
        lines.append(f"   Expected: {expected}, Predicted: {pred}, Score: {score:.3f} -> {status}")
        lines.append("")
    return lines


def render_text_image(lines, out_path, width=1200, padding=20, font_size=16):
    # Load a monospaced font if available, otherwise default
    try:
        font = ImageFont.truetype("Consola.ttf", font_size)
    except Exception:
        try:
            font = ImageFont.truetype("consola.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()

    # Estimate image height
    # PIL FreeTypeFont uses getmetrics() for ascent/descent
    try:
        ascent, descent = font.getmetrics()
        line_height = ascent + descent + 6
    except Exception:
        # fallback estimate
        line_height = font.size + 6 if hasattr(font, 'size') else 20
    img_height = padding * 2 + line_height * len(lines)

    img = Image.new("RGB", (width, max(300, img_height)), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    y = padding
    for line in lines:
        # wrap long lines
        wrapped = wrap(line, width=120)
        if not wrapped:
            y += line_height
            continue
        for w in wrapped:
            draw.text((padding, y), w, font=font, fill=(20, 20, 20))
            y += line_height

    img.save(out_path)
    return out_path


def main():
    cases = load_tests(TESTS_PATH)
    lines = make_lines(cases)
    out = render_text_image(lines, OUT_PATH)
    print("Wrote:", out)


if __name__ == "__main__":
    main()
