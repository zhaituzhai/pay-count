"""
普通计算器控制器
"""
from models.calculator_state import CalculatorState


class CalculatorController:
    _OPERATORS = {'+', '-', '×', '÷'}

    def __init__(self, state: CalculatorState):
        self.state = state

    def _evaluate(self, expr: str):
        calc_expr = expr.replace("×", "*").replace("÷", "/")
        result = eval(calc_expr)
        if isinstance(result, float):
            if result == int(result):
                result = int(result)
            else:
                result = round(result, 10)
        return result

    def _format_result(self, result) -> str:
        if isinstance(result, float):
            if result == int(result):
                return str(int(result))
            return str(round(result, 10))
        return str(result)

    def input_digit(self, digit: str) -> None:
        if self.state._new_input:
            self.state.display = digit
            self.state._new_input = False
        else:
            if self.state.display == "0" and digit != ".":
                self.state.display = digit
            else:
                if digit == "." and "." in self.state.display:
                    return
                self.state.display += digit

    def input_operator(self, op: str) -> None:
        if self.state.expression:
            expr = self.state.expression + self.state.display
            try:
                result = self._evaluate(expr)
                result_str = self._format_result(result)
                self.state.add_to_history(expr, result_str)
                self.state.display = result_str
            except (ZeroDivisionError, Exception):
                self.state.display = "错误"
                self.state.expression = ""
                self.state._new_input = True
                return
        self.state.expression = self.state.display + f" {op} "
        self.state._new_input = True

    def calculate(self) -> None:
        if not self.state.expression:
            return
        expr = self.state.expression + self.state.display
        try:
            result = self._evaluate(expr)
            result_str = self._format_result(result)
            self.state.add_to_history(expr, result_str)
            self.state.display = result_str
            self.state.expression = ""
            self.state._new_input = True
        except ZeroDivisionError:
            self.state.display = "错误"
            self.state.expression = ""
            self.state._new_input = True
        except Exception:
            self.state.display = "错误"
            self.state.expression = ""
            self.state._new_input = True

    def input_percent(self) -> None:
        try:
            val = float(self.state.display)
            self.state.display = str(val / 100)
        except ValueError:
            pass

    def toggle_sign(self) -> None:
        try:
            val = float(self.state.display)
            result = -val
            if result == int(result):
                self.state.display = str(int(result))
            else:
                self.state.display = str(result)
        except ValueError:
            pass

    def backspace(self) -> None:
        if len(self.state.display) > 1:
            self.state.display = self.state.display[:-1]
        else:
            self.state.display = "0"
