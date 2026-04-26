"""
输入区域组件
"""
import flet as ft
from typing import Callable
from models.state import CalculationMode, InputCurrency
from config import Config


class InputSection:
    """输入区域组件"""

    def __init__(
        self,
        on_change: Callable[[str, int], None],
        on_rate_change: Callable[[float], None],
        on_clear: Callable[[], None],
        on_reset: Callable[[], None],
        on_exchange_rate_change: Callable[[float], None] = None,
        on_currency_change: Callable[[InputCurrency], None] = None,
    ):
        """
        初始化输入区域组件
        
        Args:
            on_change: 输入变化回调（value, input_index）
            on_rate_change: 毛利率变化回调
            on_clear: 清空回调
            on_reset: 重置回调
            on_exchange_rate_change: 汇率变化回调
            on_currency_change: 币种切换回调
        """
        self.on_change = on_change
        self.on_rate_change = on_rate_change
        self.on_clear = on_clear
        self.on_reset = on_reset
        self.on_exchange_rate_change = on_exchange_rate_change
        self.on_currency_change = on_currency_change

        # 币种切换按钮
        self._currency_toggle = ft.SegmentedButton(
            selected=[InputCurrency.CNY.value],
            segments=[
                ft.Segment(
                    value=InputCurrency.CNY.value,
                    label=ft.Text("人民币", size=12),
                    icon=ft.Text("¥", size=14, weight=ft.FontWeight.BOLD),
                ),
                ft.Segment(
                    value=InputCurrency.HKD.value,
                    label=ft.Text("港币", size=12),
                    icon=ft.Text("HK$", size=12, weight=ft.FontWeight.BOLD),
                ),
            ],
            on_change=self._on_currency_toggle,
            width=200,
        )

        # 创建控件
        self.value_input = ft.TextField(
            label="成本价",
            hint_text="请输入金额",
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self._on_input_change,
            width=300,
        )

        # 第二个输入框（成本+售价→毛利模式使用）
        self.value_input2 = ft.TextField(
            label="卖价",
            hint_text="请输入金额",
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self._on_input2_change,
            width=300,
            visible=False,
        )

        # 毛利率滑块：用整数步进实现0.5吸附
        # 范围 1%~45%，步进0.5%，共 (45-1)/0.5 = 88 步
        self._rate_min = Config.DEFAULT_RATE_MIN * 100  # 1
        self._rate_steps = 88
        self._rate_step_size = 0.5
        default_index = int(round((Config.DEFAULT_RATE * 100 - self._rate_min) / self._rate_step_size))

        self.rate_slider = ft.Slider(
            min=0,
            max=self._rate_steps,
            value=default_index,
            divisions=self._rate_steps,
            on_change=self._on_slider_change,
            width=300,
        )

        self.rate_display = ft.Text(
            value=f"毛利率: {Config.DEFAULT_RATE * 100:.1f}%",
            size=16,
            weight=ft.FontWeight.BOLD,
        )

        self.clear_btn = ft.ElevatedButton(
            "清空",
            on_click=self._on_clear_click,
        )

        self.reset_btn = ft.OutlinedButton(
            "重置",
            on_click=self._on_reset_click,
        )

        # 汇率输入框
        self.exchange_rate_input = ft.TextField(
            label="汇率 (1 CNY → HKD)",
            value=str(Config.DEFAULT_EXCHANGE_RATE),
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self._on_exchange_rate_change,
            width=200,
            dense=True,
        )

    def build(self) -> ft.Container:
        """
        构建组件
        
        Returns:
            Container 组件
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("输入区域", size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=1),
                    self._currency_toggle,
                    self.value_input,
                    self.value_input2,
                    ft.Column(
                        controls=[
                            ft.Text("毛利率调节", size=13),
                            self.rate_slider,
                            self.rate_display,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[self.clear_btn, self.reset_btn],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    self.exchange_rate_input,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            padding=15,
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER,
        )

    def set_mode(self, mode: CalculationMode) -> None:
        """
        设置计算模式
        
        Args:
            mode: 计算模式
        """
        if mode == CalculationMode.COST_TO_PRICE:
            self.value_input.label = "成本价"
            self.value_input.visible = True
            self.value_input2.visible = False
            self.rate_slider.visible = True
            self.rate_display.visible = True
        elif mode == CalculationMode.PRICE_TO_COST:
            self.value_input.label = "卖价"
            self.value_input.visible = True
            self.value_input2.visible = False
            self.rate_slider.visible = True
            self.rate_display.visible = True
        else:  # COST_PRICE_TO_PROFIT
            self.value_input.label = "成本价"
            self.value_input.visible = True
            self.value_input2.visible = True
            self.rate_slider.visible = False
            self.rate_display.visible = False

    def _rate_index_to_value(self, index: float) -> float:
        """将滑块整数索引转换为实际毛利率值（百分比）"""
        return self._rate_min + round(index) * self._rate_step_size

    def _rate_value_to_index(self, value: float) -> int:
        """将实际毛利率值（百分比）转换为滑块整数索引"""
        return int(round((value - self._rate_min) / self._rate_step_size))

    def get_input_value(self) -> str:
        """
        获取输入值
        
        Returns:
            输入值字符串
        """
        return self.value_input.value or ""

    def get_profit_rate(self) -> float:
        """
        获取毛利率

        Returns:
            毛利率（小数形式）
        """
        rate_percent = self._rate_index_to_value(self.rate_slider.value or 0)
        return rate_percent / 100

    def clear(self) -> None:
        """清空输入框"""
        self.value_input.value = ""
        self.value_input2.value = ""
        self.value_input.update()
        self.value_input2.update()

    def reset(self) -> None:
        """重置滑块到默认值"""
        self.rate_slider.value = self._rate_value_to_index(Config.DEFAULT_RATE * 100)
        self.rate_display.value = f"毛利率: {Config.DEFAULT_RATE * 100:.1f}%"
        self.exchange_rate_input.value = str(Config.DEFAULT_EXCHANGE_RATE)
        self.rate_slider.update()
        self.rate_display.update()
        self.exchange_rate_input.update()

    def _on_input_change(self, e) -> None:
        """输入变化事件处理"""
        self.on_change(e.control.value, 1)

    def _on_input2_change(self, e) -> None:
        """第二个输入框变化事件处理"""
        self.on_change(e.control.value, 2)

    def _on_slider_change(self, e) -> None:
        """滑块变化事件处理"""
        rate_percent = self._rate_index_to_value(e.control.value)
        rate = rate_percent / 100
        self.rate_slider.label = f"{rate_percent:.1f}%"
        self.rate_display.value = f"毛利率: {rate_percent:.1f}%"
        self.rate_display.update()
        self.on_rate_change(rate)

    def _on_clear_click(self, e) -> None:
        """清空按钮点击事件"""
        self.clear()
        self.on_clear()

    def _on_reset_click(self, e) -> None:
        """重置按钮点击事件"""
        self.reset()
        self.on_reset()

    def _on_exchange_rate_change(self, e) -> None:
        """汇率输入变化事件处理"""
        if self.on_exchange_rate_change:
            try:
                value = float(e.control.value)
                if value > 0:
                    self.on_exchange_rate_change(value)
            except (ValueError, TypeError):
                pass

    def _on_currency_toggle(self, e) -> None:
        """币种切换事件处理"""
        selected = e.control.selected
        if selected:
            currency = InputCurrency(selected[0])
            self.on_currency_change(currency)
            # 切换币种后，如果输入框有值则重新触发计算
            if self.value_input.value:
                self.on_change(self.value_input.value, 1)
            if self.value_input2.visible and self.value_input2.value:
                self.on_change(self.value_input2.value, 2)

    def set_currency(self, currency: InputCurrency) -> None:
        """
        设置当前币种

        Args:
            currency: 币种
        """
        self._currency_toggle.selected = [currency.value]
        self._currency_toggle.update()
