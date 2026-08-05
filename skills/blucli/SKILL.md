---
name: blucli
displayName: "Blucli"
description: "BluOS CLI (blu) 用于设备发现、播放、分组和音量控制。"
version: 1.0.0
tags:
  - design_multimedia
license: "Unknown"
---

# blucli (blu)

Use `blu` to control Bluesound/NAD players.

Quick start
- `blu devices` (pick target)
- `blu --device <id> status`
- `blu play|pause|stop`
- `blu volume set 15`

Target selection (in priority order)
- `--device <id|name|alias>`
- `BLU_DEVICE`
- config default (if set)

Common tasks
- Grouping: `blu group status|add|remove`
- TuneIn search/play: `blu tunein search "query"`, `blu tunein play "query"`

Prefer `--json` for scripts. Confirm the target device before changing playback.
