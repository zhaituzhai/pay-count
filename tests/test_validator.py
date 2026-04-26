"""
验证器测试
"""
import unittest
from decimal import Decimal
from utils.validator import InputValidator


class TestInputValidator(unittest.TestCase):
    """输入验证器测试类"""

    def test_validate_amount_valid(self) -> None:
        """测试有效金额"""
        # 测试有效输入
        value, error = InputValidator.validate_amount("100", "成本价")
        self.assertEqual(value, Decimal("100"))
        self.assertIsNone(error)

        # 测试带空格的输入
        value, error = InputValidator.validate_amount(" 200 ", "卖价")
        self.assertEqual(value, Decimal("200"))
        self.assertIsNone(error)

    def test_validate_amount_empty(self) -> None:
        """测试空值"""
        # 测试空字符串
        value, error = InputValidator.validate_amount("", "成本价")
        self.assertIsNone(value)
        self.assertEqual(error, "请输入有效的成本价")

        # 测试空格
        value, error = InputValidator.validate_amount("   ", "卖价")
        self.assertIsNone(value)
        self.assertEqual(error, "请输入有效的卖价")

    def test_validate_amount_negative(self) -> None:
        """测试负数"""
        # 测试负数
        value, error = InputValidator.validate_amount("-100", "成本价")
        self.assertIsNone(value)
        self.assertEqual(error, "成本价必须为正数")

        # 测试零
        value, error = InputValidator.validate_amount("0", "卖价")
        self.assertIsNone(value)
        self.assertEqual(error, "卖价必须为正数")

    def test_validate_profit_rate_valid(self) -> None:
        """测试有效毛利率"""
        # 测试有效毛利率
        rate, error = InputValidator.validate_profit_rate(0.25, 0.20, 0.40)
        self.assertEqual(rate, 0.25)
        self.assertIsNone(error)

    def test_validate_profit_rate_100(self) -> None:
        """测试 100% 毛利率"""
        # 测试 100%
        rate, error = InputValidator.validate_profit_rate(1.0, 0.20, 0.40)
        self.assertEqual(rate, 1.0)
        self.assertEqual(error, "毛利率不能为 100%")

    def test_validate_profit_rate_negative(self) -> None:
        """测试负数毛利率"""
        # 测试负数
        rate, error = InputValidator.validate_profit_rate(-0.1, 0.20, 0.40)
        self.assertEqual(rate, -0.1)
        self.assertEqual(error, "毛利率不能为负数")

    def test_validate_profit_rate_range_adjustment(self) -> None:
        """测试毛利率范围自动调整"""
        # 测试小于最小值
        rate, error = InputValidator.validate_profit_rate(0.10, 0.20, 0.40)
        self.assertEqual(rate, 0.20)
        self.assertIsNone(error)

        # 测试大于最大值
        rate, error = InputValidator.validate_profit_rate(0.50, 0.20, 0.40)
        self.assertEqual(rate, 0.40)
        self.assertIsNone(error)

    def test_validate_rate_range_valid(self) -> None:
        """测试有效范围"""
        error = InputValidator.validate_rate_range(0.20, 0.40)
        self.assertIsNone(error)

    def test_validate_rate_range_invalid(self) -> None:
        """测试无效范围（min >= max）"""
        # 测试 min == max
        error = InputValidator.validate_rate_range(0.40, 0.40)
        self.assertEqual(error, "最小值必须小于最大值")

        # 测试 min > max
        error = InputValidator.validate_rate_range(0.50, 0.40)
        self.assertEqual(error, "最小值必须小于最大值")

    def test_validate_rate_range_negative(self) -> None:
        """测试负数范围"""
        # 测试负数 min
        error = InputValidator.validate_rate_range(-0.1, 0.40)
        self.assertEqual(error, "毛利率不能为负数")

        # 测试负数 max
        error = InputValidator.validate_rate_range(0.20, -0.1)
        self.assertEqual(error, "毛利率不能为负数")

    def test_validate_rate_range_100(self) -> None:
        """测试最大值达到 100%"""
        error = InputValidator.validate_rate_range(0.20, 1.0)
        self.assertEqual(error, "最大毛利率不能达到 100%")


if __name__ == "__main__":
    unittest.main()
