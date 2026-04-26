"""
普通计算器控制器单元测试
"""
import unittest
from models.calculator_state import CalculatorState, CalculatorRecord
from controllers.calculator_controller import CalculatorController


class TestCalculatorController(unittest.TestCase):

    def setUp(self):
        self.state = CalculatorState()
        self.controller = CalculatorController(self.state)

    def test_input_digit(self):
        self.controller.input_digit("5")
        self.assertEqual(self.state.display, "5")

    def test_input_multiple_digits(self):
        self.controller.input_digit("1")
        self.controller.input_digit("2")
        self.controller.input_digit("3")
        self.assertEqual(self.state.display, "123")

    def test_input_decimal(self):
        self.controller.input_digit("1")
        self.controller.input_digit(".")
        self.controller.input_digit("5")
        self.assertEqual(self.state.display, "1.5")

    def test_no_double_decimal(self):
        self.controller.input_digit("1")
        self.controller.input_digit(".")
        self.controller.input_digit(".")
        self.controller.input_digit("5")
        self.assertEqual(self.state.display, "1.5")

    def test_addition(self):
        self.controller.input_digit("2")
        self.controller.input_operator("+")
        self.controller.input_digit("3")
        self.controller.calculate()
        self.assertEqual(self.state.display, "5")

    def test_subtraction(self):
        self.controller.input_digit("9")
        self.controller.input_operator("-")
        self.controller.input_digit("4")
        self.controller.calculate()
        self.assertEqual(self.state.display, "5")

    def test_multiplication(self):
        self.controller.input_digit("6")
        self.controller.input_operator("×")
        self.controller.input_digit("7")
        self.controller.calculate()
        self.assertEqual(self.state.display, "42")

    def test_division(self):
        self.controller.input_digit("1")
        self.controller.input_digit("0")
        self.controller.input_operator("÷")
        self.controller.input_digit("2")
        self.controller.calculate()
        self.assertEqual(self.state.display, "5")

    def test_division_by_zero(self):
        self.controller.input_digit("5")
        self.controller.input_operator("÷")
        self.controller.input_digit("0")
        self.controller.calculate()
        self.assertEqual(self.state.display, "错误")

    def test_percent(self):
        self.controller.input_digit("5")
        self.controller.input_digit("0")
        self.controller.input_percent()
        self.assertEqual(self.state.display, "0.5")

    def test_toggle_sign(self):
        self.controller.input_digit("8")
        self.controller.toggle_sign()
        self.assertEqual(self.state.display, "-8")
        self.controller.toggle_sign()
        self.assertEqual(self.state.display, "8")

    def test_backspace(self):
        self.controller.input_digit("1")
        self.controller.input_digit("2")
        self.controller.input_digit("3")
        self.controller.backspace()
        self.assertEqual(self.state.display, "12")

    def test_clear(self):
        self.controller.input_digit("5")
        self.controller.input_operator("+")
        self.controller.input_digit("3")
        self.controller.calculate()
        self.state.clear()
        self.assertEqual(self.state.display, "0")
        self.assertEqual(self.state.expression, "")

    def test_history_recorded(self):
        self.controller.input_digit("2")
        self.controller.input_operator("+")
        self.controller.input_digit("3")
        self.controller.calculate()
        self.assertEqual(len(self.state.history), 1)
        self.assertEqual(self.state.history[0].expression, "2 + 3")
        self.assertEqual(self.state.history[0].result, "5")

    def test_history_max_5(self):
        for i in range(7):
            self.state.clear()
            self.controller.input_digit(str(i))
            self.controller.input_operator("+")
            self.controller.input_digit("1")
            self.controller.calculate()
        self.assertEqual(len(self.state.history), 5)

    def test_clear_all(self):
        self.controller.input_digit("2")
        self.controller.input_operator("+")
        self.controller.input_digit("3")
        self.controller.calculate()
        self.state.clear_all()
        self.assertEqual(self.state.display, "0")
        self.assertEqual(len(self.state.history), 0)

    def test_chained_calculation(self):
        self.controller.input_digit("2")
        self.controller.input_operator("+")
        self.controller.input_digit("3")
        self.controller.input_operator("×")
        self.assertEqual(self.state.display, "5")
        self.assertEqual(self.state.expression, "5 × ")
        self.controller.input_digit("4")
        self.controller.calculate()
        self.assertEqual(self.state.display, "20")

    def test_continue_after_equals(self):
        self.controller.input_digit("2")
        self.controller.input_operator("+")
        self.controller.input_digit("3")
        self.controller.calculate()
        self.assertEqual(self.state.display, "5")
        self.controller.input_operator("-")
        self.assertEqual(self.state.expression, "5 - ")
        self.controller.input_digit("1")
        self.controller.calculate()
        self.assertEqual(self.state.display, "4")

    def test_chained_multiple_operators(self):
        self.controller.input_digit("1")
        self.controller.input_digit("0")
        self.controller.input_operator("+")
        self.controller.input_digit("5")
        self.controller.input_operator("÷")
        self.assertEqual(self.state.display, "15")
        self.controller.input_digit("3")
        self.controller.calculate()
        self.assertEqual(self.state.display, "5")


class TestCalculatorRecord(unittest.TestCase):

    def test_to_display(self):
        record = CalculatorRecord(expression="2 + 3", result="5")
        self.assertEqual(record.to_display(), "2 + 3 = 5")


if __name__ == "__main__":
    unittest.main()
