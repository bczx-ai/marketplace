#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一分析调度器
Stock Researcher - Unified Analysis Engine
"""

import time
from typing import Dict, List, Optional
from dataclasses import dataclass

from .technical import TechnicalAnalyzer, TechnicalIndicators
from .valuation import ValuationAnalyzer, ValuationMetrics
from .prediction_engine import ThreeDimensionPredictionEngine, ThreeDimensionPrediction

from ..agents.buffett import BuffettAnalyzer, BuffettAnalysis
from ..agents.graham import GrahamAnalyzer, GrahamAnalysis
from ..agents.lynch import LynchAnalyzer, LynchAnalysis
from ..agents.technical import TechnicalAgent, TechnicalAgentResult
from ..agents.sentiment import SentimentAnalyzer, SentimentResult

from ..data.market import MarketData
from ..data.fundamental import FundamentalData
from ..data.money_flow import MoneyFlowData
from ..data.news import NewsData
from ..data.macro import MacroData

from ..report.generator import ReportGenerator
from ..tracker.portfolio import PortfolioTracker
from ..tracker.alerts import AlertSystem
from ..tracker.monitor import StockMonitor

from ..index_analysis.indices import IndexAnalyzer, IndexResult
from ..sector_analysis.sectors import SectorAnalyzer, SectorResult
from ..industry_chain import IndustryChainAnalyzer, AShareChainAnalyzer, ChainAnalysisResult


@dataclass
class StockAnalysisResult:
    """股票分析完整结果"""
    code: str
    name: str
    date: str

    # 行情数据
    price: float = 0
    change_pct: float = 0

    # 技术分析
    technical: Optional[TechnicalIndicators] = None

    # 估值分析
    valuation: Optional[ValuationMetrics] = None

    # 基本面
    fundamentals: Dict = None

    # 资金流向
    money_flow: Dict = None

    # 新闻舆情
    sentiment: Optional[SentimentResult] = None

    # 投资大师分析
    buffett: Optional[BuffettAnalysis] = None
    graham: Optional[GrahamAnalysis] = None
    lynch: Optional[LynchAnalysis] = None

    # 三维预测
    prediction: Optional[ThreeDimensionPrediction] = None


class StockResearcher:
    """
    专业股票研究员

    功能：
    1. 完整股票分析（技术/估值/基本面/资金/情绪）
    2. 三维预测（情绪/估值/历史案例/技术）
    3. 投资大师分析（巴菲特/格雷厄姆/林奇）
    4. 短/中/长期报告生成
    5. 股票跟踪与提醒
    6. 指数分析
    7. 板块分析
    """

    def __init__(self, data_dir: str = None):
        # 数据层
        self.market = MarketData()
        self.fundamental = FundamentalData()
        self.money_flow_data = MoneyFlowData()
        self.news_data = NewsData()
        self.macro_data = MacroData()

        # 分析引擎
        self.tech_analyzer = TechnicalAnalyzer()
        self.val_analyzer = ValuationAnalyzer()
        self.prediction_engine = ThreeDimensionPredictionEngine()

        # 投资大师Agent
        self.buffett_analyzer = BuffettAnalyzer()
        self.graham_analyzer = GrahamAnalyzer()
        self.lynch_analyzer = LynchAnalyzer()
        self.technical_agent = TechnicalAgent()
        self.sentiment_analyzer = SentimentAnalyzer()

        # 报告生成器
        self.report_gen = ReportGenerator(data_dir)

        # 跟踪器
        self.tracker = PortfolioTracker(data_dir)
        self.alert_system = AlertSystem(data_dir)
        self.monitor = StockMonitor(data_dir)

        # 指数分析器
        self.index_analyzer = IndexAnalyzer()

        # 板块分析器
        self.sector_analyzer = SectorAnalyzer()

        # 产业链分析器
        self.chain_analyzer = IndustryChainAnalyzer()
        self.ashare_chain_analyzer = AShareChainAnalyzer()

    @staticmethod
    def _estimate_percentile(value: float, metric: str) -> float:
        """估算 PE/PB 历史分位（经验值映射）

        A股常见估值区间的大致分位映射：
        - PE: <15 低估值(~20%), 15-25 合理(~50%), 25-40 偏高(~70%), >40 高估(~90%)
        - PB: <1.5 低(~20%), 1.5-3 合理(~50%), 3-6 偏高(~70%), >6 高估(~90%)
        """
        if value <= 0:
            return 50  # 无效数据返回中性值

        if metric == "pe":
            if value < 10:
                return 10
            elif value < 15:
                return 20 + (value - 10) / 5 * 10
            elif value < 25:
                return 30 + (value - 15) / 10 * 20
            elif value < 40:
                return 50 + (value - 25) / 15 * 20
            elif value < 60:
                return 70 + (value - 40) / 20 * 15
            else:
                return min(95, 85 + (value - 60) / 40 * 10)
        elif metric == "pb":
            if value < 1:
                return 10
            elif value < 1.5:
                return 20 + (value - 1) / 0.5 * 10
            elif value < 3:
                return 30 + (value - 1.5) / 1.5 * 20
            elif value < 6:
                return 50 + (value - 3) / 3 * 20
            else:
                return min(95, 70 + (value - 6) / 4 * 25)
        return 50

    def analyze_stock(self, code: str, period: str = "short") -> StockAnalysisResult:
        """
        综合分析股票

        Args:
            code: 股票代码
            period: 报告周期 short/medium/long

        Returns:
            StockAnalysisResult
        """
        code = str(code).zfill(6)

        # 1. 获取行情数据
        rt_data = self.market.fetch_realtime([code])
        if code not in rt_data:
            raise ValueError(f"无法获取股票行情: {code}")

        stock_rt = rt_data[code]
        name = stock_rt.get("name", code)
        price = stock_rt.get("price", 0)
        change_pct = stock_rt.get("change_pct", 0)

        # 2. 获取历史数据用于技术分析
        kline = self.market.fetch_history(code, days=250)
        closes = kline.get("closes", []) if kline else []
        highs = kline.get("highs", []) if kline else []
        lows = kline.get("lows", []) if kline else []

        # 3. 技术分析
        tech = None
        if len(closes) >= 20:
            tech = self.tech_analyzer.analyze(code, closes, highs, lows)

        # 4. 资金流向
        money_flow = self.money_flow_data.get_money_flow([code]).get(code, {})

        # 5. 新闻舆情
        news_list = self.news_data.fetch_stock_news(code, limit=20)
        sentiment_data = self.news_data.analyze_news_sentiment(news_list)

        # 6. 估值数据（从API获取）
        val_raw = self.fundamental.get_valuation(code)
        fin_summary = self.fundamental.get_financial_summary(code)
        pe_val = val_raw.get("pe", 0) or 0
        pb_val = val_raw.get("pb", 0) or 0
        # 估算 PE/PB 历史分位（简化：用经验值映射）
        pe_pctl = self._estimate_percentile(pe_val, "pe")
        pb_pctl = self._estimate_percentile(pb_val, "pb")
        val = ValuationMetrics(
            pe=pe_val,
            pb=pb_val,
            pe_percentile=pe_pctl,
            pb_percentile=pb_pctl,
        )

        # 计算同类股票历史收益率（从收盘价推算）
        similar_returns = []
        if len(closes) >= 61:
            similar_returns = [
                (closes[i] - closes[i-1]) / closes[i-1] * 100
                for i in range(-60, 0)
            ]
        elif len(closes) >= 2:
            similar_returns = [
                (closes[i] - closes[i-1]) / closes[i-1] * 100
                for i in range(1, len(closes))
            ]

        # 7. 三维预测
        prediction = self.prediction_engine.predict_with_factors(
            news_sentiment=sentiment_data.get("score", 0) / 100,
            money_flow=money_flow.get("score", 0),
            change_pct=change_pct,
            pe_percentile=val.pe_percentile,
            pb_percentile=val.pb_percentile,
            similar_returns=similar_returns,
            tech_score=tech.tech_score if tech else 0,
            ma_status=tech.ma_arrangement if tech else "混乱",
            rsi=tech.rsi14 if tech else 50,
            macd_hist=tech.macd_hist if tech else 0
        )

        return StockAnalysisResult(
            code=code,
            name=name,
            date=time.strftime("%Y-%m-%d"),
            price=price,
            change_pct=change_pct,
            technical=tech,
            valuation=val,
            fundamentals=fin_summary,
            money_flow=money_flow,
            sentiment=SentimentResult(
                news_score=sentiment_data.get("score", 0),
                news_positive=sentiment_data.get("positive", 0),
                news_negative=sentiment_data.get("negative", 0),
                news_neutral=sentiment_data.get("neutral", 0),
                sentiment_score=sentiment_data.get("score", 0),
                sentiment_label=sentiment_data.get("overall", "中性")
            ),
            prediction=prediction
        )

    def generate_report(self, code: str, period: str = "short") -> str:
        """
        生成研究报告

        Args:
            code: 股票代码
            period: short/medium/long

        Returns:
            str: 报告文件路径
        """
        result = self.analyze_stock(code, period)

        stock_data = {
            "code": result.code,
            "name": result.name,
            "price": result.price,
            "change_pct": result.change_pct
        }

        tech_data = {}
        if result.technical:
            tech_data = {
                "ma5": result.technical.ma5,
                "ma10": result.technical.ma10,
                "ma20": result.technical.ma20,
                "ma60": result.technical.ma60,
                "rsi14": result.technical.rsi14,
                "macd_hist": result.technical.macd_hist,
                "ma_arrangement": result.technical.ma_arrangement,
                "tech_score": result.technical.tech_score,
                "tech_signal": result.technical.tech_signal
            }

        if period == "short":
            return self.report_gen.generate_short_report(
                stock_data=stock_data,
                tech_data=tech_data,
                money_data=result.money_flow or {},
                sentiment_data={
                    "sentiment_label": result.sentiment.sentiment_label if result.sentiment else "中性",
                    "sentiment_score": result.sentiment.sentiment_score if result.sentiment else 0,
                    "news_positive": result.sentiment.news_positive if result.sentiment else 0,
                    "news_negative": result.sentiment.news_negative if result.sentiment else 0,
                },
                prediction={
                    "short_term": result.prediction.short_term if result.prediction else None,
                    "medium_term": result.prediction.medium_term if result.prediction else None,
                    "long_term": result.prediction.long_term if result.prediction else None,
                }
            )
        elif period == "medium":
            val_data = {}
            if result.valuation:
                val_data = {
                    "pe": result.valuation.pe,
                    "pb": result.valuation.pb,
                    "pe_percentile": result.valuation.pe_percentile,
                    "pb_percentile": result.valuation.pb_percentile,
                    "val_signal": result.valuation.val_signal,
                    "valuation_state": result.valuation.valuation_state,
                    "graham_number": result.valuation.graham_number
                }

            return self.report_gen.generate_medium_report(
                stock_data=stock_data,
                tech_data=tech_data,
                val_data=val_data,
                fundamental_data=result.fundamentals or {},
                prediction={
                    "short_term": result.prediction.short_term if result.prediction else None,
                    "medium_term": result.prediction.medium_term if result.prediction else None,
                    "long_term": result.prediction.long_term if result.prediction else None,
                }
            )
        else:  # long
            fund = result.fundamentals or {}
            roe_val = fund.get("roe", 0) or 0
            eps_val = fund.get("eps", 0) or 0
            bvps_val = fund.get("bvps", 0) or 0
            revenue_val = fund.get("revenue", 0) or 0
            net_profit_val = fund.get("net_profit", 0) or 0
            operating_margin_val = fund.get("operating_margin", 0) or 0
            debt_ratio_val = fund.get("debt_ratio", 0) or 0
            pe_val = result.valuation.pe if result.valuation else 0

            # 巴菲特分析
            buffett_result = self.buffett_analyzer.analyze(
                roe=roe_val,
                net_income=net_profit_val,
                total_assets=fund.get("total_assets", 0) or 0,
                revenue=revenue_val,
                operating_margin=operating_margin_val,
                shares_outstanding=0,
                price=result.price,
                bvps=bvps_val,
            )
            buffett_dict = {
                "roe": buffett_result.roe,
                "operating_margin": buffett_result.operating_margin,
                "moat_score": buffett_result.moat_score,
                "intrinsic_value": buffett_result.intrinsic_value,
                "margin_of_safety": buffett_result.margin_of_safety,
                "buffett_score": buffett_result.buffett_score,
                "signal": buffett_result.signal,
            }

            # 格雷厄姆分析
            graham_result = self.graham_analyzer.analyze(
                eps_history=[eps_val],
                current_ratio=2.0,  # 简化
                total_assets=fund.get("total_assets", 0) or 0,
                total_liabilities=fund.get("total_assets", 0) * debt_ratio_val / 100 if fund.get("total_assets") else 0,
                current_assets=fund.get("current_assets", 0) or 0,
                bvps=bvps_val,
                price=result.price,
            )
            graham_dict = {
                "graham_number": graham_result.graham_number,
                "ncav": graham_result.ncav,
                "current_ratio": graham_result.current_ratio,
                "debt_ratio": graham_result.debt_ratio,
                "margin_of_safety": graham_result.margin_of_safety,
                "graham_score": graham_result.graham_score,
            }

            # 林奇分析
            lynch_result = self.lynch_analyzer.analyze(
                revenue_history=[revenue_val],
                eps_history=[eps_val],
                pe=pe_val,
                price=result.price,
                bvps=bvps_val,
                total_debt=fund.get("total_assets", 0) * debt_ratio_val / 100 if fund.get("total_assets") else 0,
                total_assets=fund.get("total_assets", 0) or 0,
                operating_margin=operating_margin_val,
            )
            lynch_dict = {
                "revenue_growth": lynch_result.revenue_growth,
                "eps_growth": lynch_result.eps_growth,
                "cagr": lynch_result.cagr,
                "peg": lynch_result.peg,
                "debt_ratio": lynch_result.debt_ratio,
                "lynch_score": lynch_result.lynch_score,
            }

            # v5.0 新增：价值投资决策整合分析
            value_investing_dict = {}
            try:
                from stock_researcher.value_investing import ValueInvestingDecision
                vi_decision = ValueInvestingDecision()
                vi_report = vi_decision.analyze(code)
                value_investing_dict = {
                    "verdict": vi_report.verdict,
                    "weighted_score": vi_report.weighted_score,
                    "confidence": vi_report.confidence,
                    "fair_value_range": list(vi_report.fair_value_range),
                    "margin_of_safety": vi_report.margin_of_safety,
                    "breakdown": vi_report.breakdown,
                    "strengths": vi_report.strengths,
                    "risks": vi_report.risks,
                    "catalysts": vi_report.catalysts,
                    "narrative": vi_report.narrative,
                }
            except Exception as e:
                value_investing_dict = {"error": f"价值投资分析失败: {e}"}

            return self.report_gen.generate_long_report(
                stock_data=stock_data,
                fundamental_data=fund,
                buffett_analysis=buffett_dict,
                graham_analysis=graham_dict,
                lynch_analysis=lynch_dict,
                value_investing=value_investing_dict,  # v5.0 新增
                prediction={
                    "short_term": result.prediction.short_term if result.prediction else None,
                    "medium_term": result.prediction.medium_term if result.prediction else None,
                    "long_term": result.prediction.long_term if result.prediction else None,
                }
            )

    def analyze_index(self, index_code: str = None) -> List[IndexResult]:
        """
        分析指数

        Args:
            index_code: 指数代码，如不指定则分析所有

        Returns:
            List[IndexResult]
        """
        if index_code:
            return [self.index_analyzer.analyze_index(index_code)]
        return self.index_analyzer.analyze_all()

    def analyze_sector(self, sector_name: str = None) -> List[SectorResult]:
        """
        分析板块

        Args:
            sector_name: 板块名称，如不指定则分析所有

        Returns:
            List[SectorResult]
        """
        if sector_name:
            return [self.sector_analyzer.analyze_sector(sector_name)]
        return self.sector_analyzer.get_sector_ranking()

    def track_stock(self, code: str, name: str = None, cost: float = None,
                    shares: float = None, stop_loss: float = None,
                    take_profit: float = None) -> bool:
        """
        添加跟踪股票

        Args:
            code: 股票代码
            name: 股票名称
            cost: 持仓成本
            shares: 持仓数量
            stop_loss: 止损价
            take_profit: 止盈价

        Returns:
            bool
        """
        return self.tracker.add_stock(code, name, cost, shares, stop_loss, take_profit)

    def check_tracking(self) -> Dict:
        """
        检查跟踪股票

        Returns:
            Dict: 检查结果
        """
        return self.monitor.run_and_report()

    def get_tracked_summary(self) -> Dict:
        """获取跟踪汇总"""
        return self.tracker.get_tracking_summary()

    def analyze_industry_chain(self, industry: str, mode: str = "general") -> ChainAnalysisResult:
        """
        产业链分析

        Args:
            industry: 产业链名称
            mode: general(通用) / ashare(A股专版)

        Returns:
            ChainAnalysisResult
        """
        from ..industry_chain import get_preset_chain

        preset = get_preset_chain(industry)
        if not preset:
            raise ValueError(f"未找到预设产业链: {industry}")

        if mode == "ashare":
            nodes = self.ashare_chain_analyzer.build_chain_map(
                industry,
                [{"name": n, "participation": "🟡"} for n in preset["upstream"]],
                [{"name": n, "participation": "🟡"} for n in preset["midstream"]],
                [{"name": n, "participation": "🟡"} for n in preset["downstream"]]
            )
            return self.ashare_chain_analyzer.analyze(industry, nodes)
        else:
            nodes = self.chain_analyzer.build_chain_map(
                industry, preset["upstream"], preset["midstream"], preset["downstream"]
            )
            return self.chain_analyzer.analyze(industry, nodes)