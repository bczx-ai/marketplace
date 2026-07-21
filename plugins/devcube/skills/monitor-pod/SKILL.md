---
name: monitor-pod
description: "DevCube：监控域 Pod 实例查询能力，包括查询应用在指定时间范围内的 Pod 列表及CPU/内存使用率，查询系统容器实例指标定义列表，以及查询容器实例监控指标数据。"
---

# pod

> **PREREQUISITE:** 先阅读 [DevCube 公共规则](../devcube/SKILL.md)，确认配置文件、全局 flag 和输出格式。

```bash
cubelet --config "$CUBELET_CONFIG" pod <command> [flags]
```

## Commands

| Command | 说明 |
|---------|------|
| `list` | 查询应用在指定时间范围内的容器实例列表及CPU/内存使用率 |
| `getMetric` | 查询系统容器实例指标定义列表 |
| `metrics` | 根据容器实例名称、时间区间和指标列表查询容器监控指标数据 |

## 环境约定

- 常用标准环境名称映射：生产环境=`prd`，公共环境=`pub`，测试环境=`test`
- 当用户未提供环境信息时，执行本 skill 中相关 CLI 命令按 `prd`、`pub`、`test` 顺序尝试
- 如果 3 个环境都返回空数据或空数组 `[]`，询问客户对应的环境信息
- 如果客户已提供环境信息，但返回结果为空或空数组 `[]`，提示客户系统无数据返回，请确认提供的信息是否正确，尤其是环境信息

## `list`

返回结果新增 `nodeIp` 字段，表示 Pod/容器实例所在的主机节点 IP。拿到这个字段后，可以直接调用 `cubelet --config "$CUBELET_CONFIG" node metrics --nodeIp ...`，继续查看该容器实例对应主机节点的资源使用率。

按应用名称和时间范围查询 Pod 实例信息，返回每个 Pod 的名称、CPU 使用率和内存使用率。这是只读查询命令，不修改任何系统状态。

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
# 查询 prd 环境下 seraph-metadata 应用的 Pod 列表
cubelet --config "$CUBELET_CONFIG" pod list --app seraph-metadata --start 1776043865402 --end 1776045665402

# 显式指定环境
cubelet --config "$CUBELET_CONFIG" pod list --app seraph-metadata --start 1776043865402 --end 1776045665402 --env prd

# 查询 dev 环境
cubelet --config "$CUBELET_CONFIG" pod list --app demo-app --start 1776043865402 --end 1776045665402 --env dev

# 结合返回结果中的 nodeIp，查看对应主机节点资源使用率
cubelet --config "$CUBELET_CONFIG" node metrics --nodeIp 172.28.38.11 --start 1776043865402 --end 1776045665402 --m ecs_node_cpu_usage_rate,ecs_node_memory_usage_rate --env prd
```

返回字段说明：

| 字段 | 说明 |
|------|------|
| `podName` | Pod 实例名称 |
| `nodeIp` | Pod 对应的主机节点 IP，可直接用于 `cubelet --config "$CUBELET_CONFIG" node metrics --nodeIp` |
| `cpuUsageRate` | CPU 使用率（带 % 后缀） |
| `memUsageRate` | 内存使用率（带 % 后缀） |

## `getMetric`

查询监控服务系统中支持的容器实例指标定义列表。环境参数 `env` 的取值和默认尝试顺序见上文；如需只查询指定逻辑环境的指标定义列表，请显式指定环境参数。

常用参数：

- `--env`：逻辑环境名称（可选；环境约定见上文）

示例：

```bash
# 查询 prd 环境下的容器实例指标定义列表（默认）
cubelet --config "$CUBELET_CONFIG" pod getMetric

# 查询指定环境的指标定义列表
cubelet --config "$CUBELET_CONFIG" pod getMetric --env dev
```

返回字段说明：

| 字段 | 说明 |
|------|------|
| `name` | 指标编码 |
| `type` | 指标名称 |

## `metrics`

根据容器实例名称列表、查询时间区间及指标列表查询容器监控指标数据。支持同时查询多个 Pod 和多个指标，多个值之间用逗号分隔。

常用参数：

- `--pod`：容器实例名称列表，多个用逗号分隔（必填）
- `--start`：查询开始时间，毫秒时间戳（必填）
- `--end`：查询结束时间，毫秒时间戳（必填）
- `--m`：指标名称列表，多个用逗号分隔（必填）
- `--env`：逻辑环境名称（可选；环境约定见上文）

常见指标名称：

> 指标列表非固定值，请通过 `cubelet --config "$CUBELET_CONFIG" pod getMetric` 命令动态获取当前环境支持的完整指标定义列表。

示例：

```bash
# 查询单个 Pod 的 CPU 使用率
cubelet --config "$CUBELET_CONFIG" pod metrics --pod seraph-metadata-d96h8-86d78fbc7d-b848z --start 1776043865402 --end 1776045665402 --m k8s_pod_cpu_usage_rate_v1

# 查询多个 Pod 的多个指标
cubelet --config "$CUBELET_CONFIG" pod metrics --pod seraph-metadata-d96h8-86d78fbc7d-b848z,seraph-metadata-mxqjk-76d5765fc7-lps7m --start 1776043865402 --end 1776045665402 --m k8s_pod_cpu_usage_rate_v1,k8s_pod_memory_usage_wss_rate

# 指定环境查询
cubelet --config "$CUBELET_CONFIG" pod metrics --pod seraph-metadata-d96h8-86d78fbc7d-b848z --start 1776043865402 --end 1776045665402 --m k8s_pod_cpu_usage_rate_v1 --env prd
```

返回格式为指标序列列表，每个指标包含：

| 字段 | 说明 |
|------|------|
| `type` | 指标名称 |
| `data` | 时间序列数据点列表 |
| `data[].x` | 时间点 |
| `data[].y` | 指标值 |
| `data[].pod_name` | 容器实例名称 |

## 适用场景

- 查看应用在某段时间内的资源使用情况
- 排查 Pod 级别的 CPU 或内存异常
- 辅助容量评估和扩缩容决策
- 确认某时间段内的 Pod 实例是否正常运行
- 对比多个 Pod 实例的资源使用趋势
- 查看指定时间区间内的 CPU/内存指标变化曲线
