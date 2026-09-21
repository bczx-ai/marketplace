---
name: digits-fintech-swiss-template
zh_name: "瑞士网格金融模板"
zh_description: "瑞士网格风金融演示模板，黑、暖纸与荧光柠檬绿高对比，模块化数据卡配键盘与点击翻页，适合数据故事幻灯片"
description: |
  Swiss-grid fintech deck template in black / warm paper / neon-lime contrast.
  Use when users ask for premium data-story slides with strict modular layout,
  bold numeric cards, restrained motion, and keyboard/click navigation in one HTML file.
triggers:
  - "swiss fintech template"
  - "data-driven finance deck"
  - "neon lime editorial grid"
  - "high contrast strategy slides"
  - "数字金融瑞士风模板"
od:
  mode: template
  surface: video
  type: hyperframes
  platform: desktop
  preview:
    type: html
    entry: index.html
    reload: debounce-100
  outputs:
    primary: index.html
    secondary:
      - template.html
      - example.html
  example_prompt: "Create a Swiss-grid fintech strategy deck with modular data cards, lime accents, and clean keyboard navigation."
  example_prompt_i18n:
    zh-CN: "做一个瑞士网格风的金融科技策略演示文稿，含模块化数据卡片、柠檬绿点缀与干净的键盘导航。"
  capabilities_required:
    - file_write
---

# Digits Fintech Swiss Template

A premium three-slide live-artifact template for data-storytelling in a Swiss grid language.

## Resource map

```text
digits-fintech-swiss-template/
├── SKILL.md
├── assets/
│   └── template.html
├── references/
│   └── checklist.md
└── example.html
```

## Workflow

1. Start from `assets/template.html` and keep the three-slide structure intact.
2. Replace copy and metric values while preserving card hierarchy and reading order.
3. Keep interactions:
   - Prev / Next buttons
   - keyboard navigation (`ArrowLeft` / `ArrowRight`)
   - dot navigation
4. Keep motion subtle (slide fade + tiny hover lift only).
5. Keep the file self-contained (inline CSS/JS) with no sandbox-hostile APIs.

## Output contract

Emit one concise orientation sentence and then one HTML artifact:

```xml
<artifact identifier="digits-fintech-swiss" type="text/html" title="Digits Fintech Swiss Deck">
<!doctype html>
<html>...</html>
</artifact>
```
