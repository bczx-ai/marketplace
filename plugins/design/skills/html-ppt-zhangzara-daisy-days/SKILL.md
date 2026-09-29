---
name: html-ppt-zhangzara-daisy-days
zh_description: "清新花卉风格的客户上手培训幻灯片，讲清首次见效路径和留存习惯。"
en_name: "Write a Customer Onboarding Workshop like a Field Enablement Director"
zh_name: "像客户成功赋能总监一样写客户上手工作坊"
description: |
  A customer-success workshop onboarding users to a project-management app — the first-value path and the habits that retain. Built as a decision-grade professional training deck for new customers, CS team.
en_description: |
  A customer-success workshop onboarding users to a project-management app — the first-value path and the habits that retain. Built as a decision-grade professional training deck for new customers, CS team.
tags:
  - "professional-training"
  - "employee-onboarding-deck"
  - "education"
  - "training-deck"
  - "workshop"
  - "course-module"
  - "decision-deck"
  - "commercial-slide-agent"
  - "html-ppt-zhangzara-daisy-days"
zh_tags:
  - "员工入职"
  - "教育"
  - "培训演示"
  - "工作坊"
  - "课程模块"
triggers:
  - "employee-onboarding-deck"
  - "professional-training"
  - "Write a Customer Onboarding Workshop like a Field Enablement Director"
  - "像客户成功赋能总监一样写客户上手工作坊"
  - "training-deck"
  - "workshop"
  - "course-module"
  - "html deck"
  - "html slides"
od:
  mode: deck
  upstream: "https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/daisy-days"
  upstream_license: MIT
  preview:
    type: html
    entry: example.html
  design_system:
    requires: false
  speaker_notes: false
  animations: false
  category: "professional-training"
  scenario: "education"
  example_prompt: "Create \"Write a Customer Onboarding Workshop like a Field Enablement Director\" as a decision-grade Professional training deck in this template's own visual system. Subject: A customer-success workshop onboarding users to a project-management app — the first-value path and the habits that retain. Audience: new customers, CS team. First ask only for missing essentials: audience, decision target, source-of-truth materials, deadline, and must-keep numbers. Then produce the slide plan, written slides, visual direction, speaker-ready structure, and a critic pass against this rubric: can a learner perform the target task the next day."
  example_prompt_i18n:
    zh-CN: "用本模板自有的视觉系统，做一份决策级的职业培训演示文稿：「像客户成功赋能总监一样写客户上手工作坊」。主题：一场帮助用户上手项目管理 App 的客户成功工作坊——首次价值路径与带来留存的习惯。受众：新客户、客户成功团队。先只追问缺失的关键信息：受众、决策目标、权威资料、截止时间，以及必须保留的数字。然后产出幻灯片规划、成稿幻灯片、视觉方向、可直接开讲的结构，并对照这条评分标准做一次批评性检查：学员第二天能否独立完成目标任务。"
---

# Daisy Days

> Cheerful pastel deck with hand-drawn daisies, stars, and rainbows. Friendly, soft, and warm.

A single self-contained HTML deck — typography, palette, decorative system,
and slide vocabulary are all tuned together. Mixing layouts across templates
breaks the system; stay inside this one.

## At a glance

- **Scheme:** light
- **Formality:** low
- **Density:** medium
- **Slides in demo:** 10

## Best for

Anything that should feel friendly, soft, and joyful: educational content, kids and family, wellness programs, community workshops, creator portfolios for craft / illustration. Also lovely for an unexpected playful internal kickoff, a wedding planning deck, or any moment where warmth is the message — including across tech or business contexts.

## Avoid for

Contexts where the audience explicitly expects authority and precision — the hand-drawn pastel SVG decorations are the opposite of buttoned-up.

## Workflow

1. **Clone `example.html`** into the user's workspace as the working file.
2. **Replace placeholder content** with the user's real headlines, body copy,
   numbers, names, dates, and section labels. Match existing dimensions when
   swapping image placeholders.
3. **Preserve the design system.** Never substitute fonts, recolor the palette,
   restructure the layout grid, or strip decorative elements (corner brackets,
   paper grain, geometric shapes, illustrated SVGs). They are part of the
   identity.
4. **Adjust deck length by duplicating layouts.** If the user has more content
   than the demo holds, duplicate an existing slide of the most appropriate
   layout. If less, drop slides from the bottom. Update page-number labels.
5. **Designing missing layouts:** if a slide needs a layout the template
   doesn't have, design it from scratch using the same fonts, palette,
   decorative vocabulary, spacing rhythm, and component grammar — never bail
   to a different template.
6. **Keep the navigation runtime as shipped.** If the deck ships an
   `assets/deck-stage.js` or inline keyboard handler, leave it intact.

## Output contract

Emit between `<artifact>` tags:

```
<artifact identifier="zhangzara-daisy-days" type="text/html" title="Deck Title">
<!doctype html>
<html>...</html>
</artifact>
```

## Source & license

Vendored from upstream MIT-licensed
[`zarazhangrui/beautiful-html-templates`](https://github.com/zarazhangrui/beautiful-html-templates/tree/main/templates/daisy-days).

The full upstream MIT license text — including the original copyright notice — ships in this skill at
[`LICENSE`](./LICENSE) and must be redistributed alongside any copy of `example.html`,
`template.json`, or any vendored `assets/` runtime. See `template.json` for the upstream metadata snapshot.
