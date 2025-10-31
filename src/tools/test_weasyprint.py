from weasyprint import HTML, CSS
import os, time
import logging
import sys

# 配置日志以捕获WeasyPrint的警告
logging.basicConfig(level=logging.WARNING)

# 所有9个HTML测试样例
samples = [
    "base.html", "complex.html", "chinese.html", "dynamic.html",
    "svg.html", "print_styles.html", "forms.html", 
    "long_document.html", "special_chars.html"
]

# 获取当前文件的目录，然后构建相对于src目录的路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)  # 上一级目录就是src

input_dir = os.path.join(src_dir, "test_data", "samples")
output_dir = os.path.join(src_dir, "test_data", "outputs")
os.makedirs(output_dir, exist_ok=True)

def test_weasyprint():
    """运行WeasyPrint转换测试"""
    results = []
    
    for name in samples:
        try:
            start = time.time()
            html_path = os.path.join(input_dir, name)
            output_path = os.path.join(output_dir, name.replace(".html", "_weasyprint.pdf"))
            
            # 检查HTML文件是否存在
            if not os.path.exists(html_path):
                print(f"[WeasyPrint] {name} -> 文件不存在，跳过")
                results.append({
                    "sample": name,
                    "success": False,
                    "time": 0,
                    "error": "文件不存在"
                })
                continue
            
            # 使用更安全的方式处理HTML转换
            try:
                # 读取HTML内容并创建HTML对象
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                html_doc = HTML(string=html_content, base_url=os.path.dirname(html_path))
                
                # 写入PDF，添加更多错误处理
                html_doc.write_pdf(output_path)
                conversion_time = time.time() - start
                
                # 获取文件大小
                file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
                
                print(f"[WeasyPrint] {name} -> done in {conversion_time:.2f}s, size: {file_size} bytes")
                results.append({
                    "sample": name,
                    "success": True,
                    "time": conversion_time,
                    "file_size": file_size,
                    "file_path": output_path,
                    "error": ""
                })
                
            except Exception as e:
                conversion_time = time.time() - start
                error_msg = str(e)
                print(f"[WeasyPrint] {name} -> 转换失败: {error_msg}")
                results.append({
                    "sample": name,
                    "success": False,
                    "time": conversion_time,
                    "file_size": 0,
                    "file_path": "",
                    "error": error_msg
                })
            
        except Exception as e:
            print(f"[WeasyPrint] {name} -> 转换失败: {str(e)}")
            results.append({
                "sample": name,
                "success": False,
                "time": 0,
                "file_size": 0,
                "file_path": "",
                "error": str(e)
            })
    
    return results

if __name__ == "__main__":
    test_weasyprint()
