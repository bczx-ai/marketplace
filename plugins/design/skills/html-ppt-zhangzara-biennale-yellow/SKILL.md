---
name: html-ppt-zhangzara-biennale-yellow
en_name: "Curate an Art Biennale Deck like a Museum Exhibition Director"
zh_name: "像美术馆策展总监一样做双年展策展稿"
description: |
  A curatorial deck for a contemporary art biennale — the thesis, the rooms, the works, and the visitor journey. Built as a decision-grade design craft deck for museum board, curators.
en_description: |
  A curatorial deck for a contemporary art biennale — the thesis, the rooms, the works, and the visitor journey. Built as a decision-grade design craft deck for museum board, curators.
zh_description: |
  像美术馆策展总监一样做双年展策展稿——一份可商业交付的设计打磨 Deck，围绕真实主题、证据链与决策目标组织。
tags:
  - "design-craft"
  - "board-upgrade-deck-rescue"
  - "design"
  - "brand"
  - "visual-system"
  - "decision-deck"
  - "commercial-slide-agent"
  - "html-ppt-zhangzara-biennale-yellow"
zh_tags:
  - "汇报翻新"
  - "设计"
  - "品牌"
  - "视觉系统"
triggers:
  - "board-upgrade-deck-rescue"
  - "design-craft"
  - "Curate an Art Biennale Deck like a Museum Exhibition Director"
  - "像美术馆策展总监一样做双年展策展稿"
  - "design"
  - "brand"
  - "visual-system"
  - "html deck"
  - "html slides"
od:
  mode: deck
  upstream: "https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/biennale-yellow"
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
  example_prompt: "Create \"Curate an Art Biennale Deck like a Museum Exhibition Director\" as a decision-grade Design craft deck in this template's own visual system. Subject: A curatorial deck for a contemporary art biennale — the thesis, the rooms, the works, and the visitor journey. Audience: museum board, curators. First ask only for missing essentials: audience, decision target, source-of-truth materials, deadline, and must-keep numbers. Then produce the slide plan, written slides, visual direction, speaker-ready structure, and a critic pass against this rubric: does the deck feel authored by a senior designer rather than generated."
  example_prompt_i18n:
    zh-CN: "用本模板自有的视觉系统，做一份决策级的设计工艺演示文稿：「像美术馆策展总监一样做双年展策展稿」。主题：一份当代艺术双年展的策展稿——策展主张、展厅、作品与观众动线。受众：美术馆董事会、策展人。先只追问缺失的关键信息：受众、决策目标、权威资料、截止时间，以及必须保留的数字。然后产出幻灯片规划、成稿幻灯片、视觉方向、可直接开讲的结构，并对照这条评分标准做一次批评性检查：这套演示文稿是否像出自资深设计师之手，而非机器生成。"
---

# Biennale Yellow

> Solar yellow on warm parchment with deep indigo serif and atmospheric sun-glow gradients.

A single self-contained HTML deck — typography, palette, decorative system,
and slide vocabulary are all tuned together. Mixing layouts across templates
breaks the system; stay inside this one.

## At a glance

- **Scheme:** light
- **Formality:** high
- **Density:** medium
- **Slides in demo:** 8

## Best for

Anything that should feel like an art-biennale poster or a museum's annual programme: exhibition decks, arts-institution announcements, design conference brochures, curatorial pitches, literary publications, studio retrospectives. Equally good for any deck wanting Dutch-editorial atmosphere with an unmistakable single-color signature.

## Avoid for

Decks that need visual punch or saturated multi-color energy — the warm-paper canvas and one-yellow palette are intentionally quiet and atmospheric.

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
<artifact identifier="zhangzara-biennale-yellow" type="text/html" title="Deck Title">
<!doctype html>
<html>...</html>
</artifact>
```

## Source & license

Vendored from upstream MIT-licensed
[`zarazhangrui/beautiful-html-templates`](https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/biennale-yellow).

The full upstream MIT license text — including the original copyright notice — ships in this skill at
[`LICENSE`](./LICENSE) and must be redistributed alongside any copy of `example.html`,
`template.json`, or any vendored `assets/` runtime. See `template.json` for the upstream metadata snapshot.
