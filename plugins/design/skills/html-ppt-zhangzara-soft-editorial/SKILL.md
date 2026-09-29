---
name: html-ppt-zhangzara-soft-editorial
zh_description: "柔和编辑风格的数字化转型路线图幻灯片，包含现状诊断、分阶段举措和推进节奏。"
en_name: "Deliver a Digital-Transformation Roadmap like a Big-Four Partner"
zh_name: "像四大合伙人一样交付数字化转型路线图"
description: |
  A digital-transformation roadmap for a legacy insurer — the diagnosis, the sequenced bets, and the operating rhythm to land them. Built as a decision-grade consulting deck for client executives.
en_description: |
  A digital-transformation roadmap for a legacy insurer — the diagnosis, the sequenced bets, and the operating rhythm to land them. Built as a decision-grade consulting deck for client executives.
tags:
  - "consulting"
  - "consulting-final-deck"
  - "strategy"
  - "consulting-deliverable"
  - "client"
  - "decision-deck"
  - "commercial-slide-agent"
  - "html-ppt-zhangzara-soft-editorial"
zh_tags:
  - "咨询终稿"
  - "战略"
  - "咨询交付物"
  - "客户"
triggers:
  - "consulting-final-deck"
  - "consulting"
  - "Deliver a Digital-Transformation Roadmap like a Big-Four Partner"
  - "像四大合伙人一样交付数字化转型路线图"
  - "consulting-deliverable"
  - "strategy"
  - "client"
  - "html deck"
  - "html slides"
od:
  mode: deck
  upstream: "https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/soft-editorial"
  upstream_license: MIT
  preview:
    type: html
    entry: example.html
  design_system:
    requires: false
  speaker_notes: false
  animations: false
  category: "consulting"
  scenario: "strategy"
  example_prompt: "Create \"Deliver a Digital-Transformation Roadmap like a Big-Four Partner\" as a decision-grade Consulting deck in this template's own visual system. Subject: A digital-transformation roadmap for a legacy insurer — the diagnosis, the sequenced bets, and the operating rhythm to land them. Audience: client executives. First ask only for missing essentials: audience, decision target, source-of-truth materials, deadline, and must-keep numbers. Then produce the slide plan, written slides, visual direction, speaker-ready structure, and a critic pass against this rubric: would a client know what to do Monday morning."
  example_prompt_i18n:
    zh-CN: "用本模板自有的视觉系统，做一份决策级的咨询演示文稿：「像四大合伙人一样交付数字化转型路线图」。主题：一家传统保险公司的数字化转型路线图——诊断、分阶段下注与落地所需的运营节奏。受众：客户高管。先只追问缺失的关键信息：受众、决策目标、权威资料、截止时间，以及必须保留的数字。然后产出幻灯片规划、成稿幻灯片、视觉方向、可直接开讲的结构，并对照这条评分标准做一次批评性检查：客户是否知道周一早上该做什么。"
---

# Soft Editorial

> Cormorant Garamond serif on warm paper with sage, blush, and lemon accents.

A single self-contained HTML deck — typography, palette, decorative system,
and slide vocabulary are all tuned together. Mixing layouts across templates
breaks the system; stay inside this one.

## At a glance

- **Scheme:** light
- **Formality:** high
- **Density:** low
- **Slides in demo:** 12

## Best for

Anything that should feel literary, elegant, and unhurried: editorial features, longform brand stories, gallery / museum decks, advisory deliverables, wedding / lifestyle media, founder essays. Equally good for tech, research, or business decks that want a Sunday-supplement warmth instead of corporate polish.

## Avoid for

Decks that need visual heat or punch — the warm-paper palette and Cormorant serif are intentionally quiet.

## Workflow

1. **Clone `example.html` AND the `assets/` folder** into the user's workspace.
   This template ships an `assets/deck-stage.js` runtime (keyboard navigation,
   stage rendering); the HTML references it as `assets/deck-stage.js`, so the
   file must sit next to the cloned HTML or that path will 404 in the generated
   artifact and navigation will silently break. Inlining the JS into a single
   `<script>` block in the HTML is an acceptable alternative when a single
   self-contained file is preferred.
2. **Replace placeholder content** with the user's real headlines, body copy,
   numbers, names, dates, and section labels. Match existing dimensions when
   swapping image placeholders.
3. **Preserve the design system.** Never substitute fonts, recolor the palette,
   restructure the layout grid, or strip decorative elements (corner brackets,
   paper grain, geometric shapes, illustrated SVGs). They are part of the
   identity.
4. **Adjust deck length by duplicating layouts.** If the user has more content
   than the demo holds, duplicate an existing slide of the most appropriate
   layout. If less, drop slides from the bottom. Update page-number labels.
5. **Designing missing layouts:** if a slide needs a layout the template
   doesn't have, design it from scratch using the same fonts, palette,
   decorative vocabulary, spacing rhythm, and component grammar — never bail
   to a different template.
6. **Keep the navigation runtime as shipped.** If the deck ships an
   `assets/deck-stage.js` or inline keyboard handler, leave it intact.

## Output contract

Emit between `<artifact>` tags:

```
<artifact identifier="zhangzara-soft-editorial" type="text/html" title="Deck Title">
<!doctype html>
<html>...</html>
</artifact>
```

## Source & license

Vendored from upstream MIT-licensed
[`zarazhangrui/beautiful-html-templates`](https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/soft-editorial).

The full upstream MIT license text — including the original copyright notice — ships in this skill at
[`LICENSE`](./LICENSE) and must be redistributed alongside any copy of `example.html`,
`template.json`, or any vendored `assets/` runtime. See `template.json` for the upstream metadata snapshot.
