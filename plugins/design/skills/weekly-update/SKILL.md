---
name: weekly-update
zh_description: "每周指标例会幻灯片，呈现本周数据、异常项和需要做的决定。"
en_name: "Run a Metrics Standup like a Data-Driven Ops Lead"
zh_name: "像数据驱动的运营负责人一样开指标站会"
description: |
  Open Design's weekly metrics standup: this week's numbers, the one anomaly, and the single decision it forces. Built as a decision-grade data & finance deck for ops & growth team.
en_description: |
  Open Design's weekly metrics standup: this week's numbers, the one anomaly, and the single decision it forces. Built as a decision-grade data & finance deck for ops & growth team.
tags:
  - "data-finance"
  - "product-analytics-deck"
  - "finance"
  - "kpi"
  - "metrics"
  - "decision-deck"
  - "commercial-slide-agent"
  - "weekly-update"
zh_tags:
  - "产品数据分析"
  - "财务"
  - "KPI"
  - "指标"
triggers:
  - "product-analytics-deck"
  - "data-finance"
  - "Run a Metrics Standup like a Data-Driven Ops Lead"
  - "像数据驱动的运营负责人一样开指标站会"
  - "kpi"
  - "finance"
  - "metrics"
  - "html deck"
  - "html slides"
od:
  mode: deck
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
    sections: [color, typography, layout, components]
  category: "data-finance"
  scenario: "finance"
  example_prompt: "Create \"Run a Metrics Standup like a Data-Driven Ops Lead\" as a decision-grade Data, KPI & finance deck in this template's own visual system. Subject: Open Design's weekly metrics standup: this week's numbers, the one anomaly, and the single decision it forces. Audience: ops & growth team. First ask only for missing essentials: audience, decision target, source-of-truth materials, deadline, and must-keep numbers. Then produce the slide plan, written slides, visual direction, speaker-ready structure, and a critic pass against this rubric: does every chart have a decision above it."
  example_prompt_i18n:
    zh-CN: "用本模板自有的视觉系统，做一份决策级的数据、KPI 与财务演示文稿：「像数据驱动的运营负责人一样开指标站会」。主题：OpenDesign 的每周指标站会——本周数字、唯一异常，以及它逼迫你做出的那个决定。受众：运营与增长团队。先只追问缺失的关键信息：受众、决策目标、权威资料、截止时间，以及必须保留的数字。然后产出幻灯片规划、成稿幻灯片、视觉方向、可直接开讲的结构，并对照这条评分标准做一次批评性检查：每张图表上方是否都有一个待决策的问题。"
---

# Weekly Update Deck Skill

Produce a single-file horizontal-swipe HTML deck for a weekly team update.

## Workflow

1. Read DESIGN.md.
2. Identify squad name, week range, and audience (squad-internal vs cross-functional).
3. Slides:
   1. Cover (squad + week + author + date)
   2. Headline (one sentence + one number that matters this week)
   3. What shipped (3–5 items, link-style affordance)
   4. In flight (3–5 items, owner avatars)
   5. Blocked (1–3 items + clear ask)
   6. Metrics that matter (1–2 inline charts)
   7. Asks for next week (named owners)
   8. Closing + thanks
4. Arrow keys or click navigation. Each slide is 100vw wide.

## Output contract

```
<artifact identifier="weekly-update-w42" type="text/html" title="Weekly Update — Growth · W42">
<!doctype html>...</artifact>
```
