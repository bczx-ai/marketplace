---
name: video-template-frame-warm-grain
zh_name: "暖调颗粒帧"
en_name: "Warm Grain"
description: Use this plugin when the user wants a "Warm Grain" HyperFrames motion video — Cream aesthetic with grain texture
zh_description: "奶油色调配颗粒质感"
zh_tags:
  - "暖色"
  - "颗粒质感"
  - "奶油色"
  - "动画帧"
license: Apache-2.0
metadata:
  author: heygen-com / Hyperframes
  version: "0.1.0"
od:
  mode: video
  scenario: video
  surface: hyperframes
  example_prompt_i18n:
    zh-CN: "用「暖调颗粒帧」模板把我的内容做成一段「奶油色调配颗粒质感」。保持模板的视觉签名，使用真实内容和数据，避免 lorem ipsum 和占位图片。"
---

# Warm Grain

Cream aesthetic with grain texture

## What this template is

A HyperFrames-ready HTML + CSS + GSAP motion composition, bundled under `source/`. It renders deterministically to MP4 / WEBM at 16:9, default 10s, 30fps.

**Best for:** Product launch · Lifestyle brand · Magazine-style intro

## Workflow

1. Read `source/index.html` to understand the named layers and the animation timeline.
2. Replace the sample copy (headlines, figures, labels) with the user's real content; keep the motion timing and visual signature intact.
3. Keep the composition self-contained under `source/`; do not introduce external network assets that would break a headless render.
4. Render to MP4 via the html-video / HyperFrames renderer.

## Attribution

Source: html-video `templates/frame-warm-grain` (license Apache-2.0). Forked from heygen-com / Hyperframes — https://github.com/heygen-com/hyperframes/tree/main/registry/examples/warm-grain.
