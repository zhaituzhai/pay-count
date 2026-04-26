"""
代码签名工具
使用 signtool.exe 对 exe 文件进行 Authenticode 签名
"""
import subprocess
import os
from pathlib import Path
from typing import Optional
from models.code_sign_config import CodeSignConfig


class CodeSigner:
    """代码签名工具"""

    def __init__(self, config: CodeSignConfig):
        """
        初始化代码签名工具

        Args:
            config: 代码签名配置
        """
        self.config = config
        self.signtool_path = self._find_signtool()

    def _find_signtool(self) -> Optional[Path]:
        """
        查找 signtool.exe 路径

        Returns:
            signtool.exe 的完整路径，如果未找到则返回 None
        """
        # 常见的 Windows SDK 路径
        possible_paths = [
            Path("C:/Program Files (x86)/Windows Kits/10/bin/10.0.19041.0/x64/signtool.exe"),
            Path("C:/Program Files (x86)/Windows Kits/10/bin/10.0.18362.0/x64/signtool.exe"),
            Path("C:/Program Files (x86)/Windows Kits/8.1/bin/x64/signtool.exe"),
        ]

        # 搜索可能的路径
        for path in possible_paths:
            if path.exists():
                return path

        # 尝试从 PATH 环境变量查找
        for path_dir in os.environ.get("PATH", "").split(os.pathsep):
            signtool_path = Path(path_dir) / "signtool.exe"
            if signtool_path.exists():
                return signtool_path

        return None

    def sign(self, exe_path: Path) -> tuple[bool, str]:
        """
        对 exe 文件进行代码签名

        Args:
            exe_path: exe 文件路径

        Returns:
            (是否成功, 错误信息)
        """
        # 验证输入
        if not exe_path.exists():
            return False, f"文件不存在: {exe_path}"

        if not self.config.cert_path or not self.config.cert_path.exists():
            return False, f"证书文件不存在: {self.config.cert_path}"

        if not self.signtool_path:
            return False, "未找到 signtool.exe，请安装 Windows SDK"

        # 构建签名命令
        cmd = [
            str(self.signtool_path),
            "sign",
            "/f", str(self.config.cert_path),
            "/p", self.config.cert_password,
            "/t", self.config.timestamp_url,
            "/fd", self.config.hash_algorithm,
            "/d", self.config.description,
        ]

        # 添加可选参数
        if self.config.description_url:
            cmd.extend(["/du", self.config.description_url])

        if self.config.include_debug:
            cmd.append("/debug")

        # 添加文件路径
        cmd.append(str(exe_path))

        try:
            # 执行签名命令
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30  # 30秒超时
            )

            # 检查执行结果
            if result.returncode == 0:
                return True, "代码签名成功"
            else:
                # 检查是否是时间戳服务器不可用
                if "timestamp server" in result.stderr.lower():
                    # 尝试不带时间戳的签名
                    return self._sign_without_timestamp(exe_path)

                return False, f"签名失败: {result.stderr}"

        except subprocess.TimeoutExpired:
            return False, "签名超时（超过30秒）"
        except Exception as e:
            return False, f"签名异常: {str(e)}"

    def _sign_without_timestamp(self, exe_path: Path) -> tuple[bool, str]:
        """
        不带时间戳的签名（备用方案）

        Args:
            exe_path: exe 文件路径

        Returns:
            (是否成功, 错误信息)
        """
        cmd = [
            str(self.signtool_path),
            "sign",
            "/f", str(self.config.cert_path),
            "/p", self.config.cert_password,
            "/fd", self.config.hash_algorithm,
            "/d", self.config.description,
            str(exe_path)
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                print("警告：代码签名成功，但未添加时间戳")
                return True, "代码签名成功（无时间戳）"
            else:
                return False, f"签名失败: {result.stderr}"

        except Exception as e:
            return False, f"签名异常: {str(e)}"

    def verify(self, exe_path: Path) -> tuple[bool, str]:
        """
        验证 exe 文件的代码签名

        Args:
            exe_path: exe 文件路径

        Returns:
            (是否验证成功, 信息)
        """
        if not self.signtool_path:
            return False, "未找到 signtool.exe"

        cmd = [
            str(self.signtool_path),
            "verify",
            "/pa",
            "/v",
            str(exe_path)
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                return True, "数字签名有效"
            else:
                return False, f"签名验证失败: {result.stderr}"

        except Exception as e:
            return False, f"验证异常: {str(e)}"
