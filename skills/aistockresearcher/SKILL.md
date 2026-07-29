---
name: aistockresearcher
displayName: "股票、基金与期货量化分析（含舆情分析）"
description: "全球智能投研工具 v7.0 — 覆盖12个全球市场（A股/港股/美股/日韩英德法澳印台加），\n零依赖核心。股票/基金/指数/板块/商品多周期量化预测，政策解读+舆情监控+论坛情绪，\n价值投资框架，黄金/商品期货分析。\n\n数据源：腾讯财经+东方财富+新浪财经，免费无Key，国内直连。\n\n触发词：股票、基金、行情、分析、预测、涨跌、指数、板块、商品、黄金、全球市场、\n量化、技术指标、K线、持仓、筛选、港美股、日经、标普、纳斯达克、政策解读、\n舆情、情绪、研报、回测、价值投资、蒙特卡洛、VaR、Sharpe、板块轮动"
version: 1.0.26
tags:
  - business_operations
license: "Unknown"
---

# 股票研究员 v7.0 — Agent 指南

> 纯 Python 标准库，零 pip install。覆盖 12 个全球市场 + 黄金/商品期货。

## 全局代码格式

| 市场 | 格式 | 示例 |
|------|------|------|
| A股 | 6位数字 / cn:xxx | `600519` `cn:600519` |
| 港股 | hk:xxxxx / xxxxx.HK | `hk:00700` `00700.HK` |
| 美股 | us:XXXX / XXXX.US | `us:AAPL` `AAPL.US` |
| 全球指数 | idx:代码 | `idx:N225` `idx:SPX` `idx:上证指数` |
| 黄金 | gold:comex / gold:sh | COMEX黄金 / 沪金 |
| 白银 | silver:comex / silver:sh | COMEX白银 / 沪银 |
| 原油 | crude:wti | WTI原油 |
| 期货 | fut:代码 | `fut:aum` `fut:agm` |
| 海外个股 | jp:7203 / kr:005930 | 日韩（覆盖有限，不可用时降级为指数） |

## 零依赖 CLI 预测

```bash
# 单股预测（12项技术指标 + 蒙特卡洛模拟 + 七维评分）
python scripts/stock_predict.py <代码>          # 标准输出
python scripts/stock_predict.py <代码> --json   # JSON 输出（Agent 友好）
python scripts/stock_predict.py <代码> --simple # 简洁单行
python scripts/stock_predict.py <代码> --quick  # 快速模式（跳过蒙特卡洛，适合批量）

# 批量多市场
python scripts/stock_predict.py "600519,hk:00700,us:AAPL,idx:N225,gold:comex"

# 离线自检
python scripts/stock_predict.py --test
```

## 核心模块 API

### 多周期融合预测（10维信号，1d~6M）
```python
from stock_researcher.fusion import MultiHorizonForecaster
fc = MultiHorizonForecaster()
result = fc.forecast_stock("600519")          # 个股
result = fc.forecast_asset("100.N225", asset_type="index")  # 指数
# result.horizons["1d"/"3d"/"5d"/"1M"/"3M"/"6M"] 各有 direction/predicted_pct/confidence/narrative
```

### 指数趋势预测（19个全球指数）
```python
from stock_researcher.index_analysis.index_forecast import IndexForecaster, list_global_indices
fc = IndexForecaster()
result = fc.forecast("sh000001", horizons=["1M","3M","6M"])
print(fc.format_report(result))
```

### 板块趋势预测 + 排名
```python
from stock_researcher.sector_analysis.sector_forecast import SectorForecaster
fc = SectorForecaster()
result = fc.forecast("新能源", market="cn")       # 单板块
ranking = fc.rank_sectors(market="cn", horizon="1M", top_n=10)  # 排名
```

### 基金量化分析
```python
from pkg.fund_analyzer import score_fund_v4, predict_fund_short_term, compare_funds_v2
from stock_researcher.funds.fund_sentiment import analyze_fund_sentiment

result = score_fund_v4("110022")               # 十维评分
pred = predict_fund_short_term("110022")        # T+1/3/5 预判
sentiment = analyze_fund_sentiment("110022")    # 舆情
compare = compare_funds_v2(["02800","02823"])   # 对比排名（支持港股基金）
```

### 价值投资框架（6模块加权）
```python
from stock_researcher.value_investing import ValueInvestingDecision
report = ValueInvestingDecision().analyze('600519')
print(ValueInvestingDecision.format_report(report))
# 模块: DCF估值25% + 护城河20%(7维) + 财务健康15%(Altman Z+Piotroski+Beneish)
#       + 管理层15%(6维) + 行业分析15%(Porter五力+HHI) + 量化因子10%
```

### 投资筛选引擎
```python
from stock_researcher.screening import UnifiedScreener, PRESETS
screener = UnifiedScreener()
# 自定义条件
results = screener.screen_stocks({"pe_max": 20, "roe_min": 15}, market="cn")
# 预设策略: PRESETS["graham_value"] / "garp" / "dividend" / "momentum" / "quality" / "turnaround"
```

### 舆情监控（新闻+论坛+情绪）
```python
from stock_researcher.sentiment import UnifiedSentimentEngine
engine = UnifiedSentimentEngine()
report = engine.analyze_stock("00700", market="hk")
# report["label"]: 积极/中性/消极, report["score"]: 0~100
# report["good_news"]/["bad_news"], report["risk_flags"]
```

### 政策解读
```python
from stock_researcher.policy import PolicyAnalyzer
pa = PolicyAnalyzer()
impact = pa.analyze_market_impact("cn")         # 市场级
sector = pa.analyze_sector_impact("新能源","cn") # 板块级
```

### 黄金/商品期货
```python
from stock_researcher.data.global_market import analyze_gold_factors
gold = analyze_gold_factors()
# gold["score"]: -100~+100, gold["signal"], gold["factors"]
```

### 大师 Agent
```python
from stock_researcher.agents import BuffettAgent, GrahamAgent, LynchAgent
```

### 回测 + 进化学习
```python
from stock_researcher.evolution import BacktestEngine
engine = BacktestEngine("00700", market="hk")
print(engine.run_and_report())
```

## 重要约束

| 约束 | 说明 |
|------|------|
| 零依赖核心 | 纯 Python 标准库，无需 pip install（量化引擎可选 numpy） |
| 不构成投资建议 | 只输出数据和分析，买卖决策由用户自行负责 |
| 数据延迟 | 腾讯/东财接口 ~3-5s，非交易时段为收盘价 |
| 开代理失败 | 数据源需国内直连，**开启代理反而会失败** |
| 评分含义 | 预测评分 = 历史统计概率，非确定性预测 |
| 海外个股限制 | 非中美港股覆盖有限（东财免费API限制），指数/商品不受限 |

## 目录速查

```
stock-researcher/
├── SKILL.md / README.md
├── scripts/
│   ├── stock_predict.py          # ★ CLI 预测引擎（零依赖，可直接运行）
│   └── stock_researcher/         # 核心模块库
│       ├── core/                 # 技术分析 + 估值 + 预测引擎
│       ├── data/                 # 多市场数据层 + 缓存
│       │   ├── global_market.py  # 全球市场 + 黄金 + 风险偏好
│       │   └── market_classifier.py  # 全球代码识别 + 路由
│       ├── fusion/               # 多周期融合预测（10维信号）
│       ├── index_analysis/       # 指数分析 + 预测
│       ├── sector_analysis/      # 板块分析 + 轮动 + 排名
│       ├── policy/               # 政策解读
│       ├── funds/                # 基金舆情
│       ├── sentiment/            # 舆情监控
│       ├── value_investing/      # 价值投资（6模块）
│       ├── screening/            # 筛选引擎（6套预设）
│       ├── evolution/            # 回测 + 进化
│       ├── agents/               # 大师Agent（巴菲特等）
│       ├── quantitative/         # 量化引擎（可选numpy）
│       ├── recommendation/       # 投资推荐
│       ├── tracker/              # 持仓跟踪 + 预警
│       ├── advisor/              # 用户画像 + 组合分析
│       ├── research/             # 宏观信号 + 券商研报
│       └── report/               # 报告生成
├── pkg/
│   ├── crawl_utils.py            # 零依赖 HTTP 工具
│   └── fund_analyzer.py          # 基金量化引擎
├── config/                       # 配置
└── tests/                        # 46 个测试
```

## 免责声明

> ⚠️ 本工具仅供学习参考，不构成任何形式的投资建议。股市有风险，投资需谨慎。
