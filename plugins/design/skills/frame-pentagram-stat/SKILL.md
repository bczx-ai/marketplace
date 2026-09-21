---
name: video-template-frame-pentagram-stat
zh_name: "Pentagram 数据锚点帧"
en_name: "Pentagram Stat Frame"
description: Use this plugin when the user wants a "Pentagram Stat Frame" HyperFrames motion video — Swiss-grid statistic anchor — giant number, red accent, growing bars, black data bar. Rational and editorial.
zh_description: "瑞士网格统计锚点——巨大数字、红色强调、生长中的柱条、黑色数据条，理性而富有编辑感"
zh_tags:
  - "瑞士网格"
  - "数据可视化"
  - "统计"
  - "动画帧"
license: Apache-2.0
metadata:
  author: nexu-io
  version: "0.1.0"
od:
  mode: video
  scenario: video
  surface: hyperframes
  example_prompt_i18n:
    zh-CN: "用「Pentagram 数据锚点帧」模板把我的内容做成一段「瑞士网格统计锚点——巨大数字、红色强调、生长中的柱条、黑色数据条，理性而富有编辑感」。保持模板的视觉签名，使用真实内容和数据，避免 lorem ipsum 和占位图片。"
---

# Pentagram Stat Frame

Swiss-grid statistic anchor — giant number, red accent, growing bars, black data bar. Rational and editorial.

## What this template is

A HyperFrames-ready HTML + CSS + GSAP motion composition, bundled under `source/`. It renders deterministically to MP4 / WEBM at 16:9, 1:1, default 15s, 60fps.

**Best for:** Single hero metric / benchmark reveal · Editorial data slide · Rational, high-contrast brand moment

## Workflow

1. Read `source/index.html` to understand the named layers and the animation timeline.
2. Replace the sample copy (headlines, figures, labels) with the user's real content; keep the motion timing and visual signature intact.
3. Keep the composition self-contained under `source/`; do not introduce external network assets that would break a headless render.
4. Render to MP4 via the html-video / HyperFrames renderer.

## Attribution

Source: html-video `templates/frame-pentagram-stat` (license Apache-2.0). Derived from huashu-design (alchaincyf (花叔 · 花生), MIT) — https://github.com/alchaincyf/huashu-design. Stylistic inspiration (L1, not affiliated): Pentagram (Michael Bierut).
