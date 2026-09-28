---
name: meeting-notes
zh_name: "会议纪要页面"
zh_description: "会议纪要页面，含与会人标题栏、议程清单、决议块、带负责人与日期的行动项表格和下次会议页脚"
description: |
  Meeting notes page — title bar with attendees, agenda checklist, decisions
  block, action items table with owners + dates, and a "next meeting" footer.
  Use when the brief mentions "meeting notes", "minutes", "1:1 notes",
  "all-hands recap", or "会议纪要".
triggers:
  - "meeting notes"
  - "minutes"
  - "1:1 notes"
  - "all-hands recap"
  - "会议纪要"
od:
  mode: prototype
  platform: desktop
  scenario: operations
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
    sections: [color, typography, layout, components]
  example_prompt: "Write up notes from a 60-minute Growth squad weekly — agenda, decisions, action items with owners, next meeting."
  example_prompt_i18n:
    zh-CN: "整理一场 60 分钟增长小组周会的会议纪要——议程、决议、带负责人的行动项、下次会议。"
---

# Meeting Notes Skill

Produce a single-screen meeting notes page.

## Workflow

1. Read DESIGN.md.
2. Layout:
   - Header: meeting title, date, time, location/Zoom, attendees row.
   - Agenda checklist (4–6 items).
   - Decisions panel — bulleted list with strong styling.
   - Action items table with owner, due date, status.
   - "Open questions" + "next meeting" footer.
3. Subdued colour palette, clear hierarchy.

## Output contract

```
<artifact identifier="notes-name" type="text/html" title="Meeting Notes">
<!doctype html>...</artifact>
```
