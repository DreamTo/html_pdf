#!/usr/bin/env python3
"""
HTML转PDF工具对比评估脚本 (重构版)
对比WeasyPrint、Playwright和LibreOffice的HTML转PDF效果

作者: Assistant
版本: 3.0 - 模块化重构版

主要改进:
- 模块化架构，代码分离更清晰
- 修复WeasyPrint显示问题
- 更好的错误处理和日志记录
- 可扩展的评估框架
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from evaluators.html_to_pdf_evaluator import HTMLToPDFEvaluator


def main():
    """主函数 - 运行HTML转PDF工具评估"""
    try:
        print("🚀 启动HTML转PDF工具评估系统...")
        print("📋 版本: 3.0 (模块化重构版)")
        print("🔧 支持工具: WeasyPrint, Playwright, LibreOffice")
        print("-" * 60)
        
        # 创建评估器实例
        evaluator = HTMLToPDFEvaluator(output_dir="output")
        
        # 运行完整评估
        evaluator.run_complete_evaluation()
        
        print("\n" + "="*60)
        print("✅ 评估完成！")
        print("📄 查看详细报告: output/evaluation_report.html")
        print("📊 查看JSON数据: output/evaluation_results.json")
        print("="*60)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n❌ 用户中断评估")
        return 1
    except Exception as e:
        print(f"\n❌ 评估过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())