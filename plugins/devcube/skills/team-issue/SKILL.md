---
name: team-issue
description: "需要根据事项 ID 或事项编号查询事项详情。"
---

# team-issue

> **PREREQUISITE:** 先阅读 [DevCube 公共规则](../devcube/SKILL.md)，确认配置文件、全局 flag 和只读命令使用规则。

## `getissue`

```bash
cubelet team getissue --id <事项ID或事项编号>
```

- `--id`：必填。既支持纯数字事项 ID，也支持事项编号，例如 `ZA-T-98054`

示例：

```bash
cubelet team getissue --id 98054
cubelet team getissue --id ZA-T-98054
```

## 注意

- 这是只读命令。
- 命令会自动区分纯数字 ID 与事项编号。
