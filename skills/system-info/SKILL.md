---
name: system-info
displayName: "System Info"
description: "快速系统诊断：CPU、内存、磁盘、运行时间"
version: 1.0.0
tags:
  - development_programming
license: "Unknown"
---

# System Info

Quick system diagnostics covering CPU, memory, disk, and uptime. Uses standard Linux utilities that are always available.

## Commands

```bash
# Show all system info (CPU, memory, disk, uptime)
system-info

# Show CPU information
system-info cpu

# Show memory usage
system-info mem

# Show disk usage
system-info disk

# Show system uptime
system-info uptime
```

## Install

No installation needed. `free` and related utilities are always present on the system.
