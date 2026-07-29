---
name: agentlens
displayName: "Agentlens"
description: "使用agentlens层级文档导航和理解代码库。适用于探索新项目、定位模块、在大文件中查找符号、TODO/警告，或理解代码结构。"
version: "1.0.0"
tags:
  - development_programming
license: "Unknown"
---

# AgentLens - Codebase Navigation

## Before Working on Any Codebase
Always start by reading `.agentlens/INDEX.md` for the project map.

## Navigation Hierarchy

| Level | File | Purpose |
|-------|------|---------|
| L0 | `INDEX.md` | Project overview, all modules listed |
| L1 | `modules/{slug}/MODULE.md` | Module details, file list |
| L1 | `modules/{slug}/outline.md` | Symbols in large files |
| L1 | `modules/{slug}/memory.md` | TODOs, warnings, business rules |
| L1 | `modules/{slug}/imports.md` | File dependencies |
| L2 | `files/{slug}.md` | Deep docs for complex files |

## Navigation Flow

```
INDEX.md → Find module → MODULE.md → outline.md/memory.md → Source file
```

## When To Read What

| You Need | Read This |
|----------|-----------|
| Project overview | `.agentlens/INDEX.md` |
| Find a module | INDEX.md, search module name |
| Understand a module | `modules/{slug}/MODULE.md` |
| Find function/class in large file | `modules/{slug}/outline.md` |
| Find TODOs, warnings, rules | `modules/{slug}/memory.md` |
| Understand file dependencies | `modules/{slug}/imports.md` |

## Best Practices

1. **Don't read source files directly** for large codebases - use outline.md first
2. **Check memory.md before modifying** code to see warnings and TODOs
3. **Use outline.md to locate symbols**, then read only the needed source sections
4. **Regenerate docs** with `agentlens` command if they seem stale

For detailed navigation patterns, see [references/navigation.md](references/navigation.md)
For structure explanation, see [references/structure.md](references/structure.md)
