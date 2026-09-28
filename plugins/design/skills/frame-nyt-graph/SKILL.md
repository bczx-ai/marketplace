---
name: video-template-frame-nyt-graph
zh_name: "NYT 风动画图表帧"
en_name: "NYT Graph"
description: Use this plugin when the user wants a "NYT Graph" HyperFrames motion video — Animated data chart in print editorial style
zh_description: "印刷编辑风格的动画数据图表"
zh_tags:
  - "数据可视化"
  - "图表"
  - "编辑设计"
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
    zh-CN: "用「NYT 风动画图表帧」模板把我的内容做成一段「印刷编辑风格的动画数据图表」。保持模板的视觉签名，使用真实内容和数据，避免 lorem ipsum 和占位图片。"
---

# NYT Graph

Animated data chart in print editorial style

## What this template is

A HyperFrames-ready HTML + CSS + GSAP motion composition, bundled under `source/`. It renders deterministically to MP4 / WEBM at 16:9, default 15s, 30fps.

**Best for:** News-style stat reveal · Line chart over time · Editorial data point

## Workflow

1. Read `source/index.html` to understand the named layers and the animation timeline.
2. Replace the sample copy (headlines, figures, labels) with the user's real content; keep the motion timing and visual signature intact.
3. Keep the composition self-contained under `source/`; do not introduce external network assets that would break a headless render.
4. Render to MP4 via the html-video / HyperFrames renderer.

## Attribution

Source: html-video `templates/frame-nyt-graph` (license Apache-2.0). Forked from heygen-com / Hyperframes — https://github.com/heygen-com/hyperframes/tree/main/registry/examples/nyt-graph.
