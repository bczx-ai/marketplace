---
name: finance-radar
displayName: "Finance Radar"
description: "基于Yahoo Finance数据，提供股票与加密货币分析，适用于用户需要：①分析股票或加密货币价格及基本面；②追踪投资..."
version: 1.1.0
tags:
  - business_operations
license: "Unknown"
---

# Finance Radar

Stock & crypto intelligence via Yahoo Finance. Charges 0.001 USDT/call via SkillPay.

## Commands

| Command | Script | Description |
|:---|:---|:---|
| **analyze** | `scripts/analyze.py` | Stock/crypto analysis (price, fundamentals, technicals) |
| **score** | `scripts/score.py` | 8-dimension stock scoring |
| **batch** | `scripts/batch.py` | Batch analyze multiple tickers + CSV export |
| **portfolio** | `scripts/portfolio.py` | Portfolio tracking & P/L |
| **watchlist** | `scripts/watchlist.py` | Watchlist with price alerts |
| **dividend** | `scripts/dividend.py` | Dividend yield & history |
| **hot-scan** | `scripts/hot_scan.py` | Viral trend detection |
| **rumor** | `scripts/rumor.py` | Rumor & early signal detection |
| **billing** | `scripts/billing.py` | SkillPay charge/balance/payment |

## Workflow

```
1. Billing:  python3 scripts/billing.py --charge --user-id <id>
2. Execute:  python3 scripts/<command>.py --ticker AAPL
```

## Quick Examples

```bash
# Analyze a stock
python3 scripts/analyze.py --ticker AAPL

# Analyze crypto
python3 scripts/analyze.py --ticker BTC-USD

# Batch analyze (NEW)
python3 scripts/batch.py --tickers AAPL,GOOG,MSFT
python3 scripts/batch.py --tickers AAPL,GOOG,MSFT --export  # Export CSV

# 8-dimension score
python3 scripts/score.py --ticker TSLA
```

## Config

| Env Var | Required | Description |
|:---|:---:|:---|
| `SKILLPAY_API_KEY` | Yes | SkillPay.me API key |

## References

See `references/scoring-model.md` for 8-dimension scoring methodology.
