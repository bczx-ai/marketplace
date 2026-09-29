---
name: html-ppt-zhangzara-signal
zh_description: "信号风格的战略决策备忘幻灯片，列出选项、风险和最终建议。"
en_name: "Write a Strategy Decision Memo like a Corp-Dev Lead"
zh_name: "像战略发展负责人一样写战略决策备忘"
description: |
  Open Design's strategy memo: should it monetize the plugin registry now or hold — options, risks, and the recommendation. Built as a decision-grade corporate strategy deck for CEO, strategy team.
en_description: |
  Open Design's strategy memo: should it monetize the plugin registry now or hold — options, risks, and the recommendation. Built as a decision-grade corporate strategy deck for CEO, strategy team.
tags:
  - "corporate-strategy"
  - "board-pre-read-deck"
  - "strategy"
  - "board"
  - "business-review"
  - "decision-deck"
  - "commercial-slide-agent"
  - "html-ppt-zhangzara-signal"
zh_tags:
  - "董事会预读"
  - "战略"
  - "董事会"
  - "业务复盘"
triggers:
  - "board-pre-read-deck"
  - "corporate-strategy"
  - "Write a Strategy Decision Memo like a Corp-Dev Lead"
  - "像战略发展负责人一样写战略决策备忘"
  - "board"
  - "strategy"
  - "business-review"
  - "html deck"
  - "html slides"
od:
  mode: deck
  upstream: "https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/signal"
  upstream_license: MIT
  preview:
    type: html
    entry: example.html
  design_system:
    requires: false
  speaker_notes: false
  animations: false
  category: "corporate-strategy"
  scenario: "strategy"
  example_prompt: "Create \"Write a Strategy Decision Memo like a Corp-Dev Lead\" as a decision-grade Corporate strategy deck in this template's own visual system. Subject: Open Design's strategy memo: should it monetize the plugin registry now or hold — options, risks, and the recommendation. Audience: CEO, strategy team. First ask only for missing essentials: audience, decision target, source-of-truth materials, deadline, and must-keep numbers. Then produce the slide plan, written slides, visual direction, speaker-ready structure, and a critic pass against this rubric: would a board member know what to approve and why before page five."
  example_prompt_i18n:
    zh-CN: "用本模板自有的视觉系统，做一份决策级的企业战略演示文稿：「像战略发展负责人一样写战略决策备忘」。主题：OpenDesign 的战略备忘——插件注册表现在就变现还是继续观望，含可选方案、风险与建议。受众：CEO、战略团队。先只追问缺失的关键信息：受众、决策目标、权威资料、截止时间，以及必须保留的数字。然后产出幻灯片规划、成稿幻灯片、视觉方向、可直接开讲的结构，并对照这条评分标准做一次批评性检查：董事是否能在第五页之前就知道该批准什么、为什么。"
---

# Signal

> Deep navy canvas with bone paper and a single muted-gold accent; institutional with quiet weight.

A single self-contained HTML deck — typography, palette, decorative system,
and slide vocabulary are all tuned together. Mixing layouts across templates
breaks the system; stay inside this one.

## At a glance

- **Scheme:** mixed
- **Formality:** high
- **Density:** high
- **Slides in demo:** 18

## Best for

Anything that should feel weighty, considered, and credibly institutional: investor decks, board presentations, consulting deliverables, legal / policy briefs, advisory pitches. Also a strong choice for tech, research, or brand work that wants to read as quietly authoritative rather than loud.

## Avoid for

Contexts that should feel hot, fast, or intentionally playful — the navy + gold restraint commits to a sober voice.

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
<artifact identifier="zhangzara-signal" type="text/html" title="Deck Title">
<!doctype html>
<html>...</html>
</artifact>
```

## Source & license

Vendored from upstream MIT-licensed
[`zarazhangrui/beautiful-html-templates`](https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/signal).

The full upstream MIT license text — including the original copyright notice — ships in this skill at
[`LICENSE`](./LICENSE) and must be redistributed alongside any copy of `example.html`,
`template.json`, or any vendored `assets/` runtime. See `template.json` for the upstream metadata snapshot.
