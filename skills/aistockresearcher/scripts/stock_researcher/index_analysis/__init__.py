"""Index analysis"""
from .indices import IndexAnalyzer
from .global_trends import (
    GLOBAL_INDEX_UNIVERSE,
    COMMODITY_ALIASES,
    fetch_index_data,
    fetch_kline,
    fetch_quote,
    fetch_batch_quotes,
    analyze_index,
    global_market_outlook,
    index_forecast,
    sector_trend_report,
)

__all__ = [
    "IndexAnalyzer",
    "GLOBAL_INDEX_UNIVERSE",
    "COMMODITY_ALIASES",
    "fetch_index_data",
    "fetch_kline",
    "fetch_quote",
    "fetch_batch_quotes",
    "analyze_index",
    "global_market_outlook",
    "index_forecast",
    "sector_trend_report",
]
