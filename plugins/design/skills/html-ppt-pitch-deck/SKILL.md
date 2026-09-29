---
name: html-ppt-pitch-deck
zh_description: "路演日融资幻灯片，依次展示亮点、增长数据、竞争壁垒和融资计划。"
en_name: "Write a Demo Day Pitch like a Top Accelerator Partner"
zh_name: "像顶级加速器合伙人一样写 Demo Day 路演"
description: |
  Open Design's demo-day pitch: hook, traction, moat, and the raise — built to make a partner sit up by page three. Built as a decision-grade fundraising pitch deck for accelerator partners, angels.
en_description: |
  Open Design's demo-day pitch: hook, traction, moat, and the raise — built to make a partner sit up by page three. Built as a decision-grade fundraising pitch deck for accelerator partners, angels.
tags:
  - "fundraising-pitch"
  - "series-a-pitch-deck"
  - "finance"
  - "pitch-deck"
  - "fundraising"
  - "investor-deck"
  - "decision-deck"
  - "commercial-slide-agent"
  - "html-ppt-pitch-deck"
zh_tags:
  - "A 轮路演"
  - "财务"
  - "路演 Deck"
  - "融资"
  - "投资人演示"
triggers:
  - "series-a-pitch-deck"
  - "fundraising-pitch"
  - "Write a Demo Day Pitch like a Top Accelerator Partner"
  - "像顶级加速器合伙人一样写 Demo Day 路演"
  - "pitch-deck"
  - "fundraising"
  - "investor-deck"
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
  category: "fundraising-pitch"
  scenario: "finance"
  example_prompt: "Create \"Write a Demo Day Pitch like a Top Accelerator Partner\" as a decision-grade Fundraising pitch deck in this template's own visual system. Subject: Open Design's demo-day pitch: hook, traction, moat, and the raise — built to make a partner sit up by page three. Audience: accelerator partners, angels. First ask only for missing essentials: audience, decision target, source-of-truth materials, deadline, and must-keep numbers. Then produce the slide plan, written slides, visual direction, speaker-ready structure, and a critic pass against this rubric: would an investor know why this is venture-scale and urgent."
  example_prompt_i18n:
    zh-CN: "用本模板自有的视觉系统，做一份决策级的融资路演演示文稿：「像顶级加速器合伙人一样写 Demo Day 路演」。主题：OpenDesign 的 Demo Day 路演——钩子、增长势头、护城河与融资额，目标是让合伙人翻到第三页就坐直身体。受众：加速器合伙人、天使投资人。先只追问缺失的关键信息：受众、决策目标、权威资料、截止时间，以及必须保留的数字。然后产出幻灯片规划、成稿幻灯片、视觉方向、可直接开讲的结构，并对照这条评分标准做一次批评性检查：投资人是否能看懂它为什么具备风险投资级规模且紧迫。"
---
# HTML PPT · Pitch Deck

The demo-day fundraising deck template: hook, traction, moat, and the raise, in
the `pitch-deck` visual identity. Pick this template when the user wants a
decision-grade fundraising narrative aimed at accelerator partners, angels and
investors — one that makes a partner sit up by page three.

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
