"""
定价计算器应用入口
"""
import flet as ft
import sys
import os
import ssl
from models.state import AppState
from models.calculator_state import CalculatorState
from controllers.event_handler import EventHandler
from controllers.calculator_controller import CalculatorController
from views.main_view import MainView
from views.calculator_view import CalculatorView
from config import Config
from models.single_instance_config import SingleInstanceConfig
from utils.single_instance import SingleInstanceManager


# PyInstaller 打包环境下的离线运行支持
if getattr(sys, 'frozen', False):
    # 1. 修复 SSL 证书路径（打包后 Python 找不到系统 CA 证书）
    import certifi
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    ssl._create_default_https_context = lambda: ssl.create_default_context(
        cafile=certifi.where()
    )

    # 2. 预加载 flet_desktop，让 Flet 跳过运行时 pip 安装
    try:
        import flet_desktop  # noqa: F401
    except ImportError:
        print("错误：flet_desktop 未被打包进 exe，请检查打包配置")
        sys.exit(1)


def main(page: ft.Page) -> None:
    """
    应用主函数

    Args:
        page: Flet 页面对象
    """
    # 单实例检测
    single_instance_config = SingleInstanceConfig()
    single_instance_manager = SingleInstanceManager(single_instance_config)

    # 检查是否为第一个实例
    if not single_instance_manager.check_instance():
        # 不是第一个实例，激活已存在的实例并退出
        single_instance_manager.activate_existing_instance()
        single_instance_manager.show_notification()
        sys.exit(0)

    # 设置页面标题
    page.title = "定价计算器"

    # 设置窗口大小
    page.window.width = 500
    page.window.height = 835

    # 创建应用状态
    state = AppState()

    # 创建普通计算器状态和控制器
    calc_state = CalculatorState()
    calc_controller = CalculatorController(calc_state)

    # 创建界面更新回调函数
    def update_ui() -> None:
        """更新界面"""
        main_view.update_result()
        main_view.update_mode()
        page.update()

    # 创建事件处理器
    event_handler = EventHandler(state, update_ui)

    # 创建普通计算器视图
    calculator_view = CalculatorView(calc_state, calc_controller, page)

    # 创建主视图
    main_view = MainView(state, event_handler, page, calculator_view=calculator_view)

    # 设置主题
    main_view.setup_theme(state.is_dark_mode)

    # 添加主视图到页面
    page.add(main_view.build())

    # 设置窗口大小变化事件处理
    def on_resize(e) -> None:
        """窗口大小变化事件处理"""
        main_view.on_resize(page.width)
        page.update()

    page.on_resize = on_resize

    # 注册退出时的资源清理
    def on_close(e):
        """窗口关闭事件处理"""
        single_instance_manager.release()
        page.window.destroy()

    page.window.on_close = on_close


if __name__ == "__main__":
    ft.run(main)
