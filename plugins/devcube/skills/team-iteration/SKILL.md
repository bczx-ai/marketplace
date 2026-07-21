---
name: team-iteration
description: "需要查询项目迭代列表，控制是否隐藏已结束迭代。"
---

# team-iteration

> **PREREQUISITE:** 先阅读 [DevCube 公共规则](../devcube/SKILL.md)，确认配置文件、全局 flag 和只读命令使用规则。

## `iterationlist`

```bash
cubelet --config "$CUBELET_CONFIG" team iterationlist --projectid <项目ID> [flags]
```

- `--projectid`：必填，项目 ID
- `--name`：可选，迭代名称模糊查询
- `--isHide`：可选，是否隐藏已结束迭代，默认 `true`

示例：

```bash
cubelet --config "$CUBELET_CONFIG" team iterationlist --projectid 6625
cubelet --config "$CUBELET_CONFIG" team iterationlist --projectid 6625 --name V12
cubelet --config "$CUBELET_CONFIG" team iterationlist --projectid 6625 --isHide=false
```

## 注意

- 这是只读命令。
- `--isHide=true` 时只查询未结束或进行中的迭代。
