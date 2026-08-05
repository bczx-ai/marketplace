---
name: guicountrol
displayName: "Linux GUI  Control"
description: "使用 xdotool、wmctrl 和 dogtail 控制 Linux 桌面 GUI。适用于与非浏览器应用交互、模拟鼠标/键盘输入、管理窗口或检查 X11/GNOME 上的应用 UI 层级。支持：(1) 在应用中点击/输入，(2) 调整窗口大小/移动窗口，(3) 提取应用的文本 UI 树 (A11y)，(4) 截图进行视觉分析。"
version: 1.0.0
tags:
  - development_programming
license: "Unknown"
---

# Linux GUI Control

This skill provides tools and procedures for automating interactions with the Linux desktop environment.

## Quick Start

### 1. Identify Target Window
Use `wmctrl` to find the exact name of the window you want to control.
```bash
wmctrl -l
```

### 2. Inspect UI Hierarchy
For apps supporting accessibility (GNOME apps, Electron apps with `--force-renderer-accessibility`), use the inspection script to find button names without taking screenshots.
```bash
python3 scripts/inspect_ui.py "<app_name>"
```

### 3. Perform Actions
Use `xdotool` via the helper script for common actions.
```bash
# Activate window
./scripts/gui_action.sh activate "<window_name>"

# Click coordinates
./scripts/gui_action.sh click 500 500

# Type text
./scripts/gui_action.sh type "Hello World"

# Press a key
./scripts/gui_action.sh key "Return"
```

## Workflows

### Operating an App via Text UI
1. List windows with `wmctrl -l`.
2. Activate the target window.
3. Run `scripts/inspect_ui.py` to get the list of buttons and inputs.
4. Use `xdotool key Tab` and `Return` to navigate, or `click` if coordinates are known.
5. If text-based inspection fails, fallback to taking a screenshot and using vision.

### Forcing Accessibility in Electron Apps
Many modern apps (VS Code, Discord, Cider, Chrome) need a flag to expose their UI tree:
```bash
pkill <app>
nohup <app> --force-renderer-accessibility > /dev/null 2>&1 &
```

## Tool Reference

- **wmctrl**: Window management (list, activate, move, resize).
- **xdotool**: Input simulation (click, type, key, mousemove).
- **dogtail**: UI tree extraction via AT-SPI (Accessibility bus).
- **scrot**: Lightweight screenshot tool.
