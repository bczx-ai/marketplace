---
name: yahoo-data-fetcher
displayName: "yahoo fetch data of stonks"
description: "从雅虎财经获取实时股票报价。"
version: "1.0.2"
tags:
  - data_analysis
license: "Unknown"
---

# Yahoo Data Fetcher – Stock Quote

Get current stock price data from Yahoo Finance.

This skill fetches the latest market quote for one or more stock symbols and returns normalized JSON output.

---

## Command

### `/stock quote`

Fetch the latest quote for one or more stock symbols.

---

## Input

- `symbols` (string or array of strings)

Examples:
- `"AAPL"`
- `"AAPL MSFT TSLA"`
- `"AAPL,MSFT,TSLA"`
- `["AAPL", "MSFT"]`
- `{ "symbols": ["AAPL", "MSFT"] }`

---

## Output

For each symbol:

- `symbol` – stock ticker
- `price` – latest market price
- `change` – absolute price change
- `changePercent` – percentage change
- `currency` – trading currency
- `marketState` – market status (e.g. `REGULAR`, `CLOSED`)

Example output:

```json
[
  {
    "symbol": "AAPL",
    "price": 189.12,
    "change": 1.23,
    "changePercent": 0.65,
    "currency": "USD",
    "marketState": "REGULAR"
  }
]