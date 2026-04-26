"""
结果卡片组件
"""
import flet as ft
from typing import Optional
from models.result import CalculationResult
from config import Config


class ResultCard:
    """结果卡片组件"""

    def __init__(self):
        """初始化结果卡片组件"""
        self._page = None  # 页面引用，用于剪贴板操作

        # 人民币结果文本
        self.cost_price_cny_text = ft.Text(
            value="--",
            size=Config.FONT_SIZE_RESULT_DESKTOP - 2,
            weight=ft.FontWeight.BOLD,
            color=Config.COLOR_PRIMARY,
            selectable=True,
        )

        self.selling_price_cny_text = ft.Text(
            value="--",
            size=Config.FONT_SIZE_RESULT_DESKTOP - 2,
            weight=ft.FontWeight.BOLD,
            color=Config.COLOR_PRIMARY,
            selectable=True,
        )

        self.gross_profit_cny_text = ft.Text(
            value="--",
            size=Config.FONT_SIZE_RESULT_DESKTOP - 2,
            weight=ft.FontWeight.BOLD,
            color=Config.COLOR_SECONDARY,
            selectable=True,
        )

        # 港币结果文本
        self.cost_price_hkd_text = ft.Text(
            value="--",
            size=Config.FONT_SIZE_RESULT_DESKTOP - 6,
            weight=ft.FontWeight.W_500,
            color=Config.COLOR_PRIMARY,
            opacity=0.7,
            selectable=True,
        )

        self.selling_price_hkd_text = ft.Text(
            value="--",
            size=Config.FONT_SIZE_RESULT_DESKTOP - 6,
            weight=ft.FontWeight.W_500,
            color=Config.COLOR_PRIMARY,
            opacity=0.7,
            selectable=True,
        )

        self.gross_profit_hkd_text = ft.Text(
            value="--",
            size=Config.FONT_SIZE_RESULT_DESKTOP - 6,
            weight=ft.FontWeight.W_500,
            color=Config.COLOR_SECONDARY,
            opacity=0.7,
            selectable=True,
        )

        self.profit_rate_text = ft.Text(
            value="--",
            size=Config.FONT_SIZE_RESULT_DESKTOP - 2,
            weight=ft.FontWeight.BOLD,
            color=Config.COLOR_SECONDARY,
            selectable=True,
        )

        self.error_text = ft.Text(
            value="",
            size=14,
            color=Config.COLOR_ERROR,
            visible=False,
        )

        # 复制按钮
        self._copy_cost_btn = ft.IconButton(
            icon=ft.Icons.CONTENT_COPY,
            icon_size=16,
            tooltip="复制成本价（人民币+港币）",
            on_click=self._on_copy_cost_price,
        )

        self._copy_selling_btn = ft.IconButton(
            icon=ft.Icons.CONTENT_COPY,
            icon_size=16,
            tooltip="复制卖价（人民币+港币）",
            on_click=self._on_copy_selling_price,
        )

    def set_page(self, page: ft.Page) -> None:
        """设置页面引用，用于剪贴板操作"""
        self._page = page

    def build(self) -> ft.Container:
        """
        构建组件

        Returns:
            Container 组件
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("计算结果", size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=1),
                    self.error_text,
                    ft.Row(
                        controls=[
                            self._create_result_item_dual(
                                "成本价",
                                self.cost_price_cny_text,
                                self.cost_price_hkd_text,
                                copy_btn=self._copy_cost_btn,
                            ),
                            self._create_result_item_dual(
                                "卖价",
                                self.selling_price_cny_text,
                                self.selling_price_hkd_text,
                                copy_btn=self._copy_selling_btn,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    ),
                    ft.Row(
                        controls=[
                            self._create_result_item_dual(
                                "毛利润",
                                self.gross_profit_cny_text,
                                self.gross_profit_hkd_text,
                            ),
                            self._create_result_item("毛利率", self.profit_rate_text),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            padding=15,
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER,
        )

    def update(self, result: CalculationResult, exchange_rate: float = None) -> None:
        """
        更新显示

        Args:
            result: 计算结果
            exchange_rate: 汇率
        """
        display_data = result.to_display_dict(exchange_rate)
        self.cost_price_cny_text.value = display_data["cost_price_cny"]
        self.cost_price_hkd_text.value = display_data["cost_price_hkd"]
        self.selling_price_cny_text.value = display_data["selling_price_cny"]
        self.selling_price_hkd_text.value = display_data["selling_price_hkd"]
        self.gross_profit_cny_text.value = display_data["gross_profit_cny"]
        self.gross_profit_hkd_text.value = display_data["gross_profit_hkd"]
        self.profit_rate_text.value = display_data["profit_rate"]
        self.error_text.visible = False

    def clear(self) -> None:
        """清空所有显示"""
        self.cost_price_cny_text.value = "--"
        self.cost_price_hkd_text.value = "--"
        self.selling_price_cny_text.value = "--"
        self.selling_price_hkd_text.value = "--"
        self.gross_profit_cny_text.value = "--"
        self.gross_profit_hkd_text.value = "--"
        self.profit_rate_text.value = "--"
        self.error_text.visible = False

    def show_error(self, message: str) -> None:
        """
        显示错误信息

        Args:
            message: 错误信息
        """
        self.error_text.value = message
        self.error_text.visible = True
        self.clear()

    def _create_result_item(self, label: str, value_text: ft.Text) -> ft.Column:
        """
        创建结果显示项（单行）

        Args:
            label: 标签
            value_text: 值文本控件

        Returns:
            Column 组件
        """
        return ft.Column(
            controls=[
                ft.Text(label, size=13, color=ft.Colors.ON_SURFACE),
                value_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
        )

    def _create_result_item_dual(
        self, label: str, cny_text: ft.Text, hkd_text: ft.Text,
        copy_btn: ft.IconButton = None,
    ) -> ft.Column:
        """
        创建结果显示项（人民币+港币双行）

        Args:
            label: 标签
            cny_text: 人民币值文本控件
            hkd_text: 港币值文本控件
            copy_btn: 复制按钮（可选）

        Returns:
            Column 组件
        """
        label_row = ft.Row(
            controls=[
                ft.Text(label, size=13, color=ft.Colors.ON_SURFACE),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=4,
        )
        if copy_btn:
            label_row.controls.append(copy_btn)

        return ft.Column(
            controls=[
                label_row,
                cny_text,
                hkd_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
        )

    def _copy_to_clipboard(self, cny_val: str, hkd_val: str, btn: ft.IconButton, label: str) -> None:
        """复制人民币+港币到剪贴板"""
        if cny_val == "--" or hkd_val == "--":
            return
        copy_text = f"{cny_val} / {hkd_val}"
        if self._page:
            import asyncio
            asyncio.ensure_future(self._page.clipboard.set(copy_text))
            btn.icon = ft.Icons.CHECK
            btn.tooltip = "已复制!"
            btn.update()
            import threading
            def restore_icon():
                btn.icon = ft.Icons.CONTENT_COPY
                btn.tooltip = f"复制{label}（人民币+港币）"
                btn.update()
            threading.Timer(1.5, restore_icon).start()

    def _on_copy_cost_price(self, e) -> None:
        """复制成本价（人民币+港币）到剪贴板"""
        self._copy_to_clipboard(
            self.cost_price_cny_text.value,
            self.cost_price_hkd_text.value,
            self._copy_cost_btn,
            "成本价",
        )

    def _on_copy_selling_price(self, e) -> None:
        """复制卖价（人民币+港币）到剪贴板"""
        self._copy_to_clipboard(
            self.selling_price_cny_text.value,
            self.selling_price_hkd_text.value,
            self._copy_selling_btn,
            "卖价",
        )
