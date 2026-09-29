---
name: html-ppt-zhangzara-bold-poster
zh_description: "大字海报风格的 A 轮融资幻灯片，讲清增长曲线、扩张路径和市场规模。"
en_name: "Write a Series A Growth Story like a Tier-1 VC Partner"
zh_name: "像一线 VC 合伙人一样写 A 轮增长叙事"
description: |
  Open Design's Series A growth story: the traction curve, the expansion motion, and why it's venture-scale. Built as a decision-grade fundraising pitch deck for Series A partners.
en_description: |
  Open Design's Series A growth story: the traction curve, the expansion motion, and why it's venture-scale. Built as a decision-grade fundraising pitch deck for Series A partners.
tags:
  - "fundraising-pitch"
  - "series-a-pitch-deck"
  - "finance"
  - "pitch-deck"
  - "fundraising"
  - "investor-deck"
  - "decision-deck"
  - "commercial-slide-agent"
  - "html-ppt-zhangzara-bold-poster"
zh_tags:
  - "A 轮路演"
  - "财务"
  - "路演 Deck"
  - "融资"
  - "投资人演示"
triggers:
  - "series-a-pitch-deck"
  - "fundraising-pitch"
  - "Write a Series A Growth Story like a Tier-1 VC Partner"
  - "像一线 VC 合伙人一样写 A 轮增长叙事"
  - "pitch-deck"
  - "fundraising"
  - "investor-deck"
  - "html deck"
  - "html slides"
od:
  mode: deck
  upstream: "https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/bold-poster"
  upstream_license: MIT
  preview:
    type: html
    entry: example.html
  design_system:
    requires: false
  speaker_notes: false
  animations: false
  category: "fundraising-pitch"
  scenario: "finance"
  example_prompt: "Create \"Write a Series A Growth Story like a Tier-1 VC Partner\" as a decision-grade Fundraising pitch deck in this template's own visual system. Subject: Open Design's Series A growth story: the traction curve, the expansion motion, and why it's venture-scale. Audience: Series A partners. First ask only for missing essentials: audience, decision target, source-of-truth materials, deadline, and must-keep numbers. Then produce the slide plan, written slides, visual direction, speaker-ready structure, and a critic pass against this rubric: would an investor know why this is venture-scale and urgent."
  example_prompt_i18n:
    zh-CN: "用本模板自有的视觉系统，做一份决策级的融资路演演示文稿：「像一线 VC 合伙人一样写 A 轮增长叙事」。主题：OpenDesign 的 A 轮增长叙事——增长曲线、扩张动能，以及它为何具备风险投资级规模。受众：A 轮合伙人。先只追问缺失的关键信息：受众、决策目标、权威资料、截止时间，以及必须保留的数字。然后产出幻灯片规划、成稿幻灯片、视觉方向、可直接开讲的结构，并对照这条评分标准做一次批评性检查：投资人是否能看懂它为什么具备风险投资级规模且紧迫。"
---

# Bold Poster

> Editorial poster aesthetic with massive Shrikhand display and a single fire-engine red accent.

A single self-contained HTML deck — typography, palette, decorative system,
and slide vocabulary are all tuned together. Mixing layouts across templates
breaks the system; stay inside this one.

## At a glance

- **Scheme:** light
- **Formality:** medium
- **Density:** low
- **Slides in demo:** 10

## Best for

Anything that should land like a magazine cover: brand manifestos, founder vision decks, editorial / cultural pitches, creative reviews. Excellent any time you want a few words to feel like a poster — including unexpected fits like a tech keynote or a finance manifesto that wants to be quotable.

## Avoid for

Decks that need to communicate dense information per slide — the layout is built around a few large statements, not paragraphs of detail.

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
<artifact identifier="zhangzara-bold-poster" type="text/html" title="Deck Title">
<!doctype html>
<html>...</html>
</artifact>
```

## Source & license

Vendored from upstream MIT-licensed
[`zarazhangrui/beautiful-html-templates`](https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/bold-poster).

The full upstream MIT license text — including the original copyright notice — ships in this skill at
[`LICENSE`](./LICENSE) and must be redistributed alongside any copy of `example.html`,
`template.json`, or any vendored `assets/` runtime. See `template.json` for the upstream metadata snapshot.
