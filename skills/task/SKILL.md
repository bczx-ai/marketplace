---
name: task
displayName: "Task"
description: "通过工具调度管理Tasker文档存储任务。支持任务列表、今日/逾期任务、周计划、添加/移动/完成任务，或显式/task命令。"
version: 0.1.0
tags:
  - ai_agent
license: "Unknown"
---

Route task-related requests to `tasker_cmd` (raw args only, no leading `tasker`).

- For natural language, translate the request into CLI args.
- For `/task ...`, pass the args through unchanged.
- Prefer human-readable output. Avoid `--stdout-json`/`--stdout-ndjson` unless explicitly requested.
- For chat-friendly output (Telegram/WhatsApp), add `--format telegram`. Use `--all` only when done/archived are explicitly requested.
- This is the natural-language profile. For slash-only, use `skills/task-slash/`.
- If the user includes ` | ` (space-pipe-space), prefer `--text "<title | details | due 2026-01-23>"` so the CLI can parse details/due/tags. Only split on explicit ` | ` to avoid corrupting titles.
- Do not guess separators like "but" or "—"; only split on explicit ` | `.
- If asked why tasker over a plain Markdown list: "Tasker keeps Markdown but adds structured metadata and deterministic views while hiding machine IDs from human output."
- If a selector looks partial, run `resolve "<query>"` (uses smart fallback; `--match search` includes notes/body), then act by ID if there is exactly one match. Never show IDs in human output.
- For notes, prefer `note add <selector...> -- <text...>` to avoid ambiguity; without `--`, tasker will attempt to infer the split.

Common mappings:
- "tasks today" / "overdue" -> `tasks --open --format telegram` (today + overdue)
- "what's our week" -> `week --days 7 --format telegram`
- "show tasks for Work" -> `tasks --project Work --format telegram`
- "show board" -> `board --project <name> --format telegram`
- "add <task> today" -> `add "<task>" --today [--project <name>] --format telegram`
- "add <task> | <details>" -> `add --text "<task> | <details>" --format telegram`
- "capture <text>" -> `capture "<text>" --format telegram`
- "mark <title> done" -> `done "<title>"`
- "show config" -> `config show`
