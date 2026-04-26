"""
输入验证器
"""
from decimal import Decimal, InvalidOperation
from typing import Tuple, Optional


class InputValidator:
    """输入验证器"""

    @staticmethod
    def validate_amount(value: str, field_name: str) -> Tuple[Optional[Decimal], Optional[str]]:
        """
        验证金额输入
        
        Args:
            value: 输入字符串
            field_name: 字段名称（用于错误提示）
        
        Returns:
            (验证后的 Decimal 值, 错误信息)
        """
        if not value or value.strip() == "":
            return None, f"请输入有效的{field_name}"

        try:
            amount = Decimal(value.strip())
            if amount <= 0:
                return None, f"{field_name}必须为正数"
            return amount, None
        except InvalidOperation:
            return None, f"请输入有效的{field_name}数值"

    @staticmethod
    def validate_profit_rate(rate: float, rate_min: float, rate_max: float) -> Tuple[float, Optional[str]]:
        """
        验证毛利率
        
        Args:
            rate: 当前毛利率（小数形式）
            rate_min: 最小毛利率
            rate_max: 最大毛利率
        
        Returns:
            (验证后的毛利率, 错误信息)
        """
        if rate >= 1:
            return rate, "毛利率不能为 100%"

        if rate < 0:
            return rate, "毛利率不能为负数"

        # 自动调整到有效范围
        if rate < rate_min:
            return rate_min, None
        if rate > rate_max:
            return rate_max, None

        return rate, None

    @staticmethod
    def validate_rate_range(rate_min: float, rate_max: float) -> Optional[str]:
        """
        验证毛利率范围设置
        
        Args:
            rate_min: 最小毛利率
            rate_max: 最大毛利率
        
        Returns:
            错误信息，None 表示验证通过
        """
        if rate_min >= rate_max:
            return "最小值必须小于最大值"

        if rate_min < 0 or rate_max < 0:
            return "毛利率不能为负数"

        if rate_max >= 1:
            return "最大毛利率不能达到 100%"

        return None
