---
name: team-project
description: "需要查询当前用户可见项目列表，按项目名称或编号过滤项目。"
---

# team-project

> **PREREQUISITE:** 先阅读 [DevCube 公共规则](../devcube/SKILL.md)，确认配置文件、全局 flag 和只读命令使用规则。

## `projectlist`

```bash
cubelet --config "$CUBELET_CONFIG" team projectlist [flags]
```

- `--query`：可选，项目名称或项目编号模糊查询
- `--currentPage`：可选，页码，默认 `1`
- `--pageSize`：可选，每页条数，默认 `20`

示例：

```bash
cubelet --config "$CUBELET_CONFIG" team projectlist
cubelet --config "$CUBELET_CONFIG" team projectlist --query TEST
cubelet --config "$CUBELET_CONFIG" team projectlist --query 紫 --currentPage 1 --pageSize 20
```

## 注意

- 这是只读命令。
- `query` 会同时匹配项目名称和项目编号。
