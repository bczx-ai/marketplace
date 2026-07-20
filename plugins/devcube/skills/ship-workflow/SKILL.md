---
name: ship-workflow
description: "DevCube：发布流程相关能力，包括执行当前阶段和读取最新流程日志。"
---

# workflow

> **PREREQUISITE:** 先阅读 [DevCube 公共规则](../devcube/SKILL.md)，确认配置文件、全局 flag 和写操作安全规则。

```bash
cubelet workflow <command> [flags]
```

## Commands

| Command | 说明 |
|---------|------|
| `run` | 执行发布单当前流程阶段 |
| `logs` | 获取最新流程日志 |

## `run`

别名：`execute-workflow`

常用参数：

- `--publish-id`
- `--stage`
- `--app`
- `--publish-app-id`

注意：

- 这是写命令，适合明确要“重新触发”或“执行当前阶段”时使用。
- 如果用户只是想看失败原因，不要先执行 `run`，应先查 `publish status` 和 `workflow logs`。

示例：

```bash
cubelet workflow run --publish-id 10001
cubelet workflow run --publish-id 10001 --stage 部署 --app demo-app
```

## `logs`

别名：`latest-flow-log`

常用参数：

- `--publish-id`
- `--stage`
- `--app`
- `--publish-app-id`

日志读取建议：


示例：

```bash
cubelet workflow logs --publish-id 10001
cubelet workflow logs --publish-id 10001 --app demo-app
```

## 常见搭配

- 发布排障：见 [recipe-ship-troubleshoot-publish](../recipe-ship-troubleshoot-publish/SKILL.md)
