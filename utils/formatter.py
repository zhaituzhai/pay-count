"""
格式化工具
"""
from decimal import Decimal, ROUND_HALF_UP
from config import Config


class Formatter:
    """格式化工具类"""

    @staticmethod
    def format_currency(value: Decimal, symbol: str = None) -> str:
        """
        格式化金额

        Args:
            value: 金额值
            symbol: 货币符号，默认使用人民币符号

        Returns:
            格式化后的字符串，如 "¥123.45"
        """
        if symbol is None:
            symbol = Config.CURRENCY_SYMBOL_CNY
        return f"{symbol}{value:.2f}"

    @staticmethod
    def format_currency_hkd(value: Decimal, exchange_rate: float = None) -> str:
        """
        格式化港币金额（根据汇率换算）

        Args:
            value: 人民币金额值
            exchange_rate: 汇率，默认使用配置值

        Returns:
            格式化后的字符串，如 "HK$133.33"
        """
        if exchange_rate is None:
            exchange_rate = Config.DEFAULT_EXCHANGE_RATE
        rate = Decimal(str(exchange_rate))
        hkd_value = (value * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return f"{Config.CURRENCY_SYMBOL_HKD}{hkd_value:.2f}"

    @staticmethod
    def format_percentage(value: Decimal) -> str:
        """
        格式化百分比
        
        Args:
            value: 百分比值
        
        Returns:
            格式化后的字符串，如 "25.00%"
        """
        return f"{value:.2f}%"

    @staticmethod
    def format_decimal(value: Decimal, places: int = 2) -> Decimal:
        """
        格式化小数，保留指定位数
        
        Args:
            value: 数值
            places: 小数位数
        
        Returns:
            格式化后的 Decimal
        """
        return value.quantize(Decimal(f"0.{'0' * places}"), rounding=ROUND_HALF_UP)
