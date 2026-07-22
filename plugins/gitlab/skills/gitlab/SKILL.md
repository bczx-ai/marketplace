---
name: gitlab
description: 使用 GitLab 官方 glab CLI 管理项目、Issue、Merge Request、CI/CD pipeline、Release 和同源 API。用户提到 GitLab、glab、MR 审查、Issue 跟进、pipeline 排障、发布或 GitLab API 时使用。
---

# GitLab CLI

使用官方 `glab` 完成 GitLab 日常开发协作、CI/CD 排障与自动化操作。

## 准备

1. 运行 `command -v glab`。缺失表示插件 CLI 安装异常，请用户更新或重新安装 GitLab 插件，不要执行系统级安装命令。
2. 从 `GLAB_CONFIG_DIR` 对应的 Brain 连接和仓库 remote 确定 hostname，不假定一定是 `gitlab.com`。
3. 运行 `glab auth status --hostname <host>`。未登录或目标实例不一致时，请用户从插件详情为对应 hostname 建立或重新建立连接；Brain 会自动打开授权页面。不要让用户在聊天中粘贴 Token。
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
