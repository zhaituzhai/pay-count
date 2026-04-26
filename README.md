# 定价计算器应用

一个基于 Python 和 Flet 框架开发的跨平台定价计算器应用，专为 Windows 平台优化。

## 功能特性

- **成本→卖价计算**：输入成本价和毛利率，自动计算卖价
- **卖价→成本计算**：输入卖价和毛利率，自动计算成本价
- **成本+售价→毛利计算**：输入成本价和售价，自动计算毛利润和毛利率
- **毛利率调节**：提供滑块调整毛利率（默认范围 25%-33%）
- **计算结果展示**：显示卖价、成本价、毛利润、毛利率
- **深色模式支持**：自动应用深色主题
- **响应式布局**：适配不同屏幕尺寸
- **Windows 优化**：专为 Windows 平台设计和优化

## 技术栈

- Python 3.7+
- Flet 0.21.0+

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行应用

### 桌面端运行

```bash
python main.py
```

### Web 端运行

```bash
flet run main.py --web
```

## 项目结构

```
pricing-calculator/
├── main.py                 # 应用入口
├── config.py               # 配置文件
├── requirements.txt        # 依赖清单
├── models/                 # 数据模型层
│   ├── __init__.py
│   ├── state.py           # 应用状态模型
│   └── result.py          # 计算结果模型
├── controllers/           # 控制器层
│   ├── __init__.py
│   ├── calculator.py      # 计算引擎
│   └── event_handler.py   # 事件处理器
├── views/                 # 视图层
│   ├── __init__.py
│   ├── main_view.py       # 主视图
│   ├── input_section.py   # 输入区域组件
│   └── result_card.py     # 结果卡片组件
├── utils/                 # 工具类
│   ├── __init__.py
│   ├── formatter.py       # 格式化工具
│   ├── validator.py       # 输入验证器
│   └── errors.py          # 错误类型定义
└── tests/                 # 测试模块
    ├── __init__.py
    ├── test_calculator.py # 计算引擎测试
    └── test_validator.py  # 验证器测试
```

## 计算公式

- 卖价 = 成本 ÷ (1 - 毛利率)
- 成本 = 卖价 × (1 - 毛利率)
- 毛利率 = (卖价 - 成本) ÷ 卖价 × 100%

## 使用说明

### 模式 1：成本→卖价
1. 选择"成本→卖价"标签页
2. 在输入框中输入成本价
3. 使用滑块调整毛利率
4. 计算结果会实时显示卖价、毛利润等

### 模式 2：卖价→成本
1. 选择"卖价→成本"标签页
2. 在输入框中输入卖价
3. 使用滑块调整毛利率
4. 计算结果会实时显示成本价、毛利润等

### 模式 3：成本+售价→毛利
1. 选择"成本+售价→毛利"标签页
2. 在第一个输入框中输入成本价
3. 在第二个输入框中输入售价
4. 计算结果会实时显示毛利润和毛利率

### 通用操作
- 点击"清空"按钮清空输入，保留毛利率设置
- 点击"重置"按钮恢复所有默认设置

## 测试

运行测试脚本：

```bash
python run_tests.py
```

## 打包发布

### Windows

```bash
flet pack main.py --name "定价计算器"
```

### macOS

```bash
flet pack main.py --name "定价计算器" --target macos
```

### Linux

```bash
flet pack main.py --name "定价计算器" --target linux
```

## 许可证

MIT License
