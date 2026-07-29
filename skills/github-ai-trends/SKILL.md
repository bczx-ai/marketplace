---
name: github-ai-trends
displayName: "GitHub AI Trends"
description: "生成 GitHub AI 趋势项目的文本排行榜，按日、周、月抓取 AI/ML/LLM 高星仓库并渲染。用于查询 AI 项目趋势、GitHub 趋势、AI 排行榜或热门 AI 仓库。"
version: 1.1.0
tags:
  - data_analysis
license: "Unknown"
---

# GitHub AI Trends

Generate formatted leaderboard of trending AI projects on GitHub, output directly to chat.

## Usage

Run the script and paste its stdout as the reply:

```bash
python3 scripts/fetch_trends.py --period weekly --limit 20
```

## Parameters

- `--period`: `daily` | `weekly` | `monthly` (default: weekly)
- `--limit`: Number of repos (default: 20)
- `--token`: GitHub token for higher rate limits (or set `GITHUB_TOKEN` env)
- `--json`: Output raw JSON instead of formatted text

## How It Works

1. Searches GitHub API for AI-related repos (by keywords + topics) pushed within the period
2. Deduplicates and sorts by star count
3. Outputs a formatted markdown leaderboard ready for chat display

## Notes

- Without a GitHub token, API rate limit is 10 requests/minute. With token: 30/minute.
- No pip dependencies, uses only stdlib.
- Output is markdown formatted for direct chat display.
