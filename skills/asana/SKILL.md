---
name: asana
displayName: "Asana"
description: "通过 Asana REST API 管理 Asana，支持列出工作区、项目、任务，搜索、评论、更新、完成和创建任务。"
version: 1.0.2
tags:
  - business_operations
license: "Unknown"
---

# Asana

This skill provides a lightweight Asana CLI for OpenClaw.

## Auth

Recommended auth is **PAT-first**.

Priority order:
1. `--token` or `ASANA_PAT`
2. `~/.openclaw/asana/config.json` with `{ "pat": "..." }`
3. OAuth token at `~/.openclaw/asana/token.json`

OAuth remains supported for advanced use, but PAT is the preferred local/operator setup.

## Setup

### PAT mode (recommended)

```bash
node scripts/configure.mjs --mode pat --pat "$ASANA_PAT"
```

Or set `ASANA_PAT` in OpenClaw skill config.

### OAuth mode (optional)

```bash
node scripts/configure.mjs --mode oauth --client-id "$ASANA_CLIENT_ID" --client-secret "$ASANA_CLIENT_SECRET"
node scripts/oauth_oob.mjs authorize --client-id "$ASANA_CLIENT_ID"
node scripts/oauth_oob.mjs token --client-id "$ASANA_CLIENT_ID" --client-secret "$ASANA_CLIENT_SECRET" --code "..."
```

## Storage

This skill stores local state under:

- `~/.openclaw/asana/config.json`
- `~/.openclaw/asana/token.json`

## Commands

Core CLI:

```bash
node scripts/asana_api.mjs me
node scripts/asana_api.mjs list-workspaces
node scripts/asana_api.mjs set-default-workspace --workspace <gid>
node scripts/asana_api.mjs projects --workspace <gid>
node scripts/asana_api.mjs tasks-in-project --project <gid>
node scripts/asana_api.mjs tasks-assigned --workspace <gid> --assignee me
node scripts/asana_api.mjs search-tasks --workspace <gid> --text "quote"
node scripts/asana_api.mjs task <task_gid>
node scripts/asana_api.mjs update-task <task_gid> --name "New name"
node scripts/asana_api.mjs complete-task <task_gid>
node scripts/asana_api.mjs comment <task_gid> --text "Done"
node scripts/asana_api.mjs create-task --workspace <gid> --name "New task"
```

PAT helpers:

```bash
node scripts/asana_api.mjs set-pat <asana_pat>
node scripts/asana_api.mjs clear-pat
```

## OpenClaw config

Recommended skill config:

```json
{
  "skills": {
    "entries": {
      "asana": {
        "enabled": true,
        "env": {
          "ASANA_PAT": "<your-pat>"
        }
      }
    }
  }
}
```

For local/private use, PAT is the best default. Use OAuth only when you specifically need that flow.
