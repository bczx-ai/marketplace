---
name: gitee
description: 通过 Gitee 官方 MCP 管理仓库、代码、Issue、Pull Request、Release、评论和通知。用户提到 Gitee、码云、仓库协作、Issue、PR 或 Release 时使用。
---

# Gitee

使用本插件连接的 Gitee MCP。连接缺失或失效时，请用户从插件详情填写 Personal Access Token；不要让用户在聊天中粘贴 Token。

## 能力

- 仓库与代码：`list_user_repos`、`get_file_content`、`search_files_by_content`、`search_open_source_repositories`、`compare_branches_tags`。
- Issue：`list_repo_issues`、`get_repo_issue_detail`、`create_issue`、`update_issue`。
- Pull Request：`list_repo_pulls`、`get_pull_detail`、`get_diff_files`、`create_pull`、`update_pull`、`manage_pull_review`、`merge_pull`。
- 其它：`list_comments`、`create_comment`、`list_releases`、`create_release`、`list_user_notifications`、`get_user_info`、`search_users`。

先通过仓库 URL 或 `owner/repo` 确认目标；范围不明确时先查询，不猜测组织、仓库、分支或编号。读取、搜索、比较和状态查询可直接执行，并限制分页规模。

## 安全

- 创建或更新 Issue/PR、评论前，先向用户确认目标和内容摘要。
- 创建仓库、Fork、创建 Release、审批或合并 PR 属于高影响操作，执行前再次确认。
- 官方 MCP 当前的工具 annotations 不能准确区分读写，必须按上述操作语义判断风险。
- 不输出 Token，不把凭据写入仓库、命令、日志或回复。
