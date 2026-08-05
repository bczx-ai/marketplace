# 📊 Market Sentiment — 市场情绪分析器

基于**四维度市场情绪评估模型**的大盘环境诊断工具。分析全市场情绪指标并输出市场状态，可与 stock-planner 集成。

## 快速开始

```bash
# 分析市场情绪
python3 scripts/sentiment.py analyze --file market_data.csv

# 评分明细
python3 scripts/sentiment.py score --file market_data.csv

# 多日趋势
python3 scripts/sentiment.py trend --file market_data.csv

# 一句话摘要
python3 scripts/sentiment.py summary --file market_data.csv
```

## 输入格式

支持包含以下字段的 CSV 文件（列名自动识别中英文）：

| 数据 | 可识别的列名 |
|------|-------------|
| 日期 | date, 日期, trade_date |
| 指数涨跌幅 | change_pct, change, 涨跌幅 |
| 涨停家数 | close_limit_up, limit_up, 涨停 |
| 跌停家数 | close_limit_down, limit_down, 跌停 |
| 上涨家数 | advance_count, advance, 上涨 |
| 下跌家数 | decline_count, decline, 下跌 |
| 成交额 | amount, turnover, 成交额 |
| 成交量 | volume, vol, 成交量 |
| 高于MA20 | above_ma20, above_ma20_pct, 高于MA20 |
| 52周新高 | new_high, new_52w_high, 新高 |
| 52周新低 | new_low, new_52w_low, 新低 |
| 平均涨跌 | avg_change, avg_pct, 平均涨跌 |

## 输出

```json
{
  "date": "2026-07-19",
  "total_score": 42,
  "level": "weak",
  "signal": "市场情绪偏弱，建议控制仓位",
  "dimensions": {
    "emotion": {"score": 12, "max": 30, "detail": "涨停占比35%, 涨跌比38%"},
    "trend":  {"score": 15, "max": 30, "detail": "沪深300 -1.2%, 偏离均线-3.5%"},
    "volume": {"score": 8,  "max": 20, "detail": "量比0.7, 缩量"},
    "breadth": {"score": 7,  "max": 20, "detail": "高于MA20占比28%, 新高/新低=0.3"}
  },
  "market_state": "weak",
  "planner_param": "weak",
  "suggested_position": "减仓至5只，止损收紧至6%",
  "suggested_threshold": 7.0
}
```

## 与 stock-planner 集成

```bash
# 分析市场情绪后，将 market 参数传给 planner
python3 scripts/stock_planner.py --plan --market \
  $(python3 scripts/sentiment.py summary --file market_data.csv | grep 'planner' | awk '{print $NF}')
```

## 依赖

- Python 3.8+
- 纯标准库，无外部依赖

## 法律声明

本工具仅供辅助参考，不构成任何投资建议。市场有风险，投资需谨慎。
