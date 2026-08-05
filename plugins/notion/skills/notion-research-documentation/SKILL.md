---
name: notion-research-documentation
description: Research across Notion and synthesize into structured documentation; use when gathering info from multiple Notion sources to produce briefs, comparisons, or reports with citations.
metadata:
  short-description: Research Notion content and produce briefs/reports
---

# Research & Documentation

Pull relevant Notion pages, synthesize findings, and publish clear briefs or reports (with citations and links to sources).

## Quick start
1) Find sources with `Notion:search` using targeted queries; confirm scope with the user.
2) Fetch pages via `Notion:fetch`; note key sections and capture citations (`reference/citations.md`).
3) Choose output format (brief, summary, comparison, comprehensive report) using `reference/format-selection-guide.md`.
4) Draft in Notion with `Notion:notion-create-pages` using the matching template (quick, summary, comparison, comprehensive).
5) Link sources and add a references/citations section; update as new info arrives with `Notion:notion-update-page`.

## Tool-call guardrails
- Notion tool availability can vary by workspace. If a Notion MCP call returns `Tool <name> not found`, treat that tool as unavailable for the rest of the current task. Do not retry it with different arguments or call it again later; use `Notion:search` and `Notion:fetch` where sufficient.
- Use one literal search query per `Notion:search` call and include `filters: {}` when no narrower filter is needed.
- Only fetch Notion page, database, or data-source URLs/IDs. Search results can include external connected-source URLs, which are not valid `Notion:fetch` inputs.
- Create output pages with an explicit `parent` and a `pages` array.
- When updating an existing report, fetch it first and use `Notion:notion-update-page` with `update_content`, `properties: {}`, and search-and-replace pairs. For property-only updates, use `update_properties` with `content_updates: []`. The current deployed schema expects both top-level fields even when one is unused. Do not invent insertion-only commands.

## Workflow
### 0) 如果 Notion 工具不可用，暂停并让用户完成 MCP 授权：
1. 从插件的 Notion MCP 入口发起授权。
2. 在浏览器中完成 Notion OAuth。
3. 如果工具仍未出现，创建新的 Agent 会话。

授权完成后，让用户重试当前任务，再继续第 1 步。

### 1) Gather sources
- Search first (`Notion:search`); refine queries, and ask the user to confirm if multiple results appear.
- Fetch relevant pages (`Notion:fetch`), skim for facts, metrics, claims, constraints, and dates.
- Track each source URL/ID for later citation; prefer direct quotes for critical facts.

### 2) Select the format
- Quick readout → quick brief.
- Single-topic dive → research summary.
- Option tradeoffs → comparison.
- Deep dive / exec-ready → comprehensive report.
- See `reference/format-selection-guide.md` for when to pick each.

### 3) Synthesize
- Outline before writing; group findings by themes/questions.
- Note evidence with source IDs; flag gaps or contradictions.
- Keep user goal in view (decision, summary, plan, recommendation).

### 4) Create the doc
- Pick the matching template in `reference/` (brief, summary, comparison, comprehensive) and adapt it.
- Create the page with `Notion:notion-create-pages`; include title, summary, key findings, supporting evidence, and recommendations/next steps when relevant.
- Add citations inline and a references section; link back to source pages.

### 5) Finalize & handoff
- Add highlights, risks, and open questions.
- If the user needs follow-ups, create tasks or a checklist in the page; link any task database entries if applicable.
- Share a short changelog or status using `Notion:notion-update-page` when updating.

## References and examples
- `reference/` — search tactics, format selection, templates, and citation rules (e.g., `advanced-search.md`, `format-selection-guide.md`, `research-summary-template.md`, `comparison-template.md`, `citations.md`).
- `examples/` — end-to-end walkthroughs (e.g., `competitor-analysis.md`, `technical-investigation.md`, `market-research.md`, `trip-planning.md`).
