---
name: html-ppt-zhangzara-8-bit-orbit
zh_description: "8 位像素风格的个人爱好故事幻灯片。"
en_name: "Turn a Hobby into a Story Deck like a Passion-Project Storyteller"
zh_name: "像热爱驱动的讲述者一样把爱好做成故事"
description: |
  A gamer's journey building a retro-arcade collection — the obsession, the hunt, and what the machines came to mean. Built as a decision-grade story deck for friends, hobby community.
en_description: |
  A gamer's journey building a retro-arcade collection — the obsession, the hunt, and what the machines came to mean. Built as a decision-grade story deck for friends, hobby community.
tags:
  - "life"
  - "travel-photo-essay-deck"
  - "personal"
  - "story"
  - "photo-essay"
  - "decision-deck"
  - "commercial-slide-agent"
  - "html-ppt-zhangzara-8-bit-orbit"
zh_tags:
  - "旅行影像随笔"
  - "个人"
  - "故事"
  - "影像随笔"
triggers:
  - "travel-photo-essay-deck"
  - "life"
  - "Turn a Hobby into a Story Deck like a Passion-Project Storyteller"
  - "像热爱驱动的讲述者一样把爱好做成故事"
  - "story"
  - "personal"
  - "photo-essay"
  - "html deck"
  - "html slides"
od:
  mode: deck
  upstream: "https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/8-bit-orbit"
  upstream_license: MIT
  preview:
    type: html
    entry: example.html
  design_system:
    requires: false
  speaker_notes: false
  animations: false
  category: "life"
  scenario: "personal"
  example_prompt: "Create \"Turn a Hobby into a Story Deck like a Passion-Project Storyteller\" as a decision-grade Life & story deck in this template's own visual system. Subject: A gamer's journey building a retro-arcade collection — the obsession, the hunt, and what the machines came to mean. Audience: friends, hobby community. First ask only for missing essentials: audience, decision target, source-of-truth materials, deadline, and must-keep numbers. Then produce the slide plan, written slides, visual direction, speaker-ready structure, and a critic pass against this rubric: would someone retell the story after seeing it once."
  example_prompt_i18n:
    zh-CN: "用本模板自有的视觉系统，做一份决策级的生活与故事演示文稿：「像热爱驱动的讲述者一样把爱好做成故事」。主题：一位玩家搭建复古街机收藏的历程——痴迷、寻觅，以及这些机器最终意味着什么。受众：朋友、爱好社区。先只追问缺失的关键信息：受众、决策目标、权威资料、截止时间，以及必须保留的数字。然后产出幻灯片规划、成稿幻灯片、视觉方向、可直接开讲的结构，并对照这条评分标准做一次批评性检查：看过一遍之后，别人是否愿意把这个故事讲给别人听。"
---

# 8-Bit Orbit

> Pixel-art neon arcade aesthetic on a deep navy void.

A single self-contained HTML deck — typography, palette, decorative system,
and slide vocabulary are all tuned together. Mixing layouts across templates
breaks the system; stay inside this one.

## At a glance

- **Scheme:** dark
- **Formality:** low
- **Density:** medium
- **Slides in demo:** 10

## Best for

Anything that should feel like a CRT screen at 2am: cyberpunk, gaming, web3, indie dev tools, hackathon demos. Just as good for a tech talk that wants to lean into nostalgic-digital craft, a synthwave brand deck, or a creative review that wants to feel like a console.

## Avoid for

Contexts where the dark neon palette would actively work against the message — quiet institutional finance disclosures, healthcare patient-facing materials, traditional luxury.

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
<artifact identifier="zhangzara-8-bit-orbit" type="text/html" title="Deck Title">
<!doctype html>
<html>...</html>
</artifact>
```

## Source & license

Vendored from upstream MIT-licensed
[`zarazhangrui/beautiful-html-templates`](https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/8-bit-orbit).

The full upstream MIT license text — including the original copyright notice — ships in this skill at
[`LICENSE`](./LICENSE) and must be redistributed alongside any copy of `example.html`,
`template.json`, or any vendored `assets/` runtime. See `template.json` for the upstream metadata snapshot.
