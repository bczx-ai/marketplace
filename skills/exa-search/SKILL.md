---
name: exa-search
displayName: "Exa Search"
description: "使用本地 Node 脚本调用 Exa (exa.ai) Search API 搜索网页并返回包含标题、链接、摘要和正文的 structured results。当用户请求启用 Exa 搜索、配置 API Key 或使用 Exa 进行网页搜索时触发。"
version: "1.0.0"
tags:
  - data_analysis
license: "Unknown"
---

# Exa Search

Use Exa’s Search API via the bundled script.

## Requirements

- Set `EXA_API_KEY` in the Gateway environment (recommended) or in `~/.openclaw/.env`.

## Commands

- Run a search:
  - `node {baseDir}/scripts/exa_search.mjs "<query>" --count 5`

- Include page text in results (costs more):
  - `node {baseDir}/scripts/exa_search.mjs "<query>" --count 5 --text`

- Narrow by time window:
  - `--start 2025-01-01 --end 2026-02-04`

## Notes

- This skill does not modify `web_search`; it provides an Exa-backed alternative you can invoke when you specifically want Exa.
