"""
错误类型定义
"""


class CalculatorError(Exception):
    """计算器基础异常"""
    pass


class InvalidInputError(CalculatorError):
    """无效输入异常"""
    pass


class DivisionByZeroError(CalculatorError):
    """除零异常（毛利率为 100%）"""
    pass


class OutOfRangeError(CalculatorError):
    """超出范围异常"""
    pass
