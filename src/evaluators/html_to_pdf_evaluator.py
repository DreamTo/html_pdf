"""
HTML转PDF评估器
负责评估转换结果并计算评分
"""

import os
from typing import Dict, List, Any
from models.evaluation_models import (
    SampleResult, EvaluationMetrics, EVALUATION_DIMENSIONS, 
    SAMPLES_INFO, SAMPLE_WEIGHTS,
    calculate_dynamic_quality_score, calculate_dimension_scores
)
from models.objective_evaluation import ObjectiveEvaluator, ObjectiveMetrics
from utils.test_runner import TestRunner
from utils.file_operations import FileOperations
from utils.pdf_analyzer import PDFAnalyzer
from generators.html_report_generator import HTMLReportGenerator


class HTMLToPDFEvaluator:
    """HTML转PDF评估器"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        self.samples_info = SAMPLES_INFO
        self.sample_weights = SAMPLE_WEIGHTS
        self.evaluation_dimensions = EVALUATION_DIMENSIONS
        
        # 初始化组件
        self.test_runner = TestRunner()
        self.file_ops = FileOperations()
        self.html_generator = HTMLReportGenerator()
        self.pdf_analyzer = PDFAnalyzer()
        self.objective_evaluator = ObjectiveEvaluator()
        
        # 确保输出目录存在
        self.file_ops.ensure_directory_exists(output_dir)
    
    def convert_raw_results_to_sample_results(self, raw_results: Dict[str, List[Dict]]) -> Dict[str, List[SampleResult]]:
        """将原始测试结果转换为SampleResult对象"""
        converted_results = {}
        
        for tool_name, results in raw_results.items():
            sample_results = []
            for result in results:
                sample_result = SampleResult(
                    sample_name=result.get('sample', 'unknown'),
                    file_path=result.get('file_path', ''),
                    conversion_success=result.get('success', False),
                    conversion_time=result.get('time', 0.0),
                    file_size=result.get('file_size', 0),
                    error_message=result.get('error', ''),
                    quality_score=result.get('quality_score', 0.0)
                )
                sample_results.append(sample_result)
            converted_results[tool_name] = sample_results
        
        return converted_results
    
    def calculate_quality_score(self, sample_name: str, success: bool, 
                              conversion_time: float, file_size: int) -> float:
        """计算质量评分"""
        if not success:
            return 0.0
        
        # 基础分数 (50分)
        base_score = 50
        
        # 时间评分 (30分)
        time_score = 0
        if conversion_time <= 0.5:
            time_score = 30
        elif conversion_time <= 1.0:
            time_score = 25
        elif conversion_time <= 2.0:
            time_score = 20
        elif conversion_time <= 5.0:
            time_score = 15
        else:
            time_score = 10
        
        # 文件大小评分 (20分) - 根据文件大小合理性评分
        size_score = 0
        if file_size <= 50000:  # 50KB以下
            size_score = 20
        elif file_size <= 200000:  # 200KB以下
            size_score = 15
        elif file_size <= 500000:  # 500KB以下
            size_score = 10
        else:
            size_score = 5
        
        total_score = base_score + time_score + size_score
        return min(100.0, total_score)
    
    def calculate_tool_score(self, results: List[SampleResult]) -> float:
        """计算工具总分"""
        if not results:
            return 0.0
        
        total_weighted_score = 0.0
        total_weight = 0.0
        
        for result in results:
            # 获取样例权重
            weight = SAMPLE_WEIGHTS.get(result.sample_name, 1.0)
            
            quality_score = self.calculate_quality_score(
                result.sample_name,
                result.conversion_success,
                result.conversion_time,
                result.file_size
            )
            
            total_weighted_score += quality_score * weight
            total_weight += weight
        
        return total_weighted_score / total_weight if total_weight > 0 else 0.0
    
    def run_objective_evaluation(self, tool_name: str, pdf_files: List[str]) -> ObjectiveMetrics:
        """运行客观评估"""
        # 分析PDF文件
        pdf_results = {}
        for pdf_file in pdf_files:
            try:
                filename = os.path.basename(pdf_file)
                analysis = self.pdf_analyzer.analyze_pdf(pdf_file)
                pdf_results[filename] = analysis
            except Exception as e:
                print(f"⚠️ 分析PDF文件失败 {pdf_file}: {e}")
                continue
        
        if not pdf_results:
            # 返回空的客观评估结果
            return ObjectiveMetrics(
                tool_name=tool_name,
                avg_file_size=0.0,
                file_size_consistency=0.0,
                compression_efficiency=0.0,
                text_preservation_rate=0.0,
                content_density_score=0.0,
                chinese_support_score=0.0,
                special_char_support=0.0,
                image_support_rate=0.0,
                font_preservation_rate=0.0,
                form_support_rate=0.0,
                page_structure_score=0.0,
                success_rate=0.0,
                error_rate=0.0,
                overall_score=0.0
            )
        
        # 定义原始样例文本（用于文本保留率计算）
        original_samples = {
            'base.html': '基础HTML页面测试内容，包含标题、段落、列表等基本元素。',
            'chinese.html': '中文内容测试页面，包含各种中文字符、标点符号和特殊格式。测试中文字体渲染效果。',
            'complex.html': '复杂布局测试页面，包含多列布局、浮动元素、定位元素等复杂CSS样式。',
            'dynamic.html': '动态内容测试页面，包含JavaScript生成的内容和动态样式。',
            'forms.html': '表单元素测试页面，包含各种输入框、按钮、选择器等表单控件。',
            'long_document.html': '长文档测试页面，包含大量文本内容、多个章节、目录等长文档特性。',
            'print_styles.html': '打印样式测试页面，包含专门的打印CSS样式和媒体查询。',
            'special_chars.html': '特殊字符测试页面，包含各种特殊符号、数学公式、emoji等特殊字符。',
            'svg.html': 'SVG图形测试页面，包含各种SVG图形、图标和矢量图形元素。'
        }
        
        # 运行客观评估
        return self.objective_evaluator.evaluate_tool_objectively(tool_name, pdf_results, original_samples)

    def calculate_metrics(self, tool_name: str, results: List[SampleResult]) -> EvaluationMetrics:
        """计算评估指标"""
        # 计算基本统计
        successful_results = [r for r in results if r.conversion_success]
        conversion_times = [r.conversion_time for r in successful_results if r.conversion_time > 0]
        file_sizes = {r.sample_name: r.file_size for r in results if r.file_size > 0}
        
        # 使用新的动态评分系统计算各维度得分
        dimension_scores = calculate_dimension_scores(tool_name, results)
        
        return EvaluationMetrics(
            tool_name=tool_name,
            layout_visual_score=dimension_scores["layout_visual"],
            functionality_score=dimension_scores["functionality"],
            performance_score=dimension_scores["performance"],
            deployment_score=dimension_scores["deployment"],
            customization_score=dimension_scores["customization"],
            conversion_times=conversion_times,
            file_sizes=file_sizes,
            sample_results=results
        )
    
    def run_evaluation(self) -> tuple[Dict[str, List[SampleResult]], Dict[str, EvaluationMetrics], Dict[str, ObjectiveMetrics]]:
        """运行完整评估"""
        print("🚀 开始HTML转PDF工具评估...")
        
        # 运行实际测试
        raw_results = self.test_runner.run_actual_tests()
        
        # 转换结果格式
        results = self.convert_raw_results_to_sample_results(raw_results)
        
        # 重新计算质量评分
        for tool_name, tool_results in results.items():
            for result in tool_results:
                if result.conversion_success:
                    result.quality_score = self.calculate_quality_score(
                        result.sample_name,
                        result.conversion_success,
                        result.conversion_time,
                        result.file_size
                    )
        
        # 计算传统评估指标
        metrics = {}
        for tool_name, tool_results in results.items():
            metrics[tool_name] = self.calculate_metrics(tool_name, tool_results)
        
        # 运行客观评估
        print("📊 开始客观评估...")
        objective_metrics = {}
        for tool_name, tool_results in results.items():
            # 收集该工具的PDF文件路径
            pdf_files = [result.file_path for result in tool_results if result.conversion_success and result.file_path]
            if pdf_files:
                print(f"🔍 评估 {tool_name} 工具 ({len(pdf_files)} 个PDF文件)...")
                objective_metrics[tool_name] = self.run_objective_evaluation(tool_name, pdf_files)
            else:
                print(f"⚠️ {tool_name} 工具没有成功的PDF文件可供评估")
                objective_metrics[tool_name] = ObjectiveMetrics(
                    tool_name=tool_name,
                    avg_file_size=0.0,
                    file_size_consistency=0.0,
                    compression_efficiency=0.0,
                    text_preservation_rate=0.0,
                    content_density_score=0.0,
                    chinese_support_score=0.0,
                    special_char_support=0.0,
                    image_support_rate=0.0,
                    font_preservation_rate=0.0,
                    form_support_rate=0.0,
                    page_structure_score=0.0,
                    success_rate=0.0,
                    error_rate=0.0,
                    overall_score=0.0
                )
        
        return results, metrics, objective_metrics
    
    def generate_performance_analysis(self, metrics: Dict[str, EvaluationMetrics]) -> str:
        """生成性能分析报告"""
        analysis = []
        analysis.append("📊 性能分析报告")
        analysis.append("=" * 50)
        
        # 按总分排序
        sorted_tools = sorted(metrics.items(), key=lambda x: x[1].calculate_weighted_score(), reverse=True)
        
        analysis.append(f"\n🏆 综合排名:")
        for i, (tool_name, metric) in enumerate(sorted_tools, 1):
            analysis.append(f"{i}. {tool_name}: {metric.calculate_weighted_score():.1f}分")
        
        # 各维度分析
        analysis.append(f"\n📈 详细指标:")
        for tool_name, metric in sorted_tools:
            # 计算成功率
            successful_count = sum(1 for result in metric.sample_results if result.conversion_success)
            success_rate = (successful_count / len(metric.sample_results) * 100) if metric.sample_results else 0
            
            # 计算平均值
            avg_time = sum(metric.conversion_times) / len(metric.conversion_times) if metric.conversion_times else 0
            avg_size = sum(metric.file_sizes.values()) / len(metric.file_sizes) if metric.file_sizes else 0
            avg_quality = sum(r.quality_score for r in metric.sample_results) / len(metric.sample_results) if metric.sample_results else 0
            
            analysis.append(f"\n{tool_name}:")
            analysis.append(f"  • 成功率: {success_rate:.1f}%")
            analysis.append(f"  • 平均转换时间: {avg_time:.2f}s")
            analysis.append(f"  • 平均文件大小: {avg_size/1024:.1f}KB")
            analysis.append(f"  • 平均质量评分: {avg_quality:.1f}")
        
        # 性能对比
        if len(sorted_tools) >= 2:
            best = sorted_tools[0]
            second = sorted_tools[1]
            analysis.append(f"\n🔍 性能对比:")
            analysis.append(f"  • {best[0]} 比 {second[0]} 高出 {best[1].calculate_weighted_score() - second[1].calculate_weighted_score():.1f}分")
        
        return "\n".join(analysis)
    
    def print_evaluation_report(self, results: Dict[str, List[SampleResult]], 
                              metrics: Dict[str, EvaluationMetrics]) -> None:
        """打印评估报告到控制台"""
        print("\n" + "="*80)
        print("📄 HTML转PDF工具评估报告")
        print("="*80)
        
        # 评估维度说明
        print(f"\n📋 评估维度:")
        for dimension, weight, description in self.evaluation_dimensions:
            print(f"  • {dimension}: {weight} - {description}")
        
        # 工具评分
        print(f"\n🏆 工具评分 (加权总分):")
        sorted_tools = sorted(metrics.items(), key=lambda x: x[1].calculate_weighted_score(), reverse=True)
        for i, (tool_name, metric) in enumerate(sorted_tools, 1):
            print(f"  {i}. {tool_name}: {metric.calculate_weighted_score():.1f}分")
        
        # 性能分析
        print(f"\n{self.generate_performance_analysis(metrics)}")
        
        # 使用建议
        print(f"\n💡 使用建议:")
        best_tool = sorted_tools[0]
        print(f"  推荐使用: {best_tool[0]} (综合评分: {best_tool[1].calculate_weighted_score():.1f})")
        
        for tool_name, metric in sorted_tools:
            # 计算成功率
            successful_count = sum(1 for result in metric.sample_results if result.conversion_success)
            success_rate = (successful_count / len(metric.sample_results) * 100) if metric.sample_results else 0
            
            if success_rate >= 90:
                reliability = "高可靠性"
            elif success_rate >= 70:
                reliability = "中等可靠性"
            else:
                reliability = "低可靠性"
            
            # 计算平均转换时间
            avg_time = sum(metric.conversion_times) / len(metric.conversion_times) if metric.conversion_times else 0
            
            print(f"  • {tool_name}: {reliability}，适合", end="")
            if success_rate >= 90 and avg_time <= 3:
                print("生产环境使用")
            elif success_rate >= 70:
                print("一般用途")
            else:
                print("测试环境或特定场景")
        
        print("="*60)
        print()
    
    def print_objective_evaluation_report(self, objective_metrics: Dict[str, ObjectiveMetrics]) -> None:
        """打印客观评估报告"""
        print("\n" + "="*60)
        print("📊 客观评估报告")
        print("="*60)
        
        for tool_name, metrics in objective_metrics.items():
            print(f"\n🔧 {tool_name}")
            print("-" * 40)
            print(f"综合评分: {metrics.overall_score:.1f}/100")
            print(f"平均文件大小: {metrics.avg_file_size:.1f}KB")
            print(f"压缩效率: {metrics.compression_efficiency:.1f}%")
            print(f"文本保留率: {metrics.text_preservation_rate:.1f}%")
            print(f"内容密度: {metrics.content_density_score:.1f}%")
            print(f"中文支持: {metrics.chinese_support_score:.1f}%")
            print(f"特殊字符支持: {metrics.special_char_support:.1f}%")
            print(f"图片支持率: {metrics.image_support_rate:.1f}%")
            print(f"字体保留率: {metrics.font_preservation_rate:.1f}%")
            print(f"表单支持率: {metrics.form_support_rate:.1f}%")
            print(f"页面结构: {metrics.page_structure_score:.1f}%")
            print(f"成功率: {metrics.success_rate:.1f}%")
            print(f"错误率: {metrics.error_rate:.1f}%")
        
        print("\n" + "="*60)
        print()
    
    def generate_html_report(self, results: Dict[str, List[SampleResult]], 
                           metrics: Dict[str, EvaluationMetrics],
                           objective_metrics: Dict[str, ObjectiveMetrics] = None) -> str:
        """生成HTML报告"""
        return self.html_generator.generate_full_report(results, metrics, objective_metrics)
    
    def save_results(self, results: Dict[str, List[SampleResult]], 
                    metrics: Dict[str, EvaluationMetrics], 
                    objective_metrics: Dict[str, ObjectiveMetrics] = None) -> None:
        """保存评估结果"""
        # 保存JSON结果
        json_data = {
            "results": {
                tool_name: [
                    {
                        "sample_name": r.sample_name,
                        "file_path": r.file_path,
                        "conversion_success": r.conversion_success,
                        "conversion_time": r.conversion_time,
                        "file_size": r.file_size,
                        "quality_score": r.quality_score,
                        "error_message": r.error_message,
                        "notes": r.notes
                    }
                    for r in tool_results
                ]
                for tool_name, tool_results in results.items()
            },
            "metrics": {
                tool_name: {
                    "tool_name": m.tool_name,
                    "layout_visual_score": m.layout_visual_score,
                    "functionality_score": m.functionality_score,
                    "performance_score": m.performance_score,
                    "deployment_score": m.deployment_score,
                    "customization_score": m.customization_score,
                    "weighted_score": m.calculate_weighted_score(),
                    "conversion_times": m.conversion_times,
                    "file_sizes": m.file_sizes
                }
                for tool_name, m in metrics.items()
            }
        }
        
        # 添加客观评估结果
        if objective_metrics:
            json_data["objective_metrics"] = {
                tool_name: {
                    "tool_name": om.tool_name,
                    "overall_score": om.overall_score,
                    "avg_file_size": om.avg_file_size,
                    "file_size_consistency": om.file_size_consistency,
                    "compression_efficiency": om.compression_efficiency,
                    "text_preservation_rate": om.text_preservation_rate,
                    "content_density_score": om.content_density_score,
                    "chinese_support_score": om.chinese_support_score,
                    "special_char_support": om.special_char_support,
                    "image_support_rate": om.image_support_rate,
                    "font_preservation_rate": om.font_preservation_rate,
                    "form_support_rate": om.form_support_rate,
                    "page_structure_score": om.page_structure_score,
                    "success_rate": om.success_rate,
                    "error_rate": om.error_rate
                }
                for tool_name, om in objective_metrics.items()
            }
        
        json_path = f"{self.output_dir}/evaluation_results.json"
        self.file_ops.save_json(json_data, json_path)
        print(f"📄 评估结果已保存到: {json_path}")
        
        # 生成并保存HTML报告
        html_content = self.generate_html_report(results, metrics, objective_metrics)
        html_path = f"{self.output_dir}/evaluation_report.html"
        self.file_ops.save_text(html_content, html_path)
        print(f"🌐 HTML报告已生成: {html_path}")
    
    def run_complete_evaluation(self) -> None:
        """运行完整的评估流程"""
        # 运行评估
        results, metrics, objective_metrics = self.run_evaluation()
        
        # 打印传统评估报告
        self.print_evaluation_report(results, metrics)
        
        # 打印客观评估报告
        self.print_objective_evaluation_report(objective_metrics)
        
        # 保存结果
        self.save_results(results, metrics, objective_metrics)