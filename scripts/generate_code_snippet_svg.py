from pathlib import Path
import re

repo = Path(__file__).resolve().parent.parent
nlp_file = repo / 'nlp.py'
out_svg = repo / 'figures' / '06_code_threshold.svg'

if not nlp_file.exists():
    print('nlp.py not found')
    raise SystemExit(1)

text = nlp_file.read_text(encoding='utf-8')
# Extract STAR2SENT and predict_sentiment function blocks
m1 = re.search(r"STAR2SENT\s*=\s*\{[\s\S]*?\}\n", text)
start = m1.start() if m1 else 0
m2 = re.search(r"def predict_sentiment\([\s\S]*?\):\n[\s\S]*?return sentiment, score", text)
end = m2.end() if m2 else min(start+800, len(text))
snippet = text[start:end]

# Prepare lines, escape HTML
lines = snippet.splitlines()
esc_lines = [ln.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;') for ln in lines]

width = 1200
line_h = 18
height = max(120, (len(esc_lines)+4)*line_h + 40)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
       '<rect width="100%" height="100%" fill="#fff"/>',
       '<style>.mono{font:14px/1.2 "Courier New", monospace; fill:#111}</style>']

svg.append(f'<text x="20" y="24" class="mono">Hình 6 — Đoạn mã (STAR2SENT, threshold, predict_sentiment) trích từ nlp.py</text>')

y = 50
for ln in esc_lines:
    svg.append(f'<text x="12" y="{y}" class="mono">{ln}</text>')
    y += line_h

svg.append('</svg>')
out_svg.parent.mkdir(parents=True, exist_ok=True)
out_svg.write_text('\n'.join(svg), encoding='utf-8')
print('Wrote', out_svg)
