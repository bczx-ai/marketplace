---
name: a11y-debugging
description: 基于 web.dev 指南使用 Chrome DevTools MCP 调试并审计网页无障碍能力。测试语义化 HTML、ARIA 标签、焦点状态、键盘导航、触控目标或颜色对比度时使用。
---

## 核心概念

**无障碍树与 DOM**：通过 `CSS opacity: 0` 隐藏元素，与使用 `display: none` 或 `aria-hidden="true"` 对 Screen Reader 的影响不同。`take_snapshot` 返回辅助技术实际感知的无障碍树，应把它作为语义结构的主要事实来源。

**读取 web.dev 文档**：研究特定无障碍指南时，可在 URL 后追加 `.md.txt` 获取纯 Markdown。例如将 `https://web.dev/articles/accessible-tap-targets` 改为 `https://web.dev/articles/accessible-tap-targets.md.txt`。

## 工作流程

### 1. 使用 Lighthouse 自动审计

先运行 Lighthouse 无障碍审计，建立完整基线并获得失败元素和修复建议。

1. 调用 `lighthouse_audit`：
   - 设置 `mode: "navigation"`，刷新页面并捕获加载阶段问题。
   - 设置 `outputDirPath`，例如 `/tmp/lh-report`，保存完整 JSON 报告。
2. 分析摘要：
   - 检查取值范围为 0 至 1 的 `scores`；小于 1 表示存在违规项。
   - 检查 `audits.failed` 数量。
3. 查看报告：
   - 不要逐行读取完整文件。使用 `jq` 或 Node.js 只提取失败审计。

```bash
# 提取失败审计及其详细信息。
node -e "const r=require('./report.json'); Object.values(r.audits).filter(a=>a.score!==null && a.score<1).forEach(a=>console.log(JSON.stringify({id:a.id, title:a.title, items:a.details?.items})))"
```

该方式只输出失败项的 `selector`、`snippet` 等证据，避免把整份报告载入上下文。

### 2. 检查浏览器 Issue

Chrome 会自动检测常见无障碍问题。调用 `list_console_messages`：

- 设置 `types: ["issue"]`。
- 设置 `includePreservedMessages: true`，包含页面加载期间发生的问题。

该结果经常能直接发现标签缺失、ARIA 属性无效等错误。

### 3. 检查语义与结构

1. 导航到目标页面。
2. 使用 `take_snapshot` 获取无障碍树。
3. 检查 `h1`、`h2`、`h3` 等标题层级是否连续且逻辑正确。
4. 对比 `take_screenshot` 与快照结构，确认 DOM 阅读顺序与视觉顺序一致，避免 CSS Float 或绝对定位打乱逻辑顺序。

### 4. 检查标签、表单与文本替代

1. 在 `take_snapshot` 输出中定位按钮、输入框和图片。
2. 确认每个交互元素都有可访问名称；只有图标的按钮不能返回空名称。
3. 读取 [references/a11y-snippets.md](references/a11y-snippets.md)，通过 `evaluate_script` 执行“查找缺少标签的表单控件”。
4. 检查图片是否提供符合内容语义的 `alt` 文本。

### 5. 检查焦点与键盘导航

1. 使用 `press_key` 发送 `Tab` 或 `Shift+Tab` 移动焦点。
2. 使用 `take_snapshot` 获取更新后的无障碍树。
3. 在快照中定位当前获得焦点的元素，确认焦点顺序符合预期。
4. Modal 打开后，焦点必须进入 Modal，并在关闭前保持在其内部。

### 6. 检查触控目标

web.dev 建议触控目标至少为 48x48 像素，并保留足够间距。无障碍树不提供尺寸，因此读取 [references/a11y-snippets.md](references/a11y-snippets.md)，把快照中的元素 `uid` 作为参数，通过 `evaluate_script` 执行“测量触控目标尺寸”。

### 7. 检查颜色对比度

1. 调用 `list_console_messages`，设置 `types: ["issue"]`。
2. 在输出中查找 Low Contrast 问题。

Headless 环境可能不报告该问题。需要手动检查特定元素时，读取 [references/a11y-snippets.md](references/a11y-snippets.md)，执行“检查颜色对比度”。

### 8. 检查页面全局设置

读取 [references/a11y-snippets.md](references/a11y-snippets.md)，执行“检查页面全局设置”，验证页面语言、标题、Viewport 和 Reduced Motion 状态。

## 排障

标准查询失败或 `evaluate_script` 返回异常结果时：

- 自动脚本无法处理渐变图片或复杂背景上的文本时，使用 `take_screenshot` 获取元素画面。
- 截图只能辅助判断明显的可读性问题，不能替代精确的对比度计算。
