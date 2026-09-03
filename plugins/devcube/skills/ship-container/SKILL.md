---
name: ship-container
description: "Cubelet：容器服务运行态能力，包括服务详情、访问地址和最新容器日志。"
metadata:
  version: 0.1.0
  openclaw:
    category: "devops"
    requires:
      bins:
        - cubelet
    cliHelp: "cubelet container --help"
---

# container

> **PREREQUISITE:** 先阅读 `../shared/SKILL.md`，确认配置文件、全局 flag 和写操作安全规则。

```bash
cubelet container <command> [flags]
```

容器分组还支持别名 `service`。

## Commands

| Command | 说明 |
|---------|------|
| `inspect` | 获取容器服务详情和访问地址 |
| `logs` | 获取最新容器日志 |

## `inspect`

别名：`service-detail`

常用参数：

- `--name`
- `--env`

示例：

```bash
cubelet container inspect --name demo-service --env dev
```

## `logs`

别名：`latest-app-log`

常用参数：

- `--name`
- `--env`
- `--pod`
- `--container`

日志读取建议：

- 想保留结构化信息时用默认 `json`
- 想直接查看日志正文时用 `--output raw`

示例：

```bash
cubelet container logs --name demo-service --env dev
cubelet container logs --name demo-service --env dev --pod POD_NAME --container APP --output raw
```

## 适用场景

- 查询应用发布后的访问地址
- 拉取部署失败后的最新容器日志
- 辅助判断问题是流程失败还是运行态失败
