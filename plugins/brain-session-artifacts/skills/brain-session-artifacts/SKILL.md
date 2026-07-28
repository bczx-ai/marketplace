---
name: brain-session-artifacts
description: 当任务生成需要展示在当前 Brain 会话产物中的文件、链接、分支、合并请求、流水线或其它交付物时，使用本 Skill 追加产物。
---

使用 `brain-workspace-server session-artifacts` 向当前 Brain Session 的 Artifact spool 追加一个或多个产物。

流程：

1. 按规范的 Artifact schema 构造一个产物对象或对象数组。
2. 在当前 Agent Session 中执行追加命令：

```bash
brain-workspace-server session-artifacts --payload '{"type":"url","id":"preview","title":"预览","uri":"https://example.com"}'
```

说明：

- `--payload` 接受单个 JSON 对象或 JSON 对象数组。
- 命令只追加本地 JSONL 记录，实际同步由现有 Workspace watcher 完成。
- 新产物优先使用以下规范 `type`：
  - `file`：日志、图片、PDF、Office 文档或归档等本地输出文件。使用 `file://...`；保持 `id` 稳定且非空；条件允许时填写 `meta.mimeType` 和 `meta.size`。
  - `url`：没有额外业务语义的外部链接或预览 URL。兼容别名：`link`。
  - `mr`：GitLab Merge Request 或 GitHub Pull Request 等代码评审链接。兼容 merge request、pull request 和 `pr` 的空格、连字符或下划线变体。
  - `branch`：Git 分支链接或分支引用。兼容 git branch 的空格、连字符或下划线变体。
  - `pipeline`：CI/CD、workflow 或 build pipeline 链接。兼容 build、ci、ci cd、cicd、cicd pipeline 和 workflow 的常见变体。
- 类型匹配不区分大小写；`-` 和 `_` 会归一化为空格，连续空格会在别名匹配前合并。
- 未知 `type` 仍可接受，但 Web UI 会把它渲染为没有类型专属行为的普通产物。
- 完整字段说明见 `references/payload-schema.md`。
