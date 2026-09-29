---
name: html-ppt-zhangzara-creative-mode
zh_description: "品牌视觉识别系统发布幻灯片，展示 Logo、色彩、字体和使用规范。"
en_name: "Present a Visual-Identity System like a Lead Brand Designer"
zh_name: "像主创品牌设计师一样发布视觉识别系统"
description: |
  A brand visual-identity system reveal for an outdoor label — logo, color, type, and the rules that keep it consistent. Built as a decision-grade design craft deck for brand team, client.
en_description: |
  A brand visual-identity system reveal for an outdoor label — logo, color, type, and the rules that keep it consistent. Built as a decision-grade design craft deck for brand team, client.
tags:
  - "design-craft"
  - "board-upgrade-deck-rescue"
  - "design"
  - "brand"
  - "visual-system"
  - "decision-deck"
  - "commercial-slide-agent"
  - "html-ppt-zhangzara-creative-mode"
zh_tags:
  - "汇报翻新"
  - "设计"
  - "品牌"
  - "视觉系统"
triggers:
  - "board-upgrade-deck-rescue"
  - "design-craft"
  - "Present a Visual-Identity System like a Lead Brand Designer"
  - "像主创品牌设计师一样发布视觉识别系统"
  - "design"
  - "brand"
  - "visual-system"
  - "html deck"
  - "html slides"
od:
  mode: deck
  upstream: "https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/creative-mode"
  upstream_license: MIT
  preview:
    type: html
    entry: example.html
  design_system:
    requires: false
  speaker_notes: false
  animations: false
  category: "design-craft"
  scenario: "design"
  example_prompt: "Create \"Present a Visual-Identity System like a Lead Brand Designer\" as a decision-grade Design craft deck in this template's own visual system. Subject: A brand visual-identity system reveal for an outdoor label — logo, color, type, and the rules that keep it consistent. Audience: brand team, client. First ask only for missing essentials: audience, decision target, source-of-truth materials, deadline, and must-keep numbers. Then produce the slide plan, written slides, visual direction, speaker-ready structure, and a critic pass against this rubric: does the deck feel authored by a senior designer rather than generated."
  example_prompt_i18n:
    zh-CN: "用本模板自有的视觉系统，做一份决策级的设计工艺演示文稿：「像主创品牌设计师一样发布视觉识别系统」。主题：一个户外品牌的视觉识别系统发布——标识、色彩、字体，以及保持一致的规则。受众：品牌团队、客户。先只追问缺失的关键信息：受众、决策目标、权威资料、截止时间，以及必须保留的数字。然后产出幻灯片规划、成稿幻灯片、视觉方向、可直接开讲的结构，并对照这条评分标准做一次批评性检查：这套演示文稿是否像出自资深设计师之手，而非机器生成。"
---

# Creative Mode

> Cream paper canvas with confident multi-color (green, pink, orange, yellow) accents and Archivo Black display.

A single self-contained HTML deck — typography, palette, decorative system,
and slide vocabulary are all tuned together. Mixing layouts across templates
breaks the system; stay inside this one.

## At a glance

- **Scheme:** light
- **Formality:** medium
- **Density:** medium-high
- **Slides in demo:** 8

## Best for

Anything that should feel design-led and confident: creative agency pitches, design studio decks, ad shop credentials, brand creative reviews, art-direction reviews. Also a great unexpected pick for a tech talk, research findings, or finance review when the speaker wants to lead with taste rather than convention.

## Avoid for

Contexts that demand institutional restraint and a quiet authority — the saturated multi-accent palette will read as expressive, not formal.

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
<artifact identifier="zhangzara-creative-mode" type="text/html" title="Deck Title">
<!doctype html>
<html>...</html>
</artifact>
```

## Source & license

Vendored from upstream MIT-licensed
[`zarazhangrui/beautiful-html-templates`](https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/creative-mode).

The full upstream MIT license text — including the original copyright notice — ships in this skill at
[`LICENSE`](./LICENSE) and must be redistributed alongside any copy of `example.html`,
`template.json`, or any vendored `assets/` runtime. See `template.json` for the upstream metadata snapshot.
