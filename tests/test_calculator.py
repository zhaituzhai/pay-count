"""
计算引擎测试
"""
import unittest
from decimal import Decimal
from controllers.calculator import CalculatorEngine


class TestCalculatorEngine(unittest.TestCase):
    """计算引擎测试类"""

    def test_calculate_selling_price(self) -> None:
        """测试成本→卖价计算"""
        # 测试用例 1: 成本 100，毛利率 25%
        cost_price = Decimal("100")
        profit_rate = Decimal("0.25")
        result = CalculatorEngine.calculate_selling_price(cost_price, profit_rate)
        self.assertAlmostEqual(float(result), 133.33, places=2)

        # 测试用例 2: 成本 200，毛利率 30%
        cost_price = Decimal("200")
        profit_rate = Decimal("0.30")
        result = CalculatorEngine.calculate_selling_price(cost_price, profit_rate)
        self.assertAlmostEqual(float(result), 285.71, places=2)

    def test_calculate_cost_price(self) -> None:
        """测试卖价→成本计算"""
        # 测试用例: 卖价 133.33，毛利率 25%
        selling_price = Decimal("133.33")
        profit_rate = Decimal("0.25")
        result = CalculatorEngine.calculate_cost_price(selling_price, profit_rate)
        self.assertAlmostEqual(float(result), 100.00, places=2)

    def test_calculate_gross_profit(self) -> None:
        """测试毛利润计算"""
        # 测试用例: 卖价 133.33，成本 100
        selling_price = Decimal("133.33")
        cost_price = Decimal("100")
        result = CalculatorEngine.calculate_gross_profit(selling_price, cost_price)
        self.assertAlmostEqual(float(result), 33.33, places=2)

    def test_calculate_profit_rate(self) -> None:
        """测试毛利率计算"""
        # 测试用例: 卖价 133.33，成本 100
        selling_price = Decimal("133.33")
        cost_price = Decimal("100")
        result = CalculatorEngine.calculate_profit_rate(selling_price, cost_price)
        self.assertAlmostEqual(float(result), 25.00, places=2)

    def test_division_by_zero(self) -> None:
        """测试除零异常"""
        # 测试毛利率 100%
        cost_price = Decimal("100")
        profit_rate = Decimal("1.0")
        with self.assertRaises(ValueError) as context:
            CalculatorEngine.calculate_selling_price(cost_price, profit_rate)
        self.assertEqual(str(context.exception), "毛利率不能为 100%")

        # 测试卖价 0
        selling_price = Decimal("0")
        cost_price = Decimal("100")
        with self.assertRaises(ValueError) as context:
            CalculatorEngine.calculate_profit_rate(selling_price, cost_price)
        self.assertEqual(str(context.exception), "卖价不能为 0")


if __name__ == "__main__":
    unittest.main()
