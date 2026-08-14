---
name: ship-vmapp
description: "DevCube：虚拟机应用运行态能力，包括实例详情、访问地址和最新日志。"
---

# vmapp

> **PREREQUISITE:** 先阅读 [DevCube 公共规则](../devcube/SKILL.md)，确认配置文件、全局 flag 和写操作安全规则。

```bash
cubelet --config "$CUBELET_CONFIG" vmapp <command> [flags]
```

## Commands

| Command | 说明 |
|---------|------|
| `inspect` | 获取虚拟机应用详情和访问地址 |
| `logs` | 获取虚拟机应用最新日志 |

## `inspect`

常用参数：

- `--name`
- `--env`

示例：

```bash
cubelet --config "$CUBELET_CONFIG" vmapp inspect --name demo-vmapp --env fat
```

## `logs`

常用参数：

- `--name`
- `--env`
- `--host`
- `--num`

日志读取建议：

- 默认保留 `json`
- 需要原始日志时使用 `--output raw`
- 多主机场景优先带 `--host` 精确定位

示例：

```bash
cubelet --config "$CUBELET_CONFIG" vmapp logs --name demo-vmapp --env fat
cubelet --config "$CUBELET_CONFIG" vmapp logs --name demo-vmapp --env fat --host 172.28.38.19 --num 200 --output raw
```

## 适用场景

- 虚拟机类型发布后的实例信息确认
- 多主机日志排查
- 发布成功但访问异常时的运行态诊断
