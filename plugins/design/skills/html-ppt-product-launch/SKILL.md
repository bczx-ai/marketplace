---
name: html-ppt-product-launch
zh_description: "产品上线与团队推广方案幻灯片，适合向客户团队提出迁移与落地建议。"
en_name: "Pitch a Team Rollout like a Strategic Account Executive"
zh_name: "像战略客户 AE 一样推动团队落地"
description: |
  Open Design Teams: a launch-and-adoption proposal for a mid-market design team weighing a switch from closed cloud tools. Built as a decision-grade B2B sales deck for design team lead, IT.
en_description: |
  Open Design Teams: a launch-and-adoption proposal for a mid-market design team weighing a switch from closed cloud tools. Built as a decision-grade B2B sales deck for design team lead, IT.
tags:
  - "b2b-sales"
  - "b2b-saas-sales-proposal"
  - "sales"
  - "renewal"
  - "customer"
  - "decision-deck"
  - "commercial-slide-agent"
  - "html-ppt-product-launch"
zh_tags:
  - "B2B SaaS 销售提案"
  - "销售"
  - "续约"
  - "客户"
triggers:
  - "b2b-saas-sales-proposal"
  - "b2b-sales"
  - "Pitch a Team Rollout like a Strategic Account Executive"
  - "像战略客户 AE 一样推动团队落地"
  - "sales"
  - "renewal"
  - "customer"
  - "html deck"
  - "html slides"
od:
  mode: deck
  upstream: "https://github.com/lewislulu/html-ppt-skill"
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
  speaker_notes: true
  animations: true
  category: "b2b-sales"
  scenario: "sales"
  example_prompt: "Create \"Pitch a Team Rollout like a Strategic Account Executive\" as a decision-grade B2B sales deck in this template's own visual system. Subject: Open Design Teams: a launch-and-adoption proposal for a mid-market design team weighing a switch from closed cloud tools. Audience: design team lead, IT. First ask only for missing essentials: audience, decision target, source-of-truth materials, deadline, and must-keep numbers. Then produce the slide plan, written slides, visual direction, speaker-ready structure, and a critic pass against this rubric: can the champion forward this internally without rewriting it."
  example_prompt_i18n:
    zh-CN: "用本模板自有的视觉系统，做一份决策级的 B2B 销售演示文稿：「像战略客户 AE 一样推动团队落地」。主题：OpenDesign Teams——面向正在考虑从封闭云工具切换的中型设计团队，给出一份上线与采纳方案。受众：设计团队负责人、IT。先只追问缺失的关键信息：受众、决策目标、权威资料、截止时间，以及必须保留的数字。然后产出幻灯片规划、成稿幻灯片、视觉方向、可直接开讲的结构，并对照这条评分标准做一次批评性检查：支持者能否原样转发到内部、无需重写。"
---
# HTML PPT · Product Launch

The launch-and-adoption proposal template, in the `product-launch` visual
identity. Pick this template for decision-grade B2B sales and rollout decks
aimed at a buying team — a deck the internal champion can forward without
rewriting it.

## Seed

`example.html` in this skill's directory is the reference deck. **Read it first.**
Its slide structure, theme tokens, typography and layout rhythm define this
template.

## Working file

When the user picks this template in the workbench, the workbench writes a
runtime-inlined, self-contained instance of the example into the project and
references it in the brief (`模板实例：<path>`). That file is the working file —
edit its content in place.

If no instance file is referenced in the brief, recreate the deck faithfully
from `example.html`'s structure and visual system as a single self-contained
HTML file.

## Editing rules

1. **Content edits only.** Never rewrite or remove the presentation runtime
   (navigation, scaling, print styles) embedded in the instance.
2. **No repo-relative references.** Never add `<script src="../assets/...">` or
   any other repo-relative link — those paths do not exist in the project.
   Everything the deck needs stays inline in the single file.
3. **Preserve the deck's visual system.** Keep the theme tokens, typography and
   layout rhythm from the example, and keep the structural classes it ships;
   replace the demo content with the user's real content.
4. **Speaker notes go inside `<aside class="notes">` or `<div class="notes">`** —
   never as visible text on the slide.

## Attribution

Visual system, layouts, themes and the runtime keyboard model come from
the upstream MIT-licensed [`lewislulu/html-ppt-skill`](https://github.com/lewislulu/html-ppt-skill).
