---
name: brain-visualize
description: 在交互 UI 能显著减少理解、比较、探索或输入成本时，直接输出 Brain visualize HTML 围栏，并把用户确认结果填入当前输入框。适用于表单、选项、参数调节、对比和轻量模拟。
license: Apache-2.0
---

# Brain Visualize

仅在交互界面明显优于纯文本时使用本 Skill：

- 一个事实、短回答、简单确认或静态说明使用 Markdown。
- 静态流程、层级和关系图使用 Mermaid。
- 多问题表单、互斥选项、参数探索、动态摘要或轻量模拟使用 `visualize`。

## 输出合同

直接在回复中输出 `visualize` 围栏，不创建本地 HTML 文件或 artifact。围栏内容可以包含 HTML、CSS 和经典内联 JavaScript；不要使用模块、动态 `import()`、外部脚本、外部资源或网络请求。

页面唯一可调用的 Brain 能力是：

```js
await sendBrainInputBarMessage(content)
```

只在用户明确点击按钮或用键盘激活控件的事件处理器中调用并 `await` 它。不得在加载、定时器或自动流程中调用。成功只代表内容已填入当前任务的输入框，Brain 不会自动发送；失败时在界面中显示可理解的状态。

提交内容必须是完整、可独立理解的自然语言，包含问题背景和每个选择结果，不能只提交内部 id、序号或无法脱离界面理解的缩写。

## 界面约束

- 适配 320px 到 736px 的消息宽度，优先使用流式布局，避免固定大宽度和横向滚动。
- 使用原生表单控件、可见 `label`、清晰的键盘焦点、文字校验和状态提示。
- 异步提交期间禁用提交控件并保持其尺寸稳定，完成后恢复，避免重复填入。
- 使用 `--brain-background`、`--brain-foreground`、`--brain-card`、`--brain-primary`、`--brain-primary-foreground`、`--brain-muted`、`--brain-muted-foreground`、`--brain-border`、`--brain-input` 和 `--brain-destructive` 等语义变量适配主题。
- 动画遵守 `prefers-reduced-motion`；颜色不能是表达状态的唯一方式。
- 不访问 parent、storage、cookie、文件、剪贴板、preload、宿主对象、RPC 或工具。

## 完整示例

```visualize
<form id="plan" class="card">
  <fieldset>
    <legend>请选择实现分支</legend>
    <label><input type="radio" name="branch" value="新建 codex/visualize 分支" required> 新建独立分支</label>
    <label><input type="radio" name="branch" value="继续当前分支"> 继续当前分支</label>
  </fieldset>
  <fieldset>
    <legend>是否删除旧实现？</legend>
    <label><input type="radio" name="cleanup" value="删除旧实现" required> 删除</label>
    <label><input type="radio" name="cleanup" value="保留旧实现"> 保留</label>
  </fieldset>
  <label>最大并发数 <input id="concurrency" type="number" min="1" max="8" value="4"></label>
  <button type="submit">填入输入框</button>
  <p id="status" role="status" aria-live="polite"></p>
</form>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; color: var(--brain-foreground); background: var(--brain-background); font: 14px/1.5 system-ui; }
  .card { display: grid; gap: 14px; padding: 16px; border: 1px solid var(--brain-border); border-radius: 12px; background: var(--brain-card); }
  fieldset { display: grid; gap: 8px; margin: 0; padding: 0; border: 0; }
  label { display: flex; gap: 8px; align-items: center; }
  input[type="number"] { width: 72px; padding: 6px; color: inherit; background: transparent; border: 1px solid var(--brain-input); border-radius: 6px; }
  button { min-height: 40px; padding: 8px 14px; color: var(--brain-primary-foreground); background: var(--brain-primary); border: 0; border-radius: 8px; cursor: pointer; }
  button:focus-visible, input:focus-visible { outline: 2px solid var(--brain-primary); outline-offset: 2px; }
  #status { min-height: 1.5em; margin: 0; color: var(--brain-muted-foreground); }
</style>
<script>
  const form = document.getElementById("plan");
  const status = document.getElementById("status");
  const submit = form.querySelector('button[type="submit"]');
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const content = `请按以下选择继续实现：分支策略为“${data.get("branch")}”；旧实现处理为“${data.get("cleanup")}”；最大并发数为 ${document.getElementById("concurrency").value}。`;
    submit.disabled = true;
    status.textContent = "正在填入输入框…";
    try {
      await sendBrainInputBarMessage(content);
      status.textContent = "已填入输入框，请检查后发送。";
    } catch (error) {
      status.textContent = `填入失败：${error instanceof Error ? error.message : "请稍后重试"}`;
    } finally {
      submit.disabled = false;
    }
  });
</script>
```
