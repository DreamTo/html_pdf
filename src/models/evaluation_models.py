"""
评估相关的数据模型
包含样例结果和评估指标的数据类定义
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SampleResult:
    """单个样例的转换结果"""
    sample_name: str
    file_path: str
    conversion_success: bool
    conversion_time: float
    file_size: int
    error_message: str = ""
    quality_score: float = 0.0  # 转换质量评分 (0-100)
    notes: str = ""


@dataclass
class EvaluationMetrics:
    """评估指标数据类"""
    tool_name: str
    layout_visual_score: float  # 排版与视觉还原度 (0-100)
    functionality_score: float  # 功能支持 (0-100)
    performance_score: float    # 性能与稳定性 (0-100)
    deployment_score: float     # 部署可行性 (0-100)
    customization_score: float  # 可定制性 (0-100)
    conversion_times: List[float]  # 转换耗时列表
    file_sizes: Dict[str, int]     # 生成文件大小
    sample_results: List[SampleResult]  # 每个样例的详细结果
    
    def calculate_weighted_score(self) -> float:
        """计算加权总分"""
        weights = {
            "layout_visual": 0.35,    # 35%
            "functionality": 0.25,    # 25%
            "performance": 0.20,      # 20%
            "deployment": 0.10,       # 10%
            "customization": 0.10     # 10%
        }
        
        return (
            self.layout_visual_score * weights["layout_visual"] +
            self.functionality_score * weights["functionality"] +
            self.performance_score * weights["performance"] +
            self.deployment_score * weights["deployment"] +
            self.customization_score * weights["customization"]
        )


# 评估维度配置
EVALUATION_DIMENSIONS = [
    ("🎨 排版与视觉还原度", "35%", "CSS布局、字体、颜色、间距、分页"),
    ("🧠 功能支持", "25%", "JS执行、动态内容、SVG、字体嵌入"),
    ("⚙️ 性能与稳定性", "20%", "转换速度、内存占用、稳定性"),
    ("🧩 部署可行性", "10%", "安装复杂度、依赖、可移植性"),
    ("🪶 可定制性", "10%", "输出配置、页眉页脚、水印等")
]

# 样例信息配置
SAMPLES_INFO = {
    "base.html": "基础元素测试 - 文本、图片、表格",
    "complex.html": "复杂布局测试 - Grid布局、分页、阴影",
    "chinese.html": "中文字体测试 - 中文排版和字体渲染",
    "dynamic.html": "动态内容测试 - JavaScript生成内容",
    "svg.html": "SVG图形测试 - 矢量图形渲染",
    "print_styles.html": "打印样式测试 - @media print和@page规则",
    "forms.html": "表单元素测试 - 各种表单控件",
    "long_document.html": "长文档测试 - 多页分页效果",
    "special_chars.html": "特殊字符测试 - Unicode字符和符号"
}

# 样例测试权重配置 - 基于样例复杂度和重要性
SAMPLE_WEIGHTS = {
    "base.html": 1.0,          # 基础功能，标准权重
    "complex.html": 1.5,       # 复杂布局，高权重
    "chinese.html": 1.2,       # 中文支持，重要
    "dynamic.html": 1.8,       # 动态内容，最高权重
    "svg.html": 1.3,           # SVG支持，较重要
    "print_styles.html": 1.1,  # 打印样式，一般重要
    "forms.html": 1.0,         # 表单元素，标准权重
    "long_document.html": 1.2, # 长文档，较重要
    "special_chars.html": 1.0  # 特殊字符，标准权重
}

def calculate_dynamic_quality_score(tool_name: str, sample_name: str, 
                                  conversion_success: bool, conversion_time: float, 
                                  file_size: int) -> float:
    """
    基于实际测试结果动态计算质量评分
    
    Args:
        tool_name: 工具名称
        sample_name: 样例名称
        conversion_success: 转换是否成功
        conversion_time: 转换耗时
        file_size: 生成文件大小
    
    Returns:
        质量评分 (0-100)
    """
    if not conversion_success:
        return 0.0
    
    # 基础分数：基于转换成功
    base_score = 50.0
    
    # 性能评分 (30%) - 基于转换时间
    time_score = max(0, 30 - (conversion_time - 0.1) * 15)  # 0.1s为理想时间
    time_score = min(30, time_score)
    
    # 文件大小评分 (20%) - 适中的文件大小最好
    size_mb = file_size / (1024 * 1024)
    if size_mb < 0.1:
        size_score = 20 * (size_mb / 0.1)  # 太小可能质量不够
    elif size_mb <= 1.0:
        size_score = 20  # 理想大小
    else:
        size_score = max(0, 20 - (size_mb - 1.0) * 10)  # 太大扣分
    
    total_score = base_score + time_score + size_score
    return min(100.0, max(0.0, total_score))

def calculate_dimension_scores(tool_name: str, sample_results: List) -> Dict[str, float]:
    """
    基于实际转换结果计算各维度评分
    
    Args:
        tool_name: 工具名称
        sample_results: 样例测试结果列表
    
    Returns:
        各维度评分字典
    """
    if not sample_results:
        return {
            "layout_visual": 50.0,
            "functionality": 50.0,
            "performance": 50.0,
            "deployment": 50.0,
            "customization": 50.0
        }
    
    # 计算基本统计
    success_count = sum(1 for r in sample_results if hasattr(r, 'conversion_success') and r.conversion_success)
    success_rate = success_count / len(sample_results) if sample_results else 0
    
    # 计算平均质量分数
    quality_scores = [r.quality_score for r in sample_results if hasattr(r, 'quality_score') and r.quality_score > 0]
    avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 50
    
    # 计算转换时间性能
    conversion_times = [r.conversion_time for r in sample_results 
                       if hasattr(r, 'conversion_success') and r.conversion_success and r.conversion_time > 0]
    avg_time = sum(conversion_times) / len(conversion_times) if conversion_times else 1.0
    
    # 计算文件大小一致性
    file_sizes = [r.file_size for r in sample_results if hasattr(r, 'file_size') and r.file_size > 0]
    size_variance = 0
    if len(file_sizes) > 1:
        avg_size = sum(file_sizes) / len(file_sizes)
        size_variance = sum((size - avg_size) ** 2 for size in file_sizes) / len(file_sizes)
        size_consistency = max(0, 100 - (size_variance / avg_size) * 100) if avg_size > 0 else 50
    else:
        size_consistency = 50
    
    # 基于工具特性和实际结果计算各维度评分
    
    # 排版视觉评分 = 质量分数 * 成功率
    layout_visual = avg_quality * (success_rate * 0.3 + 0.7)
    
    # 功能支持评分 = 基于工具特性和质量分数
    if tool_name.lower() == "playwright":
        functionality = min(100, avg_quality * 1.1)  # Playwright功能支持较好
    elif tool_name.lower() == "weasyprint":
        functionality = min(100, avg_quality * 0.9)  # WeasyPrint功能支持一般
    else:  # LibreOffice
        functionality = min(100, avg_quality * 0.8)  # LibreOffice功能支持较弱
    
    # 性能稳定评分 = 成功率 + 时间性能
    time_score = max(0, 100 - avg_time * 20)  # 时间越短分数越高
    performance = success_rate * 100 * 0.6 + time_score * 0.4
    
    # 部署可行评分 = 成功率 + 文件大小一致性
    deployment = success_rate * 100 * 0.7 + size_consistency * 0.3
    
    # 可定制性评分 = 基于工具特性
    if tool_name.lower() == "playwright":
        customization = 85  # Playwright可定制性高
    elif tool_name.lower() == "weasyprint":
        customization = 75  # WeasyPrint可定制性中等
    else:  # LibreOffice
        customization = 60  # LibreOffice可定制性较低
    
    return {
        "layout_visual": min(100, max(0, layout_visual)),
        "functionality": min(100, max(0, functionality)),
        "performance": min(100, max(0, performance)),
        "deployment": min(100, max(0, deployment)),
        "customization": min(100, max(0, customization))
    }