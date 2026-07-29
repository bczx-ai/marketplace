---
name: grok-search
displayName: "grok-search"
description: "通过 xAI Responses API，使用 xAI Grok 服务器端工具（web_search、x_search）在网页或 X/Twitter 上搜索。适用于需要 X 的推文/话题/用户，或想用 Grok 替代 Brave，或需要结构化 JSON 与引用。"
version: 0.2.1
tags:
  - data_analysis
license: "Unknown"
---

Run xAI Grok locally via bundled scripts (search + chat + model listing). Default output for search is *pretty JSON* (agent-friendly) with citations.

## API key

The script looks for an xAI API key in this order:
- `XAI_API_KEY` env var
- `~/.clawdbot/clawdbot.json` → `env.XAI_API_KEY`
- `~/.clawdbot/clawdbot.json` → `skills.entries["grok-search"].apiKey`
- fallback: `skills.entries["search-x"].apiKey` or `skills.entries.xai.apiKey`

## Run

Use `{baseDir}` so the command works regardless of workspace layout.

### Search

- Web search (JSON):
  - `node {baseDir}/scripts/grok_search.mjs "<query>" --web`

- X/Twitter search (JSON):
  - `node {baseDir}/scripts/grok_search.mjs "<query>" --x`

### Chat

- Chat (text):
  - `node {baseDir}/scripts/chat.mjs "<prompt>"`

- Chat (vision):
  - `node {baseDir}/scripts/chat.mjs --image /path/to/image.jpg "<prompt>"`

### Models

- List models:
  - `node {baseDir}/scripts/models.mjs`

## Useful flags

Output:
- `--links-only` print just citation URLs
- `--text` hide the citations section in pretty output
- `--raw` include the raw Responses API payload on stderr (debug)

Common:
- `--max <n>` limit results (default 8)
- `--model <id>` (default `grok-4-1-fast`)

X-only filters (server-side via x_search tool params):
- `--days <n>` (e.g. 7)
- `--from YYYY-MM-DD` / `--to YYYY-MM-DD`
- `--handles @a,@b` (limit to these handles)
- `--exclude @bots,@spam` (exclude handles)

## Output shape (JSON)

```json
{
  "query": "...",
  "mode": "web" | "x",
  "results": [
    {
      "title": "...",
      "url": "...",
      "snippet": "...",
      "author": "...",
      "posted_at": "..."
    }
  ],
  "citations": ["https://..."]
}
```

## Notes

- `citations` are merged/validated from xAI response annotations where possible (more reliable than trusting the model’s JSON blindly).
- Prefer `--x` for tweets/threads, `--web` for general research.
