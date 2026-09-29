---
name: html-ppt-testing-safety-alert
zh_description: "数据治理汇报幻灯片，讲清数据风险、管控框架、责任划分和需要审批的事项。"
en_name: "Brief a Health-System Board on Data Governance like a Chief Compliance Officer"
zh_name: "像首席合规官一样向医院董事会汇报数据治理"
description: |
  A hospital data-governance briefing: patient-data risk, the control framework, accountability, and the approval the board must give. Built as a decision-grade policy briefing deck for health-system board, regulators.
en_description: |
  A hospital data-governance briefing: patient-data risk, the control framework, accountability, and the approval the board must give. Built as a decision-grade policy briefing deck for health-system board, regulators.
tags:
  - "government-policy"
  - "policy-briefing-deck"
  - "policy"
  - "regulatory"
  - "risk-review"
  - "decision-deck"
  - "commercial-slide-agent"
  - "html-ppt-testing-safety-alert"
zh_tags:
  - "政策简报"
  - "政策"
  - "监管"
  - "风险评审"
triggers:
  - "policy-briefing-deck"
  - "government-policy"
  - "Brief a Health-System Board on Data Governance like a Chief Compliance Officer"
  - "像首席合规官一样向医院董事会汇报数据治理"
  - "policy"
  - "regulatory"
  - "risk-review"
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
  category: "government-policy"
  scenario: "policy"
  example_prompt: "Create \"Brief a Health-System Board on Data Governance like a Chief Compliance Officer\" as a decision-grade Government & policy deck in this template's own visual system. Subject: A hospital data-governance briefing: patient-data risk, the control framework, accountability, and the approval the board must give. Audience: health-system board, regulators. First ask only for missing essentials: audience, decision target, source-of-truth materials, deadline, and must-keep numbers. Then produce the slide plan, written slides, visual direction, speaker-ready structure, and a critic pass against this rubric: does the deck reduce approval risk rather than create rhetorical heat."
  example_prompt_i18n:
    zh-CN: "用本模板自有的视觉系统，做一份决策级的政府与政策演示文稿：「像首席合规官一样向医院董事会汇报数据治理」。主题：一场医院数据治理简报——患者数据风险、控制框架、问责机制，以及董事会必须给出的批准。受众：医疗系统董事会、监管方。先只追问缺失的关键信息：受众、决策目标、权威资料、截止时间，以及必须保留的数字。然后产出幻灯片规划、成稿幻灯片、视觉方向、可直接开讲的结构，并对照这条评分标准做一次批评性检查：这套演示文稿是降低审批风险，还是只制造了修辞上的热度。"
---
# HTML PPT · 红琥珀警示

A focused entry point into the [`html-ppt`](../html-ppt/SKILL.md) master skill that lands the user directly on the **`testing-safety-alert`** full-deck template.

## When this card is picked

The Examples gallery wires "Use this prompt" to the example_prompt above. When you accept that prompt, this card is the right pick if the user wants exactly the visual identity of `testing-safety-alert` (see the upstream [full-decks catalog](../html-ppt/references/full-decks.md) for screenshots and rationale).

## How to author the deck

1. **Read the master skill first.** All authoring rules live in
   [`skills/html-ppt/SKILL.md`](../html-ppt/SKILL.md) — content/audience checklist,
   token rules, layout reuse, presenter mode, the keyboard runtime, and the
   "never put presenter-only text on the slide" rule.
2. **Start from the matching template folder:**
   `skills/html-ppt/templates/full-decks/testing-safety-alert/` — copy `index.html` and
   `style.css` into the project, keep the `.tpl-testing-safety-alert` body class.
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
5. **Replace demo content, not classes.** The `.tpl-testing-safety-alert` scoped CSS only
   recognises the structural classes shipped in the template — keep them.
6. **Speaker notes go inside `<aside class="notes">` or `<div class="notes">`** — never as visible text on the slide.

## Attribution

Visual system, layouts, themes and the runtime keyboard model come from
the upstream MIT-licensed [`lewislulu/html-ppt-skill`](https://github.com/lewislulu/html-ppt-skill). The
LICENSE file ships at `skills/html-ppt/LICENSE`; please keep it in place when
redistributing.
