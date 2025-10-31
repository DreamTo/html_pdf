import subprocess
import os
import time

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

# LibreOffice soffice 转换命令
soffice_cmd = "soffice --headless --convert-to pdf --outdir"

def test_soffice():
    """运行LibreOffice转换测试"""
    results = []
    
    for name in samples:
        try:
            start = time.time()
            input_path = os.path.join(input_dir, name)
            output_path = os.path.join(output_dir, name.replace(".html", "_soffice.pdf"))
            
            # 检查HTML文件是否存在
            if not os.path.exists(input_path):
                print(f"[soffice] {name} -> 文件不存在，跳过")
                results.append({
                    "sample": name,
                    "success": False,
                    "time": 0,
                    "error": "文件不存在"
                })
                continue

            # 使用 subprocess 执行命令，先转换到临时目录，然后重命名
            temp_output = os.path.join(output_dir, name.replace(".html", ".pdf"))
            cmd = f"{soffice_cmd} {output_dir} {input_path}"
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            conversion_time = time.time() - start
            
            if result.returncode == 0:
                # 重命名文件以添加 _soffice 后缀
                if os.path.exists(temp_output):
                    os.rename(temp_output, output_path)
                    
                    # 获取文件大小
                    file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
                    
                    print(f"[soffice] {name} -> done in {conversion_time:.2f}s, size: {file_size} bytes")
                    results.append({
                        "sample": name,
                        "success": True,
                        "time": conversion_time,
                        "file_size": file_size,
                        "file_path": output_path,
                        "error": ""
                    })
                else:
                    print(f"[soffice] {name} -> 转换失败: 输出文件未生成")
                    results.append({
                        "sample": name,
                        "success": False,
                        "time": conversion_time,
                        "file_size": 0,
                        "file_path": "",
                        "error": "输出文件未生成"
                    })
            else:
                error_msg = result.stderr or "转换命令执行失败"
                print(f"[soffice] {name} -> 转换失败: {error_msg}")
                results.append({
                    "sample": name,
                    "success": False,
                    "time": conversion_time,
                    "file_size": 0,
                    "file_path": "",
                    "error": error_msg
                })
                
        except Exception as e:
            print(f"[soffice] {name} -> 转换失败: {str(e)}")
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
    test_soffice()
