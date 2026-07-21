---
name: notion
description: 通过 Notion 官方 ntn CLI 查询、创建和编辑页面、数据源、文件及 Notion Workers。用户提到 Notion 页面、数据库、data source、文件上传或 Notion Worker 时使用。
---

# Notion CLI

使用官方 `ntn`，优先使用语义明确的 `pages`、`datasources`、`files` 和 `workers` 命令，必要时再使用通用 `ntn api`。

## 准备

1. 运行 `command -v ntn`。缺失时，macOS/Linux 推荐 `curl -fsSL https://ntn.dev | bash`，跨平台可用 `npm install --global ntn`（Node.js 22+）。
2. 运行 `ntn doctor` 检查认证。未登录时运行 `ntn login`；远程环境使用 `ntn login --no-browser`，由用户核对验证码后运行提示的 `ntn login poll`。
3. CLI 默认将 workspace token 保存在系统钥匙串。不要读取或迁移凭据，也不要主动设置 `NOTION_KEYRING=0` 降级为明文存储。

## 常用操作

```bash
ntn pages get <page-id>
ntn pages create --parent page:<page-id> --content "# 标题"
ntn pages edit <page-id> --content "更新后的 Markdown"
ntn datasources query <data-source-id> --limit 25
ntn files list
ntn workers list --json
ntn api ls
```

用 `ntn <command> --help` 核对当前版本参数。多 workspace 场景先通过 `ntn debug` 确认目标，再为单条命令设置 `NOTION_WORKSPACE_ID`。

## 安全

- 读取页面、查询数据源和列出资源可直接执行。
- 创建、编辑、上传、部署 Worker 或写入环境变量前先确认目标与变更摘要。
- `trash`、`delete`、覆盖页面内容、重置同步状态等破坏性操作必须再次确认，不主动使用 `--yes`。
- 不执行会打印 OAuth token 的调试命令，不回显 `NOTION_API_TOKEN`。
