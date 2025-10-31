# HTML转PDF工具对比评估系统

这是一个用于对比评估不同HTML转PDF工具性能的综合评估系统，支持WeasyPrint、Playwright和LibreOffice三种工具的客观评估和性能对比。

## 🛠️ 支持的工具

### 1. WeasyPrint
- **类型**: Python库，专门用于HTML/CSS到PDF转换
- **优势**: 对CSS支持良好，轻量级，快速
- **适用场景**: 静态HTML内容，报告生成，文档转换

### 2. Playwright
- **类型**: 浏览器自动化工具
- **优势**: 支持JavaScript，渲染效果接近真实浏览器，字体保留好
- **适用场景**: 动态内容，复杂交互页面，高保真转换

### 3. LibreOffice (soffice)
- **类型**: 办公套件的命令行工具
- **优势**: 无需额外依赖，支持多种格式，稳定可靠
- **适用场景**: 简单HTML转换，已有LibreOffice环境

## 📊 评估指标

### 客观评估指标
- **文件大小和压缩效率**: 评估生成PDF的文件大小优化
- **文本保留率**: 检查文本内容的完整性
- **中文支持**: 评估中文字符的显示效果
- **特殊字符支持**: 测试特殊符号和Unicode字符
- **图片支持率**: 检查图片的转换和显示
- **字体保留率**: 评估字体样式的保持程度
- **表单支持率**: 测试HTML表单元素的转换
- **页面结构评分**: 评估布局和结构的保持
- **转换成功率**: 统计转换成功的比例

### 综合评分
基于多个客观指标的加权平均，满分100分，为用户提供直观的工具选择建议。

## 📁 项目结构

```
script/
├── README.md                    # 项目说明文档
├── requirements.txt             # Python依赖
├── pyproject.toml              # 项目配置
├── uv.lock                     # 依赖锁定文件
├── src/                        # 源代码目录
│   ├── compare_simple.py       # 主评估脚本
│   ├── evaluators/             # 评估器模块
│   │   ├── __init__.py
│   │   └── html_to_pdf_evaluator.py
│   ├── generators/             # 报告生成器
│   │   ├── __init__.py
│   │   └── html_report_generator.py
│   ├── models/                 # 数据模型
│   │   ├── __init__.py
│   │   ├── evaluation_models.py
│   │   └── objective_evaluation.py
│   ├── tools/                  # 工具测试脚本
│   │   ├── test_playwright.py
│   │   ├── test_soffice.py
│   │   └── test_weasyprint.py
│   ├── utils/                  # 工具函数
│   │   ├── __init__.py
│   │   ├── file_operations.py
│   │   ├── pdf_analyzer.py
│   │   └── test_runner.py
│   └── test_data/              # 测试数据
│       ├── samples/            # HTML样例文件
│       └── outputs/            # 生成的PDF文件
└── output/                     # 评估结果输出
    ├── evaluation_report.html  # HTML评估报告
    └── evaluation_results.json # JSON评估数据
```

## 🚀 快速开始

### 系统要求

| 组件 | 最低版本 | 推荐版本 | 说明 |
|------|----------|----------|------|
| **Python** | 3.8+ | 3.12+ | 项目开发和测试版本 |
| **操作系统** | - | macOS/Linux | Windows需额外配置 |
| **内存** | 2GB | 4GB+ | 用于PDF处理和浏览器渲染 |

### 📦 依赖管理

本项目使用 **uv** 进行依赖管理，获得最佳性能和体验：

```bash
# 安装uv包管理器
curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆项目
git clone <repository-url>
cd script

# 自动创建虚拟环境并安装依赖
uv sync

# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate     # Windows
```

### 🔧 系统依赖安装

#### 1. LibreOffice (必需)
```bash
# macOS
brew install libreoffice

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install libreoffice

# CentOS/RHEL
sudo yum install libreoffice

# Windows
# 从官网下载: https://www.libreoffice.org/download/
```

#### 2. Playwright 浏览器 (必需)
```bash
# 安装浏览器 (在虚拟环境中执行)
playwright install chromium

# 如果网络较慢，可以设置镜像
export PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/
playwright install chromium
```

#### 3. WeasyPrint 系统依赖 (macOS)
```bash
# 安装系统库
brew install glib gobject-introspection

# 设置环境变量 (添加到 ~/.zshrc 或 ~/.bash_profile)
export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH
```

### 🚀 启动项目

#### 快速验证安装
```bash
# 验证Python环境
python --version

# 验证核心依赖
python -c "import weasyprint, playwright, pydantic; print('✅ 核心依赖安装成功')"

# 验证LibreOffice
soffice --version

# 验证Playwright浏览器
playwright --version
```

#### 运行完整评估
```bash
# 进入项目目录
cd /Users/jay/Desktop/script

# 激活虚拟环境
source .venv/bin/activate

# 运行评估脚本
python src/compare_simple.py

# 等待评估完成 (通常需要1-3分钟)
```

#### 查看评估结果
```bash
# 方式一：直接打开HTML报告
open output/evaluation_report.html  # macOS
xdg-open output/evaluation_report.html  # Linux

# 方式二：启动本地服务器
python -m http.server 8000
# 浏览器访问: http://localhost:8000/output/evaluation_report.html

# 方式三：查看JSON数据
cat output/evaluation_results.json | python -m json.tool
```

### 🧪 单独测试工具

```bash
# 测试WeasyPrint
python src/tools/test_weasyprint.py

# 测试Playwright (需要浏览器)
python src/tools/test_playwright.py

# 测试LibreOffice
python src/tools/test_soffice.py

# 查看生成的PDF文件
ls -la src/test_data/outputs/
```

### 📊 依赖更新

#### 更新所有依赖
```bash
# 更新所有依赖到最新版本
uv sync --upgrade
```

#### 更新特定依赖
```bash
# 更新特定包
uv add playwright@latest
uv add weasyprint@latest

# 重新安装Playwright浏览器
playwright install chromium

# 检查依赖版本
uv pip list | grep -E "(playwright|weasyprint|pydantic)"
```

## 📊 最新评估结果

### 综合评分 (满分100分)

| 工具 | 综合评分 | 成功率 | 推荐度 |
|------|----------|--------|--------|
| **Playwright** | **88.9** | 100% | ⭐⭐⭐⭐⭐ |
| WeasyPrint | 88.3 | 100% | ⭐⭐⭐⭐ |
| LibreOffice | 88.3 | 100% | ⭐⭐⭐⭐ |

### 详细指标对比

| 指标 | WeasyPrint | Playwright | LibreOffice |
|------|------------|------------|-------------|
| 平均文件大小 | 795.8KB | 162.7KB | 349.0KB |
| 压缩效率 | 67.3% | 64.9% | 64.8% |
| 文本保留率 | 93.0% | 95.9% | 93.0% |
| 内容密度 | 68.6% | 66.3% | 66.3% |
| 中文支持 | 100% | 100% | 100% |
| 特殊字符支持 | 100% | 100% | 100% |
| 图片支持率 | 100% | 100% | 100% |
| 字体保留率 | 100% | 100% | 100% |
| 表单支持率 | 30% | 60% | 30% |
| 页面结构 | 55.6% | 66.7% | 66.7% |

### 功能支持

| 功能 | WeasyPrint | Playwright | LibreOffice |
|------|------------|------------|-------------|
| 静态HTML | ✅ | ✅ | ✅ |
| CSS样式 | ✅ | ✅ | ⚠️ |
| JavaScript | ❌ | ✅ | ❌ |
| 中文字体 | ✅ | ✅ | ✅ |
| 复杂布局 | ✅ | ✅ | ⚠️ |
| 动态内容 | ❌ | ✅ | ❌ |
| 表单元素 | ⚠️ | ✅ | ⚠️ |

## 🔧 高级配置

### 环境变量配置

为了确保所有工具正常工作，建议在 `~/.zshrc` 或 `~/.bash_profile` 中添加以下环境变量：

```bash
# WeasyPrint库路径 (macOS)
export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH

# Playwright下载镜像 (可选，提升下载速度)
export PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/

# Python路径 (如果使用pyenv)
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
```

### 开发环境配置

#### 添加新依赖
```bash
# 添加新的依赖包
uv add package_name

# 添加开发依赖
uv add --dev package_name

# 添加指定版本的依赖
uv add "package_name>=1.0.0"
```

#### 虚拟环境管理
```bash
# 创建虚拟环境
uv venv

# 激活虚拟环境
source .venv/bin/activate

# 退出虚拟环境
deactivate

# 删除虚拟环境
rm -rf .venv
```

### 性能优化配置

#### Playwright优化
```bash
# 仅安装需要的浏览器
playwright install chromium

# 设置浏览器路径 (可选)
export PLAYWRIGHT_BROWSERS_PATH=/path/to/browsers
```

#### WeasyPrint优化
```bash
# 字体缓存优化 (Linux)
fc-cache -fv

# 内存限制设置 (大文件处理)
export WEASYPRINT_DPI=96
export WEASYPRINT_OPTIMIZE_SIZE=true
```

## 📝 使用建议

### 选择WeasyPrint当：
- 需要快速转换静态HTML
- 对CSS支持要求高
- 生成报告或文档
- 文件大小不是主要考虑因素

### 选择Playwright当：
- 页面包含JavaScript
- 需要处理动态内容
- 要求高保真度渲染
- 需要最佳的表单支持
- 文件大小优化重要

### 选择LibreOffice当：
- 环境中已安装LibreOffice
- 需要简单的HTML转换
- 不想安装额外依赖
- 对文件大小有中等要求

## 🐛 常见问题

### WeasyPrint问题
- **libgobject错误**: 安装gobject-introspection
- **字体问题**: 确保系统字体可访问

### Playwright问题
- **浏览器下载失败**: 检查网络连接，使用`playwright install`
- **渲染超时**: 增加页面加载等待时间

### LibreOffice问题
- **命令未找到**: 确保LibreOffice已正确安装
- **权限问题**: 检查输出目录写入权限

## 📄 输出文件

所有生成的PDF文件保存在 `src/test_data/outputs/` 目录中：

- `base_weasyprint.pdf` / `base_playwright.pdf` / `base_soffice.pdf`
- `complex_weasyprint.pdf` / `complex_playwright.pdf` / `complex_soffice.pdf`
- `dynamic_weasyprint.pdf` / `dynamic_playwright.pdf` / `dynamic_soffice.pdf`
- `chinese_weasyprint.pdf` / `chinese_playwright.pdf` / `chinese_soffice.pdf`

## 🔍 结论

根据最新的评估结果：

- **最佳综合性能**: Playwright (88.9分) - 在文本保留、表单支持和页面结构方面表现最佳
- **最小文件大小**: Playwright (162.7KB) - 文件压缩效果最好
- **最快转换速度**: WeasyPrint - 适合批量处理静态内容
- **最简环境**: LibreOffice - 无需额外Python依赖

**推荐选择**：
1. **首选**: Playwright - 综合性能最佳，特别适合需要高质量输出的场景
2. **备选**: WeasyPrint - 适合静态内容的快速转换
3. **简化**: LibreOffice - 适合简单需求和已有环境