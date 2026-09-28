---
name: design-loop
description: |
  Brain Design 设计任务总纲：接到「设计 / 生成 / 修改 HTML 页面、幻灯片、
  海报、原型等视觉产物」的请求时，先读项目内 `.brain/design/design.md` 并
  严格遵守其中的设计系统、品牌规范与生成约束，再动手产出单文件语义化
  HTML；同时处理「当前待处理反馈」小节里未解决的评论并在回复中逐条声明。
  当消息里引用了 `.brain/design/design.md`、或用户通过 `/design` 命令发起
  设计任务时，必须使用本 skill。
triggers:
  - "design.md"
  - ".brain/design"
  - "/design"
  - "设计任务"
  - "设计规范"
  - "生成页面"
  - "修改页面"
  - "做个网页"
  - "做一版设计"
  - "幻灯片"
  - "design loop"
  - "html page"
  - "landing page"
  - "slides"
od:
  mode: utility
  category: creative-direction
  scenario: design
  design_system:
    requires: false
  example_prompt: "帮我把首页 hero 区改成深色版本，遵守项目的设计规范。"
---

# Design Loop —— 设计任务工作法

Brain Design 面板维护项目级设计状态，本 skill 规定 agent 在设计任务中的
统一工作法。**它是流程总纲，不替代具体的视觉风格 skill**：选定风格后仍
可叠加 `html-ppt-*`、`web-prototype-*`、`poster-hero` 等专项 skill。

## 何时使用

命中以下任一条件即按本 skill 工作：

- 用户要求设计、生成、改版 HTML 页面、落地页、原型、幻灯片、海报、
  报告等视觉产物。
- 用户要求对已有 HTML 产物做视觉或结构调整。
- 消息中引用了 `.brain/design/design.md`，或来自 `/design` 命令的草稿。
- 消息中包含 Brain Design 面板回传的结构化评论（带元素选择器 / 截图坐标
  的反馈条目）。

## 第一步：先读 design.md（强制）

**动手写任何代码之前**，先在项目根目录读取 `.brain/design/design.md`。

- **文件存在**：把它当作本次任务的硬约束，严格遵守其中四个小节——
  - `## 设计系统：<name>` —— 选定的设计系统及其核心约束摘要，决定版式、
    间距、组件形态与整体气质。
  - `## 品牌规范` —— 主色 / 辅色 / 中性色（hex 色板）、标题 / 正文 /
    等宽字体、语气与禁忌。色值和字体直接照抄，不要自行"优化"或换近似色。
  - `## 生成约束` —— 输出规范化要求，逐条落实。
  - `## 当前待处理反馈` —— 见下面「第三步」。
- **文件不存在**：不要创建它，按下面的通用最佳实践执行，并在回复里说明
  「项目未配置设计规范，已按通用最佳实践产出；如需固定规范请在 Brain
  Design 面板中设置」。
- design.md 与用户当前消息冲突时，**以用户当前消息为准**，并在回复中明确
  指出偏离了哪一条规范、原因是什么。

## 第二步：产出约束

除 design.md `## 生成约束` 另有规定外，默认遵守：

- **单文件 HTML**：一个页面就是一个自包含的 `.html` 文件，CSS 与 JS 内联，
  不引入构建步骤、不拆分成多个片段文件。
- **写在项目根目录**：产物直接写入项目根目录，文件名语义化（如 `landing.html`、
  `pricing.html`）。**禁止写到项目外**（`/tmp`、`~/Desktop`、系统临时目录等），
  否则面板无法识别、无法预览、无法建版本。
- **禁止起服务器**：不要用 `python -m http.server`、`npx serve`、`vite` 等命令
  启动本地服务器或任何常驻进程来展示结果；预览由 Brain Design 面板负责，
  agent 只负责把文件写到项目根目录并在回复里给出路径。
- **token 唯一权威是 `tokens.css`**：项目已应用设计系统时，颜色、字号、间距、
  圆角、阴影一律取自 `.brain/design/system/tokens.css` 里的 CSS 变量。
  `.brain/design/system/DESIGN.md` 只是设计说明，**与 tokens.css 冲突处一律
  以 tokens.css 为准**；不要凭 DESIGN.md 的描述自行推算色值。
- **语义化标签**：用 `header` / `nav` / `main` / `section` / `article` /
  `footer` / `figure` 等结构化标签，标题层级 `h1`-`h6` 连续不跳级；图片
  必须带 `alt`；交互元素可键盘访问。
- **资源相对路径**：图片、字体等本地资源一律用相对路径（`./assets/...`），
  不要写绝对路径、`file://` 或本机专有路径，确保产物可整体移动和预览。
- **响应式**：必须带 `<meta name="viewport" content="width=device-width,
  initial-scale=1">`；用 flex / grid + 相对单位；在窄屏下不产生横向滚动；
  宽内容（表格、代码块、图表）各自套 `overflow-x: auto` 容器。
- **深浅色**：除非设计系统明确只做单一配色，否则同时适配
  `prefers-color-scheme`。
- 中文正文优先使用 design.md 指定的字体族；未指定时使用系统中文字体栈，
  不要依赖需要联网下载的远程字体。

## 第三步：处理待处理反馈

design.md 的 `## 当前待处理反馈` 小节列出的是**尚未解决**的评论（由用户在
Brain Design 预览面板中标注、回传）。

1. 开工前完整读一遍该小节，把每条反馈纳入本次改动范围。
2. 逐条落实到代码里；确实无法处理的（信息不足、与新需求冲突、超出当前
   产物范围）也要保留在清单中，不要静默跳过。
3. **完成后必须在回复中逐条声明处理结果**，一条都不能省，格式示例：

   ```
   待处理反馈：
   1. hero 标题字号偏小 → 已处理：h1 从 2rem 调至 3.25rem，窄屏 2.25rem。
   2. 价格卡片对齐不齐 → 已处理：改为 grid + align-items: stretch。
   3. 增加暗色模式 → 未处理：本次仅改 hero，暗色模式涉及全站变量，建议
      单独一轮。
   ```

4. 声明只写在**回复正文**里。反馈条目的关闭由用户在 Brain Design 面板中
   操作，agent 不代劳。

## 第四步：改动纪律

- **最小 diff**：修改已有 HTML 时只改必要的行，禁止整文件重写。用户很可能
  已经在 Brain Design 的编辑模式里手动微调过文案、间距和色值，整文件重写
  会直接抹掉这些改动。
- 保留已有的 `id`、`class`、`data-*` 属性和元素顺序——面板的选择器、评论
  锚点和编辑模式补丁都依赖它们；确需重命名时在回复中说明。
- 新建页面时把产物放在**项目根目录**，不要写进 `.brain/`，也不要写到项目外。
- 改完在回复里给出产物文件路径，便于面板自动识别并创建预览。

## 硬性禁止

- **严禁主动创建或修改 `.brain/design/` 下的任何文件**，包括 `design.md`、
  `state.json` 和 `versions/`。这是 Brain Design 面板的状态目录，由面板从
  `state.json` 渲染和维护；agent 只读不写。
- 用户明确要求改设计规范时，不要自己动手改 design.md，而是引导用户在
  Brain Design 面板中修改（面板会重新渲染 design.md）。
- 不要把 design.md 的内容整段复制进产物 HTML 的注释或页面里。
- 不要为了"更好看"擅自替换 design.md 指定的色板、字体或设计系统。
