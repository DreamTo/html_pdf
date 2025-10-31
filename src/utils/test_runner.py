"""
测试运行器
负责动态导入和运行各种测试脚本
"""

import os
import importlib.util
from typing import Dict, List, Any


class TestRunner:
    """测试脚本运行器"""
    
    def __init__(self):
        # 获取当前文件的目录，然后构建相对于src目录的路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.dirname(current_dir)  # 上一级目录就是src
        
        self.test_scripts = {
            "WeasyPrint": os.path.join(src_dir, "tools", "test_weasyprint.py"),
            "Playwright": os.path.join(src_dir, "tools", "test_playwright.py"),
            "LibreOffice": os.path.join(src_dir, "tools", "test_soffice.py")
        }
    
    def import_test_module(self, module_path: str):
        """动态导入测试模块"""
        try:
            spec = importlib.util.spec_from_file_location("test_module", module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            print(f"导入模块失败 {module_path}: {e}")
            return None
    
    def run_actual_tests(self) -> Dict[str, List[Dict]]:
        """运行实际的测试脚本"""
        print("🚀 开始运行实际转换测试...")
        
        test_results = {}
        
        for tool_name, script_name in self.test_scripts.items():
            print(f"\n📋 运行 {tool_name} 测试...")
            
            try:
                # 导入并运行测试模块
                module = self.import_test_module(script_name)
                if module:
                    if tool_name == "WeasyPrint":
                        results = module.test_weasyprint()
                    elif tool_name == "Playwright":
                        results = module.test_playwright()
                    elif tool_name == "LibreOffice":
                        results = module.test_soffice()
                    
                    test_results[tool_name] = results
                    print(f"✅ {tool_name} 测试完成，处理了 {len(results)} 个样例")
                else:
                    print(f"❌ {tool_name} 测试模块导入失败")
                    test_results[tool_name] = []
                    
            except Exception as e:
                print(f"❌ {tool_name} 测试执行失败: {e}")
                test_results[tool_name] = []
        
        return test_results