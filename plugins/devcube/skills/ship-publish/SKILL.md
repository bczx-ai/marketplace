---
name: ship-publish
description: "DevCube：单应用发布相关能力，包括快速发布、创建发布单、dry-run 预览和发布状态查询。"
---

# publish

> **PREREQUISITE:** 先阅读 [DevCube 公共规则](../devcube/SKILL.md)，确认配置文件、全局 flag 和写操作安全规则。

```bash
cubelet publish <command> [flags]
```

## Commands

| Command | 说明 |
|---------|------|
| `quick` | 快速创建并执行单应用发布，可选择等待终态 |
| `create` | 只创建发布单，不自动执行流程 |
| `status` | 查询发布单当前状态 |

## `quick`

用于“一步发版”。常用参数：

- `--app`：应用名
- `--branch`：发布分支
- `--env`：逻辑环境
- `--type`：`container` 或 `vm`
- `--pipeline`：指定流水线
- `--wait`：是否等待终态，默认 `true`
- `--dry-run`：仅预览，不真正创建发布单

配置相关参数：

- `--config-file` / `--config-content`
- `--config-label`
- `--config-name`
- `--config-format`
- `--config-type`
- `--config-mount-path`
- `--config-push-sequence`
- `--service-port`

注意：

- 使用 `--config-file` 或 `--config-content` 时，`--config-label` 是必填的。
- 这是写命令；如果不是明确要执行发布，优先先跑一次 `--dry-run`。

示例：

```bash
cubelet publish quick --app demo-app --branch release/20260401 --env dev --wait
cubelet publish quick --app demo-app --branch master --env dev --dry-run
cubelet publish quick --app demo-app --branch master --env dev --config-file ./application.yaml --config-label application.yaml
```

## `create`

适合先建单，再由后续流程决定是否执行。

关键差异：

- `--env` 对 `create` 是常规必填参数。
- 不会像 `quick` 一样自动串起完整发布流程。
- 创建成功后会产出发布单访问链接；如果当前返回里没有 `access_urls`，会补查发布状态再产出 ingress 访问地址。

示例：

```bash
cubelet publish create --app demo-app --branch release/20260401 --env dev
cubelet publish create --app demo-app --branch master --env dev --name "发布单-灰度验证"
```

## `status`

按发布单 ID 查询状态。

- `--id`：发布单 ID
- `--env`：可选；补充运行态上下文时建议带上

示例：

```bash
cubelet publish status --id 10001
cubelet publish status --id 10001 --env dev
```

## 常见搭配

- 快速发布：见 [recipe-ship-quick-publish](../recipe-ship-quick-publish/SKILL.md)
- 发布时附带配置：见 [recipe-ship-publish-with-config](../recipe-ship-publish-with-config/SKILL.md)
- 发布失败排障：见 [recipe-ship-troubleshoot-publish](../recipe-ship-troubleshoot-publish/SKILL.md)
