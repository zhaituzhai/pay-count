"""
普通计算器状态模型
"""
from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class CalculatorRecord:
    expression: str
    result: str
    timestamp: datetime = field(default_factory=datetime.now)

    def to_display(self) -> str:
        return f"{self.expression} = {self.result}"


@dataclass
class CalculatorState:
    expression: str = ""
    display: str = "0"
    history: List[CalculatorRecord] = field(default_factory=list)
    max_history: int = 5
    _new_input: bool = True

    def add_to_history(self, expression: str, result: str) -> None:
        record = CalculatorRecord(expression=expression, result=result)
        self.history.insert(0, record)
        if len(self.history) > self.max_history:
            self.history = self.history[:self.max_history]

    def clear(self) -> None:
        self.expression = ""
        self.display = "0"
        self._new_input = True

    def clear_all(self) -> None:
        self.clear()
        self.history = []
