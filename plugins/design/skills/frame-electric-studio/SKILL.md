---
name: video-template-frame-electric-studio
zh_name: "电光工作室分屏帧"
en_name: "Electric Studio Frame"
description: Use this plugin when the user wants a "Electric Studio Frame" HyperFrames motion video — Two-panel split with quote as hero — white/blue panels open from center, accent bar grows, quote reveals line by line.
zh_description: "双面板分屏以引言为主角——白/蓝面板从中心翻开、强调色条生长、引言逐行揭示"
zh_tags:
  - "分屏"
  - "引言"
  - "工作室"
  - "片头"
license: Apache-2.0
metadata:
  author: nexu-io
  version: "0.1.0"
od:
  mode: video
  scenario: video
  surface: hyperframes
  example_prompt_i18n:
    zh-CN: "用「电光工作室分屏帧」模板把我的内容做成一段「双面板分屏以引言为主角——白/蓝面板从中心翻开、强调色条生长、引言逐行揭示」。保持模板的视觉签名，使用真实内容和数据，避免 lorem ipsum 和占位图片。"
---

# Electric Studio Frame

Two-panel split with quote as hero — white/blue panels open from center, accent bar grows, quote reveals line by line.

## What this template is

A HyperFrames-ready HTML + CSS + GSAP motion composition, bundled under `source/`. It renders deterministically to MP4 / WEBM at 16:9, 1:1, default 15s, 60fps.

**Best for:** Pull-quote / testimonial reveal · Mission statement card · Clean high-contrast title

## Workflow

1. Read `source/index.html` to understand the named layers and the animation timeline.
2. Replace the sample copy (headlines, figures, labels) with the user's real content; keep the motion timing and visual signature intact.
3. Keep the composition self-contained under `source/`; do not introduce external network assets that would break a headless render.
4. Render to MP4 via the html-video / HyperFrames renderer.

## Attribution

Source: html-video `templates/frame-electric-studio` (license Apache-2.0). Derived from frontend-slides (Zara Zhang, MIT) — https://github.com/zarazhangrui/frontend-slides.
