---
name: mantis-case-generate
description: "功能用例生成：基于已固化的测试设计生成 tests/cases/**/*.cases.yaml 功能用例草稿（用例标题与步骤描述须为中文）并写入 .brain-quality 测试需求状态（阶段 05）。在用户提到功能用例生成、$ mantis-case-generate、cases.yaml、回归用例时使用。"
metadata:
  version: 0.2.0
  openclaw:
    category: "qa"
---

# mantis-case-generate（功能用例生成）

在 Brain **质量工程扩展**中完成 **阶段 05：功能用例**。依赖阶段 04 设计已由产品在触发本 skill 前自动固化（`stages.design.status === "confirmed"`）。

## 数据边界

| 路径 | 用途 |
| --- | --- |
| `tests/cases/**/*.cases.yaml` | 功能用例资产 |
| `.brain-quality/project/<编号>-<标题>.json` | 当前测试需求的质量状态 |

**不再使用** `brain-workspace-server quality upsert-draft` 或 `{sessionId}-quality.json`。

## 语言（强制）

用例文件中用户可读字段必须使用简体中文：标题、前置条件、步骤、预期结果。允许英文：用例 `id`、路径、断言中的代码标识符。

## Prerequisite

读取任务 prompt 给出的测试需求状态文件（`.brain-quality/project/<编号>-<标题>.json`）。prompt 没给路径就停止，请用户先在面板顶部选好测试需求；不要自己挑。然后检查：

- `stages.design.status === "confirmed"`，且存在设计摘要 / 资产路径 / trace ID（扩展在点「生成功能用例」时已自动 confirm）。
- 若不满足：**停止**，请用户在质量工程面板点击 **「生成功能用例」**（会先固化设计再提交 Agent）。

## Workflow

1. **读取已固化设计** — 使用 `stages.design`（`summary`、`artifactPaths`、`mindmap`、`scenarios`）及 `tests/design/**` 文件。
2. **生成用例文件** — 写入 `tests/cases/<suite>/<domain>/<feature>.cases.yaml`，追溯到 REQ/SCN。
3. **更新 state.json** — 合并 `stages.cases` 与 `trace.caseIds`（见下节）；`stages.cases.status` **保持** `"pending"`。
4. **说明下一步** — 告知用户可在面板继续编辑；需要自动化时点 **「生成自动化用例」**。

## 更新 state.json

合并示例：

```json
{
  "stages": {
    "cases": {
      "status": "pending",
      "caseIds": ["CASE-CART-001", "CASE-CART-002"],
      "artifactPaths": ["tests/cases/regression/cart/cart-checkout.cases.yaml"]
    }
  },
  "trace": {
    "caseIds": ["CASE-CART-001", "CASE-CART-002"]
  }
}
```

写回规则与 mantis-test-design 相同：`revision + 1`、`updatedAt`、`audit` 追加 `{ "action": "skill:mantis-case-generate:draft" }`。保留 `reqId`、`title`、`prd`、`source`、`context`、`stages.design`、`stages.run`。

## Rules

- **MUST** 用例标题、步骤、预期结果使用简体中文。
- **MUST** 同时写入 yaml 与更新 `state.json`。
- **MUST NOT** 在设计未固化时生成用例。
- **MUST NOT** 设置 `stages.cases.status` 为 `"confirmed"`。
- **MUST NOT** 调用已移除的 quality CLI / RPC。
- 不要强制重新生成自动化脚本；仅当用例内容实际变更时在回复中提示可继续「生成自动化用例」。
