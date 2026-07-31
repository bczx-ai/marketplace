# Brain diagnostic report template

Use every section below. Write `无` or `未知` instead of omitting a field. Keep the report concise enough for an engineer to scan before opening source code.

```markdown
# Brain 诊断报告

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 报告编号 | BR-YYYYMMDD-HHMMSS |
| 生成时间 | ISO 8601 timestamp |
| 诊断窗口 | start - end |
| 运行形态 | desktop / workspace / standalone / local |
| Runtime / Shell | version or 未知 |
| 平台 | platform + arch + OS release |
| 问题指纹 | runtime version + primary error label + stable error phrase |

## 结论

- 结论等级：已确认 / 高概率 / 证据不足
- 根因：一句可证伪的根因陈述
- 影响：用户实际受影响的流程和范围

## 用户症状与复现

- 用户看到的现象：
- 发生时间：
- 复现步骤：
- 预期行为：
- 实际行为：

## 事件时间线

| 时间 | 事件 | 证据 | 与故障关系 |
| --- | --- | --- | --- |
| ISO timestamp | concise event | evt-001 | cause / consequence / context |

## 根因分析

Describe the causal chain, why it explains the symptom, and where the chain is incomplete.

## Session Transcript 健康

- 当前会话：size / risk / modifiedAt，或 `未唯一匹配`
- 扫描汇总：filesScanned / totalBytes / searchExcludedCount / highRiskCount / scanTruncated

| 匿名引用 | 大小 | 最近修改 | 风险 | 当前会话 |
| --- | --- | --- | --- | --- |
| transcript-001 | bytes and human-readable MiB | ISO timestamp | normal / search-excluded / high-risk | 是 / 否 |

Explain whether transcript size is causally relevant to the reported symptom. Do not present a size threshold alone as the root cause.

### 仍可能的替代原因

- Alternative and the exact evidence needed to confirm or reject it.

## 关键证据

### evt-001 LABEL

Short redacted excerpt and its interpretation.

## 建议

### 用户临时处理

- Only low-risk workarounds supported by evidence. Otherwise write `无可靠临时方案`.

### 研发处理

- Source subsystem or boundary to inspect.
- Concrete verification or fix direction.
- Regression scenario to add.

## 待补信息

- Missing evidence that would materially change the conclusion, or `无`.

## 数据范围与脱敏

- Log sources and lookback window.
- `filesScanned`, `bytesRead`, `matchedEvents`, `omittedEvents`, and `truncated`.
- Session transcript metadata scope, thresholds, counts, `scanTruncated`, and warnings.
- Collector warnings.
- State that raw logs, configuration, credentials, Session content, Session/project ids, and project content were not attached.
```

Do not include unsupported reproduction steps, generic troubleshooting checklists, full stack traces, raw log files, or a claim that no error exists merely because no matching event was returned.
