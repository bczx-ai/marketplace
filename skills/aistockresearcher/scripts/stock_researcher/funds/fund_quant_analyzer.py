# -*- coding: utf-8 -*-
"""
基金量化分析模块 v1.0
Fund Quantitative Analysis

功能：
  1. 基金绩效归因（Alpha/Beta/Sharpe/Sortino/Treynor）
  2. 持仓风格分析（大盘/小盘/价值/成长）
  3. 基金经理能力评估（选股/择时/一致性）
  4. 基金对比排名
  5. 定投回测

用法：
  from funds.fund_quant_analyzer import FundQuantAnalyzer
  fqa = FundQuantAnalyzer()
  result = fqa.analyze_fund(nav_series, benchmark_returns, risk_free_rate)
"""

import math
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class FundPerformance:
    """基金绩效分析结果"""
    fund_name: str
    total_return: float  # 总回报 %
    annual_return: float  # 年化回报 %
    annual_volatility: float  # 年化波动率 %
    max_drawdown: float  # 最大回撤 %
    sharpe_ratio: float
    sortino_ratio: float
    alpha: float  # Jensen Alpha
    beta: float
    information_ratio: float
    win_rate: float  # 月度胜率 %
    avg_win: float  # 平均盈利 %
    avg_loss: float  # 平均亏损 %
    calmar_ratio: float
    omega_ratio: float
    rating: str  # A+/A/B/C/D
    score: float  # 0~100


class FundQuantAnalyzer:
    """基金量化分析器"""

    def analyze_fund(self, nav_series: List[float],
                     benchmark_returns: List[float] = None,
                     risk_free_rate: float = 0.025,
                     fund_name: str = "未命名基金") -> FundPerformance:
        """综合基金绩效分析。

        Args:
            nav_series: 基金净值序列（日度）
            benchmark_returns: 基准日收益率序列（如沪深300）
            risk_free_rate: 无风险利率（年化），默认2.5%
            fund_name: 基金名称
        """
        if not nav_series or len(nav_series) < 60:
            return FundPerformance(fund_name, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "C", 30)

        returns = self._calc_daily_returns(nav_series)
        n = len(returns)
        rf_daily = risk_free_rate / 252

        # 1. 收益率
        total_return = (nav_series[-1] / nav_series[0] - 1) * 100
        annual_return = ((nav_series[-1] / nav_series[0]) ** (252 / n) - 1) * 100

        # 2. 风险
        annual_vol = self._annual_volatility(returns)
        max_dd = self._max_drawdown(nav_series)

        # 3. Sharpe
        excess = [r - rf_daily for r in returns]
        avg_excess = sum(excess) / n
        std_excess = (sum((e - avg_excess) ** 2 for e in excess) / (n - 1)) ** 0.5
        sharpe = (avg_excess / std_excess * math.sqrt(252)) if std_excess > 0 else 0

        # 4. Sortino
        downside = [min(0, e) ** 2 for e in excess]
        downside_std = (sum(downside) / n) ** 0.5
        sortino = (annual_return / 100 - risk_free_rate) / downside_std if downside_std > 0 else 0

        # 5. Alpha/Beta（如果有基准）
        alpha, beta, ir_ = 0, 1, 0
        if benchmark_returns and len(benchmark_returns) >= n:
            bm_rf = [b - rf_daily for b in benchmark_returns[-n:]]
            fund_rf = [r - rf_daily for r in returns]
            beta = self._calc_beta(fund_rf, bm_rf)
            alpha = self._calc_alpha(fund_rf, bm_rf, beta, rf_daily, n)
            ir_ = self._information_ratio(fund_rf, bm_rf, n)

        # 6. 胜率/盈亏比
        win_rate = sum(1 for r in returns if r > 0) / n * 100
        wins = [r for r in returns if r > 0]
        losses = [r for r in returns if r < 0]
        avg_win = sum(wins) / len(wins) * 100 if wins else 0
        avg_loss = sum(losses) / len(losses) * 100 if losses else 0

        # 7. Calmar / Omega
        calmar = annual_return / abs(max_dd) if max_dd != 0 else 0
        pos_sum = sum(r for r in returns if r > 0)
        neg_sum = abs(sum(r for r in returns if r < 0))
        omega = pos_sum / neg_sum if neg_sum > 0 else 99

        # 8. 综合评分
        score = self._calc_score(sharpe, sortino, annual_return, max_dd, alpha, calmar)
        rating = self._score_to_rating(score)

        return FundPerformance(fund_name, round(total_return, 2), round(annual_return, 2),
                               round(annual_vol * 100, 2), round(max_dd, 2),
                               round(sharpe, 2), round(sortino, 2),
                               round(alpha * 100, 2), round(beta, 2),
                               round(ir_, 2), round(win_rate, 1),
                               round(avg_win, 2), round(avg_loss, 2),
                               round(calmar, 2), round(omega, 2), rating, round(score, 1))

    def _calc_daily_returns(self, nav: List[float]) -> List[float]:
        return [(nav[i] / nav[i - 1] - 1) for i in range(1, len(nav))]

    def _annual_volatility(self, returns: List[float]) -> float:
        n = len(returns)
        avg = sum(returns) / n
        variance = sum((r - avg) ** 2 for r in returns) / (n - 1)
        return math.sqrt(variance * 252)

    def _max_drawdown(self, nav: List[float]) -> float:
        peak = nav[0]
        max_dd = 0
        for v in nav:
            if v > peak:
                peak = v
            dd = (v - peak) / peak * 100
            max_dd = min(max_dd, dd)
        return abs(max_dd)

    def _calc_beta(self, fund_rf: List[float], bm_rf: List[float]) -> float:
        n = min(len(fund_rf), len(bm_rf))
        f_avg = sum(fund_rf[:n]) / n
        b_avg = sum(bm_rf[:n]) / n
        cov = sum((fund_rf[i] - f_avg) * (bm_rf[i] - b_avg) for i in range(n)) / (n - 1)
        var = sum((b - b_avg) ** 2 for b in bm_rf[:n]) / (n - 1)
        return cov / var if var > 0 else 1

    def _calc_alpha(self, fund_rf, bm_rf, beta, rf_daily, n) -> float:
        n = min(len(fund_rf), len(bm_rf))
        f_avg = sum(fund_rf[:n]) / n
        b_avg = sum(bm_rf[:n]) / n
        return f_avg - (rf_daily + beta * (b_avg - rf_daily))

    def _information_ratio(self, fund_rf, bm_rf, n) -> float:
        n = min(len(fund_rf), len(bm_rf))
        diffs = [fund_rf[i] - bm_rf[i] for i in range(n)]
        avg_diff = sum(diffs) / n
        std_diff = (sum((d - avg_diff) ** 2 for d in diffs) / (n - 1)) ** 0.5
        return avg_diff / std_diff * math.sqrt(252) if std_diff > 0 else 0

    def _calc_score(self, sharpe: float, sortino: float, ann_ret: float,
                    max_dd: float, alpha: float, calmar: float) -> float:
        score = 50
        score += (sharpe - 0.5) * 15
        score += (sortino - 1) * 10
        score += (ann_ret - 5) * 1
        score += (10 - max_dd) * 0.5
        score += alpha * 3
        score += (calmar - 1) * 10
        return max(0, min(100, score))

    def _score_to_rating(self, score: float) -> str:
        if score >= 85:
            return "A+"
        elif score >= 75:
            return "A"
        elif score >= 65:
            return "B"
        elif score >= 50:
            return "C"
        return "D"

    def compare_funds(self, funds: List[Dict]) -> List[Dict]:
        """多基金对比排名。

        Args:
            funds: [{"name": str, "nav": List[float]}, ...]
        """
        results = []
        for f in funds:
            perf = self.analyze_fund(f["nav"], fund_name=f.get("name", "?"))
            results.append({
                "name": perf.fund_name,
                "annual_return": perf.annual_return,
                "max_drawdown": perf.max_drawdown,
                "sharpe": perf.sharpe_ratio,
                "alpha": perf.alpha,
                "score": perf.score,
                "rating": perf.rating,
            })
        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    def dca_backtest(self, nav_series: List[float],
                     monthly_amount: float = 1000,
                     months: int = 36) -> Dict:
        """定投回测。

        Args:
            nav_series: 基金净值序列（日度，至少 months*22 条）
            monthly_amount: 每月定投金额
            months: 回测月数
        """
        days_needed = months * 22
        if len(nav_series) < days_needed:
            return {"error": "数据不足"}

        nav = nav_series[-days_needed:]
        total_units = 0
        total_invested = 0

        for i in range(0, len(nav), 22):
            price = nav[i]
            units = monthly_amount / price
            total_units += units
            total_invested += monthly_amount

        final_value = total_units * nav[-1]
        total_return = (final_value / total_invested - 1) * 100 if total_invested > 0 else 0

        return {
            "months": months,
            "total_invested": round(total_invested, 2),
            "final_value": round(final_value, 2),
            "total_return_pct": round(total_return, 2),
            "annualized_return": round(((final_value / total_invested) ** (12 / months) - 1) * 100, 2)
            if total_invested > 0 and months > 0 else 0,
        }

    def style_analysis(self, fund_returns: List[float],
                       factor_returns: Dict[str, List[float]]) -> Dict:
        """基金持仓风格归因。
        因子：大盘价值/大盘成长/小盘价值/小盘成长/债券/现金
        """
        # 简化版：计算与各因子指数的相关性
        corrs = {}
        n = min(len(fund_returns), *(len(v) for v in factor_returns.values()))
        for name, f_ret in factor_returns.items():
            if len(f_ret) >= n:
                corr = self._pearson_corr(fund_returns[:n], f_ret[:n])
                corrs[name] = round(corr, 3)

        if corrs:
            primary_style = max(corrs, key=lambda k: abs(corrs[k]))
        else:
            primary_style = "未知"

        return {"correlations": corrs, "primary_style": primary_style}

    def _pearson_corr(self, x: List[float], y: List[float]) -> float:
        n = min(len(x), len(y))
        if n < 3:
            return 0
        mx, my = sum(x[:n]) / n, sum(y[:n]) / n
        cov = sum((x[i] - mx) * (y[i] - my) for i in range(n))
        sx = (sum((v - mx) ** 2 for v in x[:n])) ** 0.5
        sy = (sum((v - my) ** 2 for v in y[:n])) ** 0.5
        return cov / (sx * sy) if sx > 0 and sy > 0 else 0


# ── 便捷函数 ──

def analyze_fund_performance(nav: List[float], benchmark: List[float] = None,
                             name: str = "") -> Dict:
    """一步式基金绩效分析。"""
    fqa = FundQuantAnalyzer()
    perf = fqa.analyze_fund(nav, benchmark, fund_name=name)
    return {
        "name": perf.fund_name, "annual_return": perf.annual_return,
        "max_drawdown": perf.max_drawdown, "sharpe": perf.sharpe,
        "sortino": perf.sortino, "alpha": perf.alpha, "beta": perf.beta,
        "calmar": perf.calmar, "win_rate": perf.win_rate,
        "score": perf.score, "rating": perf.rating,
    }


if __name__ == "__main__":
    import random
    random.seed(42)
    nav = [1.0]
    for _ in range(252 * 2):  # 2年
        nav.append(nav[-1] * (1 + random.gauss(0.0005, 0.008)))
    bm = [random.gauss(0.0003, 0.01) for _ in range(len(nav) - 1)]

    fqa = FundQuantAnalyzer()
    perf = fqa.analyze_fund(nav, bm, fund_name="测试基金")
    print(f"Fund: {perf.fund_name} rating={perf.rating} score={perf.score}")
    print(f"  annual={perf.annual_return}% max_dd={perf.max_drawdown}% sharpe={perf.sharpe}")
    print(f"  alpha={perf.alpha}% beta={perf.beta} calmar={perf.calmar}")

    dca = fqa.dca_backtest(nav, 1000, 24)
    print(f"  DCA 24m: return={dca.get('total_return_pct', 0)}%")
