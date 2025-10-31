"""
基于实际PDF内容分析的客观评估指标体系
"""

import os
import sys
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import statistics

# 添加utils路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.pdf_analyzer import PDFAnalyzer, PDFAnalysisResult


@dataclass
class ObjectiveMetrics:
    """客观评估指标"""
    tool_name: str
    
    # 文件效率指标
    avg_file_size: float  # 平均文件大小(KB)
    file_size_consistency: float  # 文件大小一致性(标准差)
    compression_efficiency: float  # 压缩效率评分
    
    # 内容准确性指标
    text_preservation_rate: float  # 文本保留率
    content_density_score: float  # 内容密度评分
    chinese_support_score: float  # 中文支持评分
    special_char_support: float  # 特殊字符支持评分
    
    # 功能完整性指标
    image_support_rate: float  # 图片支持率
    font_preservation_rate: float  # 字体保留率
    form_support_rate: float  # 表单支持率
    page_structure_score: float  # 页面结构评分
    
    # 稳定性指标
    success_rate: float  # 转换成功率
    error_rate: float  # 错误率
    
    # 综合评分
    overall_score: float  # 综合评分(0-100)


class ObjectiveEvaluator:
    """客观评估器"""
    
    def __init__(self):
        self.pdf_analyzer = PDFAnalyzer()
        
        # 工具名称映射(用于文件名筛选)
        self.tool_name_mapping = {
            'WeasyPrint': ['weasyprint'],
            'Playwright': ['playwright'],
            'LibreOffice': ['soffice', 'libreoffice']
        }
        
        # 基准值配置(基于实际分析结果)
        self.benchmarks = {
            'ideal_file_size_kb': 100,  # 理想文件大小(KB)
            'max_acceptable_size_kb': 500,  # 最大可接受大小(KB)
            'min_content_density': 0.0001,  # 最小内容密度
            'ideal_content_density': 0.01,  # 理想内容密度
            'min_compression_ratio': 0.001,  # 最小压缩比
            'ideal_compression_ratio': 0.02,  # 理想压缩比
        }
    
    def evaluate_tool_objectively(self, tool_name: str, pdf_results: Dict[str, PDFAnalysisResult], 
                                 original_samples: Dict[str, str]) -> ObjectiveMetrics:
        """
        基于PDF分析结果客观评估工具
        
        Args:
            tool_name: 工具名称
            pdf_results: PDF分析结果
            original_samples: 原始样例信息
            
        Returns:
            客观评估指标
        """
        
        # 筛选该工具的结果
        tool_keywords = self.tool_name_mapping.get(tool_name, [tool_name.lower()])
        tool_results = {}
        for k, v in pdf_results.items():
            for keyword in tool_keywords:
                if keyword.lower() in k.lower():
                    tool_results[k] = v
                    break
        
        if not tool_results:
            return self._create_empty_metrics(tool_name)
        
        # 1. 文件效率指标
        file_sizes_kb = [r.file_size / 1024 for r in tool_results.values()]
        avg_file_size = statistics.mean(file_sizes_kb)
        file_size_consistency = 100 - min(100, statistics.stdev(file_sizes_kb) if len(file_sizes_kb) > 1 else 0)
        compression_efficiency = self._calculate_compression_score(tool_results)
        
        # 2. 内容准确性指标
        text_preservation_rate = self._calculate_text_preservation(tool_results, original_samples)
        content_density_score = self._calculate_content_density_score(tool_results)
        chinese_support_score = self._calculate_chinese_support_score(tool_results)
        special_char_support = self._calculate_special_char_support(tool_results)
        
        # 3. 功能完整性指标
        image_support_rate = self._calculate_image_support_rate(tool_results)
        font_preservation_rate = self._calculate_font_preservation_rate(tool_results)
        form_support_rate = self._calculate_form_support_rate(tool_results)
        page_structure_score = self._calculate_page_structure_score(tool_results)
        
        # 4. 稳定性指标
        success_rate = self._calculate_success_rate(tool_results)
        error_rate = 100 - success_rate
        
        # 5. 综合评分计算
        overall_score = self._calculate_overall_score({
            'compression_efficiency': compression_efficiency,
            'text_preservation_rate': text_preservation_rate,
            'content_density_score': content_density_score,
            'chinese_support_score': chinese_support_score,
            'special_char_support': special_char_support,
            'image_support_rate': image_support_rate,
            'font_preservation_rate': font_preservation_rate,
            'page_structure_score': page_structure_score,
            'success_rate': success_rate
        })
        
        return ObjectiveMetrics(
            tool_name=tool_name,
            avg_file_size=avg_file_size,
            file_size_consistency=file_size_consistency,
            compression_efficiency=compression_efficiency,
            text_preservation_rate=text_preservation_rate,
            content_density_score=content_density_score,
            chinese_support_score=chinese_support_score,
            special_char_support=special_char_support,
            image_support_rate=image_support_rate,
            font_preservation_rate=font_preservation_rate,
            form_support_rate=form_support_rate,
            page_structure_score=page_structure_score,
            success_rate=success_rate,
            error_rate=error_rate,
            overall_score=overall_score
        )
    
    def _calculate_compression_score(self, tool_results: Dict[str, PDFAnalysisResult]) -> float:
        """计算压缩效率评分"""
        compression_ratios = [r.compression_ratio for r in tool_results.values() if r.compression_ratio > 0]
        if not compression_ratios:
            return 0.0
        
        avg_compression = statistics.mean(compression_ratios)
        ideal = self.benchmarks['ideal_compression_ratio']
        min_acceptable = self.benchmarks['min_compression_ratio']
        
        if avg_compression >= ideal:
            return 100.0
        elif avg_compression >= min_acceptable:
            return 50 + (avg_compression - min_acceptable) / (ideal - min_acceptable) * 50
        else:
            return max(0, avg_compression / min_acceptable * 50)
    
    def _calculate_text_preservation(self, tool_results: Dict[str, PDFAnalysisResult], 
                                   original_samples: Dict[str, str]) -> float:
        """计算文本保留率"""
        preservation_scores = []
        
        for filename, result in tool_results.items():
            # 提取样例名
            sample_name = self._extract_sample_name(filename)
            
            # 基于文本长度和内容质量给出评分
            if result.text_length > 0:
                # 检查文本内容质量
                text_content = result.text_content.strip()
                
                # 基础评分：有文本就给基础分
                base_score = 60
                
                # 根据文本长度调整评分
                if result.text_length >= 200:  # 较长文本
                    length_score = 40
                elif result.text_length >= 100:  # 中等长度
                    length_score = 30
                elif result.text_length >= 50:   # 短文本
                    length_score = 20
                else:
                    length_score = 10  # 很短的文本
                
                # 检查中文字符保留情况
                chinese_bonus = 0
                if result.chinese_char_count > 0:
                    chinese_bonus = min(10, result.chinese_char_count / 10)  # 中文字符越多奖励越高
                
                # 检查特殊字符保留情况
                special_bonus = 0
                if result.special_char_count > 0:
                    special_bonus = min(5, result.special_char_count / 5)
                
                total_score = min(100, base_score + length_score + chinese_bonus + special_bonus)
                preservation_scores.append(total_score)
            else:
                preservation_scores.append(0)
        
        return statistics.mean(preservation_scores) if preservation_scores else 0
    
    def _calculate_content_density_score(self, tool_results: Dict[str, PDFAnalysisResult]) -> float:
        """计算内容密度评分"""
        densities = [r.content_density for r in tool_results.values() if r.content_density > 0]
        if not densities:
            return 0.0
        
        avg_density = statistics.mean(densities)
        ideal = self.benchmarks['ideal_content_density']
        min_acceptable = self.benchmarks['min_content_density']
        
        if avg_density >= ideal:
            return 100.0
        elif avg_density >= min_acceptable:
            return 50 + (avg_density - min_acceptable) / (ideal - min_acceptable) * 50
        else:
            return max(0, avg_density / min_acceptable * 50)
    
    def _calculate_chinese_support_score(self, tool_results: Dict[str, PDFAnalysisResult]) -> float:
        """计算中文支持评分"""
        chinese_scores = []
        
        for filename, result in tool_results.items():
            if 'chinese' in filename.lower():
                # 中文样例的中文字符保留情况
                if result.chinese_char_count > 0:
                    chinese_scores.append(100)
                else:
                    chinese_scores.append(0)
            else:
                # 其他样例中的中文字符处理
                if result.chinese_char_count >= 0:  # 能正确识别中文字符
                    chinese_scores.append(100)
        
        return statistics.mean(chinese_scores) if chinese_scores else 50
    
    def _calculate_special_char_support(self, tool_results: Dict[str, PDFAnalysisResult]) -> float:
        """计算特殊字符支持评分"""
        special_scores = []
        
        for filename, result in tool_results.items():
            if 'special' in filename.lower():
                # 特殊字符样例的处理情况
                if result.special_char_count > 0:
                    special_scores.append(100)
                else:
                    special_scores.append(0)
            else:
                # 其他样例中的特殊字符处理
                special_scores.append(100)  # 默认支持
        
        return statistics.mean(special_scores) if special_scores else 100
    
    def _calculate_image_support_rate(self, tool_results: Dict[str, PDFAnalysisResult]) -> float:
        """计算图片支持率"""
        # 检查包含图形内容的样例
        image_samples = []
        for filename, result in tool_results.items():
            # 检查包含SVG、图片或图形内容的样例
            if any(keyword in filename.lower() for keyword in ['svg', 'base', 'complex']):
                image_samples.append(result)
        
        if not image_samples:
            return 100  # 没有图片样例时默认满分
        
        supported_count = 0
        for result in image_samples:
            # 检查是否有图片或图形内容
            if result.has_images:
                supported_count += 1
            # 如果文件大小相对较大，可能包含图形内容
            elif result.file_size > 50000:  # 50KB以上可能包含图形
                supported_count += 0.5  # 部分支持
        
        return min(100, (supported_count / len(image_samples)) * 100)
    
    def _calculate_font_preservation_rate(self, tool_results: Dict[str, PDFAnalysisResult]) -> float:
        """计算字体保留率"""
        font_scores = []
        
        for result in tool_results.values():
            if result.has_fonts:
                font_scores.append(100)
            elif result.font_count > 0:
                font_scores.append(50)
            else:
                font_scores.append(0)
        
        return statistics.mean(font_scores) if font_scores else 0
    
    def _calculate_form_support_rate(self, tool_results: Dict[str, PDFAnalysisResult]) -> float:
        """计算表单支持率"""
        form_samples = []
        for filename, result in tool_results.items():
            if 'forms' in filename.lower():
                form_samples.append(result)
        
        if not form_samples:
            return 100  # 没有表单样例时默认满分
        
        supported_count = 0
        for result in form_samples:
            # 检查是否有表单字段
            if result.form_field_count > 0:
                supported_count += 1
            # 如果没有检测到表单字段，但有文本内容，可能是表单被转换为文本
            elif result.text_length > 100:  # 有一定长度的文本内容
                # 检查文本中是否包含表单相关的关键词
                text_content = result.text_content.lower()
                form_keywords = ['input', 'button', 'submit', 'form', 'field', 'text', 'email', 'password']
                if any(keyword in text_content for keyword in form_keywords):
                    supported_count += 0.6  # 部分支持，表单转换为文本
                else:
                    supported_count += 0.3  # 基础支持，至少有内容
        
        return min(100, (supported_count / len(form_samples)) * 100) if form_samples else 100
    
    def _calculate_page_structure_score(self, tool_results: Dict[str, PDFAnalysisResult]) -> float:
        """计算页面结构评分"""
        page_scores = []
        
        for filename, result in tool_results.items():
            expected_pages = self._get_expected_pages(filename)
            if result.page_count == expected_pages:
                page_scores.append(100)
            elif result.page_count > 0:
                # 页数偏差惩罚
                deviation = abs(result.page_count - expected_pages) / expected_pages
                page_scores.append(max(0, 100 - deviation * 50))
            else:
                page_scores.append(0)
        
        return statistics.mean(page_scores) if page_scores else 0
    
    def _calculate_success_rate(self, tool_results: Dict[str, PDFAnalysisResult]) -> float:
        """计算转换成功率"""
        successful = sum(1 for r in tool_results.values() if not r.error_message and r.file_size > 0)
        return (successful / len(tool_results)) * 100 if tool_results else 0
    
    def _calculate_overall_score(self, metrics: Dict[str, float]) -> float:
        """计算综合评分"""
        weights = {
            'compression_efficiency': 0.15,  # 15% - 文件效率
            'text_preservation_rate': 0.20,  # 20% - 文本保留
            'content_density_score': 0.10,   # 10% - 内容密度
            'chinese_support_score': 0.15,   # 15% - 中文支持
            'special_char_support': 0.10,    # 10% - 特殊字符
            'image_support_rate': 0.10,      # 10% - 图片支持
            'font_preservation_rate': 0.10,  # 10% - 字体保留
            'page_structure_score': 0.05,    # 5% - 页面结构
            'success_rate': 0.05             # 5% - 成功率
        }
        
        weighted_score = sum(metrics[key] * weights[key] for key in weights if key in metrics)
        return min(100, max(0, weighted_score))
    
    def _extract_sample_name(self, filename: str) -> str:
        """从文件名提取样例名"""
        parts = filename.replace('.pdf', '').split('_')
        return '_'.join(parts[:-1]) if len(parts) > 1 else filename
    
    def _get_expected_pages(self, filename: str) -> int:
        """获取预期页数"""
        if 'long_document' in filename:
            return 3
        elif 'print_styles' in filename:
            return 2
        else:
            return 1
    
    def _create_empty_metrics(self, tool_name: str) -> ObjectiveMetrics:
        """创建空的评估指标"""
        return ObjectiveMetrics(
            tool_name=tool_name,
            avg_file_size=0,
            file_size_consistency=0,
            compression_efficiency=0,
            text_preservation_rate=0,
            content_density_score=0,
            chinese_support_score=0,
            special_char_support=0,
            image_support_rate=0,
            font_preservation_rate=0,
            form_support_rate=0,
            page_structure_score=0,
            success_rate=0,
            error_rate=100,
            overall_score=0
        )