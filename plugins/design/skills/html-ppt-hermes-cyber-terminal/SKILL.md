---
name: html-ppt-hermes-cyber-terminal
zh_description: "赛博终端风格的技术选型分享幻灯片，适合讲解模型选型、成本与质量权衡。"
en_name: "Run a BYOK Model-Choice Session like an Applied-AI Engineer"
zh_name: "像应用 AI 工程师一样讲 BYOK 选型"
description: |
  Open Design + BYOK: choosing and wiring your own model, hands-on — cost, quality, and the routing decision. Built as a decision-grade AI literacy deck for engineers, IT, applied-AI teams.
en_description: |
  Open Design + BYOK: choosing and wiring your own model, hands-on — cost, quality, and the routing decision. Built as a decision-grade AI literacy deck for engineers, IT, applied-AI teams.
tags:
  - "ai-literacy"
  - "enterprise-ai-copilot-rollout-brief"
  - "ai"
  - "copilot"
  - "workflow"
  - "decision-deck"
  - "commercial-slide-agent"
  - "html-ppt-hermes-cyber-terminal"
zh_tags:
  - "企业 AI Copilot 落地"
  - "AI"
  - "Copilot"
  - "工作流"
triggers:
  - "enterprise-ai-copilot-rollout-brief"
  - "ai-literacy"
  - "Run a BYOK Model-Choice Session like an Applied-AI Engineer"
  - "像应用 AI 工程师一样讲 BYOK 选型"
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
  example_prompt: "Create \"Run a BYOK Model-Choice Session like an Applied-AI Engineer\" as a decision-grade AI literacy deck in this template's own visual system. Subject: Open Design + BYOK: choosing and wiring your own model, hands-on — cost, quality, and the routing decision. Audience: engineers, IT, applied-AI teams. First ask only for missing essentials: audience, decision target, source-of-truth materials, deadline, and must-keep numbers. Then produce the slide plan, written slides, visual direction, speaker-ready structure, and a critic pass against this rubric: does the deck make AI implementation concrete enough to fund."
  example_prompt_i18n:
    zh-CN: "用本模板自有的视觉系统，做一份决策级的 AI 素养演示文稿：「像应用 AI 工程师一样讲 BYOK 选型」。主题：OpenDesign + BYOK——亲手选择和接入自己的模型，涉及成本、质量与路由决策。受众：工程师、IT、应用 AI 团队。先只追问缺失的关键信息：受众、决策目标、权威资料、截止时间，以及必须保留的数字。然后产出幻灯片规划、成稿幻灯片、视觉方向、可直接开讲的结构，并对照这条评分标准做一次批评性检查：这套演示文稿是否把 AI 落地讲得足够具体、值得投入预算。"
---
# HTML PPT · 暗终端测评

A focused entry point into the [`html-ppt`](../html-ppt/SKILL.md) master skill that lands the user directly on the **`hermes-cyber-terminal`** full-deck template.

## When this card is picked

The Examples gallery wires "Use this prompt" to the example_prompt above. When you accept that prompt, this card is the right pick if the user wants exactly the visual identity of `hermes-cyber-terminal` (see the upstream [full-decks catalog](../html-ppt/references/full-decks.md) for screenshots and rationale).

## How to author the deck

1. **Read the master skill first.** All authoring rules live in
   [`skills/html-ppt/SKILL.md`](../html-ppt/SKILL.md) — content/audience checklist,
   token rules, layout reuse, presenter mode, the keyboard runtime, and the
   "never put presenter-only text on the slide" rule.
2. **Start from the matching template folder:**
   `skills/html-ppt/templates/full-decks/hermes-cyber-terminal/` — copy `index.html` and
   `style.css` into the project, keep the `.tpl-hermes-cyber-terminal` body class.
3. **Bring the shared runtime with the template.** The upstream
   `index.html` links the shared CSS/JS via `../../../assets/...` because it
   sits three folders deep inside `skills/html-ppt/templates/full-decks/`.
   Once you copy `index.html` into the project, those parent-relative URLs
   no longer resolve and `base.css`, `animations.css`, and `runtime.js`
   will 404 — meaning the deck never activates and slide navigation is
   dead. Pick one of these two recipes per project:
   - **Recipe A — copy + rewrite (preferred):** copy
     `skills/html-ppt/assets/fonts.css`, `skills/html-ppt/assets/base.css`,
     `skills/html-ppt/assets/animations/animations.css`, and
     `skills/html-ppt/assets/runtime.js` into a project-local
     `assets/` (with `assets/animations/animations.css`), then rewrite the
     four `<link>`/`<script>` tags in `index.html` from
     `../../../assets/...` to the matching project-local paths
     (`assets/fonts.css`, `assets/base.css`,
     `assets/animations/animations.css`, `assets/runtime.js`).
   - **Recipe B — inline:** read the same four files and replace each
     `<link rel="stylesheet" href="../../../assets/...">` with a
     `<style>...</style>` containing the file's contents, and the
     `<script src="../../../assets/runtime.js">` with a
     `<script>...</script>` containing `runtime.js`. Yields a single
     self-contained `index.html`.
   Either way, do not ship the upstream `../../../assets/...` URLs
   verbatim into a project artifact — they only work in-tree.
4. **Pick a theme.** Default tokens look fine; if the user wants a different
   feel, swap in any of the 36 themes from `skills/html-ppt/assets/themes/*.css`
   via `<link id="theme-link">` and let `T` cycle.
5. **Replace demo content, not classes.** The `.tpl-hermes-cyber-terminal` scoped CSS only
   recognises the structural classes shipped in the template — keep them.
6. **Speaker notes go inside `<aside class="notes">` or `<div class="notes">`** — never as visible text on the slide.

## Attribution

Visual system, layouts, themes and the runtime keyboard model come from
the upstream MIT-licensed [`lewislulu/html-ppt-skill`](https://github.com/lewislulu/html-ppt-skill). The
LICENSE file ships at `skills/html-ppt/LICENSE`; please keep it in place when
redistributing.
