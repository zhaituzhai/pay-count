"""
计算结果模型
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from config import Config


@dataclass
class CalculationResult:
    """计算结果模型"""
    cost_price: Decimal       # 成本价
    selling_price: Decimal    # 卖价
    gross_profit: Decimal     # 毛利润
    profit_rate: Decimal      # 毛利率（百分比形式）

    def to_display_dict(self, exchange_rate: float = None) -> dict:
        """
        转换为显示用的字典格式，包含人民币和港币两种结果

        Args:
            exchange_rate: 汇率（1人民币 = X港币），默认使用配置值

        Returns:
            包含格式化字符串的字典
        """
        if exchange_rate is None:
            exchange_rate = Config.DEFAULT_EXCHANGE_RATE

        rate = Decimal(str(exchange_rate))

        # 人民币值
        cost_cny = self.cost_price
        selling_cny = self.selling_price
        profit_cny = self.gross_profit

        # 港币值 = 人民币值 × 汇率
        cost_hkd = (self.cost_price * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        selling_hkd = (self.selling_price * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        profit_hkd = (self.gross_profit * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return {
            "cost_price_cny": f"¥{cost_cny:.2f}",
            "cost_price_hkd": f"HK${cost_hkd:.2f}",
            "selling_price_cny": f"¥{selling_cny:.2f}",
            "selling_price_hkd": f"HK${selling_hkd:.2f}",
            "gross_profit_cny": f"¥{profit_cny:.2f}",
            "gross_profit_hkd": f"HK${profit_hkd:.2f}",
            "profit_rate": f"{self.profit_rate:.2f}%"
        }
