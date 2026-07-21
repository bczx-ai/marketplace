---
name: gitlab
description: 通过 GitLab 官方 glab CLI 操作 GitLab.com 或私有 GitLab 实例，包括项目、Issue、Merge Request、CI/CD、Release 和同源 API。用户提到 GitLab、glab、MR、pipeline 或私有 GitLab 地址时使用。
---

# GitLab CLI

使用官方 `glab`，同时支持公网 GitLab 和用户指定的私有 GitLab hostname。

## 准备

1. 运行 `command -v glab`。缺失时按 GitLab CLI 官方文档为当前平台安装。
2. 从仓库 remote 或用户输入确定 hostname，不假定一定是 `gitlab.com`。
3. 运行 `glab auth status --hostname <host>`。未登录时运行 `glab auth login --hostname <host> --web`；私有实例也可由用户通过 stdin 提供 Token。不要让用户在聊天中粘贴 Token。
4. 在仓库外执行时，为命令提供 `--repo <host>/<owner>/<repo>` 或先确认目标项目。

## 操作

优先使用专用命令，缺少能力时使用同源 `glab api`：

```bash
glab repo view
glab issue list
glab mr list
glab pipeline status
glab api projects/:id/merge_requests --paginate
```

使用 `--output json`、`--paginate` 和非交互参数获得稳定结果。提交评论或描述较长时使用项目内临时文件，并在完成后删除。

## 安全

- 查看、搜索、状态、日志和 diff 可直接执行。
- 创建或修改 Issue/MR、评论、审批、触发或重试 pipeline 前确认目标和内容。
- merge、delete、cancel、Release 发布、成员权限、变量、Token 和 protected resource 变更必须再次确认。
- 不运行 `glab auth token`，不打印或写入认证配置。
