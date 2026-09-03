---
name: monitor-jvm
description: "Cubelet：监控域 JVM 指标查询能力，包括查询系统容器 JVM 指标定义列表，以及根据容器实例名称和时间区间查询 JVM 监控指标数据（仅适用于 Java 语言应用）。"
metadata:
  version: 0.1.0
  openclaw:
    category: "monitor"
    domain: "monitor"
    requires:
      bins:
        - cubelet
    cliHelp: "cubelet jvm --help"
---

# jvm

> **PREREQUISITE:** 先阅读 `../shared/SKILL.md`，确认配置文件、全局 flag 和输出格式。

```bash
cubelet jvm <command> [flags]
```

## Commands

| Command | 说明 |
|---------|------|
| `getMetric` | 查询系统容器 JVM 指标定义列表 |
| `metrics` | 根据容器实例名称、时间区间和指标列表查询容器 JVM 监控指标数据 |

## 环境约定

- 常用标准环境名称映射：生产环境=`prd`，公共环境=`pub`，测试环境=`test`
- 当用户未提供环境信息时，执行本 skill 中相关 CLI 命令按 `prd`、`pub`、`test` 顺序尝试
- 如果 3 个环境都返回空数据或空数组 `[]`，询问客户对应的环境信息
- 如果客户已提供环境信息，但返回结果为空或空数组 `[]`，提示客户系统无数据返回，请确认提供的信息是否正确，尤其是环境信息

## `getMetric`

查询监控服务系统中支持的容器 JVM 指标定义列表（仅适用于 Java 语言应用）。环境参数 `env` 的取值和默认尝试顺序见上文；如需只查询指定逻辑环境的 JVM 指标定义列表，请显式指定环境参数。

常用参数：

- `--env`：逻辑环境名称（可选；环境约定见上文）

示例：

```bash
# 查询 prd 环境下的容器 JVM 指标定义列表（默认）
cubelet jvm getMetric

# 查询指定环境的 JVM 指标定义列表
cubelet jvm getMetric --env dev
```

返回字段说明：

返回按分组组织的指标定义列表，每个分组包含：

| 字段 | 说明 |
|------|------|
| `groupName` | 分组名称（如 GC信息、JVM内存信息、线程信息、其他信息） |
| `panel` | 该分组下的指标列表 |
| `panel[].name` | 指标编码 |
| `panel[].type` | 指标名称 |

## `metrics`

根据容器实例名称列表、查询时间区间及 JVM 指标列表查询容器 JVM 监控指标数据（仅适用于 Java 语言应用）。支持同时查询多个 Pod 和多个指标，多个值之间用逗号分隔。

常用参数：

- `--pod`：容器实例名称列表，多个用逗号分隔（必填，可从 `cubelet pod list` 获取）
- `--start`：查询开始时间，毫秒时间戳（必填）
- `--end`：查询结束时间，毫秒时间戳（必填）
- `--m`：JVM 指标名称列表，多个用逗号分隔（必填）
- `--env`：逻辑环境名称（可选；环境约定见上文）

JVM 指标名称：

> 指标列表非固定值，请通过 `cubelet jvm getMetric` 命令动态获取当前环境支持的完整 JVM 指标定义列表。

示例：

```bash
# 查询单个 Pod 的 fullGC 次数
cubelet jvm metrics --pod seraph-metadata-d96h8-86d78fbc7d-b848z --start 1776043865402 --end 1776045665402 --m jvm_gc_pause_seconds_count

# 查询多个 Pod 的多个 JVM 指标
cubelet jvm metrics --pod seraph-metadata-d96h8-86d78fbc7d-b848z,seraph-metadata-mxqjk-76d5765fc7-lps7m --start 1776043865402 --end 1776045665402 --m jvm_gc_pause_seconds_count,jvm_memory_pool_bytes_used

# 指定环境查询
cubelet jvm metrics --pod seraph-metadata-d96h8-86d78fbc7d-b848z --start 1776043865402 --end 1776045665402 --m jvm_gc_pause_seconds_count --env prd
```

返回格式为指标序列列表，每个指标包含：

| 字段 | 说明 |
|------|------|
| `type` | 指标名称 |
| `data` | 时间序列数据点列表 |
| `data[].x` | 时间点 |
| `data[].y` | 指标值 |
| `data[].pod_name` | 容器实例名称 |
| `data[].area` | JVM 区域标签（如 heap），部分指标包含 |
| `data[].laber` | JVM 标签（如 Tenured Gen），部分指标包含 |
| `data[].id` | JVM 标识（如内存池名称），部分指标包含 |
| `data[].gc` | GC 类型（如 MarkSweepCompact），部分指标包含 |
| `data[].cause` | GC 原因（如 CodeCache GC Threshold），部分指标包含 |

## 适用场景

- 排查 Java 应用 GC 相关问题（fullGC 次数、耗时）
- 监控 JVM 堆内存和非堆内存使用情况
- 分析线程状态（繁忙线程、峰值线程数）
- 查看 JVM 类加载和文件句柄使用状况
- 辅助 Java 应用性能调优和故障定位
