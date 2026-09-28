---
name: flowai-live-dashboard-template
zh_name: "FlowAI 团队管理看板"
en_name: "FlowAI Live Dashboard Template"
description: |
  Team-management dashboard skill in the FlowAI aesthetic — three tabs
  (Team Members, Team Details, Activity Log), KPI stat row, member table,
  role distribution bar chart, online presence and activity sparklines,
  and a top-contributors panel, all in a single self-contained HTML file
  with light/dark theming, hoverable chart tooltips, click-to-zoom panels,
  and CSV export. Use when the brief asks for a team / workspace admin
  dashboard, an interactive admin dashboard with charts, or names FlowAI.
zh_description: "FlowAI 风格的团队管理看板——三个标签页（成员、团队详情、活动日志）、KPI 指标行、成员表格、角色分布柱状图、在线状态与活跃度迷你趋势图，以及贡献者排行面板；单文件自包含 HTML，支持明暗主题、图表悬停提示、点击放大面板与 CSV 导出"
zh_tags:
  - "团队管理"
  - "管理后台"
  - "FlowAI"
  - "图表"
triggers:
  - "flowai dashboard"
  - "team dashboard"
  - "team management dashboard"
  - "interactive admin dashboard"
  - "workspace admin dashboard"
  - "团队管理后台"
  - "可交互后台"
od:
  mode: prototype
  platform: desktop
  scenario: operations
  preview:
    type: html
    entry: index.html
    reload: debounce-100
  design_system:
    requires: true
    sections: [color, typography, layout, components]
  craft:
    requires: [state-coverage, accessibility-baseline]
  example_prompt: "Create a FlowAI-style team management dashboard with Team Members, Team Details and Activity Log tabs, KPI cards, a member table with status badges, a role-distribution bar chart, an online-presence sparkline, top contributors, light/dark mode, and CSV export."
  example_prompt_i18n:
    zh-CN: "做一个 FlowAI 风格的团队管理看板，包含成员、团队详情和活动日志三个标签页、KPI 卡片、带状态徽标的成员表格、角色分布柱状图、在线状态迷你趋势图、贡献者排行、明暗模式以及 CSV 导出。"
---

# FlowAI Dashboard Skill

Produce a single-screen, multi-tab team management dashboard inspired by the
FlowAI aesthetic. The output is a self-contained HTML file (no external runtime
dependencies) with built-in interactions: tab switching, an animated bar chart,
hover tooltips on charts, click-to-zoom panels, dark mode toggle, and CSV
export of the visible team table.

## Resource map

```
flowai-live-dashboard-template/
├── SKILL.md
├── assets/
│   └── template.html          # reference seed used as the starting structure
├── references/
│   └── checklist.md           # P0/P1/P2 quality gates
└── example.html               # complete hand-built sample (gallery preview)
```

## Workflow

1. **Read the active DESIGN.md** (injected above). Map color, typography,
   spacing, and component styling tokens to the CSS variables used by
   `assets/template.html`. Do not invent new tokens.
2. Start from `assets/template.html`; never generate the shell from blank.
3. Keep three tabs: `Team Members`, `Team Details`, `Activity Log`. Tabs must
   actually switch and only one view is visible at a time.
4. Generate plausible, specific sample data (real-looking names, IDs, roles,
   departments, dates, percentages). No `Member A / Metric B` placeholders.
5. Required interactions:
   - tab switching with hash sync (`#members | #details | #activity`)
   - role bar chart animates with easing on first reveal of the details tab
   - chart hover tooltips with precise label + value
   - click any panel/card to zoom; click again or press Esc to restore
   - dark mode toggle that re-derives chart colors from CSS variables
   - "Export CSV" button that exports every row currently in the team table,
     including the `Workflow` column
6. Run through `references/checklist.md` before final output.

## Output contract

Emit one short orientation sentence, then the artifact:

```xml
<artifact identifier="flowai-team-dashboard" type="text/html" title="FlowAI Team Dashboard">
<!doctype html>
<html>...</html>
</artifact>
```

The artifact must render correctly when opened directly from disk with no
build step and no network access.
