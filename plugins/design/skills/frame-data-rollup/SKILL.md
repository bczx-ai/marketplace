---
name: video-template-frame-data-rollup
zh_name: "数据滚动帧"
en_name: "Data Rollup Frame"
description: Use this plugin when the user wants a "Data Rollup Frame" HyperFrames motion video — A native Remotion data frame — bars grow from zero by real data via spring physics while the figures roll 0→target in sync.
zh_description: "Remotion 原生数据帧——柱条按真实数据以弹簧物理从零生长、数字同步从 0 滚到目标值"
zh_tags:
  - "数据可视化"
  - "柱状图"
  - "数字滚动"
  - "Remotion"
license: Apache-2.0
metadata:
  author: nexu-io
  version: "0.1.0"
od:
  mode: video
  scenario: video
  surface: hyperframes
  example_prompt_i18n:
    zh-CN: "用「数据滚动帧」模板把我的内容做成一段「Remotion 原生数据帧——柱条按真实数据以弹簧物理从零生长、数字同步从 0 滚到目标值」。保持模板的视觉签名，使用真实内容和数据，避免 lorem ipsum 和占位图片。"
---

# Data Rollup Frame

A native Remotion data frame — bars grow from zero by real data via spring physics while the figures roll 0→target in sync.

## What this template is

A HyperFrames-ready Remotion (React/TSX) motion composition, bundled under `source/`. It renders deterministically to MP4 / WEBM at 16:9, 9:16, 1:1, default 15s, 30fps.

**Best for:** A data frame where the numbers should animate, not sit static · Weekly metrics / growth bars driven by real values · Enhancing one data segment of an otherwise hyperframes video

## Workflow

1. Read `source/entry.ts` to understand the named layers and the animation timeline.
2. Replace the sample copy (headlines, figures, labels) with the user's real content; keep the motion timing and visual signature intact.
3. Keep the composition self-contained under `source/`; do not introduce external network assets that would break a headless render.
4. Render to MP4 via the html-video / HyperFrames renderer.

## Attribution

Source: html-video `templates/frame-data-rollup` (license Apache-2.0).
