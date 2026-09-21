---
name: webgl-aurora-veil
zh_name: "WebGL 极光帷幔"
zh_description: "自包含 WebGL2 主视觉，夜空星点之上层层极光光幕随鼠标摆动，适合需要静谧氛围的页面首屏"
description: |
  A self-contained WebGL2 hero: layered aurora light curtains warped over a night sky scattered with stars; move the cursor to sway the veil.
triggers:
  - "aurora veil"
  - "webgl hero"
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

# Aurora Veil

Produce a single self-contained `index.html` — A self-contained WebGL2 hero: layered aurora light curtains warped over a night sky scattered with stars; move the cursor to sway the veil.

## Why this is a powered artifact

Open Design detects `getContext('webgl2')` / heavy WebGL and renders this file in **powered preview** (a cross-origin-isolated iframe). The full GPU + scroll pipeline runs; no opaque-sandbox workarounds are needed.

## Resource map

```
webgl-aurora-veil/
├── SKILL.md          ← you're reading this
├── example.html      ← the complete, working artifact (READ FIRST)
└── (assets, if any)
```

## Credits / attribution

- Original, self-contained (no third-party assets).

Keep any bundled LICENSE and on-screen credit intact. Replace imagery only with license-clean assets (original / AI, Lummi.ai, Unsplash/Pexels — never scraped imagery).
