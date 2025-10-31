"""
PDF内容分析器
基于实际PDF文件内容提取客观评估指标
"""

import os
import re
from typing import Dict, List, Tuple, Any
from PyPDF2 import PdfReader
from dataclasses import dataclass


@dataclass
class PDFAnalysisResult:
    """PDF分析结果"""
    file_path: str
    file_size: int  # 文件大小(字节)
    page_count: int  # 页数
    text_content: str  # 提取的文本内容
    text_length: int  # 文本长度
    has_images: bool  # 是否包含图片
    has_fonts: bool  # 是否包含字体信息
    font_count: int  # 字体数量
    chinese_char_count: int  # 中文字符数量
    special_char_count: int  # 特殊字符数量
    form_field_count: int  # 表单字段数量
    content_density: float  # 内容密度(文本长度/文件大小)
    compression_ratio: float  # 压缩比估算
    error_message: str = ""


class PDFAnalyzer:
    """PDF内容分析器"""
    
    def __init__(self):
        self.chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
        self.special_char_pattern = re.compile(r'[^\w\s\u4e00-\u9fff]')
    
    def analyze_pdf(self, file_path: str) -> PDFAnalysisResult:
        """
        分析PDF文件，提取客观指标
        
        Args:
            file_path: PDF文件路径
            
        Returns:
            PDF分析结果
        """
        try:
            # 基本文件信息
            file_size = os.path.getsize(file_path)
            
            # 读取PDF
            with open(file_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                
                # 页数
                page_count = len(pdf_reader.pages)
                
                # 提取文本内容
                text_content = ""
                for page in pdf_reader.pages:
                    text_content += page.extract_text()
                
                text_length = len(text_content)
                
                # 分析中文字符
                chinese_chars = self.chinese_pattern.findall(text_content)
                chinese_char_count = len(chinese_chars)
                
                # 分析特殊字符
                special_chars = self.special_char_pattern.findall(text_content)
                special_char_count = len(special_chars)
                
                # 检查是否有图片(通过检查PDF对象)
                has_images = self._check_images(pdf_reader)
                
                # 检查字体信息
                font_info = self._analyze_fonts(pdf_reader)
                has_fonts = font_info['has_fonts']
                font_count = font_info['font_count']
                
                # 检查表单字段
                form_field_count = self._count_form_fields(pdf_reader)
                
                # 计算内容密度
                content_density = text_length / file_size if file_size > 0 else 0
                
                # 估算压缩比(基于文本长度和文件大小的关系)
                expected_size = text_length * 2  # 假设每个字符2字节
                compression_ratio = expected_size / file_size if file_size > 0 else 0
                
                return PDFAnalysisResult(
                    file_path=file_path,
                    file_size=file_size,
                    page_count=page_count,
                    text_content=text_content,
                    text_length=text_length,
                    has_images=has_images,
                    has_fonts=has_fonts,
                    font_count=font_count,
                    chinese_char_count=chinese_char_count,
                    special_char_count=special_char_count,
                    form_field_count=form_field_count,
                    content_density=content_density,
                    compression_ratio=compression_ratio
                )
                
        except Exception as e:
            return PDFAnalysisResult(
                file_path=file_path,
                file_size=file_size if 'file_size' in locals() else 0,
                page_count=0,
                text_content="",
                text_length=0,
                has_images=False,
                has_fonts=False,
                font_count=0,
                chinese_char_count=0,
                special_char_count=0,
                form_field_count=0,
                content_density=0,
                compression_ratio=0,
                error_message=str(e)
            )
    
    def _check_images(self, pdf_reader: PdfReader) -> bool:
        """检查PDF是否包含图片"""
        try:
            for page in pdf_reader.pages:
                resources = page.get('/Resources', {})
                if hasattr(resources, 'get_object'):
                    resources = resources.get_object()
                
                if '/XObject' in resources:
                    xobjects = resources['/XObject']
                    if hasattr(xobjects, 'get_object'):
                        xobjects = xobjects.get_object()
                    
                    for obj_name in xobjects:
                        obj = xobjects[obj_name]
                        if hasattr(obj, 'get_object'):
                            obj = obj.get_object()
                        
                        if obj.get('/Subtype') == '/Image':
                            return True
                        # 检查Form XObject (可能包含图形内容)
                        elif obj.get('/Subtype') == '/Form':
                            return True
            
            # 如果没有找到XObject，检查是否有图形相关的内容
            # 通过检查页面内容流中是否有图形操作符
            for page in pdf_reader.pages:
                try:
                    if hasattr(page, 'get_contents'):
                        contents = page.get_contents()
                        if contents:
                            if hasattr(contents, 'get_object'):
                                contents = contents.get_object()
                            if hasattr(contents, 'get_data'):
                                content_data = contents.get_data().decode('latin-1', errors='ignore')
                                # 检查是否有图形绘制命令
                                if any(cmd in content_data for cmd in ['Do', 're', 'f', 'S', 'B']):
                                    return True
                except:
                    pass
            
            return False
        except Exception as e:
            # 如果检测失败，根据文件名判断
            return False
    
    def _analyze_fonts(self, pdf_reader: PdfReader) -> Dict[str, Any]:
        """分析PDF字体信息"""
        try:
            fonts = set()
            for page in pdf_reader.pages:
                resources = page.get('/Resources', {})
                if hasattr(resources, 'get_object'):
                    resources = resources.get_object()
                
                if '/Font' in resources:
                    font_dict = resources['/Font']
                    if hasattr(font_dict, 'get_object'):
                        font_dict = font_dict.get_object()
                    
                    for font_name in font_dict:
                        fonts.add(font_name)
            
            return {
                'has_fonts': len(fonts) > 0,
                'font_count': len(fonts),
                'fonts': list(fonts)
            }
        except Exception as e:
            # 如果出错，尝试简单检测
            try:
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text and len(page_text) > 0:
                        # 如果能提取到文本，说明有字体
                        return {'has_fonts': True, 'font_count': 1, 'fonts': ['default']}
                return {'has_fonts': False, 'font_count': 0, 'fonts': []}
            except:
                return {'has_fonts': False, 'font_count': 0, 'fonts': []}
    
    def _count_form_fields(self, pdf_reader: PdfReader) -> int:
        """统计表单字段数量"""
        try:
            if pdf_reader.get_form_text_fields():
                return len(pdf_reader.get_form_text_fields())
            return 0
        except:
            return 0
    
    def analyze_directory(self, directory_path: str) -> Dict[str, PDFAnalysisResult]:
        """
        分析目录中的所有PDF文件
        
        Args:
            directory_path: 目录路径
            
        Returns:
            文件名到分析结果的映射
        """
        results = {}
        
        if not os.path.exists(directory_path):
            return results
        
        for filename in os.listdir(directory_path):
            if filename.endswith('.pdf'):
                file_path = os.path.join(directory_path, filename)
                results[filename] = self.analyze_pdf(file_path)
        
        return results
    
    def compare_tools_by_sample(self, analysis_results: Dict[str, PDFAnalysisResult]) -> Dict[str, Dict[str, Any]]:
        """
        按样例对比不同工具的表现
        
        Args:
            analysis_results: 分析结果字典
            
        Returns:
            按样例分组的对比结果
        """
        sample_comparisons = {}
        
        # 按样例分组
        for filename, result in analysis_results.items():
            # 提取样例名和工具名
            parts = filename.replace('.pdf', '').split('_')
            if len(parts) >= 2:
                tool_name = parts[-1]
                sample_name = '_'.join(parts[:-1])
                
                if sample_name not in sample_comparisons:
                    sample_comparisons[sample_name] = {}
                
                sample_comparisons[sample_name][tool_name] = {
                    'file_size': result.file_size,
                    'page_count': result.page_count,
                    'text_length': result.text_length,
                    'content_density': result.content_density,
                    'has_images': result.has_images,
                    'font_count': result.font_count,
                    'chinese_char_count': result.chinese_char_count,
                    'special_char_count': result.special_char_count,
                    'compression_ratio': result.compression_ratio,
                    'error': result.error_message
                }
        
        return sample_comparisons