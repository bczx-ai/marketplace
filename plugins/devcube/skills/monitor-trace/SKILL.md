---
name: monitor-trace
description: "DevCube：监控域调用链查询能力，包括查询业务应用调用链接口性能指标、接口请求列表、调用链详情和慢查询列表。"
---

# trace

> **PREREQUISITE:** 先阅读 [DevCube 公共规则](../devcube/SKILL.md)，确认配置文件、全局 flag 和输出格式。

```bash
cubelet --config "$CUBELET_CONFIG" trace <command> [flags]
```

## Commands

| Command | 说明 |
|---------|------|
| `interfacePerf` | 查询业务应用调用链接口性能指标数据 |
| `searchSpan` | 查询业务应用调用链中具体接口请求列表数据 |
| `detail` | 根据调用链 ID 查询业务应用调用链详情数据 |
| `slowQuery` | 查询业务应用调用链中的慢查询列表数据 |

## 环境约定

- 常用标准环境名称映射：生产环境=`prd`，公共环境=`pub`，测试环境=`test`
- 当用户未提供环境信息时，执行本 skill 中相关 CLI 命令按 `prd`、`pub`、`test` 顺序尝试
- 如果 3 个环境都返回空数据或空数组 `[]`，询问客户对应的环境信息
- 如果客户已提供环境信息，但返回结果为空或空数组 `[]`，提示客户系统无数据返回，请确认提供的信息是否正确，尤其是环境信息

## `interfacePerf`

根据应用名称和查询时间区间查询业务应用调用链接口性能指标数据，包括请求次数、失败率、响应时间百分位线、QPS 等。

常用参数：

- `--app`：应用名称（必填）
- `--start`：查询开始时间，毫秒时间戳（必填）
- `--end`：查询结束时间，毫秒时间戳（必填）
- `--env`：逻辑环境名称（可选；环境约定见上文）

时间戳说明：

- 参数值为 Unix 毫秒时间戳（13 位数字）
- 例如 `1776043865402` 对应一个具体的日期时间
- 可通过 `date +%s000` 获取当前毫秒时间戳

示例：

```bash
# 查询 prd 环境下 seraph-metadata 应用的接口性能指标（默认环境）
cubelet --config "$CUBELET_CONFIG" trace interfacePerf --app seraph-metadata --start 1776043865402 --end 1776045665402

# 显式指定环境
cubelet --config "$CUBELET_CONFIG" trace interfacePerf --app seraph-metadata --start 1776043865402 --end 1776045665402 --env prd

# 查询 dev 环境
cubelet --config "$CUBELET_CONFIG" trace interfacePerf --app demo-app --start 1776043865402 --end 1776045665402 --env dev
```

返回字段说明：

| 字段 | 说明 |
|------|------|
| `operation` | 接口操作名 |
| `totalCount` | 请求次数 |
| `errorCount` | 失败次数 |
| `errorRate` | 失败率 |
| `avgTime` | 平均响应时间（ms） |
| `maxTime` | 最大响应时间（ms） |
| `minTime` | 最小响应时间（ms） |
| `p50` | 50 分位响应时间（ms） |
| `p90` | 90 分位响应时间（ms） |
| `p95` | 95 分位响应时间（ms） |
| `p99` | 99 分位响应时间（ms） |
| `qps` | 每秒请求数 |

## `searchSpan`

根据应用名称、查询时间区间、接口操作名等查询业务应用调用链中具体接口请求列表数据。

常用参数：

- `--app`：应用名称（必填）
- `--start`：查询开始时间，毫秒时间戳（必填）
- `--end`：查询结束时间，毫秒时间戳（必填）
- `--operation`：接口操作名（必填）
- `--minDuration`：查询耗时大于该值的记录（ms），默认 `100`（可选）
- `--queryErrorTrace`：是否只查询包含错误的追踪记录，默认 `false`（可选）
- `--env`：逻辑环境名称（可选；环境约定见上文）

示例：

```bash
# 查询 prd 环境下 cube-base 应用某接口的调用链请求列表
cubelet --config "$CUBELET_CONFIG" trace searchSpan --app cube-base --start 1776043865402 --end 1776045665402 --operation "GET /base/Filter/getFilterById/{id}"

# 只查询耗时大于 500ms 的请求
cubelet --config "$CUBELET_CONFIG" trace searchSpan --app cube-base --start 1776043865402 --end 1776045665402 --operation "GET /base/Filter/getFilterById/{id}" --minDuration 500

# 只查询包含错误的追踪记录
cubelet --config "$CUBELET_CONFIG" trace searchSpan --app cube-base --start 1776043865402 --end 1776045665402 --operation "GET /base/Filter/getFilterById/{id}" --queryErrorTrace true

# 查询 dev 环境
cubelet --config "$CUBELET_CONFIG" trace searchSpan --app demo-app --start 1776043865402 --end 1776045665402 --operation "POST /api/v1/orders" --env dev
```

返回字段说明：

| 字段 | 说明 |
|------|------|
| `traceID` | 调用链 ID |
| `spanID` | 调用段 ID |
| `duration` | 请求耗时（ms） |
| `startTimeMillis` | 请求开始时间（毫秒时间戳） |
| `spanName` | 调用段名称 |

## `detail`

根据调用链 ID 查询业务应用调用链详情数据。命令内部会自动为后端接口构造最近 10 分钟内的随机时间窗，并将后端返回的 `result.spans` 原样作为输出结果。

常用参数：

- `--traceId`：调用链 ID（必填，可通过 `cubelet --config "$CUBELET_CONFIG" trace interfacePerf` 结果或告警通知信息获取）
- `--env`：逻辑环境名称（可选；环境约定见上文）

调用说明：

- 命令不要求用户传入 `--start`、`--end`
- CLI 会自动调用 GET `/v3/trace`
- 请求头会自动带上 `env` 和当前登录用户组织对应的 `company-id`
- 后端响应中的 `result.spans` 会直接作为命令输出

示例：

```bash
# 查询 prd 环境下指定 traceId 的调用链详情
cubelet --config "$CUBELET_CONFIG" trace detail --traceId af65e343bdfcbbc0a1d046c235a419b6

# 显式指定环境
cubelet --config "$CUBELET_CONFIG" trace detail --traceId af65e343bdfcbbc0a1d046c235a419b6 --env prd
```

返回字段说明：

| 字段 | 监控含义 |
|------|----------|
| `timestamp` | 调用段开始时间，毫秒时间戳；用于按时间轴还原整条调用链 |
| `traceId` | 调用链 ID；同一条分布式请求链路上的所有 span 共享该值 |
| `spanId` | 当前调用段 ID；用于唯一标识当前 span |
| `parentSpanId` | 父调用段 ID；用于重建上下游调用关系和树结构 |
| `spanName` | 调用段名称；通常是接口名、RPC 方法名、SQL 操作名或消息处理动作 |
| `spanKind` | 调用段角色；`SERVER` 表示入口服务端处理，`CLIENT` 表示对下游的主动调用，其他值可表示内部处理、生产者、消费者等 |
| `serviceName` | 产生该 span 的服务名；用于识别链路中的具体业务应用 |
| `resourceAttributes` | 资源维度标签集合；描述产生 span 的服务、实例、宿主机、环境等稳定属性 |
| `scopeName` | 采集/埋点组件名称；反映该 span 由哪个 instrumentation scope 上报 |
| `scopeVersion` | 采集/埋点组件版本；用于判断采集 SDK 或探针版本差异 |
| `spanAttributes` | span 维度标签集合；描述本次请求的协议、路由、地址、状态码、租户等动态语义信息 |
| `duration` | 调用段耗时（ms）；定位慢调用、卡点和性能瓶颈的核心字段 |
| `statusCode` | OpenTelemetry span 状态码；表示该 span 是否被标记为错误，不等同于 HTTP 状态码 |
| `eventTimestamps` | span 事件时间点列表；与 `eventNames` 一一对应，常用于异常或关键事件定位 |
| `eventNames` | span 事件名称列表；例如异常、重试、超时等诊断事件 |
| `eventAttributes` | span 事件附加属性；通常承载异常类型、错误消息、堆栈等上下文 |

常见 `resourceAttributes` 语义：

| 键 | 监控含义 |
|----|----------|
| `service.name` | 服务名；和 `serviceName` 一起用于标识调用段所属应用 |
| `service.id` | 服务或实例标识；可用于区分不同部署单元 |
| `company.id` | 组织 ID；用于多组织隔离和过滤 |
| `host.name` | 主机名或 Pod 名；用于定位具体运行实例 |
| `env` | 环境标识；例如 `prd`、`test`、`dev` |

常见 `spanAttributes` 语义：

| 键 | 监控含义 |
|----|----------|
| `http.method` | HTTP 方法，如 `GET`、`POST` |
| `http.route` | 归一化路由模板；适合做接口聚合分析 |
| `http.target` | 实际请求路径；通常包含真实入参路径段 |
| `http.status_code` | HTTP 响应码；用于判断接口结果和错误类型 |
| `http.url` | 下游调用 URL 或路径 |
| `http.scheme` | 协议方案，如 `http`、`https` |
| `http.client_ip` | 客户端 IP；用于定位请求来源 |
| `http.response_content_length` | 响应体长度；辅助判断大包返回或异常响应 |
| `net.host.name` | 接收请求的主机名 |
| `net.protocol.name` | 网络协议名，如 `http` |
| `net.protocol.version` | 协议版本，如 `1.1` |
| `net.sock.peer.addr` | 对端 IP；入口 span 中通常是客户端地址，出口 span 中通常是下游地址 |
| `net.sock.peer.port` | 对端端口 |
| `net.sock.host.addr` | 本端监听地址 |
| `net.sock.host.port` | 本端监听端口 |
| `user_agent.original` | 原始 User-Agent；用于区分浏览器、客户端或探针来源 |
| `tenant` | 业务租户或逻辑租户标签；用于多租户调用链分析 |

## `slowQuery`

根据应用名称、查询时间区间等查询业务应用调用链中的慢查询列表数据。

常用参数：

- `--app`：应用名称（必填）
- `--start`：查询开始时间，毫秒时间戳（必填）
- `--end`：查询结束时间，毫秒时间戳（必填）
- `--minDuration`：按后端接口语义筛选耗时小于该值的慢查询记录，单位 ms，默认 `100`；如果显式传入，必须大于等于 `100`
- `--env`：逻辑环境名称（可选；环境约定见上文）

调用说明：

- `--start` 和 `--end` 的时间区间必须小于等于 10 分钟
- CLI 会将毫秒时间戳转换成 `YYYY-MM-DD HH:mm:ss` 后再调用后端接口
- CLI 会自动在请求头中带上 `env` 和当前登录用户组织对应的 `company-id`
- 命令输出只保留慢查询场景需要的字段，不透出多余后端字段
- 这里的 `minDuration` 语义沿用后端 GET `/v3/getSlowQuery`：筛选耗时小于该值的记录

示例：

```bash
# 查询 prd 环境下 cube-base 应用最近一段时间的慢查询列表
cubelet --config "$CUBELET_CONFIG" trace slowQuery --app cube-base --start 1776306480000 --end 1776307080000

# 显式指定筛选阈值和环境
cubelet --config "$CUBELET_CONFIG" trace slowQuery --app cube-base --start 1776306480000 --end 1776307080000 --minDuration 500 --env prd
```

返回字段说明：

| 字段 | 监控含义 |
|------|----------|
| `SpanName` | 调用段名称；通常是 SQL 摘要或数据库操作名称 |
| `hostname` | 容器名或 Pod 名；用于定位是哪一个运行实例发起了慢查询 |
| `netPeerName` | 数据库实例地址或主机名；用于识别慢查询命中的数据库实例 |
| `dbSqlTable` | 关联表名；用于定位慢查询主要涉及的数据表，可能为空 |
| `dbSystem` | 数据库系统类型；例如 `mysql`、`postgresql` |
| `dbName` | 数据库名；用于区分实例中的具体 schema 或 database |
| `TraceId` | 调用链 ID；用于把慢查询和整条业务调用链关联起来 |
| `dbOperation` | 数据库操作类型；例如 `SELECT`、`UPDATE`、`INSERT` |
| `Duration` | 当前数据库调用耗时，单位 ms |
| `Timestamp` | 当前数据库调用发生时间，毫秒时间戳 |
| `dbStatement` | 数据库操作语句；通常是原始 SQL 或被截断的 SQL 文本 |
| `SpanId` | 当前数据库调用段 ID；用于和同一条调用链中的父子 span 继续串联 |

## 适用场景

- 分析业务应用各接口的请求量和失败率
- 排查接口响应时间异常，结合 `p50`、`p90`、`p95`、`p99` 判断长尾延迟
- 评估接口 QPS 和容量趋势
- 定位慢接口和高错误率接口
- 查看具体 trace 的完整调用段列表、父子关系和上下游跳转
- 判断问题发生在哪个服务实例、哪个入口 span、哪个下游 span
- 查询某个应用在短时间窗内的数据库慢查询记录
- 结合 `hostname`、`netPeerName`、`dbName` 和 `dbStatement` 快速定位慢 SQL 来源
- 结合 `resourceAttributes` 和 `spanAttributes` 还原调用环境、租户、客户端和网络信息
- 排查包含错误事件、异常事件或超时事件的调用链记录
