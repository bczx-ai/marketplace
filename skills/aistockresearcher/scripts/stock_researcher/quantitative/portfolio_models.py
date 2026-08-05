# -*- coding: utf-8 -*-
"""
组合构建模型
Portfolio Construction Models

基于 QuantConnect Lean PortfolioConstructionModel 架构

组合模型类型：
- EqualWeightPortfolio: 等权组合
- RiskParityPortfolio: 风险平价组合
- ValueWeightedPortfolio: 价值加权组合
"""

import math
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field

from .alpha_models import Insight, InsightDirection


@dataclass
class PortfolioTarget:
    """
    组合目标持仓
    """
    symbol: str
    quantity: int = 0                    # 股数
    weight: float = 0                    # 目标权重 0-1
    target_value: float = 0              # 目标金额
    confidence: float = 0                # 置信度
    insight_direction: InsightDirection = InsightDirection.FLAT  # 信号方向


@dataclass
class PortfolioResult:
    """
    组合构建结果
    """
    targets: List[PortfolioTarget]
    total_value: float
    cash_required: float = 0
    metadata: Dict = field(default_factory=dict)


class PortfolioConstructionModel:
    """组合构建模型基类"""

    def __init__(self, name: str = ""):
        self.name = name or self.__class__.__name__

    def construct(
        self,
        insights: List[Insight],
        current_positions: Dict[str, Dict],
        total_value: float,
        price_map: Dict[str, float]
    ) -> PortfolioResult:
        """
        构建目标组合

        Args:
            insights: 信号列表
            current_positions: 当前持仓 {symbol: {'quantity': n, 'avg_price': p}}
            total_value: 总组合价值
            price_map: 当前价格 {symbol: price}

        Returns:
            PortfolioResult: 目标组合
        """
        raise NotImplementedError

    def _get_position_value(self, symbol: str, positions: Dict, price_map: Dict) -> float:
        """获取持仓价值"""
        if symbol not in positions:
            return 0
        pos = positions[symbol]
        price = price_map.get(symbol, pos.get('avg_price', 0))
        return pos.get('quantity', 0) * price


class EqualWeightPortfolio(PortfolioConstructionModel):
    """
    等权重组合模型

    原理：
    - 将总仓位平均分配给所有标的
    - 每个标的权重 = 1 / N

    适用于：分散化投资、指数增强
    """

    def __init__(self, max_positions: int = 10, name: str = ""):
        super().__init__(name or "EqualWeight")
        self.max_positions = max_positions

    def construct(
        self,
        insights: List[Insight],
        current_positions: Dict[str, Dict],
        total_value: float,
        price_map: Dict[str, float]
    ) -> PortfolioResult:
        """构建等权组合"""
        # 只选择做多信号
        buy_insights = [i for i in insights if i.direction == InsightDirection.UP]
        if not buy_insights:
            return PortfolioResult([], total_value)

        # 按置信度排序，取前N个
        buy_insights.sort(key=lambda x: x.confidence, reverse=True)
        selected = buy_insights[:self.max_positions]

        n = len(selected)
        if n == 0:
            return PortfolioResult([], total_value)

        # 等权分配
        weight_per_stock = 1.0 / n
        targets = []

        for insight in selected:
            symbol = insight.symbol
            price = price_map.get(symbol, 0)
            if price <= 0:
                continue

            target_value = total_value * weight_per_stock
            quantity = int(target_value / price / 100) * 100  # 整手

            targets.append(PortfolioTarget(
                symbol=symbol,
                quantity=quantity,
                weight=weight_per_stock,
                target_value=target_value,
                confidence=insight.confidence,
                insight_direction=insight.direction
            ))

        return PortfolioResult(
            targets=targets,
            total_value=total_value,
            metadata={'method': 'equal_weight', 'n_positions': len(targets)}
        )


class RiskParityPortfolio(PortfolioConstructionModel):
    """
    风险平价组合模型

    原理：
    - 每个标的贡献相同风险
    - 风险贡献 = 权重 * 波动率
    - 低波动标的配置更高权重

    适用于：稳健型组合、大类资产配置

    参数：
    - max_positions: 最大持仓数（默认8）
    - risk_cap: 单标的风险上限（默认20%）
    """

    def __init__(self, max_positions: int = 8, risk_cap: float = 0.20, name: str = ""):
        super().__init__(name or "RiskParity")
        self.max_positions = max_positions
        self.risk_cap = risk_cap
        self._volatility: Dict[str, float] = {}

    def set_volatility(self, symbol: str, volatility: float):
        """设置标的波动率"""
        self._volatility[symbol] = volatility

    def construct(
        self,
        insights: List[Insight],
        current_positions: Dict[str, Dict],
        total_value: float,
        price_map: Dict[str, float]
    ) -> PortfolioResult:
        """构建风险平价组合"""
        buy_insights = [i for i in insights if i.direction == InsightDirection.UP]
        if not buy_insights:
            return PortfolioResult([], total_value)

        buy_insights.sort(key=lambda x: x.confidence, reverse=True)
        selected = buy_insights[:self.max_positions]

        # 计算风险权重
        total_inv_vol = 0
        risk_weights = {}

        for insight in selected:
            symbol = insight.symbol
            vol = self._volatility.get(symbol, 0.20)  # 默认20%波动率
            inv_vol = 1.0 / vol if vol > 0 else 1.0
            risk_weights[symbol] = inv_vol
            total_inv_vol += inv_vol

        if total_inv_vol <= 0:
            return EqualWeightPortfolio(max_positions=self.max_positions).construct(
                insights, current_positions, total_value, price_map
            )

        # 波动率倒数归一化
        final_weights = {s: risk_weights[s] / total_inv_vol for s in risk_weights}

        # cap 截断后，剩余权重按 inv_vol 比例再分配（迭代至无超限），
        # 保证权重合计为 1，避免资金无故闲置
        capped_note = False
        for _ in range(len(final_weights) + 1):
            over = [s for s, w in final_weights.items() if w > self.risk_cap]
            if not over:
                break
            capped_note = True
            excess = sum(final_weights[s] - self.risk_cap for s in over)
            for s in over:
                final_weights[s] = self.risk_cap
            under = [s for s in final_weights if s not in over]
            inv_sum = sum(risk_weights[s] for s in under)
            if inv_sum <= 0:
                break
            for s in under:
                final_weights[s] += excess * risk_weights[s] / inv_sum

        targets = []

        for insight in selected:
            symbol = insight.symbol
            price = price_map.get(symbol, 0)
            if price <= 0:
                continue

            risk_weight = final_weights[symbol]

            target_value = total_value * risk_weight
            quantity = int(target_value / price / 100) * 100

            targets.append(PortfolioTarget(
                symbol=symbol,
                quantity=quantity,
                weight=risk_weight,
                target_value=target_value,
                confidence=insight.confidence,
                insight_direction=insight.direction
            ))

        return PortfolioResult(
            targets=targets,
            total_value=total_value,
            metadata={'method': 'risk_parity', 'n_positions': len(targets),
                      'risk_cap': self.risk_cap, 'cap_applied': capped_note,
                      'total_weight': round(sum(final_weights.values()), 4)}
        )


class ValueWeightedPortfolio(PortfolioConstructionModel):
    """
    价值加权组合模型

    原理：
    - 根据信号置信度和预测幅度加权
    - 置信度越高、预期收益越大，权重越高

    适用于：alpha增强、smart beta

    参数：
    - max_positions: 最大持仓数（默认10）
    - confidence_weight: 置信度权重（默认0.6）
    - magnitude_weight: 预测幅度权重（默认0.4）
    """

    def __init__(
        self,
        max_positions: int = 10,
        confidence_weight: float = 0.6,
        magnitude_weight: float = 0.4,
        name: str = ""
    ):
        super().__init__(name or "ValueWeighted")
        self.max_positions = max_positions
        self.confidence_weight = confidence_weight
        self.magnitude_weight = magnitude_weight

    def construct(
        self,
        insights: List[Insight],
        current_positions: Dict[str, Dict],
        total_value: float,
        price_map: Dict[str, float]
    ) -> PortfolioResult:
        """构建价值加权组合"""
        buy_insights = [i for i in insights if i.direction == InsightDirection.UP]
        if not buy_insights:
            return PortfolioResult([], total_value)

        buy_insights.sort(key=lambda x: x.confidence, reverse=True)
        selected = buy_insights[:self.max_positions]

        # 计算组合权重
        scores = {}
        for insight in selected:
            symbol = insight.symbol
            confidence = insight.confidence
            magnitude = min(insight.magnitude, 50) / 50  # 归一化，最大50%
            score = confidence * self.confidence_weight + magnitude * self.magnitude_weight
            scores[symbol] = score

        total_score = sum(scores.values())
        if total_score <= 0:
            return EqualWeightPortfolio(max_positions=self.max_positions).construct(
                insights, current_positions, total_value, price_map
            )

        targets = []

        for insight in selected:
            symbol = insight.symbol
            price = price_map.get(symbol, 0)
            if price <= 0:
                continue

            weight = scores[symbol] / total_score
            target_value = total_value * weight
            quantity = int(target_value / price / 100) * 100

            targets.append(PortfolioTarget(
                symbol=symbol,
                quantity=quantity,
                weight=weight,
                target_value=target_value,
                confidence=insight.confidence,
                insight_direction=insight.direction
            ))

        return PortfolioResult(
            targets=targets,
            total_value=total_value,
            metadata={'method': 'value_weighted', 'n_positions': len(targets)}
        )


class MomentumPortfolio(PortfolioConstructionModel):
    """
    动量组合模型

    原理：
    - 根据动量信号强度分配权重
    - 近期表现好的标的权重更高

    适用于：趋势跟踪、动量策略
    """

    def __init__(self, max_positions: int = 5, name: str = ""):
        super().__init__(name or "Momentum")
        self.max_positions = max_positions
        self._momentum: Dict[str, float] = {}

    def set_momentum(self, symbol: str, momentum: float):
        """设置标的动量（近N日收益率%）"""
        self._momentum[symbol] = momentum

    def construct(
        self,
        insights: List[Insight],
        current_positions: Dict[str, Dict],
        total_value: float,
        price_map: Dict[str, float]
    ) -> PortfolioResult:
        """构建动量组合"""
        buy_insights = [i for i in insights if i.direction == InsightDirection.UP]
        if not buy_insights:
            return PortfolioResult([], total_value)

        buy_insights.sort(key=lambda x: x.confidence, reverse=True)
        selected = buy_insights[:self.max_positions]

        # 计算动量权重
        total_momentum = 0
        momentum_scores = {}

        for insight in selected:
            symbol = insight.symbol
            momentum = self._momentum.get(symbol, 0)
            # 只考虑正动量
            score = max(0, momentum)
            momentum_scores[symbol] = score
            total_momentum += score

        if total_momentum <= 0:
            return EqualWeightPortfolio(max_positions=self.max_positions).construct(
                insights, current_positions, total_value, price_map
            )

        targets = []

        for insight in selected:
            symbol = insight.symbol
            price = price_map.get(symbol, 0)
            if price <= 0:
                continue

            weight = momentum_scores[symbol] / total_momentum
            target_value = total_value * weight
            quantity = int(target_value / price / 100) * 100

            targets.append(PortfolioTarget(
                symbol=symbol,
                quantity=quantity,
                weight=weight,
                target_value=target_value,
                confidence=insight.confidence,
                insight_direction=insight.direction
            ))

        return PortfolioResult(
            targets=targets,
            total_value=total_value,
            metadata={'method': 'momentum', 'n_positions': len(targets)}
        )


def create_portfolio_model(model_type: str, **kwargs) -> PortfolioConstructionModel:
    """
    工厂函数：创建组合构建模型

    Args:
        model_type: 模型类型
            - 'equal': 等权组合
            - 'risk_parity': 风险平价组合
            - 'value_weighted': 价值加权组合
            - 'momentum': 动量组合

    Returns:
        PortfolioConstructionModel: 实例化的模型
    """
    models = {
        'equal': EqualWeightPortfolio,
        'risk_parity': RiskParityPortfolio,
        'value_weighted': ValueWeightedPortfolio,
        'momentum': MomentumPortfolio,
    }

    model_class = models.get(model_type.lower())
    if not model_class:
        raise ValueError(f"Unknown model type: {model_type}")

    return model_class(**kwargs)


# ============================================================
# v3.1.0 增量 — 风险预算 + 边际风险贡献
# ============================================================

def risk_budget_weights(returns_matrix, risk_budget, l2_reg=1e-6,
                        max_iter=1000, tol=1e-10):
    """ERC（等风险预算）/ 用户给定风险预算分配权重。

    算法：循环坐标下降不动点迭代（纯 numpy，无 scipy 依赖）。
    不动点条件：w_i ∝ b_i / (Σw)_i  ⟺  RC_i / ΣRC = b_i，
    其中 (Σw)_i 为边际风险贡献，RC_i = w_i·(Σw)_i / σ_p。
    每轮迭代 w ← normalize(b / (Σw))，加阻尼保证稳定收敛。

    Args:
        returns_matrix: 形状 (T, N) 的收益矩阵，列为资产
        risk_budget: 长度为 N 的目标风险贡献比例（和为 1）
        l2_reg: 正则项
        max_iter: 最大迭代轮数
        tol: 权重收敛阈值

    Returns:
        dict: weights, marginal_risk_contrib, achieved_risk_budget
    """
    import numpy as _np
    X = _np.array(returns_matrix, dtype=float)
    if X.ndim != 2 or X.shape[0] < X.shape[1]:
        return {'weights': [], 'error': '收益矩阵形状错误'}
    cov = _np.cov(X, rowvar=False)
    cov = cov + _np.eye(cov.shape[0]) * l2_reg

    rb = _np.array(risk_budget, dtype=float)
    if rb.size != cov.shape[0] or _np.any(rb < 0) or rb.sum() <= 0:
        rb = _np.ones(cov.shape[0]) / cov.shape[0]
    rb = rb / rb.sum()

    n = cov.shape[0]
    w = _np.ones(n) / n
    converged = False
    for _ in range(max_iter):
        marg = cov @ w
        if _np.any(marg <= 0):
            break  # 协方差非正定，放弃迭代
        w_new = rb / marg
        w_new = w_new / w_new.sum()
        w_new = 0.5 * w + 0.5 * w_new  # 阻尼更新
        if float(_np.linalg.norm(w_new - w)) < tol:
            w = w_new
            converged = True
            break
        w = w_new

    port_var = float(w @ cov @ w)
    marg = cov @ w
    rc = w * marg / _np.sqrt(max(port_var, 1e-12))
    achieved = (rc / (rc.sum() or 1.0)).tolist()
    return {
        'weights': [round(float(x), 4) for x in w.tolist()],
        'marginal_risk_contrib': [round(float(x), 4) for x in rc.tolist()],
        'achieved_risk_budget': [round(x, 4) for x in achieved],
        'target_risk_budget': [round(float(x), 4) for x in rb.tolist()],
        'portfolio_vol_annual': round(_np.sqrt(port_var * 252), 4),
        'converged': converged,
    }
