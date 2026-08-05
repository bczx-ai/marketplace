---
name: openclaw-tavily-search
displayName: Tavily 搜索
description: 通过 Tavily API 进行网页搜索（Brave 替代方案）。当用户要求搜索网页、查找来源或链接，且 Brave 网页搜索不可用时使用。
version: 0.1.0
tags:
  - data_analysis
license: Unknown
---

# Tavily Search

Use the bundled script to search the web with Tavily.

## Requirements

- Provide API key via either:
  - environment variable: `TAVILY_API_KEY`, or
  - `~/.openclaw/.env` line: `TAVILY_API_KEY=...`

## Commands

Run from the OpenClaw workspace:

```bash
# raw JSON (default)
python3 {baseDir}/scripts/tavily_search.py --query "..." --max-results 5

# include short answer (if available)
python3 {baseDir}/scripts/tavily_search.py --query "..." --max-results 5 --include-answer

# stable schema (closer to web_search): {query, results:[{title,url,snippet}], answer?}
python3 {baseDir}/scripts/tavily_search.py --query "..." --max-results 5 --format brave

# human-readable Markdown list
python3 {baseDir}/scripts/tavily_search.py --query "..." --max-results 5 --format md
```

## Output

### raw (default)
- JSON: `query`, optional `answer`, `results: [{title,url,content}]`

### brave
- JSON: `query`, optional `answer`, `results: [{title,url,snippet}]`

### md
- A compact Markdown list with title/url/snippet.

## Notes

- Keep `max-results` small by default (3–5) to reduce token/reading load.
- Prefer returning URLs + snippets; fetch full pages only when needed.
