---
name: monitor-node
description: "Cubelet：监控域主机节点指标查询能力，包括查询系统主机节点指标定义列表，以及根据主机 IP 列表和时间区间查询主机节点监控指标数据。"
metadata:
  version: 0.1.0
  openclaw:
    category: "monitor"
    domain: "monitor"
    requires:
      bins:
        - cubelet
    cliHelp: "cubelet node --help"
---

# node

> **PREREQUISITE:** 先阅读 `../shared/SKILL.md`，确认配置文件、全局 flag 和输出格式。

```bash
cubelet node <command> [flags]
```

## Commands

| Command | 说明 |
|---------|------|
| `getMetric` | 查询主机监控指标定义列表 |
| `metrics` | 根据主机 IP 列表、时间区间和指标列表查询主机监控指标数据 |

## 环境约定

- 常用标准环境名称映射：生产环境=`prd`，公共环境=`pub`，测试环境=`test`
- 当用户未提供环境信息时，执行本 skill 中相关 CLI 命令按 `prd`、`pub`、`test` 顺序尝试
- 如果 3 个环境都返回空数据或空数组 `[]`，询问客户对应的环境信息
- 如果客户已提供环境信息，但返回结果为空或空数组 `[]`，提示客户系统无数据返回，请确认提供的信息是否正确，尤其是环境信息

## `getMetric`

查询监控服务系统中支持的主机节点指标定义列表。环境参数 `env` 的取值和默认尝试顺序见上文；如需只查询指定逻辑环境的主机指标定义列表，请显式指定环境参数。

常用参数：

- `--env`：逻辑环境名称（可选；环境约定见上文）

示例：

```bash
# 查询 prd 环境下的主机节点指标定义列表（默认）
cubelet node getMetric

# 查询指定环境的主机指标定义列表
cubelet node getMetric --env dev
```

返回字段说明：

返回按分组组织的指标定义列表，每个分组包含：

| 字段 | 说明 |
|------|------|
| `groupName` | 分组名称（如 CPU和内存、磁盘与网络、TCP、负载） |
| `panel` | 该分组下的指标列表 |
| `panel[].name` | 指标编码 |
| `panel[].type` | 指标名称 |

## `metrics`

`--nodeIp` 可以直接使用 `cubelet pod list` 返回结果中的 `nodeIp`。这适合在发现某个 Pod/容器实例资源异常后，继续查看其所在主机节点的 CPU、内存等资源使用率。

根据主机 IP 列表、查询时间区间及指标列表查询主机节点监控指标数据。支持同时查询多个主机 IP 和多个指标，多个值之间用逗号分隔。

常用参数：

- `--nodeIp`：主机 IP 列表，多个用逗号分隔（必填）；可直接使用 `cubelet pod list` 返回的 `nodeIp`，用于查看 Pod 所在主机节点资源使用率
- `--start`：查询开始时间，毫秒时间戳（必填）
- `--end`：查询结束时间，毫秒时间戳（必填）
- `--m`：主机指标名称列表，多个用逗号分隔（必填）
- `--env`：逻辑环境名称（可选；环境约定见上文）

主机指标名称：

> 指标列表非固定值，请通过 `cubelet node getMetric` 命令动态获取当前环境支持的完整主机指标定义列表。

示例：

```bash
# 先通过 pod list 获取 nodeIp，再查看对应主机节点指标
cubelet pod list --app seraph-metadata --start 1776043865402 --end 1776045665402 --env prd

# 查询单个主机的 CPU 使用率
cubelet node metrics --nodeIp 172.28.38.11 --start 1776043865402 --end 1776045665402 --m ecs_node_cpu_usage_rate

# 查询多个主机的多个指标
cubelet node metrics --nodeIp 172.28.38.11,172.28.38.12 --start 1776043865402 --end 1776045665402 --m ecs_node_cpu_usage_rate,ecs_node_memory_usage_rate

# 指定环境查询
cubelet node metrics --nodeIp 172.28.38.11 --start 1776043865402 --end 1776045665402 --m ecs_node_cpu_usage_rate --env prd
```

返回格式为指标序列列表，每个指标包含：

| 字段 | 说明 |
|------|------|
| `type` | 指标名称 |
| `data` | 时间序列数据点列表 |
| `data[].x` | 时间点 |
| `data[].y` | 指标值 |
| `data[].instance` | 主机节点名称 |
| `data[].type` | 主机节点 IP |
| `data[].laber` | 指标标签类型（如磁盘设备名称），部分指标包含 |

## 适用场景

- 监控主机 CPU 和内存使用情况
- 排查磁盘使用率和 inode 占用问题
- 分析网络流入流出流量趋势
- 查看 TCP 连接数状态
- 评估主机负载水平（load1/load5/load15）
- 辅助容量规划和扩容决策
