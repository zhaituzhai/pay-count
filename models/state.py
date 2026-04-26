"""
应用状态模型
定义应用的全局状态数据结构
"""
from enum import Enum
from typing import Optional
from dataclasses import dataclass


class CalculationMode(Enum):
    """计算模式枚举"""
    COST_TO_PRICE = "cost_to_price"    # 成本→卖价
    PRICE_TO_COST = "price_to_cost"    # 卖价→成本
    COST_PRICE_TO_PROFIT = "cost_price_to_profit"  # 成本+售价→毛利


class InputCurrency(Enum):
    """输入币种枚举"""
    CNY = "CNY"  # 人民币
    HKD = "HKD"  # 港币


@dataclass
class AppState:
    """应用状态模型"""

    # 当前计算模式
    mode: CalculationMode = CalculationMode.COST_TO_PRICE

    # 输入值
    input_value: Optional[float] = None      # 成本价或卖价
    input_value2: Optional[float] = None     # 第二个输入值（成本+售价→毛利模式使用）
    profit_rate: float = 0.25                 # 毛利率（小数形式，默认25%）

    # 输入币种
    input_currency: InputCurrency = InputCurrency.CNY  # 输入币种，默认人民币

    # 毛利率范围设置
    rate_min: float = 0.09                    # 最小毛利率（9%）
    rate_max: float = 0.45                    # 最大毛利率（45%）

    # 汇率设置（1人民币 = X港币）
    exchange_rate: float = 1.08               # 默认汇率

    # 主题模式
    is_dark_mode: bool = True

    # 错误信息
    error_message: Optional[str] = None
