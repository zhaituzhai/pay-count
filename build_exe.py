"""
打包脚本
使用 PyInstaller 将应用打包成 Windows 可执行文件，并自动进行代码签名
"""
import PyInstaller.__main__
import sys
import os
from pathlib import Path
from utils.code_signer import CodeSigner
from utils.config_loader import ConfigLoader
from models.code_sign_config import CodeSignConfig


def build_exe() -> Path:
    """
    执行打包流程

    Returns:
        生成的 exe 文件路径
    """
    # 获取当前目录
    current_dir = Path(__file__).parent

    # PyInstaller 参数
    args = [
        'main.py',
        '--name=定价计算器v7',
        '--onefile',
        '--windowed',
        '--clean',
        '--noconfirm',
        f'--add-data={current_dir / "models"};models',
        f'--add-data={current_dir / "controllers"};controllers',
        f'--add-data={current_dir / "views"};views',
        f'--add-data={current_dir / "utils"};utils',
        f'--add-data={current_dir / "config.py"};.',
        # Flet 核心 + 桌面客户端（含 Flutter 引擎二进制文件，离线运行必需）
        '--collect-all=flet',
        '--collect-all=flet_desktop',
        # SSL 证书（打包后 Python 找不到系统 CA 证书，需要 certifi 提供）
        '--collect-all=certifi',
        # 排除不必要的模块以减小文件大小
        '--exclude-module=tkinter',
        '--exclude-module=matplotlib',
        '--exclude-module=numpy',
        '--exclude-module=pandas',
        '--exclude-module=IPython',
        '--exclude-module=jupyter',
        # 优化选项
        '--noupx',
    ]

    print("开始打包...")
    print(f"参数: {args}")

    # 执行打包
    PyInstaller.__main__.run(args)

    # 获取生成的 exe 文件路径
    exe_path = current_dir / "dist" / "定价计算器v7.exe"

    if not exe_path.exists():
        print(f"错误：exe 文件未生成: {exe_path}")
        sys.exit(1)

    print(f"\n打包完成！")
    print(f"可执行文件位于: {exe_path}")

    return exe_path


def sign_exe(exe_path: Path) -> None:
    """
    对 exe 文件进行代码签名

    Args:
        exe_path: exe 文件路径
    """
    print("\n开始代码签名...")

    # 加载配置
    config_path = Path(__file__).parent / "utils" / "cert_config.ini"

    if not config_path.exists():
        print(f"警告：证书配置文件不存在: {config_path}")
        print("跳过代码签名步骤")
        return

    try:
        config = ConfigLoader.load_code_sign_config(config_path)

        # 创建签名工具
        signer = CodeSigner(config)

        # 执行签名
        success, message = signer.sign(exe_path)

        if success:
            print(f"✓ {message}")
            print(f"✓ 签名文件: {exe_path}")

            # 验证签名
            verify_success, verify_message = signer.verify(exe_path)
            if verify_success:
                print(f"✓ {verify_message}")
            else:
                print(f"✗ 签名验证失败: {verify_message}")
        else:
            print(f"✗ 代码签名失败: {message}")
            print("提示：请检查证书配置和权限")

    except Exception as e:
        print(f"✗ 代码签名异常: {e}")
        print("提示：请检查证书配置文件和环境")


def main():
    """主函数"""
    # 执行打包
    exe_path = build_exe()

    # 执行代码签名
    sign_exe(exe_path)

    print("\n所有步骤完成！")
    print(f"最终文件: {exe_path}")


if __name__ == "__main__":
    main()
