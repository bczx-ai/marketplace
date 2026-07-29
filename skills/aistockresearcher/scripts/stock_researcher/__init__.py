"""
全球智能投研模块 v7.0
Professional Global Investment Research Module

覆盖12个全球主流市场 + 黄金/商品期货。
纯 Python 标准库核心，零 pip install。
"""
import sys
sys.dont_write_bytecode = True

from .core.analyzer import StockResearcher

# v7.0 新模块导出
from .data.market_classifier import MarketClassifier, detect_market, normalize_code
from .data.global_market import (
    fetch_global_quote, fetch_global_kline,
    get_global_risk_appetite, analyze_gold_factors,
    get_market_correlation, GLOBAL_INDICES, GLOBAL_MARKETS,
)

__all__ = [
    "StockResearcher",
    "MarketClassifier", "detect_market", "normalize_code",
    "fetch_global_quote", "fetch_global_kline",
    "get_global_risk_appetite", "analyze_gold_factors",
    "get_market_correlation", "GLOBAL_INDICES", "GLOBAL_MARKETS",
]
__version__ = "7.0.0"