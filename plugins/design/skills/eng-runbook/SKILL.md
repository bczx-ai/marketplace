---
name: eng-runbook
zh_name: "工程运维手册"
zh_description: "面向服务的单页工程运维手册，含告警表、仪表盘链接、常用操作步骤、值班轮值与事故响应清单"
description: |
  An engineering runbook — service overview, alerts table, dashboards
  links, common procedures with copy-pasteable commands, on-call rotation,
  and an incident-response checklist. Use when the brief mentions
  "runbook", "ops doc", "on-call guide", "SRE doc", or "运维手册".
triggers:
  - "runbook"
  - "ops doc"
  - "on-call"
  - "sre doc"
  - "service runbook"
  - "运维手册"
od:
  mode: prototype
  platform: desktop
  scenario: engineering
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
    sections: [color, typography, layout, components]
  example_prompt: "Write a runbook for our auth service — alerts, dashboards, common procedures, on-call rotation."
  example_prompt_i18n:
    zh-CN: "为我们的 auth 服务写一份 runbook——告警、仪表盘、常用操作步骤、值班轮值。"
---

# Engineering Runbook Skill

Produce a single-page engineering runbook.

## Workflow

1. Read DESIGN.md.
2. Identify the service from the brief.
3. Layout:
   - Header: service name, owner team, severity tier, version.
   - Service summary paragraph + dependency list.
   - Alerts table: alert name / severity / what it means / first response.
   - Dashboards & links list.
   - Common procedures block (3–4) with code blocks (deploy, rollback, rotate keys).
   - On-call rotation table (week / primary / secondary / backup).
   - Incident response checklist (5 numbered steps).
4. One inline `<style>`, semantic HTML, monospace for code blocks.

## Output contract

```
<artifact identifier="runbook-name" type="text/html" title="Service Runbook">
<!doctype html>...</artifact>
```
