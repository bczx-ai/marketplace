---
name: eightctl
displayName: "Eightctl"
description: "控制Eight Sleep睡眠舱（状态、温度、闹钟、排程）"
version: 1.0.0
tags:
  - development_programming
license: "Unknown"
---

# eightctl

Use `eightctl` for Eight Sleep pod control. Requires auth.

Auth
- Config: `~/.config/eightctl/config.yaml`
- Env: `EIGHTCTL_EMAIL`, `EIGHTCTL_PASSWORD`

Quick start
- `eightctl status`
- `eightctl on|off`
- `eightctl temp 20`

Common tasks
- Alarms: `eightctl alarm list|create|dismiss`
- Schedules: `eightctl schedule list|create|update`
- Audio: `eightctl audio state|play|pause`
- Base: `eightctl base info|angle`

Notes
- API is unofficial and rate-limited; avoid repeated logins.
- Confirm before changing temperature or alarms.
