---
name: mantis-test-design
description: "测试设计：基于 @ 需求文件或 Cube 事项生成测试设计草稿（摘要、脑图、场景、覆盖矩阵，用户可见文案须为中文），并写入项目 .brain-quality 会话状态（阶段 04）。在用户提到测试设计、$ mantis-test-design、质量设计、需求转测试设计时使用。"
metadata:
  version: 0.2.0
  openclaw:
    category: "qa"
    requires:
      bins:
        - cubelet
    cliHelp: "cubelet team getissue --help"
---

# mantis-test-design（测试设计）

在 Brain **质量工程扩展**（`devcube.quality-engineering`）中完成 **阶段 04：测试设计**。产出写入项目工作区测试资产，并更新会话状态文件；**不得**把阶段标记为 `confirmed`。

## 数据边界（强制）

| 路径 | 用途 |
| --- | --- |
| `tests/design/**/*.md` | 测试设计交付物 |
| `.brain-quality/sessions/<sessionId>/state.json` | 当前会话质量工程状态（**唯一 sidecar**） |
| `.brain-quality/targets/project.json` | 项目默认 UI/API 地址（只读，勿在本阶段修改） |

**不再使用** `brain-workspace-server quality upsert-draft` 或 `{sessionId}-quality.json`（Brain 内核已移除 quality CLI）。

扩展任务 prompt 会给出具体 `state.json` 路径（形如 `.brain-quality/sessions/<sessionId>/state.json`）。`<sessionId>` 以该路径为准。

## 会话绑定（最高优先级）

本 Skill 可能由质量工程扩展命令调用，也可能由用户直接调用。两种入口都必须把结果写入**当前 Brain 会话**，禁止通过历史文件推断会话。

1. 先读取运行时注入的 `BRAIN_SESSION_ID`。在 Brain 会话中不得手工设置或覆盖这个变量。
2. 若任务 prompt 明确给出“会话质量状态文件”路径，使用该精确路径；同时校验路径中的会话 ID 与 `BRAIN_SESSION_ID` 一致。两者不一致时立即停止并报告绑定冲突。
3. 若 prompt 没有给出状态文件路径，必须使用 `.brain-quality/sessions/${BRAIN_SESSION_ID}/state.json`。`BRAIN_SESSION_ID` 为空时立即停止并报告当前运行环境缺少会话上下文。
4. 写入前后都必须校验 `state.json.sessionId` 等于当前会话 ID。状态文件不存在时，只能在上述精确路径创建，不能先扫描其它会话寻找模板。

禁止使用 `find`、`rg`、`ls`、文件修改时间、需求标题、事项 ID、最近打开记录或 transcript 扫描来选择会话；禁止读取或写入其它会话的 `state.json`。这类“猜一个最像的会话”的行为会把面板和聊天拆开，是错误而不是降级策略。

## 语言（强制）

产品默认语言为中文（zh-CN）。所有**用户可见产出物**必须使用简体中文，禁止用英文写验收点、场景标题、摘要、脑图节点文案。

| 允许英文/原文 | 必须中文 |
| --- | --- |
| `REQ-*` / `SCN-*` 等稳定 ID | `summary`、设计 md 正文 |
| 文件路径、协议字段 | `mindmap.title`、节点 `label`（除 ID 叶子可并列 ID） |
| 专有名词、产品名、API 名 | `coverageRows.acLabel`（验收点） |
| | `scenarios.title`、`pathSummary` |
| | 会话回复中对用户的说明 |

## Mindmap 结构（强制）

写入 `stages.design.mindmap` 时，**必须**满足分层结构与边关系，禁止仅输出扁平节点列表。

### 节点 kind（必填）

| kind | 用途 | label 语言 |
| --- | --- | --- |
| `root` | 唯一根节点 | 中文 |
| `group` | 分组（如「需求」「场景」） | 中文 |
| `req` | 需求叶子，`id` 建议 `req:REQ-*` | ID 可英文 |
| `scenario` | 场景叶子，`id` 建议 `scn:SCN-*` | ID 可英文 |

### 边 edges（必填）

- **MUST** 提供 `edges: [{ from, to }]`，形成 `root → group → leaf`。
- 典型：`root → g-req → req:*`，`root → g-scn → scn:*`。
- 脑图只放**测试场景设计**，不要把需求正文塞进节点 label。

### 主路径 scenarios

**MUST** 写入 `stages.design.scenarios`：

```json
"scenarios": [
  { "id": "SCN-CART-001", "title": "主路径结算", "pathSummary": "选品→结算→支付成功" }
]
```

待覆盖的 `req` / `scenario` 叶子节点设 `"status": "pending"`。

## Workflow

1. **读取需求** — 先读 `state.json` 的 `source`。若 `source.sourceType === "cube-item"`，用 `source.cubeItemId` 执行 `cubelet team getissue`，**勿**要求用户再次 `@` 需求文件；否则读用户 `@` 的文件或 prompt 内嵌需求上下文（看板触发时 prompt 已含 Team 详情，**以 prompt 为唯一事实源**）。
2. **产出设计资产** — 写入 `tests/design/<domain>/<feature>.design.md`（中文正文）。
3. **更新会话状态** — 读取现有 `state.json`，合并更新后写回（见下节）。`stages.design.status` **保持** `"pending"`。
4. **说明下一步** — 告知用户可在右侧 **质量工程** 面板继续编辑；需要功能用例时点 **「生成功能用例」**（产品会自动固化设计并提交 Agent）。

## 更新 state.json

1. 若文件不存在，以如下骨架创建（`projectId` / `sessionId` 与 Brain 当前会话一致）：

```json
{
  "version": 1,
  "projectId": "<projectId>",
  "sessionId": "<sessionId>",
  "context": { "branch": "", "env": "" },
  "stages": {
    "design": { "status": "pending" },
    "cases": { "status": "pending", "caseIds": [] },
    "scripts": { "status": "pending", "paths": [] },
    "run": { "status": "queued" }
  },
  "trace": { "reqIds": [], "scenarioIds": [], "caseIds": [], "runIds": [] },
  "audit": [],
  "revision": 0,
  "updatedAt": "<ISO8601>"
}
```

2. 合并写入（保留 `source`、`context`、`stages.run`、既有 `audit`）：

```json
{
  "stages": {
    "design": {
      "status": "pending",
      "summary": "购物车结算主路径",
      "artifactPaths": ["tests/design/cart/cart-checkout.design.md"],
      "mindmap": { "title": "购物车结算", "nodes": [...], "edges": [...] },
      "coverageRows": [{ "reqLabel": "REQ-CART-01", "acLabel": "主路径可下单", "scenarioLabel": "SCN-CART-001", "status": "pending" }],
      "scenarios": [{ "id": "SCN-CART-001", "title": "主路径结算", "pathSummary": "选品→结算→支付成功" }]
    }
  },
  "trace": {
    "reqIds": ["REQ-CART-01"],
    "scenarioIds": ["SCN-CART-001"]
  }
}
```

3. 写回时：`revision` 在现有值上 **+1**；`updatedAt` 设为当前 ISO 时间；`audit` 末尾追加 `{ "at": "<ISO>", "by": "agent", "action": "skill:mantis-test-design:draft" }`（保留最近 200 条）。

4. **只改** `stages.design` 与 `trace.reqIds` / `trace.scenarioIds`；不要清空 `source`，不要改 `stages.cases` / `stages.scripts` / `stages.run`（扩展在触发本 skill 前可能已重置下游阶段）。

## Rules

- **MUST** 用户可见文案使用简体中文。
- **MUST** 同时写入设计 md 与 `state.json`；仅写文件不更新 state 会导致面板空白。
- **MUST NOT** 设置 `stages.design.status` 为 `"confirmed"`；固化由产品在「生成功能用例」等下一动作前自动完成。
- **MUST NOT** 调用已移除的 `quality:*` RPC / `brain-workspace-server quality` CLI。
- **MUST NOT** 要求用户人工确认阶段。
- 发现当前需求与旧设计不一致时，以**当前需求**为准覆盖本会话状态（看板 re-trigger 时扩展会重置 design 为 pending）。
