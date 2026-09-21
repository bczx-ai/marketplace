---
description: Design 产物优先 HTML-first 工作流
---

# Brain Design HTML-first

当用户要求制作幻灯片、Deck、原型、线框图、落地页或类似设计产物时：

1. 优先使用已安装的 Design Plugin Skill（如 `simple-deck`、`web-prototype`、`wireframe-*`、`web-clone`）。
2. Deck、原型与线框图使用 **HTML-first**：先生成可在工作台预览的 HTML。
3. Deck HTML 每页使用 `.slide` 结构；不要直接调用通用 `pptx` Skill 从零生成最终 PPTX。
4. 先生成与预览，再导出 PDF/PPTX。
5. 若用户已删除 Skill 引用或明确要求其它方式，尊重用户选择。
6. 普通编码、文档与非设计任务不受本规则影响。
