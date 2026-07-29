---
name: cron
displayName: "Cron"
description: "本地优先的重复计划引擎，用于提醒、重复任务和基于时间的执行计划。当用户提到重复时间、周期性时使用。"
version: 1.0.0
tags:
  - ai_agent
license: "Unknown"
---

# Cron

Turn recurring intentions into structured local schedules.

## Core Philosophy
1. Repetition should be captured once, then trusted.
2. A schedule is not just a reminder — it is an execution contract over time.
3. The system should make recurrence visible, editable, and pausable.
4. Users should always know what runs next.

## Runtime Requirements
- Python 3 must be available as `python3`
- No external packages required

## Storage
All data is stored locally only under:
- `~/.openclaw/workspace/memory/cron/jobs.json`
- `~/.openclaw/workspace/memory/cron/runs.json`
- `~/.openclaw/workspace/memory/cron/stats.json`

No external sync. No cloud storage. No third-party cron service.

## Job Status
- `active`: schedule is live
- `paused`: temporarily disabled
- `archived`: no longer active, kept for history

## Schedule Types
- `daily`
- `weekly`
- `monthly`
- `interval`

## Key Workflows
- **Capture recurring job**: `add_job.py`
- **See what runs next**: `next_run.py`
- **Pause or resume**: `pause_job.py`, `resume_job.py`
- **Inspect one job**: `show_job.py`
- **Review all jobs**: `list_jobs.py`
