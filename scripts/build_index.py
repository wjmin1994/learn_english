#!/usr/bin/env python3
"""扫描 articles/*.md：
1. 生成 articles/index.json（文章列表）；
2. 把所有文章内容嵌入 index.html 的 <script id="articles-data">，
   这样单独打开 index.html（例如在 Claude App 里预览）也能播放。
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTICLES = ROOT / "articles"
INDEX_HTML = ROOT / "index.html"

items = []
for md in sorted(ARTICLES.glob("*.md"), reverse=True):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", md.stem):
        continue
    content = md.read_text(encoding="utf-8")
    first = content.splitlines()[0]
    title = re.sub(r"^#\s*\d{4}-\d{2}-\d{2}\s*·\s*", "", first).strip("# ").strip()
    items.append({"date": md.stem, "title": title, "file": f"articles/{md.name}", "content": content})

listing = [{k: v for k, v in it.items() if k != "content"} for it in items]
(ARTICLES / "index.json").write_text(json.dumps(listing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# 嵌入 index.html；转义 "</" 防止提前结束 <script>
data = json.dumps(items, ensure_ascii=False).replace("</", "<\\/")
html = INDEX_HTML.read_text(encoding="utf-8")
pattern = re.compile(r'(<script id="articles-data" type="application/json">)[\s\S]*?(</script>)')
if not pattern.search(html):
    raise SystemExit("index.html 里找不到 <script id=\"articles-data\">")
html = pattern.sub(lambda m: m.group(1) + data + m.group(2), html, count=1)
INDEX_HTML.write_text(html, encoding="utf-8")
print(f"articles/index.json 和 index.html: {len(items)} 篇")
