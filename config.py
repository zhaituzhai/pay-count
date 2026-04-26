"""
定价计算器应用配置文件
定义应用的全局配置常量
"""


class Config:
    """应用配置类"""

    # 默认毛利率范围
    DEFAULT_RATE_MIN = 0.01  # 最小毛利率 1%
    DEFAULT_RATE_MAX = 0.45  # 最大毛利率 45%
    DEFAULT_RATE = 0.25      # 默认毛利率 25%

    # 货币符号
    CURRENCY_SYMBOL_CNY = "¥"     # 人民币符号
    CURRENCY_SYMBOL_HKD = "HK$"  # 港币符号

    # 汇率（1人民币 = X港币）
    DEFAULT_EXCHANGE_RATE = 1.08  # 默认汇率：1 CNY ≈ 1.08 HKD

    # 小数位数
    DECIMAL_PLACES = 2

    # 响应式断点
    MOBILE_BREAKPOINT = 768  # 移动端断点（像素）

    # 性能参数
    DEBOUNCE_DELAY = 100     # 防抖延迟（毫秒）
    SLIDER_THROTTLE = 50     # 滑块节流（毫秒）

    # 界面配置
    MAX_WIDTH_DESKTOP = 600  # 桌面端最大宽度（像素）
    PADDING_MOBILE = 10      # 移动端内边距（像素）
    PADDING_DESKTOP = 20     # 桌面端内边距（像素）

    # 字体大小
    FONT_SIZE_TITLE_MOBILE = 18
    FONT_SIZE_TITLE_DESKTOP = 20
    FONT_SIZE_BODY_MOBILE = 14
    FONT_SIZE_BODY_DESKTOP = 16
    FONT_SIZE_RESULT_MOBILE = 20
    FONT_SIZE_RESULT_DESKTOP = 24

    # 主题颜色
    COLOR_PRIMARY = "#4A90E2"        # 主色调：蓝色
    COLOR_SECONDARY = "#50C878"      # 次要色：绿色
    COLOR_ERROR = "#FF6B6B"          # 错误色：红色

    # 深色主题
    DARK_BACKGROUND = "#1E1E1E"      # 背景色：深灰
    DARK_SURFACE = "#2D2D2D"         # 表面色：中灰
    DARK_ON_BACKGROUND = "#FFFFFF"   # 背景上的文字：白色
    DARK_ON_SURFACE = "#FFFFFF"      # 表面上的文字：白色

    # 浅色主题
    LIGHT_BACKGROUND = "#F5F5F5"     # 背景色：浅灰
    LIGHT_SURFACE = "#FFFFFF"        # 表面色：白色
    LIGHT_ON_BACKGROUND = "#333333"  # 背景上的文字：深灰
    LIGHT_ON_SURFACE = "#333333"     # 表面上的文字：深灰
