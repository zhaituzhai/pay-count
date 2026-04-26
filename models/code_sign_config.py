"""
代码签名配置模型
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class CodeSignConfig:
    """
    代码签名配置模型

    用于配置代码签名过程的各项参数，包括证书路径、密码、时间戳服务器等。
    """

    # 证书文件路径（.pfx 或 .p12 格式）
    cert_path: Optional[Path] = None

    # 证书密码（从环境变量或安全存储读取，不要明文存储）
    cert_password: Optional[str] = None

    # 时间戳服务器 URL（用于确保证书过期后签名仍然有效）
    timestamp_url: str = "http://timestamp.digicert.com"

    # 签名算法（推荐使用 sha256）
    hash_algorithm: str = "sha256"

    # 是否包含调试信息
    include_debug: bool = False

    # 签名描述（显示在文件属性中）
    description: str = "定价计算器"

    # 签名 URL（可选，可链接到应用官网）
    description_url: Optional[str] = None
