---
name: html-ppt-xhs-white-editorial
zh_description: "小红书白底编辑风格的晋升材料幻灯片，呈现职责范围、关键成果和影响力。"
en_name: "Write a Staff-Engineer Promotion Case like a Calibration-Committee Insider"
zh_name: "像晋升评审内部人一样写 Staff 工程师晋升材料"
description: |
  A staff-engineer promotion packet — scope, the proof moments, the artifacts, and the impact that clears the bar. Built as a decision-grade career deck for manager, calibration committee.
en_description: |
  A staff-engineer promotion packet — scope, the proof moments, the artifacts, and the impact that clears the bar. Built as a decision-grade career deck for manager, calibration committee.
tags:
  - "career"
  - "year-end-self-review-deck"
  - "personal"
  - "portfolio"
  - "promotion"
  - "self-review"
  - "decision-deck"
  - "commercial-slide-agent"
  - "html-ppt-xhs-white-editorial"
zh_tags:
  - "年终自评"
  - "个人"
  - "作品集"
  - "晋升"
  - "自我复盘"
triggers:
  - "year-end-self-review-deck"
  - "career"
  - "Write a Staff-Engineer Promotion Case like a Calibration-Committee Insider"
  - "像晋升评审内部人一样写 Staff 工程师晋升材料"
  - "portfolio"
  - "promotion"
  - "self-review"
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
  category: "career"
  scenario: "personal"
  example_prompt: "Create \"Write a Staff-Engineer Promotion Case like a Calibration-Committee Insider\" as a decision-grade Career deck in this template's own visual system. Subject: A staff-engineer promotion packet — scope, the proof moments, the artifacts, and the impact that clears the bar. Audience: manager, calibration committee. First ask only for missing essentials: audience, decision target, source-of-truth materials, deadline, and must-keep numbers. Then produce the slide plan, written slides, visual direction, speaker-ready structure, and a critic pass against this rubric: does the evidence make the claim feel earned."
  example_prompt_i18n:
    zh-CN: "用本模板自有的视觉系统，做一份决策级的职业发展演示文稿：「像晋升评审内部人一样写 Staff 工程师晋升材料」。主题：一份 Staff 工程师晋升材料——职责范围、证明时刻、作品证据，以及足以跨过门槛的影响力。受众：主管、晋升评审委员会。先只追问缺失的关键信息：受众、决策目标、权威资料、截止时间，以及必须保留的数字。然后产出幻灯片规划、成稿幻灯片、视觉方向、可直接开讲的结构，并对照这条评分标准做一次批评性检查：证据是否让这个主张显得实至名归。"
---
# HTML PPT · 白底杂志风

A focused entry point into the [`html-ppt`](../html-ppt/SKILL.md) master skill that lands the user directly on the **`xhs-white-editorial`** full-deck template.

## When this card is picked

The Examples gallery wires "Use this prompt" to the example_prompt above. When you accept that prompt, this card is the right pick if the user wants exactly the visual identity of `xhs-white-editorial` (see the upstream [full-decks catalog](../html-ppt/references/full-decks.md) for screenshots and rationale).

## How to author the deck

1. **Read the master skill first.** All authoring rules live in
   [`skills/html-ppt/SKILL.md`](../html-ppt/SKILL.md) — content/audience checklist,
   token rules, layout reuse, presenter mode, the keyboard runtime, and the
   "never put presenter-only text on the slide" rule.
2. **Start from the matching template folder:**
   `skills/html-ppt/templates/full-decks/xhs-white-editorial/` — copy `index.html` and
   `style.css` into the project, keep the `.tpl-xhs-white-editorial` body class.
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
5. **Replace demo content, not classes.** The `.tpl-xhs-white-editorial` scoped CSS only
   recognises the structural classes shipped in the template — keep them.
6. **Speaker notes go inside `<aside class="notes">` or `<div class="notes">`** — never as visible text on the slide.

## Attribution

Visual system, layouts, themes and the runtime keyboard model come from
the upstream MIT-licensed [`lewislulu/html-ppt-skill`](https://github.com/lewislulu/html-ppt-skill). The
LICENSE file ships at `skills/html-ppt/LICENSE`; please keep it in place when
redistributing.
