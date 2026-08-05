---
name: seo-competitor-analysis
displayName: "SEO Intelligence & Competitor Analysis Pro"
description: "执行深度SEO竞品分析，包括关键词研究、反向链接检查及内容策略规划。适用于用户需要分析网站竞争对手或通过研究对手提升自身SEO排名的场景。"
version: 1.0.0
tags:
  - content_creation
license: "Unknown"
---

# SEO Competitor Analysis Skill

This skill automates the process of identifying and analyzing SEO competitors to inform content and ranking strategies.

## Workflow

1. **Identify Competitors**: If not provided, search for the target domain and identify top-ranking sites for similar keywords.
2. **Analyze Keywords**: Use `web_search` to find ranking keywords and search volume (if available via snippets).
3. **Content Gap Analysis**: Compare the user's content with competitors to identify missing topics.
4. **Report Generation**: Summarize findings into a structured report.

## Tools to Use

- `web_search`: To find competitors and their ranking content.
- `web_fetch`: To extract content from competitor pages for deep analysis.
- `browser`: For complex pages that require JavaScript or manual navigation patterns.

## Scripts

- `scripts/competitor_finder.py`: (Optional) Logic to automate the discovery of competitors using search APIs.

## References

- `references/seo_metrics_guide.md`: Definition of SEO terms and how to interpret them.
- `references/report_template.md`: A standard structure for the final SEO analysis report.
