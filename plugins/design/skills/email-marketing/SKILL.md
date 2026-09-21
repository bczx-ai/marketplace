---
name: email-marketing
zh_name: "品牌发布邮件"
zh_description: "品牌产品发布邮件版式，报头加主视觉、倾斜斜体标题锁定、正文、主行动号召与规格网格，纯 HTML 单列加表格降级"
description: |
  A brand product-launch email — masthead with wordmark, hero image block,
  headline lockup with skewed-italic accent, body copy, primary CTA, and a
  specifications grid. Pure HTML email layout (centered single column, table
  fallback). Use when the brief asks for an "email", "newsletter blast",
  "MJML", "product launch email", or "email template".
triggers:
  - "email"
  - "email template"
  - "newsletter"
  - "email blast"
  - "product launch email"
  - "mjml"
  - "邮件营销"
  - "邮件模板"
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
  example_prompt: "Design a launch email for a sporty running shoe brand — masthead, hero, big headline lockup, specs grid, CTA."
  example_prompt_i18n:
    zh-CN: "为一个运动跑鞋品牌设计上线邮件——报头、主视觉、大标题锁定、规格网格、行动号召。"
---

# Email Marketing Skill

Produce a single HTML email — centered, single column, no chrome around the
email body. Treat it like a marketing artifact: one big idea, one CTA.

## Workflow

1. **Read the active DESIGN.md** (injected above). Email leans on the display
   font more than any other surface — pick the loudest type token in the DS
   for the headline lockup.
2. **Pick the brand + product** from the brief. Generate a real wordmark, a
   real product name, and one real benefit sentence — no placeholders.
3. **Layout**, in order, all centered inside a 600–680px column on a tinted
   page background (so the email body looks like an email, not the page):
   - **Masthead** — wordmark on the left + 3 short nav links (SHOP, JOURNAL,
     MEMBERS) on the right. Thin underline.
   - **Hero block** — a 16:9 product image placeholder. Use a DS-tinted
     gradient or a stylized SVG silhouette of the product (shoe, bottle,
     headphones, whatever the brief implies). Add a tiny brand stamp on the
     top-left and a colorway tag on the bottom-left.
   - **Eyebrow** — small caps, accent color, separated by `·` characters
     (e.g. "NEW · MAX-CUSHION TRAINER · EMBER FLARE").
   - **Headline lockup** — 2–3 line headline using the display font, all caps,
     extra-tight tracking. Apply a slight skew (`transform: skew(-6deg)`) on
     one accent word to give it a sporty parallelogram feel.
   - **Body** — 2–3 sentence paragraph, left-aligned, body font.
   - **Primary CTA** — solid pill or block button. One only.
   - **Specs grid** — 2×2 grid of (big number + unit + label) callouts using
     the display font for the numbers.
   - **Footer** — wordmark, address line, unsubscribe + view-in-browser links.
4. **Write** a single HTML document:
   - `<!doctype html>` through `</html>`, CSS inline.
   - Center the column with `margin: 0 auto`. Set `body { background: <tint> }`
     so the email-on-page metaphor reads.
   - No external images — use inline SVG or DS-tinted gradient blocks for the
     product photo.
   - `data-od-id` on the masthead, hero, headline, CTA, specs.
5. **Self-check**:
   - Email reads top to bottom in 8–10 seconds.
   - One CTA. Accent appears at most twice (eyebrow + CTA, or headline word).
   - Looks legible on a 480px window (column reflows, type drops one step).

## Output contract

Emit between `<artifact>` tags:

```
<artifact identifier="email-slug" type="text/html" title="Email — Subject Line">
<!doctype html>
<html>...</html>
</artifact>
```

One sentence before the artifact, nothing after.
