"""
事件处理器
"""
from typing import Callable, Optional
from decimal import Decimal
from models.state import AppState, CalculationMode, InputCurrency
from models.result import CalculationResult
from controllers.calculator import CalculatorEngine
from utils.validator import InputValidator


class EventHandler:
    """事件处理器"""

    def __init__(self, state: AppState, on_update_callback: Callable[[], None]):
        """
        初始化事件处理器
        
        Args:
            state: 应用状态
            on_update_callback: 界面更新回调函数
        """
        self.state = state
        self.on_update_callback = on_update_callback
        self.result: Optional[CalculationResult] = None

    def _convert_to_cny(self, value: float) -> float:
        """
        将输入值转换为人民币

        Args:
            value: 输入值

        Returns:
            人民币值
        """
        if self.state.input_currency == InputCurrency.HKD:
            return value / self.state.exchange_rate
        return value

    def on_input_change(self, value: str, input_index: int = 1) -> None:
        """
        处理输入变化
        
        Args:
            value: 输入值
            input_index: 输入框索引（1或2）
        """
        # 验证输入
        if self.state.mode == CalculationMode.COST_TO_PRICE:
            field_name = "成本价"
        elif self.state.mode == CalculationMode.PRICE_TO_COST:
            field_name = "卖价"
        else:
            field_name = "成本价" if input_index == 1 else "卖价"
        
        amount, error = InputValidator.validate_amount(value, field_name)

        if error:
            self.state.error_message = error
            self.result = None
            self.on_update_callback()
            return

        # 转换为人民币后更新状态
        cny_value = self._convert_to_cny(float(amount))
        if input_index == 1:
            self.state.input_value = cny_value
        else:
            self.state.input_value2 = cny_value
        self.state.error_message = None

        # 执行计算
        self._calculate()

        # 更新界面
        self.on_update_callback()

    def on_rate_change(self, rate: float) -> None:
        """
        处理毛利率变化
        
        Args:
            rate: 毛利率（小数形式）
        """
        # 验证毛利率
        validated_rate, error = InputValidator.validate_profit_rate(
            rate, self.state.rate_min, self.state.rate_max
        )

        if error:
            self.state.error_message = error
            self.on_update_callback()
            return

        # 更新状态
        self.state.profit_rate = validated_rate
        self.state.error_message = None

        # 如果有输入值，重新计算
        if self.state.input_value is not None:
            self._calculate()

        # 更新界面
        self.on_update_callback()

    def on_mode_change(self, mode: CalculationMode) -> None:
        """
        处理模式切换
        
        Args:
            mode: 新的计算模式
        """
        # 更新模式
        self.state.mode = mode

        # 清空错误信息
        self.state.error_message = None

        # 如果有输入值，用新模式重新计算
        if self.state.input_value is not None:
            if mode == CalculationMode.COST_PRICE_TO_PROFIT:
                # 成本+售价→毛利模式需要两个输入值
                if self.state.input_value2 is not None:
                    self._calculate()
                else:
                    self.result = None
            else:
                self._calculate()
        else:
            self.result = None

        # 更新界面
        self.on_update_callback()

    def on_clear(self) -> None:
        """处理清空"""
        # 清空输入值
        self.state.input_value = None
        self.state.input_value2 = None
        self.state.error_message = None
        self.result = None

        # 保留毛利率设置
        # 更新界面
        self.on_update_callback()

    def on_reset(self) -> None:
        """处理重置"""
        # 恢复所有默认设置
        from config import Config
        self.state.mode = CalculationMode.COST_TO_PRICE
        self.state.input_value = None
        self.state.input_value2 = None
        self.state.profit_rate = Config.DEFAULT_RATE
        self.state.rate_min = Config.DEFAULT_RATE_MIN
        self.state.rate_max = Config.DEFAULT_RATE_MAX
        self.state.exchange_rate = Config.DEFAULT_EXCHANGE_RATE
        self.state.input_currency = InputCurrency.CNY
        self.state.error_message = None
        self.result = None

        # 更新界面
        self.on_update_callback()

    def on_exchange_rate_change(self, rate: float) -> None:
        """
        处理汇率变化

        Args:
            rate: 新的汇率值
        """
        self.state.exchange_rate = rate

        # 如果有计算结果，重新更新界面显示
        if self.result is not None:
            self.on_update_callback()

    def on_currency_change(self, currency: InputCurrency) -> None:
        """
        处理币种切换

        Args:
            currency: 新的币种
        """
        self.state.input_currency = currency
        # 币种切换后需要重新计算（因为输入值的含义变了）
        # 但输入框中的原始值已经不在状态中保存，所以这里只更新界面
        self.on_update_callback()

    def _calculate(self) -> None:
        """执行计算"""
        if self.state.mode == CalculationMode.COST_PRICE_TO_PROFIT:
            # 成本+售价→毛利模式需要两个输入值
            if self.state.input_value is None or self.state.input_value2 is None:
                self.result = None
                return
        else:
            # 其他模式只需要一个输入值
            if self.state.input_value is None:
                self.result = None
                return

        try:
            if self.state.mode == CalculationMode.COST_PRICE_TO_PROFIT:
                # 成本+售价→毛利计算
                cost_price = Decimal(str(self.state.input_value))
                selling_price = Decimal(str(self.state.input_value2))
                
                # 验证卖价必须大于成本价
                if selling_price <= cost_price:
                    self.state.error_message = "卖价必须大于成本价"
                    self.result = None
                    return
            else:
                input_decimal = Decimal(str(self.state.input_value))
                rate_decimal = Decimal(str(self.state.profit_rate))

                if self.state.mode == CalculationMode.COST_TO_PRICE:
                    # 成本→卖价计算
                    selling_price = CalculatorEngine.calculate_selling_price(
                        input_decimal, rate_decimal
                    )
                    cost_price = input_decimal
                else:
                    # 卖价→成本计算
                    cost_price = CalculatorEngine.calculate_cost_price(
                        input_decimal, rate_decimal
                    )
                    selling_price = input_decimal

            # 计算毛利润
            gross_profit = CalculatorEngine.calculate_gross_profit(
                selling_price, cost_price
            )

            # 计算毛利率（百分比形式）
            profit_rate_percent = CalculatorEngine.calculate_profit_rate(
                selling_price, cost_price
            )

            # 创建结果对象
            self.result = CalculationResult(
                cost_price=cost_price,
                selling_price=selling_price,
                gross_profit=gross_profit,
                profit_rate=profit_rate_percent
            )

        except ValueError as e:
            self.state.error_message = str(e)
            self.result = None
