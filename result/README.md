# HTML转PDF工具评估报告 - 独立打包版

这是一个完整的、可独立使用的评估报告包，包含了所有必要的文件。

## 文件结构

```
result/
├── evaluation_report.html    # 主要的HTML评估报告
├── evaluation_results.json   # 原始评估数据（JSON格式）
├── pdfs/                     # 所有生成的PDF文件
│   ├── base_*.pdf           # 基础测试用例的PDF输出
│   ├── chinese_*.pdf        # 中文测试用例的PDF输出
│   ├── complex_*.pdf        # 复杂布局测试用例的PDF输出
│   ├── dynamic_*.pdf        # 动态内容测试用例的PDF输出
│   ├── forms_*.pdf          # 表单测试用例的PDF输出
│   ├── long_document_*.pdf  # 长文档测试用例的PDF输出
│   ├── print_styles_*.pdf   # 打印样式测试用例的PDF输出
│   ├── special_chars_*.pdf  # 特殊字符测试用例的PDF输出
│   └── svg_*.pdf            # SVG测试用例的PDF输出
└── README.md                # 本说明文件
```

## 使用方法

1. **查看报告**: 直接在浏览器中打开 `evaluation_report.html` 文件
2. **查看PDF**: 在HTML报告中点击"查看PDF"链接可以直接查看对应的PDF文件
3. **数据分析**: 可以使用 `evaluation_results.json` 进行进一步的数据分析

## 特点

- **完全独立**: 这个文件夹包含了查看报告所需的所有文件
- **相对路径**: HTML文件中的PDF链接使用相对路径，确保在任何位置都能正常工作
- **便于分享**: 可以直接压缩整个文件夹进行分享或归档

## 工具对比

报告包含了以下三个HTML转PDF工具的详细对比：
- **WeasyPrint**: 专业的HTML/CSS转PDF工具
- **Playwright**: 基于浏览器引擎的转换工具
- **LibreOffice**: 开源办公套件的转换功能

每个工具都在9个不同的测试用例上进行了评估，包括基础布局、中文支持、复杂样式、动态内容、表单处理、长文档、打印样式、特殊字符和SVG支持等方面。