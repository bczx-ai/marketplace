---
name: html-ppt-course-module
zh_description: "新员工入职培训课件，包含行为要求、练习、考核和主管跟进。"
en_name: "Build a New-Hire Onboarding Module like a Top Enablement Lead"
zh_name: "像顶级赋能负责人一样做新人培训模块"
description: |
  A first-30-days onboarding module for new hospitality hires — the behaviors, the practice, the checks, and the manager follow-up. Built as a decision-grade professional training deck for new hires, managers.
en_description: |
  A first-30-days onboarding module for new hospitality hires — the behaviors, the practice, the checks, and the manager follow-up. Built as a decision-grade professional training deck for new hires, managers.
tags:
  - "professional-training"
  - "employee-onboarding-deck"
  - "education"
  - "training-deck"
  - "workshop"
  - "course-module"
  - "decision-deck"
  - "commercial-slide-agent"
  - "html-ppt-course-module"
zh_tags:
  - "员工入职"
  - "教育"
  - "培训演示"
  - "工作坊"
  - "课程模块"
triggers:
  - "employee-onboarding-deck"
  - "professional-training"
  - "Build a New-Hire Onboarding Module like a Top Enablement Lead"
  - "像顶级赋能负责人一样做新人培训模块"
  - "training-deck"
  - "workshop"
  - "course-module"
  - "html deck"
  - "html slides"
od:
  mode: deck
  upstream: "https://github.com/lewislulu/html-ppt-skill"
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
  speaker_notes: true
  animations: true
  category: "professional-training"
  scenario: "education"
  example_prompt: "Create \"Build a New-Hire Onboarding Module like a Top Enablement Lead\" as a decision-grade Professional training deck in this template's own visual system. Subject: A first-30-days onboarding module for new hospitality hires — the behaviors, the practice, the checks, and the manager follow-up. Audience: new hires, managers. First ask only for missing essentials: audience, decision target, source-of-truth materials, deadline, and must-keep numbers. Then produce the slide plan, written slides, visual direction, speaker-ready structure, and a critic pass against this rubric: can a learner perform the target task the next day."
  example_prompt_i18n:
    zh-CN: "用本模板自有的视觉系统，做一份决策级的职业培训演示文稿：「像顶级赋能负责人一样做新人培训模块」。主题：面向酒店业新员工的入职 30 天模块——行为、练习、检查点与管理者的跟进。受众：新员工、管理者。先只追问缺失的关键信息：受众、决策目标、权威资料、截止时间，以及必须保留的数字。然后产出幻灯片规划、成稿幻灯片、视觉方向、可直接开讲的结构，并对照这条评分标准做一次批评性检查：学员第二天能否独立完成目标任务。"
---
# HTML PPT · Course Module

The training-delivery deck template, in the `course-module` visual identity.
Pick this template for onboarding and enablement modules — behaviors, practice,
checks and manager follow-up — built so a learner can perform the target task
the next day.

## Seed

`example.html` in this skill's directory is the reference deck. **Read it first.**
Its slide structure, theme tokens, typography and layout rhythm define this
template.

## Working file

When the user picks this template in the workbench, the workbench writes a
runtime-inlined, self-contained instance of the example into the project and
references it in the brief (`模板实例：<path>`). That file is the working file —
edit its content in place.

If no instance file is referenced in the brief, recreate the deck faithfully
from `example.html`'s structure and visual system as a single self-contained
HTML file.

## Editing rules

1. **Content edits only.** Never rewrite or remove the presentation runtime
   (navigation, scaling, print styles) embedded in the instance.
2. **No repo-relative references.** Never add `<script src="../assets/...">` or
   any other repo-relative link — those paths do not exist in the project.
   Everything the deck needs stays inline in the single file.
3. **Preserve the deck's visual system.** Keep the theme tokens, typography and
   layout rhythm from the example, and keep the structural classes it ships;
   replace the demo content with the user's real content.
4. **Speaker notes go inside `<aside class="notes">` or `<div class="notes">`** —
   never as visible text on the slide.

## Attribution

Visual system, layouts, themes and the runtime keyboard model come from
the upstream MIT-licensed [`lewislulu/html-ppt-skill`](https://github.com/lewislulu/html-ppt-skill).
