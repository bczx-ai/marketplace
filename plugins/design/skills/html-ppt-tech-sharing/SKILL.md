---
name: html-ppt-tech-sharing
en_name: "Give an Engineering Tech Talk like a Staff Developer-Advocate"
zh_name: "像 Staff DevRel 一样做工程分享"
description: |
  Open Design internals: how the agent stream, sandbox, and artifacts work — an engineering deep-dive talk. Built as a decision-grade AI literacy deck for engineers, dev community.
en_description: |
  Open Design internals: how the agent stream, sandbox, and artifacts work — an engineering deep-dive talk. Built as a decision-grade AI literacy deck for engineers, dev community.
zh_description: |
  像 Staff DevRel 一样做工程分享——一份可商业交付的AI 素养 Deck，围绕真实主题、证据链与决策目标组织。
tags:
  - "ai-literacy"
  - "enterprise-ai-copilot-rollout-brief"
  - "ai"
  - "copilot"
  - "workflow"
  - "decision-deck"
  - "commercial-slide-agent"
  - "html-ppt-tech-sharing"
zh_tags:
  - "企业 AI Copilot 落地"
  - "AI"
  - "Copilot"
  - "工作流"
triggers:
  - "enterprise-ai-copilot-rollout-brief"
  - "ai-literacy"
  - "Give an Engineering Tech Talk like a Staff Developer-Advocate"
  - "像 Staff DevRel 一样做工程分享"
  - "ai"
  - "copilot"
  - "workflow"
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
  category: "ai-literacy"
  scenario: "ai"
  example_prompt: "Create \"Give an Engineering Tech Talk like a Staff Developer-Advocate\" as a decision-grade AI literacy deck in this template's own visual system. Subject: Open Design internals: how the agent stream, sandbox, and artifacts work — an engineering deep-dive talk. Audience: engineers, dev community. First ask only for missing essentials: audience, decision target, source-of-truth materials, deadline, and must-keep numbers. Then produce the slide plan, written slides, visual direction, speaker-ready structure, and a critic pass against this rubric: does the deck make AI implementation concrete enough to fund."
  example_prompt_i18n:
    zh-CN: "用本模板自有的视觉系统，做一份决策级的 AI 素养演示文稿：「像 Staff DevRel 一样做工程分享」。主题：OpenDesign 内部机制——智能体流、沙箱与产物如何运作，一场工程深度分享。受众：工程师、开发者社区。先只追问缺失的关键信息：受众、决策目标、权威资料、截止时间，以及必须保留的数字。然后产出幻灯片规划、成稿幻灯片、视觉方向、可直接开讲的结构，并对照这条评分标准做一次批评性检查：这套演示文稿是否把 AI 落地讲得足够具体、值得投入预算。"
---
# HTML PPT · Tech Sharing

The engineering deep-dive talk template, in the `tech-sharing` visual identity.
Pick this template for technical and AI-literacy sessions aimed at engineers and
dev communities — decks that make an implementation concrete enough to fund.

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
