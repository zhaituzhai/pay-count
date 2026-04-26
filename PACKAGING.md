# 定价计算器打包说明

## 方法一：使用 Flet 打包（推荐）

Flet 提供了内置的打包功能，可以轻松将应用打包成 Windows 可执行文件。

### 步骤：

1. **确保已安装 Flet**
   ```bash
   pip install flet
   ```

2. **执行打包命令**
   ```bash
   flet pack main.py --name "定价计算器"
   ```

3. **查找生成的 exe 文件**
   打包完成后，可执行文件通常位于 `dist` 目录中。

## 方法二：使用 PyInstaller 打包

如果 Flet 打包不成功，可以使用 PyInstaller 进行打包。

### 步骤：

1. **安装 PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **执行打包命令**
   ```bash
   pyinstaller --onefile --windowed --name "定价计算器" main.py
   ```

   参数说明：
   - `--onefile`: 打包成单个可执行文件
   - `--windowed`: 窗口模式，不显示控制台
   - `--name`: 设置应用名称

3. **查找生成的 exe 文件**
   可执行文件位于 `dist` 目录中。

## 方法三：使用打包脚本

运行项目中的打包脚本：

```bash
python build_exe.py
```

## 打包后的文件结构

```
dist/
└── 定价计算器.exe    # 可执行文件
```

## 注意事项

1. **首次打包可能较慢**
   PyInstaller 需要分析依赖关系，首次打包可能需要几分钟时间。

2. **文件大小**
   打包后的 exe 文件可能较大（通常 50-100MB），因为包含了 Python 解释器和所有依赖库。

3. **杀毒软件误报**
   某些杀毒软件可能会误报打包的 exe 文件为病毒，这是误报，可以添加信任。

4. **运行环境**
   打包后的 exe 文件可以在没有安装 Python 的 Windows 系统上直接运行。

5. **更新应用**
   如果修改了代码，需要重新执行打包命令。

## 测试打包结果

打包完成后，双击 `dist/定价计算器.exe` 文件即可运行应用。

## 分发应用

可以将打包后的 exe 文件分发给其他用户，他们无需安装 Python 或任何依赖即可使用应用。

## 常见问题

### 问题1：打包失败
- 确保所有依赖都已安装
- 尝试使用管理员权限运行打包命令
- 检查是否有文件被占用

### 问题2：exe 文件无法运行
- 检查杀毒软件是否拦截
- 尝试以管理员权限运行
- 检查 Windows 防火墙设置

### 问题3：文件太大
- 这是正常现象，因为包含了完整的运行环境
- 可以使用 `--onedir` 参数代替 `--onefile` 来减小单个文件大小

## 高级选项

### 自定义图标
```bash
flet pack main.py --name "定价计算器" --icon icon.ico
```

### 添加版本信息
创建 `version.txt` 文件，然后：
```bash
flet pack main.py --name "定价计算器" --version-file version.txt
```

### 隐藏控制台窗口
```bash
flet pack main.py --name "定价计算器" --windowed
```
