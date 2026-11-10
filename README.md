# learn_english

每天把在[墨墨背单词](https://www.maimemo.com/)里学过的单词，自动写成一段简短的日常英语对话（四级以下难度），附中文翻译、生词表（音标和释义）和阅读理解题，方便快速复习。

## 🔊 在线收听

**https://wjmin1994.github.io/learn_english/** —— 点任意一句对话即可朗读，支持全部连续播放、0.7×/0.85×/1× 语速、隐藏中文自测，生词表里的单词也能点着听。

## 工作方式

- 每晚由 Claude 定时任务运行：拉取当天单词 → 选出 10–12 个重点词（新学和"忘记"的词优先）→ 写对话 → 提交到本仓库。
- 单词数据来自[墨墨开放 API](https://open.maimemo.com/)，保存在 `data/words/`。
- 文章保存在 `articles/`，格式和要求见 [CLAUDE.md](CLAUDE.md)。

## 本地运行

```bash
export MAIMEMO_TOKEN=你的墨墨开放API Token   # 墨墨 App：我的 → 更多设置 → 实验功能 → 开放 API
python3 scripts/fetch_today_words.py
```

## 文章列表

<!-- 新文章加在最上面 -->
- [2026-11-10 · A New Job](articles/2026-11-10.md) —— employ, excite, establish, mention, wage, worth, unique, drop, unless, supper, fit, carry
