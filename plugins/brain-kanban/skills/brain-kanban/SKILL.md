---
name: brain-kanban
description: 当用户要求按 ID、编号或 Team 父事项编码读取当前 Workspace 项目的单个看板事项，或按状态和分页查询项目事项时，使用本 Skill。
---

使用 `brain-workspace-server kanban getissue` 通过 Workspace Controller 读取单个最新看板事项详情，或使用 `brain-workspace-server kanban listissue` 分页读取项目事项。

流程：

1. 确定目标项目的绝对 cwd。
2. 读取单个事项时确定事项标识。优先使用 Provider 事项 ID，也支持 `WEB-1` 形式的事项编号；Team 父事项或当前看板快照以外的事项优先使用 Provider `code`。
3. 执行对应命令：

```bash
brain-workspace-server kanban getissue --project "/absolute/project/cwd" --issue-id "WEB-1"

brain-workspace-server kanban listissue --project "/absolute/project/cwd" --status "To Do" --page 1 --page-size 20
```

说明：

- `--project` 必须是项目绝对 cwd。
- `listissue --status` 可省略，并按 status key、label 或 column key 匹配。
- `listissue` 通过 `--page` 和 `--page-size` 分页。
- 当前版本命令只读，不要通过本 Skill 尝试更新事项。
- `getissue` 直接输出事项 JSON 对象，`listissue` 输出分页包装对象。
- `getissue` 返回 `parent` 对象时，再以 `parent.code` 调用一次 `getissue` 读取父事项详情。

精确参数和响应结构见 [CLI 说明](references/cli.md)。
