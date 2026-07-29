# 股票研究员 v7.0（全球零依赖版）

> 纯 Python 标准库，零 pip install，覆盖 12 个全球市场。
> 数据源：腾讯财经 + 东方财富，免费无 Key，国内直连。

## 30 秒上手

```bash
# 1. 离线自检（确认一切就绪）
python scripts/stock_predict.py --test

# 2. 查看一只股票
python scripts/stock_predict.py 600519 --simple

# 3. 快速模式（跳过耗时计算，适合批量使用）
python scripts/stock_predict.py 600519 --simple --quick
```

## 常用命令

| 场景 | 命令 |
|------|------|
| A股单股 | `python scripts/stock_predict.py 600519` |
| 港股 | `python scripts/stock_predict.py hk:00700 --simple` |
| 美股 | `python scripts/stock_predict.py us:AAPL --simple` |
| 全球指数 | `python scripts/stock_predict.py idx:N225 --simple` |
| 黄金期货 | `python scripts/stock_predict.py gold:comex --simple` |
| 批量多市场 | `python scripts/stock_predict.py "600519,hk:00700,us:AAPL"` |
| JSON 输出 | `python scripts/stock_predict.py 600519 --json` |

## 代码格式速查

| 市场 | 格式 | 示例 |
|------|------|------|
| A股 | 6 位数字 | `600519` `cn:600519` |
| 港股 | hk: + 代码 | `hk:00700` `00700.HK` |
| 美股 | us: + 代码 | `us:AAPL` `AAPL.US` |
| 全球指数 | idx: + 指数码 | `idx:N225` `idx:SPX` `idx:上证指数` |
| 商品期货 | 品种:交易所 | `gold:comex` `crude:wti` |

## 功能速查

```python
# 价值投资分析
from stock_researcher.value_investing import ValueInvestingDecision
print(ValueInvestingDecision.format_report(ValueInvestingDecision().analyze('600519')))

# 基金十维评分
from pkg.fund_analyzer import score_fund_v4
print(score_fund_v4('110022'))

# 投资筛选（PE<20 且 ROE>15 的港股）
from stock_researcher.screening import UnifiedScreener
r = UnifiedScreener().screen_stocks({'pe_max': 20, 'roe_min': 15}, market='hk')
print(r[:5])

# 舆情监控
from stock_researcher.sentiment import UnifiedSentimentEngine
print(UnifiedSentimentEngine().analyze_stock('00700', 'hk'))

# 回测验证
from stock_researcher.evolution import BacktestEngine
print(BacktestEngine('00700', 'hk').run_and_report())
```

## 主要功能模块

| 模块 | 说明 | 依赖 |
|------|------|------|
| **stock_predict.py** | CLI 预测引擎（12项指标+蒙特卡洛+七维评分） | 零依赖 |
| **value_investing/** | DCF估值+护城河+财务健康+管理层+行业分析 | 零依赖 |
| **fund_analyzer** | 基金十维评分+VaR+风格漂移检测 | 零依赖 |
| **fusion/** | 多周期预测（1d~6M，10维信号融合） | 零依赖 |
| **screening/** | 多市场多条件筛选+6套预设策略 | 零依赖 |
| **sentiment/** | 新闻+论坛+研报舆情监控 | 零依赖 |
| **agents/** | 巴菲特/格雷厄姆/林奇大师风格分析 | 零依赖 |
| **quantitative/** | GARCH/10因子/配对交易/ML预测 | 可选 numpy |

## 重要提示

- **评分不等于预测盈利**：预测评分表示历史上相似条件下约X%的概率上涨，不保证未来
- **数据延迟**：腾讯/东财接口约 3~5 秒，非交易时段返回收盘价
- **网络**：需国内直连，**开启代理反而会失败**
- **不构成投资建议**：仅供学习参考，买卖决策自行负责
- **--quick 模式**：跳过蒙特卡洛模拟和全球风险偏好获取，速度提升约 60%

## 目录结构

```
stock-researcher/
├── SKILL.md              # Agent 触发指南
├── README.md             # 本文件
├── scripts/
│   ├── stock_predict.py  # ★ CLI 预测引擎（零依赖，可直接运行）
│   └── stock_researcher/ # ★ 核心模块库
├── pkg/                  # 基金分析 + HTTP 工具
├── config/               # 配置文件
└── tests/                # 46 个测试用例
```

## 免责声明

> ⚠️ **本工具仅供学习参考，不构成任何形式的投资建议。** 股市有风险，投资需谨慎。
