---
name: codex-interactive-capability-map
zh_name: "Codex 交互式能力地图"
zh_description: "把长文、推文串、备忘或产品叙事提炼成可点击的能力地图，含工作流回路、用例矩阵与响应式详情面板"
en_name: "Codex Interactive Capability Map"
emoji: "🗺️"
description: "Turn a long-form article, thread, memo, or product narrative into a compact clickable capability map with a workflow loop, use-case matrix, and responsive detail panel."
category: prototype
scenario: knowledge
aspect_hint: "desktop web prototype, responsive down to tablet"
featured: 42
tags: ["codex", "article", "thread", "knowledge", "map", "interactive", "capability", "explainer"]
zh_tags:
  - "Codex"
  - "文章"
  - "长推文"
  - "知识"
  - "图谱"
  - "交互"
  - "能力"
  - "图解"
example_id: sample-codex-interactive-capability-map
example_name: "Codex Interactive Capability Map · Operating Model"
example_format: html
example_tagline: "Long text → clickable operating model"
example_desc: "A long post transformed into a concise visual map with linked concepts, use cases, and detail cards."
od:
  mode: prototype
  surface: web
  platform: desktop
  scenario: knowledge
  featured: 42
  preview:
    type: html
    entry: example.html
  design_system:
    requires: false
  example_prompt: "Turn this long-form article or thread into a Codex-style interactive capability map. Extract the core concepts, organize them into a workflow loop and use-case matrix, then build a polished single-file HTML prototype with clickable cards and a detail panel."
  example_prompt_i18n:
    zh-CN: "把这篇长文或推文串转成 Codex 风格的交互式能力地图：提炼核心概念，整理成工作流回路与用例矩阵，再构建一个精致的单文件 HTML 原型，含可点击卡片与详情面板。"
---

# Codex Interactive Capability Map

Transform a long article, social thread, memo, product essay, or launch narrative into a visual explainer that people can scan and click through.

## Use When

- The input is mostly text and the user wants a clearer mental model.
- The content contains repeated concepts, a process, a framework, capabilities, or operating principles.
- The desired output is a polished web artifact, not a static summary.

## Workflow

1. Read the source material and extract 6-10 core concepts.
2. Name the overall model in plain language. Prefer a short noun phrase such as "Operating Model", "Capability Map", or "Workflow Loop".
3. Build three linked views:
   - A hero that frames the source and the promise.
   - A workflow loop that shows the main sequence or system.
   - A use-case matrix that combines concepts into practical scenarios.
4. Add a right-side detail panel. Clicking any nav item, loop node, matrix card, or maturity level must update the panel.
5. Make the clicked element and the detail panel visibly correspond through shared color, motion, icon/mark shape, or gradient.
6. Keep copy short. The artifact should reduce reading effort, not recreate the article.

## Visual Direction

- Use a Codex-inspired refined product style with soft liquid motion, glassy surfaces, and crisp functional controls.
- Make the first viewport feel like a finished product surface, not a wireframe.
- Favor diagrams, loops, matrices, rails, cards, and progressive disclosure over paragraphs.
- Use meaningful hover and active states. A click should feel consequential.
- Avoid external image dependencies unless the user explicitly provides assets.

## Interaction Requirements

- All clickable elements must update content or scroll to a meaningful section.
- The active state must be visually obvious.
- The detail panel should animate on each change.
- Long labels must wrap cleanly and never be clipped.
- The layout must work at 1280px wide and collapse cleanly below 900px.

## Output Contract

Emit one single-file HTML artifact:

```html
<artifact identifier="codex-interactive-capability-map" type="text/html" title="Codex Interactive Capability Map">
<!doctype html>
<html>...</html>
</artifact>
```

Include all CSS and JavaScript inline. Do not use lorem ipsum. Do not leave placeholder cards. If the source does not include enough concrete details, infer a small, clearly labeled conceptual model from the source instead of inventing unrelated content.
