---
name: openclaw-aisa-web-search-tavily
displayName: "Web Search by Tavily"
description: "通过 Tavily API 代理实现 AI 优化的网页搜索，提供简洁且相关的结果，并支持深度查询或新闻聚焦查询。"
version: 1.0.0
tags:
  - knowledge_management
license: "Unknown"
---

# AIsa Tavily Search

AI-optimized web search using Tavily API through AIsa's unified gateway. Designed for AI agents - returns clean, relevant content.

## Search

```bash
node {baseDir}/scripts/search.mjs "query"
node {baseDir}/scripts/search.mjs "query" -n 10
node {baseDir}/scripts/search.mjs "query" --deep
node {baseDir}/scripts/search.mjs "query" --topic news
```

## Options

- `-n <count>`: Number of results (default: 5, max: 20)
- `--deep`: Use advanced search for deeper research (slower, more comprehensive)
- `--topic <topic>`: Search topic - `general` (default) or `news`
- `--days <n>`: For news topic, limit to last n days

## Extract content from URL

```bash
node {baseDir}/scripts/extract.mjs "https://example.com/article"
```

Notes:
- Needs `AISA_API_KEY` from https://marketplace.aisa.one
- Powered by AIsa's unified API gateway (https://aisa.one)
- Use `--deep` for complex research questions
- Use `--topic news` for current events
