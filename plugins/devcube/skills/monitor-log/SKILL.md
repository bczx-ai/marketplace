---
name: monitor-log
description: "DevCube：监控域日志查询能力。用于通过 Brain DevCube 应用连接查询业务应用系统日志数据，按应用名、毫秒时间区间、日志级别、traceId、spanId 等条件筛选，并理解系统日志输出字段和常见日志属性含义。"
---

# log

> **PREREQUISITE:** 先阅读 [DevCube 公共规则](../devcube/SKILL.md)，确认配置文件、全局 flag 和输出格式。

```bash
cubelet --config "$CUBELET_CONFIG" log <command> [flags]
```

## Commands

| Command | 说明 |
|---------|------|
| `system` | 查询业务应用系统日志数据 |

## 环境约定

- 常用标准环境名称映射：生产环境=`prd`，公共环境=`pub`，测试环境=`test`
- 当用户未提供环境信息时，执行本 skill 中相关 CLI 命令按 `prd`、`pub`、`test` 顺序尝试
- 如果 3 个环境都返回空数据或空数组 `[]`，询问客户对应的环境信息
- 如果客户已提供环境信息，但返回结果为空或空数组 `[]`，提示客户系统无数据返回，请确认提供的信息是否正确，尤其是环境信息

## `system`

根据应用名称、查询时间区间和可选筛选条件查询业务应用系统日志。该命令是只读查询，不修改任何系统状态。

常用参数：

- `--app`：应用名称（必填）
- `--start`：查询开始时间，Unix 毫秒时间戳（必填）
- `--end`：查询结束时间，Unix 毫秒时间戳（必填）
- `--level`：日志级别，可选值 `ERROR`、`WARN`、`INFO`
- `--traceId`：调用链 ID（可选）
- `--spanId`：调用段 ID（可选）
- `--env`：逻辑环境名称（可选；环境约定见上文）

调用说明：

- `--start` 和 `--end` 的输入值必须是毫秒时间戳，CLI 会先校验区间不能超过 10 分钟。
- CLI 会把毫秒时间戳转换为 `YYYY-MM-DD HH:mm:ss` 后再调用后端日志查询接口。
- `env` 不作为 query 参数，而是写入请求头 `env`；未传时按 `prd`、`pub`、`test` 顺序尝试。
- 请求头 `company-id` 自动取当前登录用户的组织 ID。
- 当输入 `--level`、`--traceId`、`--spanId` 时，CLI 会按顺序拼装后端所需的 `queryString`，例如：

```text
level = 'ERROR' and traceId = '2a82df828b10898e14a97f69f9fa4b63' and spanId = '3453f7b0f246d62f'
```

- 命令输出只保留系统日志查询场景需要的字段，不返回分页等后端冗余字段。

示例：

```bash
# 查询 prd 环境下 cube-base 在指定 10 分钟时间窗内的系统日志
cubelet --config "$CUBELET_CONFIG" log system --app cube-base --start 1776333432000 --end 1776334032000

# 按日志级别过滤
cubelet --config "$CUBELET_CONFIG" log system --app cube-base --start 1776333432000 --end 1776334032000 --level ERROR

# 结合 traceId 和 spanId 精确定位某次调用的日志
cubelet --config "$CUBELET_CONFIG" log system --app cube-base --start 1776333432000 --end 1776334032000 --traceId 2a82df828b10898e14a97f69f9fa4b63 --spanId 3453f7b0f246d62f

# 显式指定环境
cubelet --config "$CUBELET_CONFIG" log system --app cube-base --start 1776333432000 --end 1776334032000 --level WARN --env test
```

返回字段说明：

| 字段 | 监控含义 |
|------|----------|
| `traceId` | 调用链 ID；用于把日志和一次完整业务请求关联起来 |
| `spanId` | 调用段 ID；用于把日志定位到调用链中的具体 span |
| `level` | 日志级别；反映事件严重程度，常用于区分错误、告警和普通信息 |
| `logAttributes` | 日志属性集合；描述日志来源实例、线程、类名、文件路径、环境等上下文 |
| `time` | 日志事件时间戳，毫秒值；适合程序按时间排序或二次处理 |
| `serviceName` | 应用名称；标识日志归属的业务服务 |
| `body` | 日志详情原文；通常包含异常、调用参数、错误原因等诊断信息 |
| `timestamp` | 日志时间的可读格式；适合人工阅读和快速定位问题时间点 |

常见 `logAttributes` 语义：

| 键 | 监控含义 |
|----|----------|
| `companyId` | 组织 ID；用于多组织隔离和日志筛选 |
| `hostname` | 容器名或 Pod 名；用于定位具体运行实例 |
| `ip` | 实例 IP；用于排查节点或网络侧问题 |
| `filePath` | 日志文件路径；用于判断日志来源文件 |
| `thread` | 线程名；用于定位并发请求和线程上下文 |
| `env` | 环境标识；例如 `prd`、`test`、`dev` |
| `class` | 产生日志的类名；用于快速回溯代码位置 |
| `codeline` | 代码文件与行号；用于进一步定位触发日志的源码位置 |
| `configId` | 日志采集配置 ID；用于识别日志归属的采集配置 |
| `namespace` | 运行命名空间；用于区分不同部署域 |

## 适用场景

- 按应用和时间窗口检索业务系统日志
- 结合 `traceId` 和 `spanId` 回溯一次调用链上的异常日志
- 按 `ERROR` 或 `WARN` 快速聚焦高优先级问题
- 结合 `hostname`、`class`、`codeline` 和 `body` 定位具体报错实例与代码位置
