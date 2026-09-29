---
name: html-ppt-zhangzara-monochrome
zh_description: "黑白极简风格的科研基金申请幻灯片，讲清假设、方法、里程碑和风险。"
en_name: "Write a Grant Committee Brief like a Funded Principal Investigator"
zh_name: "像拿到资助的 PI 一样写基金评审简报"
description: |
  A grant proposal on CRISPR base-editing for sickle-cell disease — the hypothesis, the approach, the milestones, and the risk. Built as a decision-grade academic research deck for grant review committee.
en_description: |
  A grant proposal on CRISPR base-editing for sickle-cell disease — the hypothesis, the approach, the milestones, and the risk. Built as a decision-grade academic research deck for grant review committee.
tags:
  - "academic-research"
  - "academic-review-deck"
  - "research"
  - "grant"
  - "review"
  - "decision-deck"
  - "commercial-slide-agent"
  - "html-ppt-zhangzara-monochrome"
zh_tags:
  - "学术评审"
  - "研究"
  - "课题经费"
  - "评审"
triggers:
  - "academic-review-deck"
  - "academic-research"
  - "Write a Grant Committee Brief like a Funded Principal Investigator"
  - "像拿到资助的 PI 一样写基金评审简报"
  - "research"
  - "grant"
  - "review"
  - "html deck"
  - "html slides"
od:
  mode: deck
  upstream: "https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/monochrome"
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
  example_prompt: "Create \"Write a Grant Committee Brief like a Funded Principal Investigator\" as a decision-grade Academic research deck in this template's own visual system. Subject: A grant proposal on CRISPR base-editing for sickle-cell disease — the hypothesis, the approach, the milestones, and the risk. Audience: grant review committee. First ask only for missing essentials: audience, decision target, source-of-truth materials, deadline, and must-keep numbers. Then produce the slide plan, written slides, visual direction, speaker-ready structure, and a critic pass against this rubric: does the deck prove novelty without overclaiming."
  example_prompt_i18n:
    zh-CN: "用本模板自有的视觉系统，做一份决策级的学术研究演示文稿：「像拿到资助的 PI 一样写基金评审简报」。主题：一份关于 CRISPR 碱基编辑治疗镰状细胞病的基金申请——假设、方法、里程碑与风险。受众：基金评审委员会。先只追问缺失的关键信息：受众、决策目标、权威资料、截止时间，以及必须保留的数字。然后产出幻灯片规划、成稿幻灯片、视觉方向、可直接开讲的结构，并对照这条评分标准做一次批评性检查：这套演示文稿能否在不过度宣称的前提下证明新颖性。"
---

# Monochrome

> Ivory ledger paper with all-black type; Lora serif headlines, Jost body, no color at all.

A single self-contained HTML deck — typography, palette, decorative system,
and slide vocabulary are all tuned together. Mixing layouts across templates
breaks the system; stay inside this one.

## At a glance

- **Scheme:** light
- **Formality:** high
- **Density:** high
- **Slides in demo:** 16

## Best for

Anything that should feel like a hand-typeset ledger: user research synthesis, white papers, longform reports, academic and policy briefs, advisory deliverables, bilingual EN/CN reports. Equally good for tech, design, or brand decks that want their words to be the only thing on the page.

## Avoid for

Decks that need visual personality or color-led storytelling — the all-ink palette is intentionally austere.

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
<artifact identifier="zhangzara-monochrome" type="text/html" title="Deck Title">
<!doctype html>
<html>...</html>
</artifact>
```

## Source & license

Vendored from upstream MIT-licensed
[`zarazhangrui/beautiful-html-templates`](https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/monochrome).

The full upstream MIT license text — including the original copyright notice — ships in this skill at
[`LICENSE`](./LICENSE) and must be redistributed alongside any copy of `example.html`,
`template.json`, or any vendored `assets/` runtime. See `template.json` for the upstream metadata snapshot.
