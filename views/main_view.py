"""
主视图
"""
import flet as ft
from models.state import AppState, CalculationMode
from controllers.event_handler import EventHandler
from views.input_section import InputSection
from views.result_card import ResultCard
from views.calculator_view import CalculatorView
from config import Config


class MainView:
    """主视图"""

    def __init__(self, state: AppState, event_handler: EventHandler, page: ft.Page,
                 calculator_view: CalculatorView = None):
        """
        初始化主视图

        Args:
            state: 应用状态
            event_handler: 事件处理器
            page: Flet 页面对象
            calculator_view: 普通计算器视图
        """
        self.state = state
        self.event_handler = event_handler
        self.page = page
        self.calculator_view = calculator_view

        # 创建组件
        self.input_section = InputSection(
            on_change=event_handler.on_input_change,
            on_rate_change=event_handler.on_rate_change,
            on_clear=event_handler.on_clear,
            on_reset=event_handler.on_reset,
            on_exchange_rate_change=event_handler.on_exchange_rate_change,
            on_currency_change=event_handler.on_currency_change,
        )

        self.result_card = ResultCard()
        self.result_card.set_page(page)

        # 创建定价计算模式子标签页
        self._pricing_tab_count = 3

        self.pricing_tab_bar = ft.TabBar(
            tabs=[
                ft.Tab(label="成本→卖价"),
                ft.Tab(label="卖价→成本"),
                ft.Tab(label="成本+售价→毛利"),
            ],
            scrollable=False,
            tab_alignment=ft.TabAlignment.FILL,
        )

        self.pricing_tab_bar_view = ft.TabBarView(
            controls=[
                ft.Container(),
                ft.Container(),
                ft.Container(),
            ],
            height=1,
        )

        self.pricing_tabs = ft.Tabs(
            content=ft.Column(
                controls=[self.pricing_tab_bar, self.pricing_tab_bar_view],
            ),
            length=self._pricing_tab_count,
            selected_index=0,
            animation_duration=300,
            on_change=self._on_pricing_tab_change,
        )

        # 定价计算内容
        self._pricing_content = ft.Column(
            controls=[
                ft.Container(
                    content=self.pricing_tabs,
                    padding=5,
                ),
                self.input_section.build(),
                ft.Container(height=10),
                self.result_card.build(),
            ],
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # 普通计算器内容
        self._calculator_content = ft.Container()
        if self.calculator_view:
            self._calculator_content = self.calculator_view.build()

        # 创建顶层标签页
        self._top_tab_count = 2
        self.top_tab_bar = ft.TabBar(
            tabs=[
                ft.Tab(label="定价计算"),
                ft.Tab(label="普通计算器"),
            ],
            scrollable=False,
            tab_alignment=ft.TabAlignment.FILL,
        )

        self.top_tab_bar_view = ft.TabBarView(
            controls=[
                self._pricing_content,
                self._calculator_content,
            ],
            expand=True,
        )

        self.top_tabs = ft.Tabs(
            content=ft.Column(
                controls=[self.top_tab_bar, self.top_tab_bar_view],
                expand=True,
            ),
            length=self._top_tab_count,
            selected_index=0,
            animation_duration=300,
            on_change=self._on_top_tab_change,
        )

    def build(self) -> ft.Column:
        """
        构建主视图

        Returns:
            Column 组件
        """
        return ft.Column(
            controls=[
                self.top_tabs,
            ],
            expand=True,
        )

    def setup_theme(self, is_dark: bool) -> None:
        """
        设置主题

        Args:
            is_dark: 是否为深色模式
        """
        if is_dark:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.page.theme = ft.Theme(
                color_scheme=ft.ColorScheme(
                    primary=Config.COLOR_PRIMARY,
                    secondary=Config.COLOR_SECONDARY,
                    surface_container_lowest=Config.DARK_BACKGROUND,
                    surface=Config.DARK_SURFACE,
                    on_surface_variant=Config.DARK_ON_BACKGROUND,
                    on_surface=Config.DARK_ON_SURFACE,
                    error=Config.COLOR_ERROR,
                )
            )
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.page.theme = ft.Theme(
                color_scheme=ft.ColorScheme(
                    primary=Config.COLOR_PRIMARY,
                    secondary=Config.COLOR_SECONDARY,
                    surface_container_lowest=Config.LIGHT_BACKGROUND,
                    surface=Config.LIGHT_SURFACE,
                    on_surface_variant=Config.LIGHT_ON_BACKGROUND,
                    on_surface=Config.LIGHT_ON_SURFACE,
                    error=Config.COLOR_ERROR,
                )
            )

    def on_resize(self, width: int) -> None:
        """
        处理窗口大小变化

        Args:
            width: 窗口宽度
        """
        is_mobile = width <= Config.MOBILE_BREAKPOINT

        font_size_result = (
            Config.FONT_SIZE_RESULT_MOBILE if is_mobile
            else Config.FONT_SIZE_RESULT_DESKTOP
        )

        self.result_card.cost_price_cny_text.size = font_size_result
        self.result_card.selling_price_cny_text.size = font_size_result
        self.result_card.gross_profit_cny_text.size = font_size_result
        self.result_card.profit_rate_text.size = font_size_result

        font_size_hkd = font_size_result - 4
        self.result_card.cost_price_hkd_text.size = font_size_hkd
        self.result_card.selling_price_hkd_text.size = font_size_hkd
        self.result_card.gross_profit_hkd_text.size = font_size_hkd

    def update_result(self) -> None:
        """更新结果显示"""
        if self.state.error_message:
            self.result_card.show_error(self.state.error_message)
        elif self.event_handler.result:
            self.result_card.update(self.event_handler.result, self.state.exchange_rate)
        else:
            self.result_card.clear()

    def update_mode(self) -> None:
        """更新模式显示"""
        if self.state.mode == CalculationMode.COST_TO_PRICE:
            self.pricing_tabs.selected_index = 0
            self.input_section.set_mode(CalculationMode.COST_TO_PRICE)
        elif self.state.mode == CalculationMode.PRICE_TO_COST:
            self.pricing_tabs.selected_index = 1
            self.input_section.set_mode(CalculationMode.PRICE_TO_COST)
        else:  # COST_PRICE_TO_PROFIT
            self.pricing_tabs.selected_index = 2
            self.input_section.set_mode(CalculationMode.COST_PRICE_TO_PROFIT)

        self.input_section.set_currency(self.state.input_currency)

    def _on_pricing_tab_change(self, e) -> None:
        """定价计算子标签页切换事件处理"""
        selected_index = int(e.data)
        if selected_index == 0:
            self.event_handler.on_mode_change(CalculationMode.COST_TO_PRICE)
        elif selected_index == 1:
            self.event_handler.on_mode_change(CalculationMode.PRICE_TO_COST)
        else:
            self.event_handler.on_mode_change(CalculationMode.COST_PRICE_TO_PROFIT)

    def _on_top_tab_change(self, e) -> None:
        """顶层标签页切换事件处理"""
        selected_index = int(e.data)
        if self.calculator_view:
            self.calculator_view.set_focused(selected_index == 1)
