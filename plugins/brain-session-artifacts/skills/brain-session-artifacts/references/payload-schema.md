# brain-session-artifacts payload schema

Payload 使用规范的 Session Artifact 结构：

```json
{
  "type": "file",
  "id": "artifact-build-log",
  "title": "build.log",
  "uri": "file:///workspace/app/build.log",
  "createdAt": "2026-04-21T10:00:00Z",
  "meta": {
    "mimeType": "text/plain",
    "size": 28194
  },
  "args": {
    "cwd": "/workspace/app"
  }
}
```

字段：

- `type`：Artifact 的规范类型；新 payload 优先使用下方列出的规范值。
- `id`：稳定的 Artifact 标识，强烈建议填写。`type=file` 的 Web 下载流程要求稳定且非空的 `id`。
- `title`：Session Artifacts 面板中的展示标题。
- `uri`：Artifact 地址。`type=file` 使用 `file://...`，链接类类型使用可打开的 `https://...` URL。
- `createdAt`：可选 RFC 3339 / ISO 8601 时间；省略时由 Workspace Server 在同步期间补齐。
- `meta`：可选元数据；`type=file` 通常使用 `meta.mimeType` 和 `meta.size`。
- `args`：可选的生产者上下文，按原值透传。

规范 `type`：

- `file`：日志、图片、PDF、Office 文档或归档等本地输出文件。建议使用 `file://...`，保持 `id` 稳定且非空，并尽量填写 `meta.mimeType` 与 `meta.size`。
- `url`：没有额外业务语义的外部链接或预览 URL。兼容别名：`link`。
- `mr`：GitLab Merge Request 或 GitHub Pull Request 等代码评审链接。新写入统一使用 `mr`；兼容 merge request、merge-request、merge_request、pull request、pull-request、pull_request 和 `pr`。
- `branch`：Git 分支链接或分支引用。新写入统一使用 `branch`；兼容 git branch、git-branch 和 git_branch。
- `pipeline`：CI/CD、workflow 或 build pipeline 链接。新写入统一使用 `pipeline`；兼容 build、ci、ci cd、ci/cd、ci-cd、ci_cd、cicd、cicd pipeline、cicd-pipeline、cicd_pipeline 和 workflow。

类型匹配规则：

- 不区分大小写。
- `-` 和 `_` 归一化为空格。
- 连续空格会在别名匹配前合并。
- 未知 `type` 仍可接受，但 Web UI 会将其渲染为没有类型专属行为的普通 Artifact。

`--payload` 可以是单个 Artifact 对象或 Artifact 对象数组。
