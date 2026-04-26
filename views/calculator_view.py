"""
普通计算器视图
"""
import flet as ft
from models.calculator_state import CalculatorState
from controllers.calculator_controller import CalculatorController
from config import Config


class CalculatorView:
    def __init__(self, state: CalculatorState, controller: CalculatorController, page: ft.Page):
        self.state = state
        self.controller = controller
        self.page = page

        self._display_text = ft.Text(
            value="0",
            size=36,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.RIGHT,
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
        )

        self._expression_text = ft.Text(
            value="",
            size=16,
            color=ft.Colors.ON_SURFACE_VARIANT,
            text_align=ft.TextAlign.RIGHT,
            max_lines=1,
        )

        self._history_column = ft.Column(
            controls=[],
            spacing=4,
        )

    def build(self) -> ft.Column:
        btn_style = {
            "width": 70,
            "height": 55,
        }

        digit_btn = lambda t: ft.ElevatedButton(
            content=ft.Text(t),
            on_click=self._on_digit,
            **btn_style,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )

        op_btn = lambda t, color=Config.COLOR_PRIMARY: ft.ElevatedButton(
            content=ft.Text(t),
            on_click=self._on_operator,
            **btn_style,
            bgcolor=color,
            color=ft.Colors.ON_PRIMARY,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )

        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            self._expression_text,
                            self._display_text,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                    padding=ft.padding.only(left=10, right=10, top=15, bottom=10),
                    border_radius=10,
                    bgcolor=ft.Colors.SURFACE_CONTAINER,
                    width=310,
                ),
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(ft.Text("C"), on_click=self._on_clear, **btn_style, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                                ft.ElevatedButton(ft.Text("⌫"), on_click=self._on_backspace, **btn_style, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                                ft.ElevatedButton(ft.Text("%"), on_click=self._on_percent, **btn_style, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                                op_btn("÷"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5,
                        ),
                        ft.Row(
                            controls=[
                                digit_btn("7"),
                                digit_btn("8"),
                                digit_btn("9"),
                                op_btn("×"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5,
                        ),
                        ft.Row(
                            controls=[
                                digit_btn("4"),
                                digit_btn("5"),
                                digit_btn("6"),
                                op_btn("-"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5,
                        ),
                        ft.Row(
                            controls=[
                                digit_btn("1"),
                                digit_btn("2"),
                                digit_btn("3"),
                                op_btn("+"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5,
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(ft.Text("±"), on_click=self._on_toggle_sign, **btn_style, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                                digit_btn("0"),
                                digit_btn("."),
                                ft.ElevatedButton(ft.Text("="), on_click=self._on_equals, **btn_style, bgcolor=Config.COLOR_SECONDARY, color=ft.Colors.ON_PRIMARY, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                ),
                ft.Container(height=8),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("最近记录", size=14, weight=ft.FontWeight.BOLD),
                            ft.Divider(height=1),
                            self._history_column,
                        ],
                        spacing=4,
                    ),
                    padding=15,
                    border_radius=10,
                    bgcolor=ft.Colors.SURFACE_CONTAINER,
                    width=310,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        )

    def update_display(self) -> None:
        self._display_text.value = self.state.display
        self._expression_text.value = self.state.expression
        self._update_history()
        self._display_text.update()
        self._expression_text.update()
        self._history_column.update()

    def _update_history(self) -> None:
        self._history_column.controls = []
        if not self.state.history:
            self._history_column.controls.append(
                ft.Text("暂无记录", size=12, color=ft.Colors.ON_SURFACE_VARIANT, italic=True)
            )
        else:
            for record in self.state.history:
                self._history_column.controls.append(
                    ft.Text(
                        record.to_display(),
                        size=13,
                        selectable=True,
                    )
                )

    def _on_digit(self, e) -> None:
        self.controller.input_digit(e.control.content.value)
        self.update_display()

    def _on_operator(self, e) -> None:
        self.controller.input_operator(e.control.content.value)
        self.update_display()

    def _on_equals(self, e) -> None:
        self.controller.calculate()
        self.update_display()

    def _on_clear(self, e) -> None:
        self.controller.state.clear()
        self.update_display()

    def _on_backspace(self, e) -> None:
        self.controller.backspace()
        self.update_display()

    def _on_percent(self, e) -> None:
        self.controller.input_percent()
        self.update_display()

    def _on_toggle_sign(self, e) -> None:
        self.controller.toggle_sign()
        self.update_display()
