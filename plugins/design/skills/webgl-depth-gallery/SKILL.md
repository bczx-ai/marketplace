---
name: webgl-depth-gallery
zh_name: "WebGL 纵深画廊"
zh_description: "Three.js 滚动响应式 3D 图片画廊，Z 轴堆叠图片在情绪底色间交叉淡入，配光标拖尾与印刷色卡"
description: |
  A scroll-reactive 3D image gallery in Three.js: Z-stacked images crossfade over per-image mood backgrounds with velocity breath, a glowing cursor trail and an editorial CMYK/RGB/HEX/PMS color card.
triggers:
  - "depth gallery"
  - "webgl gallery"
od:
  mode: prototype
  platform: web
  scenario: design
  preview:
    type: html
    entry: index.html
    reload: debounce-100
  design_system:
    requires: false
  craft:
    requires: [animation-discipline]
---

# Depth Gallery

Produce a single self-contained `index.html` — A scroll-reactive 3D image gallery in Three.js: Z-stacked images crossfade over per-image mood backgrounds with velocity breath, a glowing cursor trail and an editorial CMYK/RGB/HEX/PMS color card.

## Why this is a powered artifact

Open Design detects `getContext('webgl2')` / heavy WebGL and renders this file in **powered preview** (a cross-origin-isolated iframe). The full GPU + scroll pipeline runs; no opaque-sandbox workarounds are needed.

## Resource map

```
webgl-depth-gallery/
├── SKILL.md          ← you're reading this
├── example.html      ← the complete, working artifact (READ FIRST)
└── (assets, if any)
```

## Credits / attribution

- effect: Houmahani Kane / Codrops (MIT)
- imagery: Lummi.ai

Keep any bundled LICENSE and on-screen credit intact. Replace imagery only with license-clean assets (original / AI, Lummi.ai, Unsplash/Pexels — never scraped imagery).
