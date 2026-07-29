---
name: tavily-tool
displayName: "Tavily"
description: "使用 Tavily 网络搜索/发现查找 URL/来源，进行前期研究，收集最新链接，或生成带引用的网络摘要。"
version: 0.1.1
tags:
  - knowledge_management
license: "Unknown"
---

# Tavily

Use the bundled CLI to run Tavily searches from the terminal and collect sources fast.

## Quick start (CLI)

The scripts **require** `TAVILY_API_KEY` in the environment (sent as `Authorization: Bearer ...`).

```bash
export TAVILY_API_KEY="..."
node skills/tavily/scripts/tavily_search.js --query "best rust http client" --max_results 5
```

- JSON response is printed to **stdout**.
- A simple URL list is printed to **stderr** by default.

## Common patterns

### Get URLs only

```bash
export TAVILY_API_KEY="..."
node skills/tavily/scripts/tavily_search.js --query "OpenTelemetry collector config" --urls-only
```

### Restrict to (or exclude) specific domains

```bash
export TAVILY_API_KEY="..."
node skills/tavily/scripts/tavily_search.js \
  --query "oauth device code flow" \
  --include_domains oauth.net,datatracker.ietf.org \
  --exclude_domains medium.com
```

## Notes

- The bundled CLI supports a subset of Tavily’s request fields (query, max_results, include_domains, exclude_domains).
- For API field notes and more examples, read: `references/tavily-api.md`.
- Wrapper script (optional): `scripts/tavily_search.sh`.
