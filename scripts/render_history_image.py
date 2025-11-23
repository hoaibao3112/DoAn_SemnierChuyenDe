#!/usr/bin/env python3
"""Render recent sentiment DB records to a PNG table image.

Reads from SQLite `sentiments.db` by default (or from `figures/sentiments_export.csv` if DB missing),
selects 10 most recent records and writes `figures/figure_recent_records.png`.
"""
from pathlib import Path
import sqlite3
import csv
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:
    print("Pillow is required. Please install pillow in your venv.")
    sys.exit(1)

try:
    import pandas as pd
except Exception:
    pd = None

DB_DEFAULT = Path("sentiments.db")
CSV_FALLBACK = Path("figures/sentiments_export.csv")
OUT = Path("figures/figure_recent_records.png")


def read_from_db(db_path, limit=10):
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    q = "SELECT id, text, sentiment, score, timestamp FROM sentiments ORDER BY timestamp DESC LIMIT ?"
    cur.execute(q, (limit,))
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    conn.close()
    return cols, rows


def read_from_csv(csv_path, limit=10):
    rows = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for r in reader:
            rows.append(r)
    # assume header contains same columns
    return header, rows[:limit]


def render_table_image(columns, rows, out_path):
    # layout params
    col_widths = [60, 700, 120, 100, 180]  # id, text, sentiment, score, timestamp
    header_height = 36
    row_height = 30
    padding = 10

    ncols = len(columns)
    nrows = max(1, len(rows))
    width = sum(col_widths[:ncols]) + padding * 2
    height = header_height + nrows * row_height + padding * 2

    img = Image.new("RGB", (width, height), "#ffffff")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 14)
        font_bold = ImageFont.truetype("arialbd.ttf", 14)
    except Exception:
        font = ImageFont.load_default()
        font_bold = font

    x = padding
    y = padding

    # header background
    draw.rectangle([x, y, width - padding, y + header_height], fill="#f0f0f0")
    cx = x
    for i, col in enumerate(columns[:ncols]):
        w = col_widths[i]
        draw.text((cx + 6, y + 8), str(col), font=font_bold, fill="#000000")
        cx += w

    # rows
    y += header_height
    for ridx, row in enumerate(rows):
        # alternate background
        if ridx % 2 == 0:
            draw.rectangle([x, y, width - padding, y + row_height], fill="#ffffff")
        else:
            draw.rectangle([x, y, width - padding, y + row_height], fill="#fbfbfb")

        cx = x
        for i in range(ncols):
            w = col_widths[i]
            cell = ''
            try:
                cell = str(row[i])
            except Exception:
                cell = ''
            # crop long text
            if i == 1 and len(cell) > 120:
                cell = cell[:117] + '...'
            draw.text((cx + 6, y + 7), cell, font=font, fill="#000000")
            cx += w

        y += row_height

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    print("Wrote:", str(out_path))


def main():
    # prefer DB, fallback to CSV
    if DB_DEFAULT.exists():
        cols, rows = read_from_db(DB_DEFAULT, limit=10)
    elif CSV_FALLBACK.exists():
        cols, rows = read_from_csv(CSV_FALLBACK, limit=10)
    else:
        print("No DB or CSV fallback found. Expected `sentiments.db` or `figures/sentiments_export.csv`.")
        sys.exit(2)

    render_table_image(cols, rows, OUT)


if __name__ == '__main__':
    main()
