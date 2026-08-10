---
name: github
description: 通过 GitHub 官方 gh CLI 操作仓库、Issue、Pull Request、Actions、Release 和 GitHub API。用户提到 GitHub、gh、PR、Actions workflow、GitHub Release 或仓库协作时使用。
---

# GitHub

使用 GitHub 官方 `gh` CLI 读取和管理仓库、Issue、Pull Request、评论、Actions 与 Release。

## 工作流分流

- 常规仓库、Issue 和 PR 查询留在本 Skill。
- 未解决的 PR 评审意见使用 `../gh-address-comments/SKILL.md`。
- GitHub Actions 失败排查使用 `../gh-fix-ci/SKILL.md`。
- 提交、推送并创建草稿 PR 使用 `../yeet/SKILL.md`。

所有 GitHub 操作统一使用 `gh`；查询优先使用 `--json` 和 `--jq`，GitHub REST 或 GraphQL 能力通过 `gh api` 调用。

## 准备

1. 运行 `command -v gh`。缺失表示插件 CLI 安装异常，请用户更新或重新安装 GitHub 插件，不要执行系统级安装命令。
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
