---
name: mantis-auto-generate
description: "自动化用例生成：基于已固化的功能用例生成 Playwright(UI) / k6(API) 脚本草稿并写入 .brain-quality 会话状态（阶段 06）。在用户提到自动化用例生成、$ mantis-auto-generate、spec.js、UI/API 自动化脚本时使用。"
---

# mantis-auto-generate（自动化用例生成）

在 Brain **质量工程扩展**中完成 **阶段 06：自动化用例**。依赖阶段 05 用例已由产品在触发前自动固化（`stages.cases.status === "confirmed"`）。

## 数据边界

| 路径 | 用途 |
| --- | --- |
| `tests/ui/**/*.spec.js` | Playwright UI 脚本 |
| `tests/api/**/*.spec.js` | k6 API 脚本 |
| `.brain-quality/sessions/<sessionId>/state.json` | 会话质量状态 |
| `.brain-quality/targets/project.json` | 项目默认 UI/API 地址（只读参考） |

**不再使用** `brain-workspace-server quality upsert-draft` 或 `{sessionId}-quality.json`。

## 执行环境（硬约束）

质量工程扩展本机执行**只**支持：

| 路径 | 运行时 |
| --- | --- |
| `tests/ui/**/*.spec.js` | Playwright（Brain 私有运行时） |
| `tests/api/**/*.spec.js` | k6（Brain 私有运行时） |

### MUST

- UI：`require('@playwright/test')`，用 `test` / `test.describe`。
- UI：文件或 `describe` 级 `test.use({ screenshot: 'only-on-failure', trace: 'retain-on-failure' })`；**禁止**每用例手写 `page.screenshot()` 作失败截图方案。
- API：k6——`import http from 'k6/http'`、`import { check } from 'k6'`，`export default function () { ... }`；环境变量用 `__ENV.NAME`。
- 被测地址由 Brain 注入（勿写死唯一 localhost）：
  - UI：`process.env.BRAIN_QUALITY_UI_BASE_URL`
  - API：`__ENV.BRAIN_QUALITY_API_BASE_URL`
- 缺少 Playwright/k6 时，引导用户在面板 **「准备并执行」**；不要改业务项目 `package.json`。

### MUST NOT

- **禁止** API 写成 Node 脚本（`fetch`、`process.env` 跑测试、`module.exports`）。
- **禁止** Jest / Mocha / vitest 替代 Playwright 或 k6。
- **禁止** 在 Skill 内自行 `spawn` 执行。

## Prerequisite

读取 `state.json`：

- `stages.cases.status === "confirmed"` 且存在 `caseIds` / `artifactPaths`。
- 若 `stages.scripts.status === "written"`：**停止**（脚本已固化，需用户在面板重新生成流程）。

若不满足：**停止**，请用户点击 **「生成自动化用例」**。

## Workflow

1. **读取已固化用例** — `stages.cases` + `tests/cases/**/*.cases.yaml` + 关联设计摘要。
2. **生成脚本** — UI → `tests/ui/...spec.js`；API → `tests/api/...spec.js`。
3. **更新 state.json** — 合并 `stages.scripts.paths`；`stages.scripts.status` **保持** `"pending"`（执行前由产品设为 `written`）。
4. **交付下一步** — 引导用户在 **自动化用例** Tab 点击 **「执行 UI」** / **「执行 API」** / **「执行用例」**。

## 更新 state.json

```json
{
  "stages": {
    "scripts": {
      "status": "pending",
      "paths": [
        "tests/ui/cart/cart-checkout.spec.js",
        "tests/api/cart/cart-checkout.spec.js"
      ]
    }
  }
}
```

写回：`revision + 1`、`updatedAt`、`audit` 追加 `{ "action": "skill:mantis-auto-generate:draft" }`。

## 最小骨架示例

### UI（Playwright）

```js
const { expect, test } = require('@playwright/test')

test.use({
  screenshot: 'only-on-failure',
  trace: 'retain-on-failure',
})

test.describe('功能名 UI', () => {
  test('场景标题', async ({ page }) => {
    await page.goto(process.env.BRAIN_QUALITY_UI_BASE_URL || 'http://localhost:5173')
    await expect(page.getByText('示例')).toBeVisible()
  })
})
```

### API（k6）

```js
import http from 'k6/http'
import { check, fail } from 'k6'

export const options = { vus: 1, iterations: 1 }

const baseURL = __ENV.BRAIN_QUALITY_API_BASE_URL || 'http://localhost:8080/api/v1'

export default function () {
  const res = http.get(`${baseURL}/health`)
  if (!check(res, { 'status is 200': (r) => r.status === 200 })) {
    fail(`health 失败 status=${res.status}`)
  }
}
```

## Rules

- **MUST NOT** 在 cases 未固化时生成脚本。
- **MUST NOT** 设置 `stages.scripts.status` 为 `"written"` 或 `"confirmed"`。
- **MUST NOT** 调用已移除的 quality CLI / RPC。
- **MUST NOT** 要求用户人工确认脚本；生成后只引导执行。
