---
name: video-template-frame-product-promo-30s
zh_description: "30 秒产品宣传视频模板，适合新品发布和功能亮点展示。"
zh_name: "产品宣传片 30 秒帧"
en_name: "Product Promo · 30s"
description: "Use this plugin when the user wants a \"Product Promo · 30s\" HyperFrames motion video — Multi-scene 30-second product promo: problem-type intro, brand reveal, benefits flowchart, product surfaces, value pillars, foundation, CTA outro. Forked from Nate Herk's hyperframes-student-kit (linear-promo-30s); brand-specific copy + assets replaced with generic placeholders."
zh_tags:
  - "产品宣传"
  - "30 秒"
  - "多场景"
  - "行动号召"
license: MIT
metadata:
  author: Nate Herk
  version: "0.1.0"
od:
  mode: video
  scenario: video
  surface: hyperframes
  example_prompt_i18n:
    zh-CN: "用「产品宣传片 30 秒帧」模板把我的内容做成一段「多场景 30 秒产品宣传片——问题式开场、品牌揭示、卖点流程图、产品界面、价值支柱、底座、行动号召收尾；派生自 Nate Herk 的 hyperframes-student-kit（linear-promo-30s），品牌专属文案与素材已替换为通用占位」。保持模板的视觉签名，使用真实内容和数据，避免 lorem ipsum 和占位图片。"
---

# Product Promo · 30s

Multi-scene 30-second product promo: problem-type intro, brand reveal, benefits flowchart, product surfaces, value pillars, foundation, CTA outro. Forked from Nate Herk's hyperframes-student-kit (linear-promo-30s); brand-specific copy + assets replaced with generic placeholders.

## What this template is

A HyperFrames-ready HTML + CSS + GSAP motion composition, bundled under `source/`. It renders deterministically to MP4 / WEBM at 16:9, default 30s, 30fps.

**Best for:** 30-second product promo · B2B SaaS launch · Multi-feature reel with sound

## Workflow

1. Read `source/index.html` to understand the named layers and the animation timeline.
2. Replace the sample copy (headlines, figures, labels) with the user's real content; keep the motion timing and visual signature intact.
3. Keep the composition self-contained under `source/`; do not introduce external network assets that would break a headless render.
4. Render to MP4 via the html-video / HyperFrames renderer.

## Attribution

Source: html-video `templates/frame-product-promo-30s` (license MIT). Forked from Nate Herk — https://github.com/nateherkai/hyperframes-student-kit/tree/main/video-projects/linear-promo-30s.
