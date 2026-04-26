"""
单实例管理器
使用 Windows API 互斥量确保同一时间只有一个应用实例运行
"""
import ctypes
import sys
from typing import Optional
from models.single_instance_config import SingleInstanceConfig


class SingleInstanceManager:
    """
    单实例管理器

    通过 Windows API 互斥量机制检测和防止多个应用实例同时运行。
    """

    def __init__(self, config: SingleInstanceConfig):
        """
        初始化单实例管理器

        Args:
            config: 单实例配置
        """
        self.config = config
        self.mutex: Optional[int] = None
        self.is_first_instance: bool = True

    def check_instance(self) -> bool:
        """
        检查是否为第一个实例

        Returns:
            True 表示第一个实例，False 表示已有实例运行
        """
        try:
            # 尝试创建全局互斥量
            self.mutex = ctypes.windll.kernel32.CreateMutexW(
                None,
                False,
                self.config.mutex_name
            )

            # 检查互斥量是否已存在
            # ERROR_ALREADY_EXISTS = 183
            error_code = ctypes.windll.kernel32.GetLastError()

            if error_code == 183:
                # 互斥量已存在，说明已有实例运行
                self.is_first_instance = False
                return False
            else:
                # 互斥量创建成功，这是第一个实例
                self.is_first_instance = True
                return True

        except Exception as e:
            # 异常情况，默认允许启动
            print(f"单实例检测异常: {e}")
            return True

    def activate_existing_instance(self) -> bool:
        """
        激活已存在的实例窗口

        Returns:
            True 表示激活成功，False 表示激活失败
        """
        if self.is_first_instance:
            return True

        try:
            import win32gui
            import win32con

            # 查找应用主窗口
            def enum_windows_callback(hwnd, _):
                """枚举窗口回调函数"""
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if "定价计算器" in window_title:
                        # 恢复窗口（如果已最小化）
                        if win32gui.IsIconic(hwnd):
                            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

                        # 置顶窗口
                        win32gui.SetForegroundWindow(hwnd)
                        win32gui.SetFocus(hwnd)
                        return False  # 停止枚举
                return True

            win32gui.EnumWindows(enum_windows_callback, None)
            return True

        except ImportError:
            print("未安装 pywin32，无法激活窗口")
            return False
        except Exception as e:
            print(f"激活窗口失败: {e}")
            return False

    def show_notification(self) -> None:
        """显示提示信息"""
        if not self.config.show_notification:
            return

        try:
            import tkinter as tk
            from tkinter import messagebox

            # 创建临时窗口
            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口

            # 显示提示信息
            messagebox.showinfo(
                "提示",
                self.config.notification_text
            )

            # 销毁窗口
            root.destroy()

        except Exception as e:
            print(f"显示提示信息失败: {e}")

    def release(self) -> None:
        """释放互斥量资源"""
        if self.mutex:
            ctypes.windll.kernel32.CloseHandle(self.mutex)
            self.mutex = None

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.release()
