# brain-kanban CLI 说明

命令：

```bash
brain-workspace-server kanban getissue --project "/absolute/project/cwd" --issue-id "WEB-1"

brain-workspace-server kanban listissue --project "/absolute/project/cwd" --status "To Do" --page 1 --page-size 20
```

- `--project`：必须是当前项目的绝对 cwd。
- `--issue-id`：可以是 Provider 事项 ID、事项编号，或 `POC-PR-98070` 形式的 Team 父事项编码。
- `--status`：`listissue` 的可选参数。按事项 `status.key`、`status.label` 或 `status.columnKey` 匹配，忽略大小写以及空格与连字符差异。
- `--page`：`listissue` 的可选参数，默认为 `1`。
- `--page-size`：`listissue` 的可选参数，默认为 `50`。
- `getissue` 输出：直接打印事项 JSON 对象。
- `listissue` 输出：打印包含 `projectId`、`projectCwd`、`board`、`issues`、`page`、`pageSize` 和 `total` 的 JSON 对象。
- 父事项跟进：`getissue` 返回 `parent` 对象时，以 `parent.code` 再次调用 `getissue` 读取父事项详情。
