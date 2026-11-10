#!/usr/bin/env python3
"""拉取墨墨背单词「今日学习单词」，按复习优先级排序后保存为 JSON。

用法:
    python3 scripts/fetch_today_words.py            # 保存到 data/words/<北京日期>.json
    python3 scripts/fetch_today_words.py --stdout   # 只打印，不写文件

认证:
    - 云端会话中 Token 由网络代理自动注入，无需任何配置。
    - 本地运行时设置环境变量 MAIMEMO_TOKEN（墨墨 App：我的 → 更多设置 → 实验功能 → 开放 API）。

仅使用 Python 标准库。
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

API = "https://open.maimemo.com/open/api/v1/memo/study"
BEIJING = timezone(timedelta(hours=8))
ROOT = Path(__file__).resolve().parent.parent

# 数字越小越优先：今天新学且忘记 > 忘记 > 新学 > 模糊 > 其他
def priority(item):
    resp = item.get("first_response") or ""
    new = item.get("is_new", False)
    if new and resp == "FORGET":
        return 0
    if resp == "FORGET":
        return 1
    if new:
        return 2
    if resp == "VAGUE":
        return 3
    return 4


def post(path, body):
    req = urllib.request.Request(
        f"{API}/{path}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    token = os.environ.get("MAIMEMO_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            payload = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"请求 {path} 失败: HTTP {e.code} {e.read().decode(errors='replace')[:300]}")
    if not payload.get("success"):
        sys.exit(f"请求 {path} 返回错误: {payload.get('errors')}")
    return payload["data"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stdout", action="store_true", help="只打印结果，不写文件")
    args = ap.parse_args()

    date = datetime.now(BEIJING).strftime("%Y-%m-%d")
    progress = post("get_study_progress", {}).get("progress", {})
    items = post("get_today_items", {"limit": 1000}).get("today_items", [])

    words = []
    for it in items:
        spelling = (it.get("voc_spelling") or "").strip()
        if not spelling:
            continue
        words.append({
            "spelling": spelling,
            "is_new": it.get("is_new", False),
            "first_response": it.get("first_response"),
            "is_finished": it.get("is_finished", False),
            "order": it.get("order"),
            "priority": priority(it),
        })
    words.sort(key=lambda w: (w["priority"], w["order"] or 0))

    result = {
        "date": date,
        "progress": progress,
        "total": len(words),
        "new_count": sum(w["is_new"] for w in words),
        "words": words,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.stdout:
        print(text)
        return

    out = ROOT / "data" / "words" / f"{date}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text + "\n", encoding="utf-8")
    labels = {0: "新学+忘记", 1: "忘记", 2: "新学", 3: "模糊", 4: "熟悉"}
    print(f"{date}: 共 {len(words)} 个单词（新学 {result['new_count']}），已保存到 {out.relative_to(ROOT)}")
    print(f"今日进度: {progress.get('finished')}/{progress.get('total')}")
    for p in range(5):
        group = [w["spelling"] for w in words if w["priority"] == p]
        if group:
            print(f"  [{labels[p]}] {', '.join(group)}")


if __name__ == "__main__":
    main()
