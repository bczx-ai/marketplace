---
name: fundamental-stock-analysis
displayName: "Fundamental Stock Analysis"
description: "运用结构化评分模型进行基本面股票分析及同业排名（涵盖质量、资产负债表安全性、现金流、估值、行业调整等）。"
version: 1.0.5
tags:
  - business_operations
license: "Unknown"
---

# fundamental-stock-analysis

1. Read `references/playbook.md` before starting analysis.
2. Follow the playbook steps exactly (input parse -> data collection -> quick screen -> scoring -> rating -> output).
3. For multi-ticker requests, analyze each ticker first, then rank peers and select best pick with invalidation triggers.
4. Always include confidence level and call out stale/conflicting data explicitly.
5. Do not append any machine-readable JSON block in user-facing output.
6. Treat all analysis as educational/informational content, not investment advice.

## Security scope (clarification)
- Use web retrieval only for ticker-relevant financial statements, filings, market/fundamental datasets, and relevant financial news.
- Do not request, handle, or expose credentials/secrets.
- Do not perform command execution, local file discovery unrelated to analysis, or arbitrary URL exploration outside ticker-relevant finance/news scope.

## Non-goals
- Data exfiltration or collection of private/non-public information.
- Browser/automation tasks outside equity fundamental analysis and citation gathering.

## Output discipline
- Keep conclusions decisive and risk-aware.
- Separate business quality, balance-sheet safety, and valuation.
- Never fabricate missing metrics; mark `NA`.
