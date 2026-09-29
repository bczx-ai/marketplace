---
name: html-ppt-zhangzara-scatterbrain
zh_description: "拼贴风格的毕业设计展示幻灯片，讲清设计任务、过程和成果。"
en_name: "Pitch a Graduation Design Project like a Portfolio-Ready Design Student"
zh_name: "像作品集出众的设计学生一样讲毕业设计"
description: |
  A design-school graduation project: a civic wayfinding system for a transit hub — the brief, the process, and the outcome. Built as a decision-grade coursework defense deck for crit panel, faculty.
en_description: |
  A design-school graduation project: a civic wayfinding system for a transit hub — the brief, the process, and the outcome. Built as a decision-grade coursework defense deck for crit panel, faculty.
tags:
  - "student-coursework"
  - "senior-capstone-defense-deck"
  - "education"
  - "coursework"
  - "defense"
  - "academic"
  - "decision-deck"
  - "commercial-slide-agent"
  - "html-ppt-zhangzara-scatterbrain"
zh_tags:
  - "毕业答辩"
  - "教育"
  - "课程作业"
  - "答辩"
  - "学术"
triggers:
  - "senior-capstone-defense-deck"
  - "student-coursework"
  - "Pitch a Graduation Design Project like a Portfolio-Ready Design Student"
  - "像作品集出众的设计学生一样讲毕业设计"
  - "coursework"
  - "defense"
  - "academic"
  - "html deck"
  - "html slides"
od:
  mode: deck
  upstream: "https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/scatterbrain"
  upstream_license: MIT
  preview:
    type: html
    entry: example.html
  design_system:
    requires: false
  speaker_notes: false
  animations: false
  category: "student-coursework"
  scenario: "education"
  example_prompt: "Create \"Pitch a Graduation Design Project like a Portfolio-Ready Design Student\" as a decision-grade Student coursework deck in this template's own visual system. Subject: A design-school graduation project: a civic wayfinding system for a transit hub — the brief, the process, and the outcome. Audience: crit panel, faculty. First ask only for missing essentials: audience, decision target, source-of-truth materials, deadline, and must-keep numbers. Then produce the slide plan, written slides, visual direction, speaker-ready structure, and a critic pass against this rubric: can a reviewer find the contribution, evidence, and limitation in under 90 seconds."
  example_prompt_i18n:
    zh-CN: "用本模板自有的视觉系统，做一份决策级的学生课业演示文稿：「像作品集出众的设计学生一样讲毕业设计」。主题：一个设计学院的毕业设计——为交通枢纽做的公共导视系统，含任务书、过程与成果。受众：评审小组、院系。先只追问缺失的关键信息：受众、决策目标、权威资料、截止时间，以及必须保留的数字。然后产出幻灯片规划、成稿幻灯片、视觉方向、可直接开讲的结构，并对照这条评分标准做一次批评性检查：评审者能否在 90 秒内找到贡献、证据与局限。"
---

# Scatterbrain

> Post-it inspired: pastel sticky notes, Caveat handwriting, Shrikhand and Zilla Slab type stack.

A single self-contained HTML deck — typography, palette, decorative system,
and slide vocabulary are all tuned together. Mixing layouts across templates
breaks the system; stay inside this one.

## At a glance

- **Scheme:** light
- **Formality:** low
- **Density:** high
- **Slides in demo:** 10

## Best for

Anything that should feel like a designer's whiteboard: brainstorms, workshops, creative-agency credentials, design-thinking sessions, ideation pitches, art-direction reviews. Equally fun for any deck — including tech, research, or business — that wants to read as in-progress thinking rather than polished conclusions.

## Avoid for

Contexts that demand precision and institutional weight — the post-it sticky-note aesthetic intentionally reads as warm and unfinished.

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
<artifact identifier="zhangzara-scatterbrain" type="text/html" title="Deck Title">
<!doctype html>
<html>...</html>
</artifact>
```

## Source & license

Vendored from upstream MIT-licensed
[`zarazhangrui/beautiful-html-templates`](https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/scatterbrain).

The full upstream MIT license text — including the original copyright notice — ships in this skill at
[`LICENSE`](./LICENSE) and must be redistributed alongside any copy of `example.html`,
`template.json`, or any vendored `assets/` runtime. See `template.json` for the upstream metadata snapshot.
