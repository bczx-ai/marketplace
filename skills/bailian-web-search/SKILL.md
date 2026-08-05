---
name: bailian-web-search
displayName: "Bailian Web Search"
description: "通过百炼（阿里云ModelStdio）API实现AI优化网络搜索，为大模型返回多源、精简的搜索结果。"
version: 1.0.4
tags:
  - knowledge_management
license: "Unknown"
---

# Bailian Web Search

AI-optimized web search using Bailian WebSearch(Enable_search) API. Designed for AI agents - returns clean, relevant content.

## Search

```bash
{baseDir}/scripts/mcp-websearch.sh "query"
{baseDir}/scripts/mcp-websearch.sh  "query"  10
```

## Options

- `<count>`: Number of results (default: 5, max: 20)
- `<query>`: User Query for Websearch
