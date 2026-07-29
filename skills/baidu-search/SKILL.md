---
name: baidu-search
displayName: Baidu web search
description: 使用百度AI搜索引擎(BDSE)进行网络搜索。适用于获取实时信息、文档资料或研究课题。
version: 1.1.4
tags:
  - knowledge_management
license: Unknown
---

# Baidu Search

Search the web via Baidu AI Search API.

## Prerequisites

### API Key Configuration
This skill requires a **BAIDU_API_KEY** to be configured in OpenClaw.

If you don't have an API key yet, please visit:
**https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey**

For detailed setup instructions, see:
[references/apikey-fetch.md](references/apikey-fetch.md)

## Usage

```bash
python3 skills/baidu-search/scripts/search.py '<JSON>'
```

## Request Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| query | str | yes | - | Search query |
| count | int | no | 10 | Number of results to return, range 1-50 |
| freshness | str | no | Null | Time range, two formats: format one is ”YYYY-MM-DDtoYYYY-MM-DD“, and format two includes pd, pw, pm, and py, representing the past 24 hours, past 7 days, past 31 days, and past 365 days respectively |

## Examples

```bash
# Basic search
python3 scripts/search.py '{"query":"人工智能"}'

# Freshness first format "YYYY-MM-DDtoYYYY-MM-DD" example
python3 scripts/search.py '{
  "query":"最新新闻",
  "freshness":"2025-09-01to2025-09-08"
}'

# Freshness second format pd、pw、pm、py example
python3 scripts/search.py '{
  "query":"最新新闻",
  "freshness":"pd"
}'

# set count, the number of results to return
python3 scripts/search.py '{
  "query":"旅游景点",
  "count": 20,
}'
```

## Current Status

Fully functional.
