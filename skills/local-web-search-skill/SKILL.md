---
name: local-web-search-skill
displayName: "Local Web Search"
description: "**Translation:**\n\n通过DuckDuckGo HTML抓取实现免费本地网页搜索，无需API密钥。适用于web_search工具不可用或缺少API密钥且需要快速查询结果的场景。"
version: 0.1.0
tags:
  - data_analysis
license: "Unknown"
---

# Local Web Search

Run local search without paid APIs.

## Command

```bash
./skills/local-web-search/scripts/local_search.py "<query>" --max 8
```

## Output

Returns JSON with:
- query
- count
- disclaimer
- security
- results[] {title, url, snippet, trust{score,tier,reason}}

## Trust Scoring

- high: docs/papers/.gov/.edu/authoritative domains
- medium: reputable publications/default domains
- low: user-generated platforms (e.g., dev.to, medium, substack)

Use trust score for ranking/filtering only; always verify key claims with primary sources.

## Security

- No environment/token exfiltration
- No external writes
- Outbound HTTPS GET only to search endpoint

## Reliability

- Handles transient errors with exponential backoff + jitter
- Public scraping behavior can change; parser may need updates
