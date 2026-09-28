---
name: video-template-frame-decision-tree
zh_name: "决策树帧"
en_name: "Decision Tree"
description: Use this plugin when the user wants a "Decision Tree" HyperFrames motion video — Animated flowchart with branching paths
zh_description: "带分支路径的动画流程图"
zh_tags:
  - "流程图"
  - "决策"
  - "分支"
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
    zh-CN: "用「决策树帧」模板把我的内容做成一段「带分支路径的动画流程图」。保持模板的视觉签名，使用真实内容和数据，避免 lorem ipsum 和占位图片。"
---

# Decision Tree

Animated flowchart with branching paths

## What this template is

A HyperFrames-ready HTML + CSS + GSAP motion composition, bundled under `source/`. It renders deterministically to MP4 / WEBM at 16:9, default 15s, 30fps.

**Best for:** How-to flow · Decision branching · Process diagram

## Workflow

1. Read `source/index.html` to understand the named layers and the animation timeline.
2. Replace the sample copy (headlines, figures, labels) with the user's real content; keep the motion timing and visual signature intact.
3. Keep the composition self-contained under `source/`; do not introduce external network assets that would break a headless render.
4. Render to MP4 via the html-video / HyperFrames renderer.

## Attribution

Source: html-video `templates/frame-decision-tree` (license Apache-2.0). Forked from heygen-com / Hyperframes — https://github.com/heygen-com/hyperframes/tree/main/registry/examples/decision-tree.
