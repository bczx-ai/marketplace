---
name: team-kanban
description: "Use when需要查询事项看板列表，或查看指定事项看板的泳道、状态和事项卡片数据。"
metadata:
  version: 0.1.0
  openclaw:
    category: "project-management"
    requires:
      bins:
        - cubelet
    cliHelp: "cubelet team --help"
---

# team-kanban

> **PREREQUISITE:** 先阅读 `../shared/SKILL.md`，确认配置文件、全局 flag 和只读命令使用规则。

```bash
cubelet team <command> [flags]
```

## Commands

| Command | 说明 |
|---------|------|
| `kanbanlist` | 查询当前用户可见的事项看板列表 |
| `kanbandatas` | 查询指定看板的泳道、状态和事项数据 |

## `kanbanlist`

- `--name`：可选，看板名称模糊查询
- `--currentPage`：可选，页码，默认 `1`
- `--pageSize`：可选，每页条数，默认 `20`

示例：

```bash
cubelet team kanbanlist
cubelet team kanbanlist --name 需求
cubelet team kanbanlist --name 事项看板 --currentPage 2 --pageSize 10
```

## `kanbandatas`

- `--id`：必填，看板 ID

示例：

```bash
cubelet team kanbandatas --id 503
```

## 注意

- 两个命令都是只读查询，不会修改看板或事项状态。
- 默认优先使用 `--output json`。
