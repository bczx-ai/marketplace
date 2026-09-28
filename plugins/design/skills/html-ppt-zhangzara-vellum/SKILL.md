---
name: html-ppt-zhangzara-vellum
en_name: "Deliver a Humanities Research Lecture like a Tenured Art Historian"
zh_name: "像终身教授一样做人文研究讲座"
description: |
  A humanities lecture: how Renaissance linear perspective reshaped early cartography — sources, argument, and evidence. Built as a decision-grade academic research deck for faculty, graduate seminar.
en_description: |
  A humanities lecture: how Renaissance linear perspective reshaped early cartography — sources, argument, and evidence. Built as a decision-grade academic research deck for faculty, graduate seminar.
zh_description: |
  像终身教授一样做人文研究讲座——一份可商业交付的学术研究 Deck，围绕真实主题、证据链与决策目标组织。
tags:
  - "academic-research"
  - "academic-review-deck"
  - "research"
  - "grant"
  - "review"
  - "decision-deck"
  - "commercial-slide-agent"
  - "html-ppt-zhangzara-vellum"
zh_tags:
  - "学术评审"
  - "研究"
  - "课题经费"
  - "评审"
triggers:
  - "academic-review-deck"
  - "academic-research"
  - "Deliver a Humanities Research Lecture like a Tenured Art Historian"
  - "像终身教授一样做人文研究讲座"
  - "research"
  - "grant"
  - "review"
  - "html deck"
  - "html slides"
od:
  mode: deck
  upstream: "https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/vellum"
  upstream_license: MIT
  preview:
    type: html
    entry: example.html
  design_system:
    requires: false
  speaker_notes: false
  animations: false
  category: "academic-research"
  scenario: "research"
  example_prompt: "Create \"Deliver a Humanities Research Lecture like a Tenured Art Historian\" as a decision-grade Academic research deck in this template's own visual system. Subject: A humanities lecture: how Renaissance linear perspective reshaped early cartography — sources, argument, and evidence. Audience: faculty, graduate seminar. First ask only for missing essentials: audience, decision target, source-of-truth materials, deadline, and must-keep numbers. Then produce the slide plan, written slides, visual direction, speaker-ready structure, and a critic pass against this rubric: does the deck prove novelty without overclaiming."
  example_prompt_i18n:
    zh-CN: "用本模板自有的视觉系统，做一份决策级的学术研究演示文稿：「像终身教授一样做人文研究讲座」。主题：一场人文学科讲座——文艺复兴线性透视如何重塑早期地图绘制，含史料、论证与证据。受众：教师、研究生研讨班。先只追问缺失的关键信息：受众、决策目标、权威资料、截止时间，以及必须保留的数字。然后产出幻灯片规划、成稿幻灯片、视觉方向、可直接开讲的结构，并对照这条评分标准做一次批评性检查：这套演示文稿能否在不过度宣称的前提下证明新颖性。"
---

# Vellum

> Deep navy canvas with warm-yellow italic Cormorant serifs and a single dusty teal accent. A quiet, scholarly aesthetic.

A single self-contained HTML deck — typography, palette, decorative system,
and slide vocabulary are all tuned together. Mixing layouts across templates
breaks the system; stay inside this one.

## At a glance

- **Scheme:** dark
- **Formality:** high
- **Density:** low
- **Slides in demo:** 9

## Best for

Anything that should feel scholarly, literary, and quietly intelligent: research synthesis, white papers, academic and policy briefs, advisory deliverables, longform editorial pieces, founder reflections. Equally strong for any deck — including tech, business, or creator work — that wants a calm, considered atmosphere instead of energetic visuals.

## Avoid for

Contexts that need visual heat or pop — the navy + warm-yellow italic-Cormorant aesthetic is intentionally low-tempo.

## Workflow

1. **Clone `example.html`** into the user's workspace as the working file.
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
<artifact identifier="zhangzara-vellum" type="text/html" title="Deck Title">
<!doctype html>
<html>...</html>
</artifact>
```

## Source & license

Vendored from upstream MIT-licensed
[`zarazhangrui/beautiful-html-templates`](https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/vellum).

The full upstream MIT license text — including the original copyright notice — ships in this skill at
[`LICENSE`](./LICENSE) and must be redistributed alongside any copy of `example.html`,
`template.json`, or any vendored `assets/` runtime. See `template.json` for the upstream metadata snapshot.
