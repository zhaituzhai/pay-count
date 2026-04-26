"""
计算引擎
"""
from decimal import Decimal, ROUND_HALF_UP


class CalculatorEngine:
    """定价计算引擎"""

    @staticmethod
    def calculate_selling_price(
        cost_price: Decimal,
        profit_rate: Decimal
    ) -> Decimal:
        """
        成本→卖价计算
        
        公式：卖价 = 成本 ÷ (1 - 毛利率)
        
        Args:
            cost_price: 成本价
            profit_rate: 毛利率（小数形式，如 0.25 表示 25%）
        
        Returns:
            卖价（保留两位小数）
        
        Raises:
            ValueError: 当毛利率为 1 (100%) 时抛出
        """
        if profit_rate >= 1:
            raise ValueError("毛利率不能为 100%")

        selling_price = cost_price / (1 - profit_rate)
        return selling_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @staticmethod
    def calculate_cost_price(
        selling_price: Decimal,
        profit_rate: Decimal
    ) -> Decimal:
        """
        卖价→成本计算
        
        公式：成本 = 卖价 × (1 - 毛利率)
        
        Args:
            selling_price: 卖价
            profit_rate: 毛利率（小数形式）
        
        Returns:
            成本价（保留两位小数）
        """
        cost_price = selling_price * (1 - profit_rate)
        return cost_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @staticmethod
    def calculate_gross_profit(
        selling_price: Decimal,
        cost_price: Decimal
    ) -> Decimal:
        """
        计算毛利润
        
        公式：毛利润 = 卖价 - 成本
        
        Args:
            selling_price: 卖价
            cost_price: 成本价
        
        Returns:
            毛利润（保留两位小数）
        """
        gross_profit = selling_price - cost_price
        return gross_profit.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @staticmethod
    def calculate_profit_rate(
        selling_price: Decimal,
        cost_price: Decimal
    ) -> Decimal:
        """
        计算毛利率
        
        公式：毛利率 = (卖价 - 成本) ÷ 卖价 × 100%
        
        Args:
            selling_price: 卖价
            cost_price: 成本价
        
        Returns:
            毛利率（百分比形式，如 25.00 表示 25%）
        
        Raises:
            ValueError: 当卖价为 0 时抛出
        """
        if selling_price == 0:
            raise ValueError("卖价不能为 0")

        rate = (selling_price - cost_price) / selling_price * 100
        return rate.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
