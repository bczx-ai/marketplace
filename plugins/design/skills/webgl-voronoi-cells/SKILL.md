---
name: webgl-voronoi-cells
zh_name: "WebGL 泰森多边形"
zh_description: "自包含 WebGL2 主视觉，会呼吸的 Voronoi 网络配漂移特征点、配色分区的细胞与发光边界，移动光标可推挤细胞"
description: |
  A self-contained WebGL2 hero: a living Voronoi network with drifting feature points, palette-keyed cells and glowing boundaries; move the cursor to push the cells.
triggers:
  - "voronoi cells"
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

# Voronoi Cells

Produce a single self-contained `index.html` — A self-contained WebGL2 hero: a living Voronoi network with drifting feature points, palette-keyed cells and glowing boundaries; move the cursor to push the cells.

## Why this is a powered artifact

Open Design detects `getContext('webgl2')` / heavy WebGL and renders this file in **powered preview** (a cross-origin-isolated iframe). The full GPU + scroll pipeline runs; no opaque-sandbox workarounds are needed.

## Resource map

```
webgl-voronoi-cells/
├── SKILL.md          ← you're reading this
├── example.html      ← the complete, working artifact (READ FIRST)
└── (assets, if any)
```

## Credits / attribution

- Original, self-contained (no third-party assets).

Keep any bundled LICENSE and on-screen credit intact. Replace imagery only with license-clean assets (original / AI, Lummi.ai, Unsplash/Pexels — never scraped imagery).
