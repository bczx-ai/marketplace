---
name: market-sentiment
displayName: "Market Sentiment"
description: "基于四个维度对市场情绪进行0–100评分，提供市场状态和交易建议。"
version: "1.0.0"
tags:
  - data_analysis
license: "Unknown"
---

# 📊 Market Sentiment — 市场情绪分析器

基于**四维度市场情绪评估模型**，对大盘环境进行诊断分析，输出 0–100 综合评分及对应的市场状态。

## 核心功能

- **analyze** — 综合情绪分析（含评分、状态、操作建议）
- **score** — 评分明细（四维度 + ASCII 条形图）
- **trend** — 多日趋势追踪
- **summary** — 一句话市场诊断

## 四维度模型

| 维度 | 满分 | 说明 |
|------|------|------|
| 情绪极端度 | 30 | 涨停/跌停比、涨跌比、连板效应 |
| 趋势极端度 | 30 | 指数涨跌幅、MA20 偏离、平均涨跌 |
| 量能极端度 | 20 | 量比、成交额变化 |
| 宽度极端度 | 20 | MA20 占比、新高/新低比、大小盘分化 |

## 状态映射

| 评分 | 状态 | planner 参数 |
|------|------|-------------|
| ≥ 75 | 超买 (overbought) | bear |
| 65–74 | 偏强 (strong) | strong |
| 45–64 | 中性 (neutral) | oscillate |
| 30–44 | 偏弱 (weak) | weak |
| < 30 | 超卖 (oversold) | moderate |

## 集成工作流

```bash
# 1. 分析市场情绪
python3 scripts/sentiment.py analyze --file market_data.csv

# 2. 获取市场参数，传给 stock-planner
python3 scripts/stock_planner.py --plan \
  --market $(python3 scripts/sentiment.py summary --file market_data.csv | grep 'planner' | awk '{print $NF}')
```

## 触发关键词

市场情绪、大盘环境、sentiment、market context、情绪分析、大盘诊断、market state、overbought、oversold、市场状态

## 法律免责声明

本工具仅供辅助参考，不构成任何投资建议。市场有风险，投资需谨慎。
作者和贡献者不对因使用本工具产生的任何损失承担责任。
