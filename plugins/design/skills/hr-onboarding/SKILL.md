---
name: hr-onboarding
zh_name: "新员工入职计划"
zh_description: "单页新员工入职计划，含首周日程、伙伴与主管引荐、学习路径、设备清单与达成即上手的成果，适合入职场景"
description: |
  A new-hire onboarding plan as a single page — first week schedule,
  buddy + manager intro, learning track, equipment checklist, and "you're
  set when…" outcomes. Use when the brief mentions "onboarding",
  "new hire", "first week plan", or "入职".
triggers:
  - "onboarding"
  - "new hire"
  - "first week"
  - "入职"
  - "新员工"
od:
  mode: prototype
  platform: desktop
  scenario: hr
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
    sections: [color, typography, layout, components]
  craft:
    requires: [accessibility-baseline]
  example_prompt: "Build a 30-day onboarding plan for a new product designer joining a 40-person startup."
  example_prompt_i18n:
    zh-CN: "为一位加入 40 人创业公司的新产品设计师制定一份 30 天入职计划。"
---

# HR Onboarding Skill

Produce a single-screen onboarding plan in HTML.

## Workflow

1. Read the active DESIGN.md.
2. Identify the role + tenure expectations from the brief. Default to a
   30/60/90-day shape if unspecified.
3. Layout:
   - Cover banner: name placeholder, role, start date, manager + buddy.
   - "Day 1" panel with the literal schedule (kickoff time, lunch, 1:1 slot).
   - First-week timeline (Mon → Fri, two activities per day).
   - 30 / 60 / 90 day milestone cards with three concrete outcomes each.
   - Resource list: handbook, Slack channels, key dashboards, payroll setup.
   - "You're set when…" checklist — five outcomes with checkboxes.
4. Single inline `<style>`, semantic HTML.

## Output contract

```
<artifact identifier="onboarding-plan" type="text/html" title="Onboarding Plan">
<!doctype html>...</artifact>
```
