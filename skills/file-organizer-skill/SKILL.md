---
name: file-organizer-skill
displayName: "File Organizer Skill"
description: "{ \"translation\": \"按扩展名或日期分文件夹整理目录文件，支持预演、递归及撤销功能。\" }"
version: 1.0.0
tags:
  - office_productivity
license: "Unknown"
---

# File Organizer (Gold Standard)

## Features
- **Smart Sorting**: Group by Extension (Default) or Date (Year/Month).
- **Safety**: Conflict resolution (auto-rename), Dry Run mode, and Undo capability.
- **Deep Clean**: Recursive scanning option.
- **Audit**: Generates `organize_history.json` for tracking.

## Usage

### Basic Sort (by Extension)
```bash
python3 scripts/organize.py /path/to/folder
```

### Date Sort (Year/Month)
Great for photos or archives.
```bash
python3 scripts/organize.py /path/to/folder --date
```

### Dry Run (Simulate)
See what *would* happen without moving anything.
```bash
python3 scripts/organize.py /path/to/folder --dry-run
```

### Undo
Revert changes using the history file.
```bash
python3 scripts/organize.py --undo /path/to/folder/organize_history.json
```

## Config
Modify `scripts/organize.py` `get_default_mapping()` to add custom extensions.
