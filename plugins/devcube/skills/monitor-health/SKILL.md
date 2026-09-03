---
name: monitor-health
description: "Cubelet：监控域健康检查查询能力。用于通过 cubelet 查询业务应用在指定毫秒时间区间内的健康检查时序数据，并理解健康检查时间点与心跳值的含义。"
metadata:
  version: 0.1.0
  openclaw:
    category: "monitor"
    domain: "monitor"
    requires:
      bins:
        - cubelet
    cliHelp: "cubelet health --help"
---

# health

> **PREREQUISITE:** 先阅读 `../shared/SKILL.md`，确认配置文件、全局 flag 和输出格式。

```bash
cubelet health <command> [flags]
```

## Commands

| Command | 说明 |
|---------|------|
| `check` | 查询业务应用健康检查数据 |

## 环境约定

- 常用标准环境名称映射：生产环境=`prd`，公共环境=`pub`，测试环境=`test`
- 当用户未提供环境信息时，执行本 skill 中相关 CLI 命令按 `prd`、`pub`、`test` 顺序尝试
- 如果 3 个环境都返回空数据或空数组 `[]`，询问客户对应的环境信息
- 如果客户已提供环境信息，但返回结果为空或空数组 `[]`，提示客户系统无数据返回，请确认提供的信息是否正确，尤其是环境信息

## `check`

根据应用名称和查询时间区间查询业务应用健康检查时序数据。该命令是只读查询，不修改任何系统状态。

常用参数：

- `--app`：应用名称（必填）
- `--start`：查询开始时间，Unix 毫秒时间戳（必填）
- `--end`：查询结束时间，Unix 毫秒时间戳（必填）
- `--env`：逻辑环境名称（可选；环境约定见上文）

调用说明：

- `--start` 和 `--end` 需要使用毫秒时间戳。
- CLI 会校验时间区间不能超过 1 小时。
- CLI 调用后端接口时会自动把 `type` 固定为 `HTTP`，用于查询 HTTP 心跳检查结果。
- `env` 不放在 query 参数中，而是写入请求头 `env`；未传时按 `prd`、`pub`、`test` 顺序尝试。
- CLI 会在请求头中自动带上当前登录用户组织对应的 `company-id`。
- 命令输出只保留健康检查场景需要的 `x` 和 `y` 两个字段。

示例：

```bash
# 查询 prd 环境下 cube-base 的健康检查数据
cubelet health check --app cube-base --start 1776340140000 --end 1776340740000

# 显式指定环境
cubelet health check --app cube-base --start 1776340140000 --end 1776340740000 --env test
```

返回字段说明：

| 字段 | 监控含义 |
|------|----------|
| `x` | 健康检查时间点；表示该次心跳检查发生的时间 |
| `y` | 健康检查心跳值；`0` 代表不健康，`1` 代表健康 |

输出示例：

```json
[
  {
    "x": "2026-04-16T19:49:00",
    "y": 1.0
  },
  {
    "x": "2026-04-16T19:50:00",
    "y": 0.0
  }
]
```

## 适用场景

- 确认某个业务应用在指定时间窗口内是否持续存活
- 回看某段时间内健康检查是否出现抖动或中断
- 辅助判断应用不可用是持续故障还是瞬时异常
- 结合其他监控或日志结果，定位故障发生前后的健康状态变化
