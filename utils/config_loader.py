"""
配置加载器
用于从 INI 文件加载代码签名配置
"""
import configparser
import os
from pathlib import Path
from typing import Optional
from models.code_sign_config import CodeSignConfig


class ConfigLoader:
    """配置加载器"""

    @staticmethod
    def load_code_sign_config(config_path: Path) -> CodeSignConfig:
        """
        加载代码签名配置

        Args:
            config_path: 配置文件路径

        Returns:
            代码签名配置对象

        Raises:
            FileNotFoundError: 配置文件不存在时抛出
        """
        if not config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')

        # 读取证书路径
        cert_path_str = config.get('certificate', 'cert_path', fallback='')
        cert_path = Path(cert_path_str) if cert_path_str else None

        # 读取证书密码（优先从环境变量读取）
        cert_password = os.environ.get('CODE_SIGN_PASSWORD')
        if not cert_password:
            cert_password = config.get('certificate', 'cert_password', fallback=None)

        # 读取其他配置
        timestamp_url = config.get('certificate', 'timestamp_url',
                                   fallback='http://timestamp.digicert.com')
        hash_algorithm = config.get('certificate', 'hash_algorithm',
                                    fallback='sha256')
        description = config.get('certificate', 'description',
                                fallback='定价计算器')
        description_url = config.get('certificate', 'description_url',
                                    fallback=None)
        include_debug = config.getboolean('certificate', 'include_debug',
                                         fallback=False)

        return CodeSignConfig(
            cert_path=cert_path,
            cert_password=cert_password,
            timestamp_url=timestamp_url,
            hash_algorithm=hash_algorithm,
            description=description,
            description_url=description_url,
            include_debug=include_debug
        )
