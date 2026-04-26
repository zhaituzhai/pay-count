# 代码签名配置说明

## 概述

本文档说明如何配置代码签名证书，以便在打包 Windows exe 文件时自动进行签名。

## 配置步骤

### 1. 准备代码签名证书

确保您拥有有效的代码签名证书文件（.pfx 或 .p12 格式）。代码签名证书可以从以下机构获取：
- DigiCert
- Sectigo
- GlobalSign
- 其他受信任的证书颁发机构

### 2. 放置证书文件

将证书文件放置在项目目录中，建议创建 `certs/` 目录：

```
pay-count/
├── certs/
│   └── my_cert.pfx
├── utils/
│   └── cert_config.ini
└── ...
```

### 3. 创建配置文件

复制 `utils/cert_config.ini.example` 为 `utils/cert_config.ini`：

```bash
copy utils\cert_config.ini.example utils\cert_config.ini
```

### 4. 编辑配置文件

编辑 `utils/cert_config.ini`，填入正确的配置信息：

```ini
[certificate]
cert_path = certs/my_cert.pfx
timestamp_url = http://timestamp.digicert.com
hash_algorithm = sha256
description = 定价计算器
```

### 5. 设置证书密码（重要）

**推荐方式：使用环境变量**

在 Windows 命令行中设置环境变量：

```bash
# 临时设置（当前命令行窗口有效）
set CODE_SIGN_PASSWORD=your_password

# 永久设置
setx CODE_SIGN_PASSWORD "your_password"
```

**不推荐方式：在配置文件中明文存储**

如果必须使用配置文件存储密码，可以在 `cert_config.ini` 中添加：

```ini
cert_password = your_password
```

⚠️ **警告：** 请勿将包含密码的 `cert_config.ini` 提交到版本控制系统！

### 6. 验证配置

运行打包脚本验证配置是否正确：

```bash
python build_exe.py
```

如果配置正确，您将看到：

```
开始打包...
...
打包完成！
可执行文件位于: dist\定价计算器.exe

开始代码签名...
✓ 代码签名成功
✓ 签名文件: dist\定价计算器.exe
✓ 数字签名有效
```

## 配置项说明

| 配置项 | 说明 | 必需 | 默认值 |
|--------|------|------|--------|
| cert_path | 证书文件路径 | 是 | 无 |
| cert_password | 证书密码 | 是 | 无 |
| timestamp_url | 时间戳服务器 URL | 是 | http://timestamp.digicert.com |
| hash_algorithm | 签名算法 | 是 | sha256 |
| description | 签名描述 | 是 | 定价计算器 |
| description_url | 签名 URL | 否 | 无 |
| include_debug | 是否包含调试信息 | 否 | false |

## 安全注意事项

1. **不要提交敏感信息到版本控制**
   - 将 `utils/cert_config.ini` 添加到 `.gitignore`
   - 不要将证书文件提交到版本控制

2. **使用环境变量存储密码**
   - 优先使用 `CODE_SIGN_PASSWORD` 环境变量
   - 避免在配置文件中明文存储密码

3. **定期更新证书**
   - 监控证书有效期
   - 及时续期或更换证书

4. **限制证书访问权限**
   - 设置证书文件权限为仅所有者可读写
   - 不要在公共网络上传输证书

## 常见问题

### Q: signtool.exe 未找到

A: 请安装 Windows SDK，确保 signtool.exe 在系统 PATH 中或使用完整路径。

### Q: 签名失败，提示密码错误

A: 检查环境变量 `CODE_SIGN_PASSWORD` 是否正确设置，或配置文件中的密码是否正确。

### Q: 时间戳服务器不可用

A: 系统会自动尝试不带时间戳的签名。如需使用时间戳，可以更换其他时间戳服务器：
- http://timestamp.sectigo.com
- http://timestamp.globalsign.com/scripts/timstamp.dll

### Q: 如何验证签名是否成功？

A: 右键点击 exe 文件 -> 属性 -> 数字签名，查看签名信息。

## 禁用代码签名

如果暂时不需要代码签名，可以：

1. 删除或重命名 `utils/cert_config.ini` 文件
2. 打包脚本将自动跳过签名步骤

## 技术支持

如有问题，请联系开发团队或查看项目文档。
