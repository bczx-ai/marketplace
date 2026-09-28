---
name: video-template-frame-build-minimal
zh_name: "极简留白帧"
en_name: "Build Minimal Frame"
description: Use this plugin when the user wants a "Build Minimal Frame" HyperFrames motion video — Luxury-minimal whitespace hero — single word reveals letter by letter, warm-gold hairline, breathing indicators.
zh_description: "奢华极简留白主视觉——单个词逐字揭示、暖金色发丝线、呼吸感指示器"
zh_tags:
  - "极简"
  - "留白"
  - "奢华"
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
    zh-CN: "用「极简留白帧」模板把我的内容做成一段「奢华极简留白主视觉——单个词逐字揭示、暖金色发丝线、呼吸感指示器」。保持模板的视觉签名，使用真实内容和数据，避免 lorem ipsum 和占位图片。"
---

# Build Minimal Frame

Luxury-minimal whitespace hero — single word reveals letter by letter, warm-gold hairline, breathing indicators.

## What this template is

A HyperFrames-ready HTML + CSS + GSAP motion composition, bundled under `source/`. It renders deterministically to MP4 / WEBM at 16:9, 1:1, default 15s, 60fps.

**Best for:** Premium product / brand hero · Calm single-word statement · Elegant title card

## Workflow

1. Read `source/index.html` to understand the named layers and the animation timeline.
2. Replace the sample copy (headlines, figures, labels) with the user's real content; keep the motion timing and visual signature intact.
3. Keep the composition self-contained under `source/`; do not introduce external network assets that would break a headless render.
4. Render to MP4 via the html-video / HyperFrames renderer.

## Attribution

Source: html-video `templates/frame-build-minimal` (license Apache-2.0). Derived from huashu-design (alchaincyf (花叔 · 花生), MIT) — https://github.com/alchaincyf/huashu-design. Stylistic inspiration (L1, not affiliated): Build.
