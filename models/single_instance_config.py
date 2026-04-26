"""
单实例配置模型
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class SingleInstanceConfig:
    """
    单实例配置模型

    用于配置单实例运行机制的各项参数，包括互斥量名称、超时时间、提示信息等。
    """

    # 应用标识符（用于互斥量）
    app_id: str = "pricing-calculator-app"

    # 互斥量名称（全局命名，确保整个系统唯一）
    mutex_name: str = "Global\\PricingCalculatorMutex"

    # 超时时间（毫秒）
    timeout_ms: int = 100

    # 是否显示提示信息
    show_notification: bool = True

    # 提示信息文本
    notification_text: str = "定价计算器已在运行中"

    # 提示信息显示时长（毫秒）
    notification_duration_ms: int = 2000
