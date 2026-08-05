---
name: codex-quota
displayName: "Codex Quota"
description: "检查 OpenAI Codex CLI 的每日/每周配额使用情况，基于本地会话日志。便携式 Python 脚本，读取 ~/.codex/sessions/ 目录获取配额数据。"
version: 1.2.2
tags:
  - development_programming
license: "Unknown"
---

# Skill: codex-quota

Check OpenAI Codex CLI rate limit status.

## Quick Reference

```bash
# Run the included Python script
./codex-quota.py

# Or if installed to PATH
codex-quota
```

## Options

```bash
codex-quota              # Show current quota (cached from latest session)
codex-quota --fresh      # Ping Codex first for live data
codex-quota --all --yes  # Update all accounts, save to /tmp/codex-quota-all.json
codex-quota --json       # Output as JSON
codex-quota --help       # Show help
```

## Setup

See [SETUP.md](SETUP.md) for prerequisites and setup instructions.

## What It Shows

- **Primary Window** (5 hours) — Short-term rate limit
- **Secondary Window** (7 days) — Weekly rate limit
- Reset times in local timezone with countdown
- Source session file and age

## When to Use

- Before starting heavy Codex work (check weekly quota)
- When Codex seems slow (might be rate-limited)
- Monitoring quota across multiple accounts
