---
name: ship-config
description: "DevCube：应用配置管理能力，包括查询配置、创建配置、查看版本和创建新版本。"
---

# config

> **PREREQUISITE:** 先阅读 [DevCube 公共规则](../devcube/SKILL.md)，确认配置文件、全局 flag 和写操作安全规则。

```bash
cubelet --config "$CUBELET_CONFIG" config <command> [flags]
```

## Commands

| Command | 说明 |
|---------|------|
| `list` | 查询应用在指定环境下的配置列表 |
| `create` | 创建配置并生成初始版本 |
| `versions` | 查询配置版本列表 |
| `create-version` | 为已有配置创建新版本 |

## `list`

常用参数：

- `--app`
- `--env`
- `--config-name`
- `--config-type`

示例：

```bash
cubelet --config "$CUBELET_CONFIG" config list --app demo-app --env dev
cubelet --config "$CUBELET_CONFIG" config list --app demo-app --env dev --config-name application.yaml
```

## `create`

这是写命令。常用参数：

- `--app`
- `--env`
- `--label`
- `--file` 或 `--data`
- `--config-name`
- `--format`
- `--version`
- `--description`
- `--config-type`

注意：

- 多行配置优先使用 `--file`。
- `--label` 是配置项标识，通常应与实际文件名或配置项名一致。

示例：

```bash
cubelet --config "$CUBELET_CONFIG" config create --app demo-app --env dev --file ./application.yaml --label application.yaml
cubelet --config "$CUBELET_CONFIG" config create --app demo-app --env dev --data 'key: value' --label application.yaml
```

## `versions`

按配置 ID 查询版本历史。

```bash
cubelet --config "$CUBELET_CONFIG" config versions --config-id 10001
```

## `create-version`

为已有配置追加版本。常用参数：

- `--config-id`
- `--file` 或 `--data`
- `--version`
- `--description`

示例：

```bash
cubelet --config "$CUBELET_CONFIG" config create-version --config-id 10001 --file ./application.yaml
cubelet --config "$CUBELET_CONFIG" config create-version --config-id 10001 --data 'new_key: new_value' --version v2
```

## 常见搭配

- 如果用户只是要“带配置发布”，优先看 [recipe-ship-publish-with-config](../recipe-ship-publish-with-config/SKILL.md)
- 如果用户要独立维护配置生命周期，再使用 `config create` / `config create-version`
