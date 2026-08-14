---
name: mantis-auto-run
description: "自动化执行提示：在自动化脚本已生成后，引导用户在质量工程面板本机跑 Playwright(UI)/k6(API)（阶段 07）。在用户提到执行自动化、$ mantis-auto-run、跑脚本、执行报告时使用。"
---

# mantis-auto-run（自动化执行）

质量工程 **阶段 07：本机执行**。由 **质量工程扩展** 面板触发 Playwright / k6；本 Skill 只做前置检查与引导，**不要**在 Agent 侧自行 `spawn`。

## 数据边界

| 路径 | 用途 |
| --- | --- |
| `.brain-quality/sessions/<sessionId>/state.json` | 阶段与脚本路径 |
| `.brain-quality/targets/project.json` | 项目默认 UI/API 地址 |
| `.brain-quality/runs/<runId>/` | 单次运行日志与报告 |
| `.brain-quality/runs/history.jsonl` | 运行历史（只读参考） |

**不再使用** Brain 内核 `quality:trigger-run` RPC 或 `brain-workspace-server`。

## 执行环境（硬约束）

| 路径 | 运行时 | 来源 |
| --- | --- | --- |
| `tests/ui/**` | Playwright | Brain 私有运行时 |
| `tests/api/**` | k6 | Brain 私有运行时 |

**不要**要求业务仓库安装 `@playwright/test` 或 k6。缺少组件时，引导用户在面板 **「准备并执行」**。

## Prerequisite

读取 `state.json`：

1. `stages.scripts.paths` 非空（已有脚本草稿或已固化）。
2. `stages.run.status !== "running"`。
3. 面板「执行目标」已配置有效地址（`tests/ui/**` 需 UI 基址，`tests/api/**` 需 API 基址）；会话 `context.uiBaseUrl` / `context.apiBaseUrl` 可覆盖项目默认（`.brain-quality/targets/project.json`）。

若脚本路径为空：**停止**，请用户先生成自动化脚本。  
若地址缺失：**停止**，请用户在「执行目标」填写后再执行。

## Workflow

1. **核对 state** — 确认 `stages.scripts.paths` 与脚本文件存在。
2. **核对执行目标** — 提醒有效 UI/API 地址；脚本应读 `BRAIN_QUALITY_UI_BASE_URL` / `BRAIN_QUALITY_API_BASE_URL`（k6 用 `__ENV`）。
3. **引导面板执行** — 打开 **质量工程 → 自动化用例**，点击 **「执行 UI」**、**「执行 API」** 或 **「执行用例」**（全部时 UI → API 串行）。
4. **解读结果** — 根据面板报告（runId、passed/failed/env_error、summary）说明下一步；失败时读 `.brain-quality/runs/<runId>/logs/ui.log` 或 `logs/api.log`。

## Rules

- **MUST NOT** 自行调用本机 `npx playwright` / `k6 run` 作为主路径。
- **MUST NOT** 修改 `state.json` 中的 `stages.run`（扩展 runner 负责）。
- **MUST NOT** 调用尚未开放的缺陷发现 / 提单 RPC。
- 环境缺失对应 `env_error`：提示在面板准备 Playwright、Chromium 或 k6，而不是改写脚本。
