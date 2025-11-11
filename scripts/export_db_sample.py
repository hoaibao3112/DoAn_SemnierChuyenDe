import sqlite3
import csv
from pathlib import Path

repo = Path(__file__).resolve().parent.parent
db_path = repo / 'sentiments.db'
out_csv = repo / 'artifacts' / 'db_sample.csv'
out_svg = repo / 'figures' / '04_db_sample.svg'

out_csv.parent.mkdir(parents=True, exist_ok=True)
out_svg.parent.mkdir(parents=True, exist_ok=True)

if not db_path.exists():
    print('DB not found:', db_path)
    raise SystemExit(1)

con = sqlite3.connect(db_path)
cur = con.cursor()
cur.execute("SELECT id, text, sentiment, score, timestamp FROM sentiments ORDER BY id DESC LIMIT 10")
rows = cur.fetchall()

with open(out_csv, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['id','text','sentiment','score','timestamp'])
    for r in rows:
        w.writerow(r)

print('Wrote', out_csv)

# Generate a simple SVG table
lines = ["ID | Text | Sentiment | Score | Time"]
for r in rows:
    id_, text, sent, score, ts = r
    text_short = text if len(text) <= 60 else text[:57] + '...'
    lines.append(f"{id_} | {text_short} | {sent} | {score:.2f} | {ts}")

# Render SVG
width = 1200
line_h = 20
height = max(120, (len(lines)+2)*line_h + 40)
svg_lines = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
             '<rect width="100%" height="100%" fill="#fff"/>',
             '<style>.mono{font:14px/1.2 "Courier New", monospace; fill:#222}</style>']

y = 30
svg_lines.append(f'<text x="20" y="20" class="mono">Hình 4 — DB sample (10 bản ghi mới nhất)</text>')
for ln in lines:
    svg_lines.append(f'<text x="20" y="{y}" class="mono">{ln}</text>')
    y += line_h

svg_lines.append('</svg>')

with open(out_svg, 'w', encoding='utf-8') as f:
    f.write('\n'.join(svg_lines))

print('Wrote', out_svg)
