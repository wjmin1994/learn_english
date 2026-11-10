#!/usr/bin/env python3
"""扫描 articles/*.md，生成 articles/index.json，供网页播放器 index.html 读取文章列表。"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTICLES = ROOT / "articles"

items = []
for md in sorted(ARTICLES.glob("*.md"), reverse=True):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", md.stem):
        continue
    first = md.read_text(encoding="utf-8").splitlines()[0]
    title = re.sub(r"^#\s*\d{4}-\d{2}-\d{2}\s*·\s*", "", first).strip("# ").strip()
    items.append({"date": md.stem, "title": title, "file": f"articles/{md.name}"})

(ARTICLES / "index.json").write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"articles/index.json: {len(items)} 篇")
