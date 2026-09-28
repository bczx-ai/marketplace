---
name: digital-eguide
zh_name: "电子指南折页"
zh_description: "双页电子指南预览，封面页含主标题、作者与目录预告，内页为带引言块与步骤清单的正文，适合创作者品牌"
description: |
  A two-spread digital e-guide preview — page 1 is a cover (display title,
  author, "What's inside" stats, table of contents teaser); page 2 is a
  spread (lesson body with pull-quote and a step list). Lifestyle / creator
  brand tone. Use when the brief asks for an "e-guide", "digital guide",
  "lookbook", "lead magnet", "creator guide", "playbook", "PDF guide",
  or "电子指南".
triggers:
  - "e-guide"
  - "digital guide"
  - "lead magnet"
  - "lookbook"
  - "creator guide"
  - "playbook"
  - "pdf guide"
  - "ebook"
  - "电子指南"
  - "电子书"
od:
  mode: prototype
  platform: desktop
  scenario: marketing
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
    sections: [color, typography, layout, components]
  craft:
    requires: [typography, typography-hierarchy, typography-hierarchy-editorial, rtl-and-bidi]
  example_prompt: "Design 'The Creator's Style & Format Guide' — cover page and one inside spread, lifestyle creator brand."
  example_prompt_i18n:
    zh-CN: "设计《The Creator's Style & Format Guide》——封面页加一个内页跨页，生活方式创作者品牌。"
---

# Digital E-Guide Skill

Produce a two-page digital guide preview side-by-side. Cover on the inline-start,
inside spread on the inline-end. Lifestyle creator tone, lots of negative space,
serif display headings, careful column rhythm.

## Workflow

1. **Read the active DESIGN.md** (injected above). Pick a serif display
   token for the title (italic ligatures encouraged), a body serif for
   long-form, and a mono token for stats / labels.
2. **Pick the topic + author** from the brief. Generate a real title (e.g.
   "The Creator's Style & Format Guide"), a real subtitle, and a one-line
   author byline.
3. **Layout** — center two pages on a tinted backdrop:
   - **Page 1 — cover**:
     - Eyebrow ("STYLE & FORMAT GUIDE FOR CREATORS").
     - Display title with mixed weights and one italic flourish word
       ("The Creator's Style & Format guide" — `&` and `guide` italic).
     - 3-cell stat row ("16 PRINCIPLES OF STYLE", "38 DOS & DON'TS",
       "1 BLOCK, ZERO TEMPLATES") in mono, separated by `·`.
     - "What's inside" header with a 2-column TOC (chapters + page numbers
       in mono, leader dots).
     - Footer: "FIND YOUR VOICE" + page 01 mono.
     - Subtle decorative dot or sticker (CSS) in a corner.
   - **Page 2 — spread**:
     - Eyebrow with chapter number + name ("CHAPTER 02 · TONE").
     - Display sub-title ("Write like you talk — only sharper.").
     - 2-column body: opening paragraph + a numbered 4-step list ("01 Pick
       the rule", "02 Drop the filler"…).
     - Pull-quote pinned to inline-end: for Latin scripts use large italic display
      and accent color; for Arabic, Persian, and Urdu use regular or light
      emphasis (no italics); for Hebrew use regular or light emphasis (no
      italics). Include attribution. (script-aware)
     - Bottom strip with "EXERCISE" callout (mono label + 1 sentence prompt
       in italic).
     - Footer: chapter title + page 18 mono.
4. **Write** a single HTML document:
   - `<!doctype html>` through `</html>`, CSS inline.
   - Pages are 600×860 paper-tone cards with 6px shadow, slight rotation
     opposing each other (±0.6deg) for a magazine-on-desk feel.
   - `data-od-id` on cover, spread, toc, pull-quote, exercise.
5. **Self-check**:
   - Type hierarchy is editorial — title owns page 1, sub-title owns page 2.
   - Italic accent appears once per page.
   - Mono used only for labels, stats, and TOC numbers.

## Output contract

Emit between `<artifact>` tags:

```
<artifact identifier="eguide-slug" type="text/html" title="E-Guide — Title">
<!doctype html>
<html>...</html>
</artifact>
```

One sentence before the artifact, nothing after.
