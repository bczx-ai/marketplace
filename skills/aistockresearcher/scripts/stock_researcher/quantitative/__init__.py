# -*- coding: utf-8 -*-
"""
量化模型模块
Quantitative Models Module

基于 QuantConnect Lean 架构的A股量化模型：
- Alpha模型：信号生成
- Risk模型：风险管理
- Portfolio模型：组合构建
- 技术指标：技术分析
- GARCH模型：波动率预测 (v2.1.0 新增)
- 因子分析：A股多因子评分 (v2.1.0 新增)
- 配对交易：协整统计套利 (v2.1.0 新增)
- ML预测：机器学习涨跌方向预测 (v2.1.0 新增)

适配A股市场数据源（东方财富/腾讯财经/同花顺/mootdx）
"""

from .alpha_models import (
    DualThrustAlpha,
    RateOfChangeAlpha,
    MeanReversionAlpha,
    MomentumAlpha,
    ValueInvestingAlpha,
)
from .risk_models import (
    MaximumDrawdownRiskModel,
    StopLossRiskModel,
    TargetProfitRiskModel,
)
from .portfolio_models import (
    EqualWeightPortfolio,
    RiskParityPortfolio,
    ValueWeightedPortfolio,
)
from .indicators import (
    QuantIndicators,
    BollingerBands,
    MACD,
    RSI,
    ADX,
    HurstIndex,
)
from .engine import QuantitativeEngine

# v2.1.0 新增量化工具 — 可选依赖，按需导入
# (numpy/scipy/statsmodels/arch/sklearn 可能未安装)
GarchForecaster = GarchResult = None
FactorAnalyzer = FactorScore = StockFactorReport = None
PairsTrader = PairResult = None
MLPredictor = FeatureEngineer = MLPrediction = None
GoldAnalyzer = GoldSignal = None
FuturesAnalyzer = FuturesSignal = None

try:
    from .garch_model import GarchForecaster, GarchResult
except ImportError:
    pass

try:
    from .factor_analysis import FactorAnalyzer, FactorScore, StockFactorReport
except ImportError:
    pass

try:
    from .pairs_trading import PairsTrader, PairResult
except ImportError:
    pass

try:
    from .ml_predictor import MLPredictor, FeatureEngineer, MLPrediction
except ImportError:
    pass

# v4.4 新增：商品/黄金 + 期货量化分析
try:
    from .commodity_analyzer import GoldAnalyzer, GoldSignal, analyze_gold
except ImportError:
    pass

try:
    from .futures_analyzer import FuturesAnalyzer, FuturesSignal, analyze_futures
except ImportError:
    pass

__all__ = [
    # Alpha模型
    "DualThrustAlpha", "RateOfChangeAlpha", "MeanReversionAlpha",
    "MomentumAlpha", "ValueInvestingAlpha",
    # 风险模型
    "MaximumDrawdownRiskModel", "StopLossRiskModel", "TargetProfitRiskModel",
    # 组合模型
    "EqualWeightPortfolio", "RiskParityPortfolio", "ValueWeightedPortfolio",
    # 指标
    "QuantIndicators", "BollingerBands", "MACD", "RSI", "ADX", "HurstIndex",
    # 引擎
    "QuantitativeEngine",
    # v2.1.0
    "GarchForecaster", "GarchResult",
    "FactorAnalyzer", "FactorScore", "StockFactorReport",
    "PairsTrader", "PairResult",
    "MLPredictor", "FeatureEngineer", "MLPrediction",
    # v4.4 商品/期货
    "GoldAnalyzer", "GoldSignal", "analyze_gold",
    "FuturesAnalyzer", "FuturesSignal", "analyze_futures",
]
