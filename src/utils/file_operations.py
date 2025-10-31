"""
文件操作工具
处理文件和目录相关的操作
"""

import os
import json
from typing import Any, Dict


class FileOperations:
    """文件操作工具类"""
    
    @staticmethod
    def ensure_directory_exists(directory: str) -> None:
        """确保目录存在，如果不存在则创建"""
        os.makedirs(directory, exist_ok=True)
    
    @staticmethod
    def save_json(data: Dict[str, Any], file_path: str, encoding: str = "utf-8") -> None:
        """保存数据为JSON文件"""
        # 确保目录存在
        directory = os.path.dirname(file_path)
        FileOperations.ensure_directory_exists(directory)
        
        with open(file_path, "w", encoding=encoding) as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    @staticmethod
    def save_text(content: str, file_path: str, encoding: str = "utf-8") -> None:
        """保存文本内容到文件"""
        # 确保目录存在
        directory = os.path.dirname(file_path)
        FileOperations.ensure_directory_exists(directory)
        
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
    
    @staticmethod
    def load_json(file_path: str, encoding: str = "utf-8") -> Dict[str, Any]:
        """从JSON文件加载数据"""
        with open(file_path, "r", encoding=encoding) as f:
            return json.load(f)
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """检查文件是否存在"""
        return os.path.exists(file_path)
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """获取文件大小（字节）"""
        if FileOperations.file_exists(file_path):
            return os.path.getsize(file_path)
        return 0