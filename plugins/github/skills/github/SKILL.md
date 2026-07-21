---
name: github
description: 通过 GitHub 官方 gh CLI 操作仓库、Issue、Pull Request、Actions、Release 和 GitHub API。用户提到 GitHub、gh、PR、Actions workflow、GitHub Release 或仓库协作时使用。
---

# GitHub CLI

使用官方 `gh`，优先使用专用子命令，必要时使用 `gh api`。

## 准备

1. 运行 `command -v gh`。缺失时按 GitHub CLI 官方文档为当前平台安装。
2. 确认 `GH_CONFIG_DIR` 已由 Brain 注入，并运行 `gh auth status`。未登录时请用户从插件详情重新连接；Brain 会自动打开浏览器授权页。不要要求用户在聊天中提供 PAT。
3. 从当前 Git remote 确认仓库；在仓库外使用 `--repo owner/repo`。

## 操作

```bash
gh repo view
gh issue list
gh pr list
gh pr checks <number>
gh run list
gh api repos/{owner}/{repo}/issues --paginate
```

使用 `--json`、`--jq`、`--limit` 和非交互参数保持输出稳定。需要写较长正文时使用项目内临时文件，并在完成后删除。

## 安全

- 查看、搜索、状态、日志和 diff 可直接执行。
- 创建或修改 Issue/PR、评论、review、触发或重跑 workflow 前确认目标和内容。
- merge、delete、cancel、Release 发布、成员权限、Secret、变量和分支保护变更必须再次确认。
- 不运行 `gh auth token`，不读取认证配置，不在输出中暴露 Token。
