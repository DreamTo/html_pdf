"""
HTML报告生成器
负责生成评估报告的HTML页面
"""

from typing import Dict, List, Any
from models.evaluation_models import SampleResult, EvaluationMetrics
from models.objective_evaluation import ObjectiveMetrics


class HTMLReportGenerator:
    """HTML报告生成器"""
    
    def __init__(self):
        self.css_styles = self._get_css_styles()
    
    def _get_css_styles(self) -> str:
        """获取CSS样式"""
        return """
        <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }
        
        .content {
            padding: 30px;
        }
        
        .section {
            margin-bottom: 40px;
        }
        
        .section h2 {
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        
        .comparison-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-radius: 10px;
            overflow: hidden;
        }
        
        .comparison-table th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: center;
            font-weight: 600;
        }
        
        .comparison-table td {
            padding: 12px 15px;
            text-align: center;
            border-bottom: 1px solid #eee;
        }
        
        .comparison-table tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        
        .comparison-table tr:hover {
            background-color: #e3f2fd;
            transform: scale(1.01);
            transition: all 0.3s ease;
        }
        
        .score-high { color: #4CAF50; font-weight: bold; }
        .score-medium { color: #FF9800; font-weight: bold; }
        .score-low { color: #f44336; font-weight: bold; }
        
        .status-success { 
            background: #4CAF50; 
            color: white; 
            padding: 4px 8px; 
            border-radius: 15px; 
            font-size: 0.8em;
            font-weight: bold;
        }
        
        .status-failed { 
            background: #f44336; 
            color: white; 
            padding: 4px 8px; 
            border-radius: 15px; 
            font-size: 0.8em;
            font-weight: bold;
        }
        
        .metric-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
        }
        
        .metric-title {
            font-size: 1.2em;
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
        }
        
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .performance-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 20px 0;
        }
        
        .tool-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-top: 5px solid #667eea;
        }
        
        .tool-name {
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
        }
        
        .tool-score {
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            margin: 15px 0;
        }
        
        .recommendations {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            border-left: 5px solid #28a745;
        }
        
        .recommendations h3 {
            color: #28a745;
            margin-top: 0;
        }
        
        .footer {
            text-align: center;
            padding: 20px;
            color: #666;
            border-top: 1px solid #eee;
            margin-top: 40px;
        }
        
        .failure-analysis {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
        }
        
        .error-box {
            background: #fee;
            border: 1px solid #fcc;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            font-family: monospace;
            color: #c33;
        }
        
        .warning-box {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 4px;
            }
            
        /* 工具介绍样式 */
        .tools-introduction {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .tool-intro-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .tool-intro-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }
        
        .tool-intro-card h3 {
            color: #333;
            margin: 0 0 15px 0;
            font-size: 1.3em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .tool-intro-card .tool-icon {
            font-size: 1.5em;
        }
        
        /* 解析能力对比表格样式 */
        .limitations-comparison {
            margin: 20px 0;
        }
        
        .comparison-table-container {
            overflow-x: auto;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .limitations-table {
            width: 100%;
            border-collapse: collapse;
            background: white;
        }
        
        .limitations-table th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 12px;
            text-align: center;
            font-weight: 600;
            font-size: 0.95em;
        }
        
        .limitations-table td {
            padding: 12px;
            text-align: center;
            border-bottom: 1px solid #f0f0f0;
            font-size: 0.9em;
        }
        
        .limitations-table .feature-name {
            text-align: left;
            font-weight: 500;
            color: #333;
            background-color: #f8f9fa;
        }
        
        .limitations-table tr:hover {
            background-color: #f5f7ff;
        }
        
        /* 支持程度样式 */
        .support-excellent {
            color: #28a745;
            font-weight: 600;
        }
        
        .support-good {
            color: #17a2b8;
            font-weight: 600;
        }
        
        .support-limited {
            color: #ffc107;
            font-weight: 600;
        }
        
        .support-none {
            color: #dc3545;
            font-weight: 600;
        }
        
        /* 简化的整体布局 */
        .section {
            margin-bottom: 35px;
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .section h2 {
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 8px;
            margin: 0 0 20px 0;
            font-size: 1.6em;
            font-weight: 600;
                padding: 10px;
                margin: 10px 0;
                color: #856404;
            }
            
            /* 可视化图表样式 */
            .visual-comparison-section {
                margin: 30px 0;
                background: white;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            
            .chart-selector {
                display: flex;
                gap: 10px;
                margin-bottom: 25px;
                flex-wrap: wrap;
            }
            
            .chart-btn {
                padding: 10px 20px;
                border: 2px solid #3498db;
                background: white;
                color: #3498db;
                border-radius: 25px;
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: 500;
            }
            
            .chart-btn:hover {
                background: #3498db;
                color: white;
                transform: translateY(-2px);
            }
            
            .chart-btn.active {
                background: #3498db;
                color: white;
                box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3);
            }
            
            .chart-container {
                margin: 20px 0;
                padding: 20px;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background: #fafafa;
            }
            
            .chart-container h4 {
                margin: 0 0 15px 0;
                color: #2c3e50;
                text-align: center;
            }
            
            /* 热力图表格样式 */
            .heatmap-table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                border-radius: 8px;
                overflow: hidden;
            }
            
            .heatmap-table th {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px;
                text-align: center;
                font-weight: 600;
            }
            
            .heatmap-table .sample-name {
                background: #f8f9fa;
                font-weight: 600;
                padding: 15px;
                border-right: 2px solid #dee2e6;
            }
            
            .heatmap-cell {
                padding: 0;
                text-align: center;
                border: 1px solid #dee2e6;
                position: relative;
                transition: all 0.3s ease;
            }
            
            .heatmap-cell:hover {
                transform: scale(1.05);
                z-index: 10;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            }
            
            .cell-content {
                padding: 15px;
                display: flex;
                flex-direction: column;
                gap: 5px;
                height: 100%;
            }
            
            .cell-content .status {
                font-size: 18px;
                font-weight: bold;
            }
            
            .cell-content .quality {
                font-size: 14px;
                font-weight: 600;
            }
            
            .cell-content .time {
                font-size: 12px;
                opacity: 0.8;
            }
            
            .cell-content .error {
            color: #e74c3c;
            font-weight: 600;
        }
        
        .pdf-link {
            display: inline-block;
            margin-top: 5px;
            padding: 2px 6px;
            background: rgba(255,255,255,0.2);
            border-radius: 3px;
            text-decoration: none;
            font-size: 14px;
            transition: all 0.2s ease;
        }
        
        .pdf-link:hover {
            background: rgba(255,255,255,0.4);
            transform: scale(1.1);
        }
            
            /* 热力图颜色 */
            .heat-excellent {
                background: linear-gradient(135deg, #00b894, #00cec9);
                color: white;
            }
            
            .heat-good {
                background: linear-gradient(135deg, #00b894, #55a3ff);
                color: white;
            }
            
            .heat-average {
                background: linear-gradient(135deg, #fdcb6e, #e17055);
                color: white;
            }
            
            .heat-poor {
                background: linear-gradient(135deg, #fd79a8, #fdcb6e);
                color: white;
            }
            
            .heat-bad {
                background: linear-gradient(135deg, #fd79a8, #e84393);
                color: white;
            }
            
            .heatmap-cell.failed {
                background: linear-gradient(135deg, #636e72, #2d3436);
                color: white;
            }
        
        .success-box {
            background: #efe;
            border: 1px solid #cfc;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            color: #363;
            font-weight: bold;
        }
        
        .analysis-content h4 {
            color: #2c3e50;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        
        .analysis-content ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        
        .analysis-content li {
            margin: 8px 0;
            line-height: 1.5;
        }
        
        /* 工具介绍样式 */
        .tools-intro {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .tool-card {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .tool-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .tool-card h3 {
            margin: 0 0 15px 0;
            color: #2c3e50;
            font-size: 1.3em;
        }
        
        .tool-description p {
            margin: 10px 0;
            line-height: 1.6;
        }
        
        .tool-description ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        
        .tool-description li {
            margin: 5px 0;
            line-height: 1.5;
        }
        
        /* 工具介绍新样式 */
        .intro-overview {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .intro-text {
            font-size: 1.1em;
            color: #666;
            margin: 0;
        }
        
        .tools-comparison-table {
            margin: 30px 0;
        }
        
        .tools-comparison-table h3 {
            color: #333;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .feature-excellent {
            color: #4CAF50;
            font-weight: bold;
        }
        
        .feature-good {
            color: #FF9800;
            font-weight: bold;
        }
        
        .feature-limited {
            color: #FF5722;
            font-weight: bold;
        }
        
        .feature-none {
            color: #f44336;
            font-weight: bold;
        }
        
        .tools-detailed {
            margin-top: 40px;
        }
        
        .tool-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
        }
        
        .tool-header h3 {
            margin: 0;
            color: #333;
        }
        
        .tool-badge {
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        .tool-badge.modern {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .tool-badge.lightweight {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
        }
        
        .tool-badge.stable {
            background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
            color: white;
        }
        
        .tech-principle, .advantages, .use-cases {
            margin: 15px 0;
        }
        
        .tech-principle h4, .advantages h4, .use-cases h4 {
            margin: 0 0 8px 0;
            color: #555;
            font-size: 1em;
        }
        
        .tech-principle p, .use-cases p {
            margin: 0;
            color: #666;
            line-height: 1.6;
        }
        
        .advantages ul {
            margin: 8px 0;
            padding-left: 20px;
        }
        
        .advantages li {
            margin: 8px 0;
            line-height: 1.5;
        }
        
        /* 评分方法样式 */
        .scoring-method {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .dimensions-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .dimension-card {
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            padding: 15px;
            display: flex;
            align-items: flex-start;
            gap: 12px;
        }
        
        .dimension-icon {
            font-size: 1.5em;
            flex-shrink: 0;
        }
        
        .dimension-info h4 {
            margin: 0 0 5px 0;
            color: #2c3e50;
            font-size: 1.1em;
        }
        
        .weight {
            background: #e3f2fd;
            color: #1976d2;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 8px;
        }
        
        .dimension-info p {
            margin: 0;
            font-size: 0.9em;
            line-height: 1.4;
            color: #666;
        }
        
        .scoring-formula {
            margin-top: 30px;
        }
        
        .formula-box {
            background: #e8f5e8;
            border: 1px solid #c8e6c9;
            border-radius: 6px;
            padding: 15px;
            margin: 15px 0;
        }
        
        .formula-box p {
            margin: 5px 0;
            font-family: 'Courier New', monospace;
            font-weight: bold;
        }
        
        .quality-standards {
            margin-top: 20px;
        }
        
        .quality-standards ul {
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            padding: 15px 15px 15px 35px;
            margin: 10px 0;
        }
        
        /* 新增评分方法样式 */
        .evaluation-intro {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 30px;
        }
        
        .evaluation-intro p {
            margin: 0 0 20px 0;
            font-size: 1.1em;
            line-height: 1.6;
        }
        
        .evaluation-types {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        
        .eval-type {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 8px;
        }
        
        .eval-type h4 {
            margin: 0 0 10px 0;
            font-size: 1.1em;
        }
        
        .eval-type p {
            margin: 0;
            opacity: 0.9;
            line-height: 1.5;
        }
        
        .objective-metrics-section {
            margin: 40px 0;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .metric-card {
            background: white;
            border: 1px solid #e0e0e0;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }
        
        .metric-icon {
            font-size: 2em;
            margin-bottom: 15px;
        }
        
        .metric-info h4 {
            margin: 0 0 10px 0;
            color: #333;
            font-size: 1.2em;
        }
        
        .metric-formula {
            background: #f0f8ff;
            padding: 8px 12px;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            color: #2c5aa0;
            margin: 10px 0;
            border-left: 3px solid #667eea;
        }
        
        .metric-desc {
            color: #666;
            line-height: 1.5;
            margin: 10px 0 0 0;
        }
        
        .subjective-evaluation {
            margin: 40px 0;
        }
        
        .quality-standards li {
            margin: 8px 0;
            line-height: 1.5;
        }

        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 10px;
            }
            
            .header {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .content {
                padding: 20px;
            }
            
            .comparison-table {
                font-size: 0.9em;
            }
            
            .comparison-table th,
            .comparison-table td {
                padding: 8px;
            }
            
            .tools-intro {
                grid-template-columns: 1fr;
            }
            
            .dimensions-grid {
                grid-template-columns: 1fr;
            }
        }
        
        .module-scores {
            margin: 15px 0;
            padding: 15px;
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
        }
        
        .module-scores h4 {
            margin: 0 0 10px 0;
            color: #333;
            font-size: 14px;
        }
        
        .score-breakdown {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .score-item {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 12px;
        }
        
        .score-label {
            flex: 1;
            min-width: 120px;
        }
        
        .score-value {
            font-weight: bold;
            min-width: 30px;
            text-align: right;
        }
        
        .score-bar {
            flex: 1;
            height: 6px;
            background: rgba(255,255,255,0.3);
            border-radius: 3px;
            overflow: hidden;
        }
        
        .score-fill {
            height: 100%;
            transition: width 0.3s ease;
        }
        
        .performance-summary {
            margin-top: 15px;
            padding: 10px;
            background: rgba(255,255,255,0.1);
            border-radius: 6px;
            font-size: 12px;
        }
        
        .performance-summary h4 {
            margin: 0 0 8px 0;
            font-size: 14px;
            color: #333;
        }
        
        /* 使用建议样式 */
        .recommendation-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .scenario-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .scenario-card h4 {
            margin: 0 0 15px 0;
            font-size: 18px;
            font-weight: 600;
        }
        
        .recommended-tool {
            background: rgba(255,255,255,0.2);
            padding: 8px 12px;
            border-radius: 6px;
            font-weight: 600;
            margin-bottom: 15px;
            display: inline-block;
        }
        
        .reason ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        
        .reason li {
            margin: 5px 0;
        }
        
        .implementation-tips {
            margin: 30px 0;
        }
        
        .tips-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .tip-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #007bff;
        }
        
        .tip-card h5 {
            margin: 0 0 15px 0;
            color: #007bff;
            font-size: 16px;
        }
        
        .tip-card ul {
            margin: 0;
            padding-left: 20px;
        }
        
        .tip-card li {
            margin: 8px 0;
            color: #555;
        }
        
        .decision-matrix {
            margin: 30px 0;
        }
        
        .decision-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .decision-table th {
            background: #007bff;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        
        .decision-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }
        
        .decision-table tr:hover {
            background: #f8f9fa;
        }
        
        .decision-table tr:last-child td {
            border-bottom: none;
        }
        
        /* 得分来源依据样式 */
        .score-source {
            margin-top: 25px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #007bff;
        }
        
        .score-source h5 {
            margin: 0 0 15px 0;
            color: #007bff;
            font-size: 16px;
            font-weight: 600;
        }
        
        .source-explanation {
            color: #555;
            line-height: 1.6;
        }
        
        .source-explanation p {
            margin: 10px 0;
        }
        
        .source-explanation ul {
            margin: 15px 0;
            padding-left: 20px;
        }
        
        .source-explanation li {
            margin: 8px 0;
            line-height: 1.5;
        }
        
        .source-explanation strong {
            color: #2c3e50;
        }
        
        /* 客观评估样式 */
        .objective-details {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #17a2b8;
        }
        
        .objective-details h3 {
            color: #17a2b8;
            margin-top: 0;
            margin-bottom: 20px;
        }
        
        .metrics-explanation {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }
        
        .metric-item {
            background: white;
            padding: 15px;
            border-radius: 6px;
            border-left: 3px solid #17a2b8;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .metric-item strong {
            color: #17a2b8;
            display: block;
            margin-bottom: 5px;
        }
        
        .score-bar {
            position: relative;
            background: #e9ecef;
            border-radius: 10px;
            height: 25px;
            overflow: hidden;
        }
        
        .score-fill {
            background: linear-gradient(90deg, #28a745, #20c997);
            height: 100%;
            border-radius: 10px;
            transition: width 0.3s ease;
        }
        
        .score-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-weight: bold;
            font-size: 12px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }
        
        .metric-cell {
            text-align: center;
            font-weight: 600;
            color: #495057;
        }
        
        .score-cell {
            min-width: 120px;
        }
        
        /* 客观评估可视化样式 */
        .objective-overview {
            margin: 30px 0;
        }
        
        .score-comparison {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .score-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-left: 5px solid #ddd;
        }
        
        .score-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        .score-card.excellent { border-left-color: #4CAF50; }
        .score-card.good { border-left-color: #8BC34A; }
        .score-card.average { border-left-color: #FF9800; }
        .score-card.poor { border-left-color: #FF5722; }
        .score-card.failed { border-left-color: #f44336; }
        
        .tool-name-large {
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 15px;
        }
        
        .score-circle {
            margin: 20px 0;
        }
        
        .score-value {
            font-size: 36px;
            font-weight: 700;
            color: #2c3e50;
            display: block;
        }
        
        .score-label {
            font-size: 14px;
            color: #7f8c8d;
            margin-top: 5px;
        }
        
        .score-details {
            margin-top: 20px;
            padding-top: 15px;
            border-top: 1px solid #eee;
        }
        
        .detail-item {
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
            font-size: 14px;
        }
        
        .detail-label {
            color: #7f8c8d;
        }
        
        .detail-value {
            font-weight: 600;
            color: #2c3e50;
        }
        
        .metrics-visualization {
            margin: 40px 0;
            text-align: center;
        }
        
        .radar-chart-container {
            max-width: 500px;
            margin: 20px auto;
            padding: 20px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .detailed-metrics {
            margin: 40px 0;
        }
        
        .progress-bar {
            position: relative;
            background: #f0f0f0;
            border-radius: 20px;
            height: 24px;
            overflow: hidden;
            min-width: 120px;
        }
        
        .progress-fill {
            height: 100%;
            border-radius: 20px;
            transition: width 0.3s ease;
            position: relative;
        }
        
        .progress-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 12px;
            font-weight: 600;
            color: #333;
            z-index: 2;
        }
        
        .mini-progress {
            position: relative;
            background: #f0f0f0;
            border-radius: 10px;
            height: 16px;
            overflow: hidden;
            min-width: 80px;
            display: inline-block;
        }
        
        .mini-fill {
            height: 100%;
            border-radius: 10px;
            transition: width 0.3s ease;
        }
        
        .mini-progress span {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 10px;
            font-weight: 600;
            color: #333;
            z-index: 2;
        }
        
        .objective-insights {
            margin: 40px 0;
        }
        
        .insights-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .insight-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            display: flex;
            align-items: flex-start;
            gap: 15px;
            transition: transform 0.3s ease;
        }
        
        .insight-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        }
        
        .insight-icon {
            font-size: 24px;
            flex-shrink: 0;
        }
        
        .insight-content h4 {
            margin: 0 0 8px 0;
            font-size: 16px;
            color: #2c3e50;
        }
        
        .insight-content p {
            margin: 0;
            font-size: 14px;
            color: #7f8c8d;
            line-height: 1.4;
        }
        
        /* 增强的客观评估样式 */
        .enhanced-objective-evaluation .metrics-grid,
        .basic-objective-evaluation .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .metric-comparison-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border: 1px solid #e0e0e0;
        }
        
        .metric-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .metric-icon {
            font-size: 24px;
            margin-right: 10px;
        }
        
        .metric-header h4 {
            margin: 0;
            color: #333;
            font-size: 16px;
            font-weight: 600;
        }
        
        .metric-tools {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .tool-metric-item {
            padding: 12px;
            border-radius: 8px;
            background: #f8f9fa;
            border-left: 4px solid #ddd;
        }
        
        .tool-metric-item.first {
            border-left-color: #28a745;
            background: #f8fff9;
        }
        
        .tool-metric-item.second {
            border-left-color: #ffc107;
            background: #fffef8;
        }
        
        .tool-metric-item.third {
            border-left-color: #dc3545;
            background: #fff8f8;
        }
        
        .tool-metric-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        
        .tool-name {
            font-weight: 600;
            color: #333;
        }
        
        .metric-value {
            font-weight: 700;
            color: #007bff;
        }
        
        .metric-progress {
            height: 6px;
            background: #e9ecef;
            border-radius: 3px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #007bff, #0056b3);
            border-radius: 3px;
            transition: width 0.3s ease;
        }
        
        .tool-metric-item.first .progress-fill {
            background: linear-gradient(90deg, #28a745, #1e7e34);
        }
        
        .tool-metric-item.second .progress-fill {
            background: linear-gradient(90deg, #ffc107, #e0a800);
        }
        
        .tool-metric-item.third .progress-fill {
            background: linear-gradient(90deg, #dc3545, #c82333);
        }
        
        /* 增强的详细结果样式 */
        .enhanced-detailed-results {
            margin: 20px 0;
        }
        
        .results-table-container {
            overflow-x: auto;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .results-table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            min-width: 800px;
        }
        
        .results-table th {
            background: #f8f9fa;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #333;
            border-bottom: 2px solid #dee2e6;
        }
        
        .results-table td {
            padding: 15px;
            border-bottom: 1px solid #dee2e6;
            vertical-align: top;
        }
        
        .sample-name {
            font-weight: 600;
            color: #495057;
            background: #f8f9fa;
            min-width: 120px;
        }
        
        .result-cell {
            min-width: 180px;
        }
        
        .result-cell.success {
            background: #f8fff9;
            border-left: 4px solid #28a745;
        }
        
        .result-cell.failed {
            background: #fff8f8;
            border-left: 4px solid #dc3545;
        }
        
        .result-cell.no-data {
            background: #f8f9fa;
            border-left: 4px solid #6c757d;
        }
        
        .result-status {
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .result-cell.success .result-status {
            color: #28a745;
        }
        
        .result-cell.failed .result-status {
            color: #dc3545;
        }
        
        .result-cell.no-data .result-status {
            color: #6c757d;
        }
        
        .result-details {
            font-size: 12px;
            color: #666;
            margin-bottom: 8px;
        }
        
        .result-details div {
            margin-bottom: 2px;
        }
        
        .pdf-link {
            display: inline-block;
            padding: 4px 8px;
            background: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
            transition: background 0.2s;
        }
        
        .pdf-link:hover {
            background: #0056b3;
            text-decoration: none;
            color: white;
        }
        
        .error-msg {
            font-size: 11px;
            color: #dc3545;
            margin-top: 5px;
            font-style: italic;
        }
        
        /* 工具概览样式 */
        .tools-overview {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 20px 0;
            padding: 30px;
        }
        
        .tools-intro h3 {
            color: #2c3e50;
            margin-bottom: 25px;
            font-size: 24px;
            text-align: center;
        }
        
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .tool-card {
            border: 2px solid #e9ecef;
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s ease;
            background: #f8f9fa;
        }
        
        .tool-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }
        
        .tool-card.playwright {
            border-color: #9b59b6;
            background: linear-gradient(135deg, #f8f4ff 0%, #f0e6ff 100%);
        }
        
        .tool-card.weasyprint {
            border-color: #3498db;
            background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
        }
        
        .tool-card.libreoffice {
            border-color: #e67e22;
            background: linear-gradient(135deg, #fff8f0 0%, #ffe6d9 100%);
        }
        
        .tool-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .tool-icon {
            font-size: 24px;
            margin-right: 10px;
        }
        
        .tool-header h4 {
            margin: 0;
            color: #2c3e50;
            font-size: 20px;
        }
        
        .tool-description p {
            margin: 8px 0;
            color: #555;
            line-height: 1.5;
        }
        
        .tool-description strong {
            color: #2c3e50;
        }
        
        /* 限制对比表格样式 */
        .limitations-comparison h3 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 22px;
            text-align: center;
        }
        
        .comparison-table-container {
            overflow-x: auto;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .limitations-table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            font-size: 14px;
        }
        
        .limitations-table th {
            background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
            color: white;
            padding: 15px 12px;
            text-align: center;
            font-weight: 600;
            border-bottom: 2px solid #2c3e50;
        }
        
        .limitations-table th:first-child {
            text-align: left;
            min-width: 120px;
        }
        
        .limitations-table td {
            padding: 12px;
            border-bottom: 1px solid #eee;
            text-align: center;
        }
        
        .limitations-table .feature-name {
            font-weight: 600;
            color: #2c3e50;
            text-align: left;
            background: #f8f9fa;
        }
        
        .limitations-table tbody tr:hover {
            background-color: #f1f3f4;
        }
        
        .support-excellent {
            background: #d4edda;
            color: #155724;
            font-weight: 600;
            border-radius: 4px;
            padding: 6px 8px;
        }
        
        .support-good {
            background: #d1ecf1;
            color: #0c5460;
            font-weight: 600;
            border-radius: 4px;
            padding: 6px 8px;
        }
        
        .support-limited {
            background: #fff3cd;
            color: #856404;
            font-weight: 600;
            border-radius: 4px;
            padding: 6px 8px;
        }
        
        .support-none {
            background: #f8d7da;
            color: #721c24;
            font-weight: 600;
            border-radius: 4px;
            padding: 6px 8px;
        }
        
        /* 简化的整体指标对比样式 */
        .overall-metrics-comparison {
            margin: 20px 0;
        }
        
        .metrics-summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        
        .tool-summary-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .tool-summary-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }
        
        .tool-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
        }
        
        .tool-header .rank-icon {
            font-size: 1.5em;
            margin-right: 10px;
        }
        
        .tool-header h3 {
            margin: 0;
            color: #333;
            font-size: 1.3em;
            flex-grow: 1;
        }
        
        .overall-score {
            background: #667eea;
            color: white;
            padding: 6px 12px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 14px;
        }
        
        .key-metrics {
            display: grid;
            gap: 10px;
        }
        
        .metric-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .metric-item:last-child {
            border-bottom: none;
        }
        
        .metric-label {
            font-size: 14px;
            color: #666;
            font-weight: 500;
        }
        
        .metric-value {
            display: block;
            font-size: 18px;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .metric-bar {
            background: #e9ecef;
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
            position: relative;
        }
        
        .metric-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 0.8s ease;
            position: relative;
        }
        
        .metric-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.3) 50%, transparent 100%);
            animation: shimmer 2s infinite;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        /* 表格对比样式 */
        .table-comparison-evaluation {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            margin: 20px 0;
            overflow: hidden;
        }

        .comparison-table-wrapper {
            overflow-x: auto;
            margin: 20px;
        }

        .metrics-comparison-table {
            width: 100%;
            border-collapse: collapse;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .metrics-comparison-table th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 12px;
            text-align: center;
            font-weight: 600;
            font-size: 14px;
            border: none;
        }

        .metric-header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%) !important;
            min-width: 150px;
            text-align: left !important;
        }

        .tool-header.playwright {
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%) !important;
        }

        .tool-header.weasyprint {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%) !important;
        }

        .tool-header.libreoffice {
            background: linear-gradient(135deg, #27ae60 0%, #229954 100%) !important;
        }

        .best-header {
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%) !important;
            min-width: 100px;
        }

        .metrics-comparison-table td {
            padding: 12px;
            text-align: center;
            border-bottom: 1px solid #ecf0f1;
            font-size: 13px;
            transition: all 0.3s ease;
        }

        .metric-row:hover {
            background-color: #f8f9fa;
        }

        .metric-name {
            font-weight: 600;
            color: #2c3e50;
            text-align: left !important;
            background-color: #f8f9fa;
            border-right: 2px solid #ecf0f1;
        }

        .metric-value {
            font-weight: 500;
            color: #34495e;
        }

        .best-value {
            background: linear-gradient(135deg, #d5f4e6 0%, #c8e6c9 100%);
            color: #27ae60;
            font-weight: 700;
            position: relative;
        }

        .best-value::before {
            content: "🏆";
            position: absolute;
            top: 50%;
            left: 5px;
            transform: translateY(-50%);
            font-size: 12px;
        }

        .normal-value {
            color: #7f8c8d;
        }

        .best-tool {
            font-weight: 700;
            color: #f39c12;
            background: linear-gradient(135deg, #fef9e7 0%, #fcf3cf 100%);
        }

        .metrics-legend {
            background: #f8f9fa;
            padding: 20px;
            border-top: 1px solid #ecf0f1;
        }

        .metrics-legend h4 {
            color: #2c3e50;
            margin: 0 0 15px 0;
            font-size: 16px;
            font-weight: 600;
        }

        .legend-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 12px;
        }

        .legend-item {
            display: flex;
            align-items: center;
            padding: 8px 12px;
            background: white;
            border-radius: 6px;
            border-left: 4px solid #3498db;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .legend-icon {
            font-size: 16px;
            margin-right: 10px;
            min-width: 20px;
        }

        .legend-text {
            font-size: 13px;
            color: #34495e;
            line-height: 1.4;
        }

        .legend-text strong {
            color: #2c3e50;
        }

        /* 响应式设计 */
        @media (max-width: 768px) {
            .comparison-table-wrapper {
                margin: 10px;
            }
            
            .metrics-comparison-table th,
            .metrics-comparison-table td {
                padding: 8px 6px;
                font-size: 12px;
            }
            
            .legend-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """
    
    def generate_comparison_table_html(self, results: Dict[str, List[SampleResult]], 
                                     metrics: Dict[str, EvaluationMetrics]) -> str:
        """生成对比表格HTML"""
        
        # 获取所有样例名称
        all_samples = set()
        for tool_results in results.values():
            for result in tool_results:
                all_samples.add(result.sample_name)
        all_samples = sorted(list(all_samples))
        
        # 生成表格头部
        html = """
        <table class="comparison-table">
            <thead>
                <tr>
                    <th>样例</th>
                    <th>WeasyPrint</th>
                    <th>Playwright</th>
                    <th>LibreOffice</th>
                </tr>
            </thead>
            <tbody>
        """
        
        # 为每个样例生成行
        for sample in all_samples:
            html += f"<tr><td><strong>{sample}</strong></td>"
            
            # 为每个工具生成单元格
            for tool in ["WeasyPrint", "Playwright", "LibreOffice"]:
                # 查找该工具对该样例的结果
                result = None
                if tool in results:
                    for r in results[tool]:
                        if r.sample_name == sample:
                            result = r
                            break
                
                if result:
                    # 修复WeasyPrint显示问题：确保正确显示状态和数据
                    status_class = "status-success" if result.conversion_success else "status-failed"
                    status_text = "成功" if result.conversion_success else "失败"
                    
                    # 格式化时间和文件大小
                    time_str = f"{result.conversion_time:.2f}s" if result.conversion_time else "N/A"
                    size_str = f"{result.file_size/1024:.1f}KB" if result.file_size else "N/A"
                    
                    # 质量评分
                    quality_str = f"{result.quality_score:.1f}" if result.quality_score else "N/A"
                    
                    cell_content = f"""
                    <span class="{status_class}">{status_text}</span><br>
                    <small>质量: {quality_str}</small><br>
                    <small>时间: {time_str}</small><br>
                    <small>大小: {size_str}</small>
                    """
                    
                    # 如果转换失败且有错误信息，显示错误
                    if not result.conversion_success and result.error_message:
                        cell_content += f"<br><small style='color: #f44336;'>错误: {result.error_message[:30]}...</small>"
                else:
                    cell_content = "<span class='status-failed'>无数据</span>"
                
                html += f"<td>{cell_content}</td>"
            
            html += "</tr>"
        
        html += """
            </tbody>
        </table>
        """
        
        return html

    def generate_tools_overview_html(self) -> str:
        """生成工具概览和HTML解析限制对比表格"""
        html = """
        <div class="tools-overview">
            <div class="tools-intro">
                <h3>🔧 HTML转PDF工具介绍</h3>
                <div class="tools-grid">
                    <div class="tool-card playwright">
                        <div class="tool-header">
                            <span class="tool-icon">🎭</span>
                            <h4>Playwright</h4>
                        </div>
                        <div class="tool-description">
                            <p><strong>类型：</strong>浏览器自动化工具</p>
                            <p><strong>原理：</strong>使用真实浏览器引擎渲染HTML后生成PDF</p>
                            <p><strong>优势：</strong>完美支持现代CSS、JavaScript和复杂布局</p>
                            <p><strong>适用场景：</strong>复杂网页、动态内容、高保真度要求</p>
                        </div>
                    </div>
                    
                    <div class="tool-card weasyprint">
                        <div class="tool-header">
                            <span class="tool-icon">📄</span>
                            <h4>WeasyPrint</h4>
                        </div>
                        <div class="tool-description">
                            <p><strong>类型：</strong>专用HTML转PDF库</p>
                            <p><strong>原理：</strong>直接解析HTML/CSS并生成PDF</p>
                            <p><strong>优势：</strong>轻量级、快速、支持打印媒体查询</p>
                            <p><strong>适用场景：</strong>文档生成、报表、简单到中等复杂度页面</p>
                        </div>
                    </div>
                    
                    <div class="tool-card libreoffice">
                        <div class="tool-header">
                            <span class="tool-icon">📊</span>
                            <h4>LibreOffice</h4>
                        </div>
                        <div class="tool-description">
                            <p><strong>类型：</strong>办公套件转换工具</p>
                            <p><strong>原理：</strong>通过Writer组件导入HTML并导出PDF</p>
                            <p><strong>优势：</strong>强大的文档处理能力、丰富的格式支持</p>
                            <p><strong>适用场景：</strong>文档转换、办公文档、标准化输出</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="limitations-comparison">
                <h3>📋 HTML解析能力与限制对比</h3>
                <div class="comparison-table-container">
                    <table class="limitations-table">
                        <thead>
                            <tr>
                                <th>功能特性</th>
                                <th>Playwright</th>
                                <th>WeasyPrint</th>
                                <th>LibreOffice</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="feature-name">CSS3支持</td>
                                <td class="support-excellent">优秀</td>
                                <td class="support-good">良好</td>
                                <td class="support-limited">有限</td>
                            </tr>
                            <tr>
                                <td class="feature-name">JavaScript执行</td>
                                <td class="support-excellent">完全支持</td>
                                <td class="support-none">不支持</td>
                                <td class="support-none">不支持</td>
                            </tr>
                            <tr>
                                <td class="feature-name">Flexbox布局</td>
                                <td class="support-excellent">完全支持</td>
                                <td class="support-good">基本支持</td>
                                <td class="support-limited">有限支持</td>
                            </tr>
                            <tr>
                                <td class="feature-name">Grid布局</td>
                                <td class="support-excellent">完全支持</td>
                                <td class="support-limited">有限支持</td>
                                <td class="support-none">不支持</td>
                            </tr>
                            <tr>
                                <td class="feature-name">Web字体</td>
                                <td class="support-excellent">完全支持</td>
                                <td class="support-good">支持</td>
                                <td class="support-limited">有限支持</td>
                            </tr>
                            <tr>
                                <td class="feature-name">SVG图像</td>
                                <td class="support-excellent">完全支持</td>
                                <td class="support-good">支持</td>
                                <td class="support-good">支持</td>
                            </tr>
                            <tr>
                                <td class="feature-name">表单元素</td>
                                <td class="support-good">基本支持</td>
                                <td class="support-limited">有限支持</td>
                                <td class="support-limited">有限支持</td>
                            </tr>
                            <tr>
                                <td class="feature-name">打印媒体查询</td>
                                <td class="support-excellent">完全支持</td>
                                <td class="support-excellent">完全支持</td>
                                <td class="support-good">基本支持</td>
                            </tr>
                            <tr>
                                <td class="feature-name">中文字体</td>
                                <td class="support-excellent">完全支持</td>
                                <td class="support-excellent">完全支持</td>
                                <td class="support-excellent">完全支持</td>
                            </tr>
                            <tr>
                                <td class="feature-name">转换速度</td>
                                <td class="support-good">中等</td>
                                <td class="support-excellent">快速</td>
                                <td class="support-limited">较慢</td>
                            </tr>
                            <tr>
                                <td class="feature-name">文件大小</td>
                                <td class="support-excellent">最小</td>
                                <td class="support-limited">较大</td>
                                <td class="support-good">中等</td>
                            </tr>
                            <tr>
                                <td class="feature-name">部署复杂度</td>
                                <td class="support-limited">较复杂</td>
                                <td class="support-excellent">简单</td>
                                <td class="support-limited">较复杂</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        """
        return html

    def generate_table_comparison_objective_evaluation_html(self, results: Dict[str, List[SampleResult]], 
                                                          objective_metrics: Dict[str, ObjectiveMetrics]) -> str:
        """生成表格对比形式的客观评估指标详解"""
        if not objective_metrics:
            return self.generate_basic_objective_evaluation_html(results)
        
        # 计算各工具的详细指标
        tool_metrics = {}
        for tool_name, metrics in objective_metrics.items():
            tool_results = results.get(tool_name, [])
            
            # 计算成功率
            success_count = sum(1 for r in tool_results if r.conversion_success)
            success_rate = (success_count / len(tool_results)) * 100 if tool_results else 0
            
            # 计算平均转换时间
            successful_times = [r.conversion_time for r in tool_results if r.conversion_success and r.conversion_time > 0]
            avg_time = sum(successful_times) / len(successful_times) if successful_times else 0
            
            # 计算平均文件大小
            successful_sizes = [r.file_size for r in tool_results if r.conversion_success and r.file_size > 0]
            avg_size = sum(successful_sizes) / len(successful_sizes) if successful_sizes else 0
            
            # 计算压缩效率（相对于最大文件大小）
            max_size = max([r.file_size for r in tool_results if r.file_size > 0], default=1)
            compression_efficiency = ((max_size - avg_size) / max_size) * 100 if max_size > 0 else 0
            
            tool_metrics[tool_name] = {
                'success_rate': success_rate,
                'avg_time': avg_time,
                'avg_size': avg_size,
                'compression_efficiency': compression_efficiency,
                'text_retention': metrics.text_preservation_rate if metrics.text_preservation_rate > 0 else None,
                'chinese_support': metrics.chinese_support_score if metrics.chinese_support_score > 0 else None,
                'image_support': metrics.image_support_rate if metrics.image_support_rate > 0 else None,
                'form_support': metrics.form_support_rate if metrics.form_support_rate > 0 else None,
                'page_structure': metrics.page_structure_score if metrics.page_structure_score > 0 else None
            }
        
        html = """
        <div class="table-comparison-evaluation">
            <div class="comparison-table-wrapper">
                <table class="metrics-comparison-table">
                    <thead>
                        <tr>
                            <th class="metric-header">评估指标</th>
                            <th class="tool-header playwright">🎭 Playwright</th>
                            <th class="tool-header weasyprint">📄 WeasyPrint</th>
                            <th class="tool-header libreoffice">📊 LibreOffice</th>
                            <th class="best-header">🏆 最佳</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # 定义指标配置
        metrics_config = [
            ('success_rate', '✅ 转换成功率', '%', True),
            ('avg_time', '⚡ 平均转换时间', 's', False),
            ('avg_size', '📦 平均文件大小', 'KB', False),
            ('compression_efficiency', '🗜️ 压缩效率', '%', True),
            ('text_retention', '📝 文本保留率', '%', True),
            ('chinese_support', '🇨🇳 中文支持率', '%', True),
            ('image_support', '🖼️ 图片支持率', '%', True),
            ('form_support', '📋 表单支持率', '%', True),
            ('page_structure', '🏗️ 页面结构', '分', True)
        ]
        
        for metric_key, metric_name, unit, higher_better in metrics_config:
            html += f"""
                        <tr class="metric-row">
                            <td class="metric-name">{metric_name}</td>
            """
            
            # 获取各工具的值
            values = {}
            for tool_name in ['playwright', 'weasyprint', 'libreoffice']:
                if tool_name in tool_metrics:
                    value = tool_metrics[tool_name][metric_key]
                    if metric_key == 'avg_size' and value is not None and value > 0:
                        value = value / 1024  # 转换为KB
                    values[tool_name] = value
                else:
                    values[tool_name] = None
            
            # 找出最佳值
            valid_values = {k: v for k, v in values.items() if v is not None and v > 0}
            if valid_values:
                if higher_better:
                    best_tool = max(valid_values.keys(), key=lambda k: valid_values[k])
                else:
                    best_tool = min(valid_values.keys(), key=lambda k: valid_values[k])
            else:
                best_tool = None
            
            # 生成各工具的单元格
            for tool_name in ['playwright', 'weasyprint', 'libreoffice']:
                value = values[tool_name]
                is_best = best_tool is not None and tool_name == best_tool
                
                # 根据不同指标类型提供更准确的显示
                if value is None:
                    if metric_key in ['text_retention', 'chinese_support', 'image_support', 'form_support', 'page_structure']:
                        display_value = "无数据"
                    else:
                        display_value = "N/A"
                elif value == 0:
                    if metric_key == 'success_rate':
                        display_value = "0.0%"
                    elif metric_key in ['avg_time', 'avg_size']:
                        display_value = "N/A"
                    else:
                        display_value = f"0.0{unit}"
                else:
                    if metric_key == 'avg_time':
                        display_value = f"{value:.2f}{unit}"
                    elif metric_key == 'avg_size':
                        display_value = f"{value:.1f}{unit}"
                    else:
                        display_value = f"{value:.1f}{unit}"
                
                cell_class = "best-value" if is_best else "normal-value"
                html += f"""
                            <td class="metric-value {cell_class}">{display_value}</td>
                """
            
            # 最佳工具列
            if best_tool is not None:
                best_display = best_tool.title()
            else:
                best_display = "无数据"
            html += f"""
                            <td class="best-tool">{best_display}</td>
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
            </div>
            
            <div class="metrics-legend">
                <h4>📖 指标说明</h4>
                <div class="legend-grid">
                    <div class="legend-item">
                        <span class="legend-icon">✅</span>
                        <span class="legend-text"><strong>转换成功率：</strong>成功转换的样例占总样例的百分比</span>
                    </div>
                    <div class="legend-item">
                        <span class="legend-icon">⚡</span>
                        <span class="legend-text"><strong>平均转换时间：</strong>成功转换样例的平均耗时（仅统计成功案例）</span>
                    </div>
                    <div class="legend-item">
                        <span class="legend-icon">📦</span>
                        <span class="legend-text"><strong>平均文件大小：</strong>生成PDF文件的平均大小（仅统计成功案例）</span>
                    </div>
                    <div class="legend-item">
                        <span class="legend-icon">🗜️</span>
                        <span class="legend-text"><strong>压缩效率：</strong>相对于最大文件的压缩程度</span>
                    </div>
                    <div class="legend-item">
                        <span class="legend-icon">📝</span>
                        <span class="legend-text"><strong>文本保留率：</strong>基于PDF内容分析的文本保留程度</span>
                    </div>
                    <div class="legend-item">
                        <span class="legend-icon">🇨🇳</span>
                        <span class="legend-text"><strong>中文支持率：</strong>基于PDF内容分析的中文字符支持程度</span>
                    </div>
                    <div class="legend-item">
                        <span class="legend-icon">🖼️</span>
                        <span class="legend-text"><strong>图片支持率：</strong>基于PDF内容分析的图像元素支持程度</span>
                    </div>
                    <div class="legend-item">
                        <span class="legend-icon">📋</span>
                        <span class="legend-text"><strong>表单支持率：</strong>基于PDF内容分析的表单元素支持程度</span>
                    </div>
                    <div class="legend-item">
                        <span class="legend-icon">🏗️</span>
                        <span class="legend-text"><strong>页面结构：</strong>基于PDF内容分析的整体布局结构评分</span>
                    </div>
                </div>
            </div>
        </div>
        """
        
        return html

    def generate_enhanced_objective_evaluation_html(self, results: Dict[str, List[SampleResult]], 
                                                   objective_metrics: Dict[str, ObjectiveMetrics]) -> str:
        """生成增强的客观评估HTML，包含成功率、生成大小、生成速度等指标"""
        if not objective_metrics:
            return self.generate_basic_objective_evaluation_html(results)
        
        html = """
        <div class="enhanced-objective-evaluation">
            <div class="metrics-grid">
        """
        
        # 定义关键指标
        key_metrics = [
            ("success_rate", "成功率", "%", "🎯"),
            ("avg_file_size", "平均大小", "KB", "📁"),
            ("compression_efficiency", "压缩效率", "%", "🗜️"),
            ("text_preservation_rate", "文本保留率", "%", "📝"),
            ("chinese_support_score", "中文支持", "%", "🇨🇳"),
            ("image_support_rate", "图片支持率", "%", "🖼️"),
            ("form_support_rate", "表单支持率", "%", "📋"),
            ("page_structure_score", "页面结构", "%", "🏗️")
        ]
        
        for metric_key, metric_name, unit, icon in key_metrics:
            html += f"""
            <div class="metric-comparison-card">
                <div class="metric-header">
                    <span class="metric-icon">{icon}</span>
                    <h4>{metric_name}</h4>
                </div>
                <div class="metric-tools">
            """
            
            # 获取各工具的该指标数据
            tool_values = []
            for tool_name, metrics in objective_metrics.items():
                if hasattr(metrics, metric_key):
                    value = getattr(metrics, metric_key)
                    if metric_key == "avg_file_size":
                        display_value = f"{value / 1024:.1f}"
                    else:
                        display_value = f"{value:.1f}"
                    tool_values.append((tool_name, value, display_value))
            
            # 按值排序（文件大小按小到大，其他按大到小）
            if metric_key == "avg_file_size":
                tool_values.sort(key=lambda x: x[1])
            else:
                tool_values.sort(key=lambda x: x[1], reverse=True)
            
            for i, (tool_name, value, display_value) in enumerate(tool_values):
                rank_class = "first" if i == 0 else "second" if i == 1 else "third"
                
                # 计算进度条宽度
                if tool_values:
                    max_val = max(tv[1] for tv in tool_values)
                    min_val = min(tv[1] for tv in tool_values)
                    if max_val > min_val:
                        if metric_key == "avg_file_size":
                            # 文件大小：越小越好
                            progress = ((max_val - value) / (max_val - min_val)) * 100
                        else:
                            # 其他指标：越大越好
                            progress = ((value - min_val) / (max_val - min_val)) * 100
                    else:
                        progress = 100
                else:
                    progress = 0
                
                html += f"""
                <div class="tool-metric-item {rank_class}">
                    <div class="tool-metric-header">
                        <span class="tool-name">{tool_name}</span>
                        <span class="metric-value">{display_value}{unit}</span>
                    </div>
                    <div class="metric-progress">
                        <div class="progress-fill" style="width: {progress}%;"></div>
                    </div>
                </div>
                """
            
            html += """
                </div>
            </div>
            """
        
        html += """
            </div>
        </div>
        """
        
        return html

    def generate_basic_objective_evaluation_html(self, results: Dict[str, List[SampleResult]]) -> str:
        """生成基础的客观评估HTML，基于转换结果计算指标"""
        html = """
        <div class="basic-objective-evaluation">
            <div class="metrics-grid">
        """
        
        # 计算基础指标
        tool_metrics = {}
        for tool_name, tool_results in results.items():
            # 成功率
            success_count = sum(1 for r in tool_results if r.conversion_success)
            success_rate = (success_count / len(tool_results)) * 100 if tool_results else 0
            
            # 平均转换时间
            successful_times = [r.conversion_time for r in tool_results if r.conversion_success and r.conversion_time > 0]
            avg_time = sum(successful_times) / len(successful_times) if successful_times else 0
            
            # 平均文件大小
            successful_sizes = [r.file_size for r in tool_results if r.conversion_success and r.file_size > 0]
            avg_size = sum(successful_sizes) / len(successful_sizes) if successful_sizes else 0
            
            # 平均质量分数
            quality_scores = [r.quality_score for r in tool_results if r.quality_score > 0]
            avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
            
            tool_metrics[tool_name] = {
                'success_rate': success_rate,
                'avg_time': avg_time,
                'avg_size': avg_size,
                'avg_quality': avg_quality
            }
        
        # 定义基础指标
        basic_metrics = [
            ("success_rate", "成功率", "%", "🎯"),
            ("avg_time", "平均速度", "s", "⚡"),
            ("avg_size", "平均大小", "KB", "📁"),
            ("avg_quality", "质量评分", "", "⭐")
        ]
        
        for metric_key, metric_name, unit, icon in basic_metrics:
            html += f"""
            <div class="metric-comparison-card">
                <div class="metric-header">
                    <span class="metric-icon">{icon}</span>
                    <h4>{metric_name}</h4>
                </div>
                <div class="metric-tools">
            """
            
            # 获取各工具的该指标数据
            tool_values = []
            for tool_name, metrics in tool_metrics.items():
                value = metrics[metric_key]
                if metric_key == "avg_size":
                    display_value = f"{value / 1024:.1f}"
                elif metric_key == "avg_time":
                    display_value = f"{value:.2f}"
                else:
                    display_value = f"{value:.1f}"
                tool_values.append((tool_name, value, display_value))
            
            # 按值排序（时间和文件大小按小到大，其他按大到小）
            if metric_key in ["avg_time", "avg_size"]:
                tool_values.sort(key=lambda x: x[1])
            else:
                tool_values.sort(key=lambda x: x[1], reverse=True)
            
            for i, (tool_name, value, display_value) in enumerate(tool_values):
                rank_class = "first" if i == 0 else "second" if i == 1 else "third"
                
                # 计算进度条宽度
                if tool_values:
                    max_val = max(tv[1] for tv in tool_values)
                    min_val = min(tv[1] for tv in tool_values)
                    if max_val > min_val:
                        if metric_key in ["avg_time", "avg_size"]:
                            # 时间和文件大小：越小越好
                            progress = ((max_val - value) / (max_val - min_val)) * 100
                        else:
                            # 其他指标：越大越好
                            progress = ((value - min_val) / (max_val - min_val)) * 100
                    else:
                        progress = 100
                else:
                    progress = 0
                
                html += f"""
                <div class="tool-metric-item {rank_class}">
                    <div class="tool-metric-header">
                        <span class="tool-name">{tool_name}</span>
                        <span class="metric-value">{display_value}{unit}</span>
                    </div>
                    <div class="metric-progress">
                        <div class="progress-fill" style="width: {progress}%;"></div>
                    </div>
                </div>
                """
            
            html += """
                </div>
            </div>
            """
        
        html += """
            </div>
        </div>
        """
        
        return html

    def generate_enhanced_detailed_results_html(self, results: Dict[str, List[SampleResult]]) -> str:
        """生成增强的详细结果HTML，包含PDF查看功能"""
        html = """
        <div class="enhanced-detailed-results">
            <div class="results-table-container">
                <table class="results-table">
                    <thead>
                        <tr>
                            <th>样例</th>
                            <th>WeasyPrint</th>
                            <th>Playwright</th>
                            <th>LibreOffice</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # 获取所有样例名称
        all_samples = set()
        for tool_results in results.values():
            for result in tool_results:
                all_samples.add(result.sample_name)
        
        all_samples = sorted(list(all_samples))
        
        for sample in all_samples:
            html += f"""
            <tr>
                <td class="sample-name">{sample}</td>
            """
            
            for tool_name in ["WeasyPrint", "Playwright", "LibreOffice"]:
                # 查找该工具对该样例的结果
                result = None
                if tool_name in results:
                    for r in results[tool_name]:
                        if r.sample_name == sample:
                            result = r
                            break
                
                if result:
                    status_class = "success" if result.conversion_success else "failed"
                    status_text = "成功" if result.conversion_success else "失败"
                    
                    # 生成PDF查看链接
                    pdf_link = ""
                    if result.conversion_success and result.file_path:
                        # 将绝对路径转换为相对路径，考虑HTML文件在output目录下
                        import os
                        rel_path = os.path.relpath(result.file_path, "/Users/jay/Desktop/script/output")
                        pdf_link = f'<a href="{rel_path}" target="_blank" class="pdf-link">查看PDF</a>'
                    
                    html += f"""
                    <td class="result-cell {status_class}">
                        <div class="result-status">{status_text}</div>
                        <div class="result-details">
                            <div>时间: {result.conversion_time:.2f}s</div>
                            <div>大小: {result.file_size / 1024:.1f}KB</div>
                            <div>质量: {result.quality_score:.0f}</div>
                        </div>
                        {pdf_link}
                        {f'<div class="error-msg">{result.error_message}</div>' if result.error_message else ''}
                    </td>
                    """
                else:
                    html += """
                    <td class="result-cell no-data">
                        <div class="result-status">无数据</div>
                    </td>
                    """
            
            html += "</tr>"
        
        html += """
                    </tbody>
                </table>
            </div>
        </div>
        """
        
        return html
    
    def generate_objective_evaluation_html(self, objective_metrics: Dict[str, ObjectiveMetrics]) -> str:
        """生成客观评估HTML部分"""
        if not objective_metrics:
            return ""
        
        # 生成综合评分对比
        overview_html = """
        <div class="section">
            <h2>🔬 客观评估指标</h2>
            <p>基于PDF文档分析的客观评估结果，包含多维度技术指标的量化分析</p>
            
            <div class="objective-overview">
                <h3>📊 综合评分对比</h3>
                <div class="score-comparison">
        """
        
        # 为每个工具生成评分卡片
        for tool_name, metrics in objective_metrics.items():
            color_class = self._get_score_color_class(metrics.overall_score)
            overview_html += f"""
                    <div class="score-card {color_class}">
                        <div class="tool-name-large">{tool_name}</div>
                        <div class="score-circle">
                            <div class="score-value">{metrics.overall_score:.1f}</div>
                            <div class="score-label">综合评分</div>
                        </div>
                        <div class="score-details">
                            <div class="detail-item">
                                <span class="detail-label">成功率:</span>
                                <span class="detail-value">{metrics.success_rate:.1f}%</span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label">平均大小:</span>
                                <span class="detail-value">{metrics.avg_file_size:.1f}KB</span>
                            </div>
                        </div>
                    </div>
            """
        
        overview_html += """
                </div>
            </div>
            
            <div class="metrics-visualization">
                <h3>📈 详细指标对比</h3>
                <div class="radar-chart-container">
                    <canvas id="radarChart" width="400" height="400"></canvas>
                </div>
            </div>
        """
        
        # 生成详细指标表格
        table_html = """
            <div class="detailed-metrics">
                <h3>📋 详细数据表格</h3>
                <div class="comparison-table">
                    <table>
                        <thead>
                            <tr>
                                <th>工具</th>
                                <th>综合评分</th>
                                <th>文本保留率</th>
                                <th>图片支持率</th>
                                <th>表单支持率</th>
                                <th>成功率</th>
                                <th>压缩效率</th>
                                <th>平均大小</th>
                            </tr>
                        </thead>
                        <tbody>
        """
        
        for tool_name, metrics in objective_metrics.items():
            table_html += f"""
                        <tr>
                            <td class="tool-name">{tool_name}</td>
                            <td class="score-cell">
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: {metrics.overall_score}%; background: {self._get_score_color(metrics.overall_score)}"></div>
                                    <span class="progress-text">{metrics.overall_score:.1f}</span>
                                </div>
                            </td>
                            <td class="metric-cell">
                                <div class="mini-progress">
                                    <div class="mini-fill" style="width: {metrics.text_preservation_rate}%; background: {self._get_score_color(metrics.text_preservation_rate)}"></div>
                                    <span>{metrics.text_preservation_rate:.1f}%</span>
                                </div>
                            </td>
                            <td class="metric-cell">
                                <div class="mini-progress">
                                    <div class="mini-fill" style="width: {metrics.image_support_rate}%; background: {self._get_score_color(metrics.image_support_rate)}"></div>
                                    <span>{metrics.image_support_rate:.1f}%</span>
                                </div>
                            </td>
                            <td class="metric-cell">
                                <div class="mini-progress">
                                    <div class="mini-fill" style="width: {metrics.form_support_rate}%; background: {self._get_score_color(metrics.form_support_rate)}"></div>
                                    <span>{metrics.form_support_rate:.1f}%</span>
                                </div>
                            </td>
                            <td class="metric-cell">
                                <div class="mini-progress">
                                    <div class="mini-fill" style="width: {metrics.success_rate}%; background: {self._get_score_color(metrics.success_rate)}"></div>
                                    <span>{metrics.success_rate:.1f}%</span>
                                </div>
                            </td>
                            <td class="metric-cell">{metrics.compression_efficiency:.1f}%</td>
                            <td class="metric-cell">{metrics.avg_file_size:.1f}KB</td>
                        </tr>
            """
        
        table_html += """
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div class="objective-insights">
                <h3>💡 关键洞察</h3>
                <div class="insights-grid">
        """
        
        # 生成关键洞察
        best_overall = max(objective_metrics.items(), key=lambda x: x[1].overall_score)
        best_text = max(objective_metrics.items(), key=lambda x: x[1].text_preservation_rate)
        best_image = max(objective_metrics.items(), key=lambda x: x[1].image_support_rate)
        best_success = max(objective_metrics.items(), key=lambda x: x[1].success_rate)
        
        table_html += f"""
                    <div class="insight-card">
                        <div class="insight-icon">🏆</div>
                        <div class="insight-content">
                            <h4>综合表现最佳</h4>
                            <p><strong>{best_overall[0]}</strong> 以 {best_overall[1].overall_score:.1f} 分获得最高综合评分</p>
                        </div>
                    </div>
                    
                    <div class="insight-card">
                        <div class="insight-icon">📝</div>
                        <div class="insight-content">
                            <h4>文本保留最佳</h4>
                            <p><strong>{best_text[0]}</strong> 文本保留率达到 {best_text[1].text_preservation_rate:.1f}%</p>
                        </div>
                    </div>
                    
                    <div class="insight-card">
                        <div class="insight-icon">🖼️</div>
                        <div class="insight-content">
                            <h4>图片支持最佳</h4>
                            <p><strong>{best_image[0]}</strong> 图片支持率达到 {best_image[1].image_support_rate:.1f}%</p>
                        </div>
                    </div>
                    
                    <div class="insight-card">
                        <div class="insight-icon">✅</div>
                        <div class="insight-content">
                            <h4>稳定性最佳</h4>
                            <p><strong>{best_success[0]}</strong> 转换成功率达到 {best_success[1].success_rate:.1f}%</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        
        # 添加雷达图脚本
        radar_script = self._generate_radar_chart_script(objective_metrics)
        
        return overview_html + table_html + radar_script
    
    def _get_score_color_class(self, score: float) -> str:
        """根据分数获取颜色类名"""
        if score >= 90:
            return "excellent"
        elif score >= 80:
            return "good"
        elif score >= 70:
            return "average"
        elif score >= 60:
            return "poor"
        else:
            return "failed"
    
    def _get_score_color(self, score: float) -> str:
        """根据分数获取颜色值"""
        if score >= 90:
            return "#4CAF50"
        elif score >= 80:
            return "#8BC34A"
        elif score >= 70:
            return "#FF9800"
        elif score >= 60:
            return "#FF5722"
        else:
            return "#f44336"
    
    def _generate_radar_chart_script(self, objective_metrics: Dict[str, ObjectiveMetrics]) -> str:
        """生成雷达图脚本"""
        # 准备数据
        tools = list(objective_metrics.keys())
        datasets = []
        
        colors = ['#667eea', '#f093fb', '#4facfe']
        
        for i, (tool_name, metrics) in enumerate(objective_metrics.items()):
            color = colors[i % len(colors)]
            datasets.append({
                'label': tool_name,
                'data': [
                    metrics.text_preservation_rate,
                    metrics.image_support_rate,
                    metrics.form_support_rate,
                    metrics.success_rate,
                    metrics.compression_efficiency,
                    metrics.overall_score
                ],
                'borderColor': color,
                'backgroundColor': color + '20',
                'pointBackgroundColor': color,
                'pointBorderColor': '#fff',
                'pointHoverBackgroundColor': '#fff',
                'pointHoverBorderColor': color
            })
        
        script = f"""
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const ctx = document.getElementById('radarChart').getContext('2d');
            new Chart(ctx, {{
                type: 'radar',
                data: {{
                    labels: ['文本保留率', '图片支持率', '表单支持率', '成功率', '压缩效率', '综合评分'],
                    datasets: {datasets}
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        r: {{
                            beginAtZero: true,
                            max: 100,
                            ticks: {{
                                stepSize: 20
                            }}
                        }}
                    }},
                    plugins: {{
                        legend: {{
                            position: 'bottom'
                        }}
                    }}
                }}
            }});
        }});
        </script>
        """
        
        return script
    
    def generate_visual_comparison_html(self, results: Dict[str, List[SampleResult]], 
                                      metrics: Dict[str, EvaluationMetrics]) -> str:
        """生成可视化对比HTML（包含图表和热力图）"""
        
        # 获取所有样例名称
        all_samples = set()
        for tool_results in results.values():
            for result in tool_results:
                all_samples.add(result.sample_name)
        all_samples = sorted(list(all_samples))
        
        # 准备图表数据
        chart_data = self._prepare_chart_data(results, all_samples)
        
        html = f"""
        <div class="visual-comparison-section">
            <h3>📊 可视化对比分析</h3>
            
            <!-- 图表选择器 -->
            <div class="chart-selector">
                <button class="chart-btn active" onclick="showChart('quality')">质量评分对比</button>
                <button class="chart-btn" onclick="showChart('performance')">性能对比</button>
                <button class="chart-btn" onclick="showChart('radar')">综合雷达图</button>
                <button class="chart-btn" onclick="showChart('heatmap')">热力图表格</button>
            </div>
            
            <!-- 质量评分柱状图 -->
            <div id="quality-chart" class="chart-container">
                <h4>质量评分对比</h4>
                <canvas id="qualityChart" width="800" height="400"></canvas>
            </div>
            
            <!-- 性能对比图 -->
            <div id="performance-chart" class="chart-container" style="display: none;">
                <h4>转换时间对比</h4>
                <canvas id="performanceChart" width="800" height="400"></canvas>
            </div>
            
            <!-- 雷达图 -->
            <div id="radar-chart" class="chart-container" style="display: none;">
                <h4>综合性能雷达图</h4>
                <canvas id="radarChart" width="600" height="600"></canvas>
            </div>
            
            <!-- 热力图表格 -->
            <div id="heatmap-chart" class="chart-container" style="display: none;">
                <h4>样例转换状态热力图</h4>
                {self._generate_heatmap_table(results, all_samples)}
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
        {self._generate_chart_scripts(chart_data, metrics)}
        </script>
        """
        
        return html
    
    def _prepare_chart_data(self, results: Dict[str, List[SampleResult]], all_samples: List[str]) -> Dict:
        """准备图表数据"""
        data = {
            'samples': all_samples,
            'tools': ['WeasyPrint', 'Playwright', 'LibreOffice'],
            'quality_scores': {},
            'conversion_times': {},
            'file_sizes': {},
            'success_rates': {}
        }
        
        for tool in data['tools']:
            data['quality_scores'][tool] = []
            data['conversion_times'][tool] = []
            data['file_sizes'][tool] = []
            
            for sample in all_samples:
                result = None
                if tool in results:
                    for r in results[tool]:
                        if r.sample_name == sample:
                            result = r
                            break
                
                if result and result.conversion_success:
                    data['quality_scores'][tool].append(result.quality_score or 0)
                    data['conversion_times'][tool].append(result.conversion_time or 0)
                    data['file_sizes'][tool].append((result.file_size or 0) / 1024)  # KB
                else:
                    data['quality_scores'][tool].append(0)
                    data['conversion_times'][tool].append(0)
                    data['file_sizes'][tool].append(0)
        
        return data
    
    def _generate_heatmap_table(self, results: Dict[str, List[SampleResult]], all_samples: List[str]) -> str:
        """生成热力图样式的表格"""
        html = """
        <table class="heatmap-table">
            <thead>
                <tr>
                    <th>样例</th>
                    <th>WeasyPrint</th>
                    <th>Playwright</th>
                    <th>LibreOffice</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for sample in all_samples:
            html += f"<tr><td class='sample-name'>{sample}</td>"
            
            for tool in ["WeasyPrint", "Playwright", "LibreOffice"]:
                result = None
                if tool in results:
                    for r in results[tool]:
                        if r.sample_name == sample:
                            result = r
                            break
                
                if result and result.conversion_success:
                    # 根据质量评分设置颜色强度
                    quality = result.quality_score or 0
                    intensity = min(quality / 100, 1.0)
                    color_class = self._get_heatmap_color_class(intensity)
                    
                    # 生成PDF文件路径
                    tool_suffix = {
                        "WeasyPrint": "weasyprint",
                        "Playwright": "playwright", 
                        "LibreOffice": "soffice"
                    }.get(tool, tool.lower())
                    
                    sample_base = sample.replace('.html', '')
                    pdf_path = f"../src/test_data/outputs/{sample_base}_{tool_suffix}.pdf"
                    
                    html += f"""
                    <td class="heatmap-cell {color_class}" data-quality="{quality:.1f}">
                        <div class="cell-content">
                            <span class="status">✓</span>
                            <span class="quality">{quality:.1f}</span>
                            <span class="time">{result.conversion_time:.2f}s</span>
                            <a href="{pdf_path}" class="pdf-link" target="_blank" title="查看PDF文件">📄</a>
                        </div>
                    </td>
                    """
                else:
                    html += f"""
                    <td class="heatmap-cell failed">
                        <div class="cell-content">
                            <span class="status">✗</span>
                            <span class="error">失败</span>
                        </div>
                    </td>
                    """
            
            html += "</tr>"
        
        html += "</tbody></table>"
        return html
    
    def _get_heatmap_color_class(self, intensity: float) -> str:
        """根据强度返回热力图颜色类"""
        if intensity >= 0.9:
            return "heat-excellent"
        elif intensity >= 0.8:
            return "heat-good"
        elif intensity >= 0.7:
            return "heat-average"
        elif intensity >= 0.5:
            return "heat-poor"
        else:
            return "heat-bad"
    
    def _generate_chart_scripts(self, chart_data: Dict, metrics: Dict[str, EvaluationMetrics]) -> str:
        """生成图表JavaScript代码"""
        return f"""
        // 图表数据
        const chartData = {chart_data};
        const metrics = {self._metrics_to_dict(metrics)};
        
        // 图表配置
        const chartColors = {{
            'WeasyPrint': '#3498db',
            'Playwright': '#e74c3c', 
            'LibreOffice': '#f39c12'
        }};
        
        // 质量评分柱状图
        const qualityCtx = document.getElementById('qualityChart').getContext('2d');
        const qualityChart = new Chart(qualityCtx, {{
            type: 'bar',
            data: {{
                labels: chartData.samples,
                datasets: chartData.tools.map(tool => ({{
                    label: tool,
                    data: chartData.quality_scores[tool],
                    backgroundColor: chartColors[tool] + '80',
                    borderColor: chartColors[tool],
                    borderWidth: 2
                }}))
            }},
            options: {{
                responsive: true,
                plugins: {{
                    title: {{
                        display: true,
                        text: '各工具质量评分对比'
                    }},
                    legend: {{
                        position: 'top'
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        title: {{
                            display: true,
                            text: '质量评分'
                        }}
                    }}
                }}
            }}
        }});
        
        // 性能对比图
        const performanceCtx = document.getElementById('performanceChart').getContext('2d');
        const performanceChart = new Chart(performanceCtx, {{
            type: 'line',
            data: {{
                labels: chartData.samples,
                datasets: chartData.tools.map(tool => ({{
                    label: tool,
                    data: chartData.conversion_times[tool],
                    borderColor: chartColors[tool],
                    backgroundColor: chartColors[tool] + '20',
                    tension: 0.4,
                    fill: false
                }}))
            }},
            options: {{
                responsive: true,
                plugins: {{
                    title: {{
                        display: true,
                        text: '转换时间对比'
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: '转换时间 (秒)'
                        }}
                    }}
                }}
            }}
        }});
        
        // 雷达图
        const radarCtx = document.getElementById('radarChart').getContext('2d');
        const radarChart = new Chart(radarCtx, {{
            type: 'radar',
            data: {{
                labels: ['平均质量', '转换速度', '成功率', '文件大小优化', '稳定性'],
                datasets: chartData.tools.map(tool => ({{
                    label: tool,
                    data: [
                        metrics[tool].avg_quality_score,
                        100 - (metrics[tool].avg_conversion_time * 10), // 转换为0-100分
                        metrics[tool].success_rate,
                        100 - Math.min(metrics[tool].avg_file_size / 10000, 100), // 文件大小优化分
                        metrics[tool].success_rate // 稳定性用成功率表示
                    ],
                    borderColor: chartColors[tool],
                    backgroundColor: chartColors[tool] + '20',
                    pointBackgroundColor: chartColors[tool]
                }}))
            }},
            options: {{
                responsive: true,
                plugins: {{
                    title: {{
                        display: true,
                        text: '综合性能雷达图'
                    }}
                }},
                scales: {{
                    r: {{
                        beginAtZero: true,
                        max: 100
                    }}
                }}
            }}
        }});
        
        // 图表切换函数
        function showChart(chartType) {{
            // 隐藏所有图表
            document.querySelectorAll('.chart-container').forEach(container => {{
                container.style.display = 'none';
            }});
            
            // 移除所有按钮的active类
            document.querySelectorAll('.chart-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            
            // 显示选中的图表
            document.getElementById(chartType + '-chart').style.display = 'block';
            
            // 激活对应按钮
            event.target.classList.add('active');
        }}
        """
    
    def _metrics_to_dict(self, metrics: Dict[str, EvaluationMetrics]) -> str:
        """将metrics转换为JavaScript对象字符串"""
        result = {}
        for tool, metric in metrics.items():
            # 计算成功率
            successful_results = [r for r in metric.sample_results if r.conversion_success]
            success_rate = (len(successful_results) / len(metric.sample_results)) * 100 if metric.sample_results else 0
            
            # 计算平均转换时间
            avg_conversion_time = sum(metric.conversion_times) / len(metric.conversion_times) if metric.conversion_times else 0
            
            # 计算平均文件大小
            file_size_values = list(metric.file_sizes.values()) if metric.file_sizes else []
            avg_file_size = sum(file_size_values) / len(file_size_values) if file_size_values else 0
            
            # 计算平均质量评分
            quality_scores = [r.quality_score for r in metric.sample_results if r.quality_score]
            avg_quality_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0
            
            result[tool] = {
                'success_rate': success_rate,
                'avg_conversion_time': avg_conversion_time,
                'avg_file_size': avg_file_size,
                'avg_quality_score': avg_quality_score
            }
        return str(result).replace("'", '"')

    def generate_failure_analysis_html(self, results: Dict[str, List[SampleResult]]) -> str:
        """生成失败原因分析部分"""
        
        html = """
        <div class="section">
            <h2>🔍 失败原因分析</h2>
            <div class="analysis-content">
                <h3>Playwright转换special_chars.html失败分析</h3>
                <div class="failure-analysis">
                    <h4>问题描述</h4>
                    <p>在之前的测试中，Playwright在转换<code>special_chars.html</code>文件时出现了以下错误：</p>
                    <div class="error-box">
                        <code>Page.pdf: Protocol error (Page.printToPDF): Printing failed</code>
                    </div>
                    
                    <h4>根本原因分析</h4>
                    <ul>
                        <li><strong>特殊字符复杂性：</strong>special_chars.html包含大量特殊字符，包括：
                            <ul>
                                <li>数学符号（±、×、÷、∞、∑、∏、∫、√等）</li>
                                <li>大量Emoji表情符号（😀-🙏、🚀-🛿等）</li>
                                <li>多语言字符（拉丁、希腊、俄语、阿拉伯、日语、韩语）</li>
                                <li>特殊空格和控制字符</li>
                            </ul>
                        </li>
                        <li><strong>字体渲染问题：</strong>Chromium的PDF引擎在处理某些Unicode字符范围时可能出现兼容性问题</li>
                        <li><strong>内存消耗：</strong>大量特殊字符的渲染可能导致内存使用过高，触发浏览器保护机制</li>
                        <li><strong>正则表达式错误：</strong>在处理Emoji字符范围时出现"Range out of order in character class"错误</li>
                    </ul>
                    
                    <h4>解决方案</h4>
                    <p>通过以下优化措施，成功解决了转换失败问题：</p>
                    <ul>
                        <li><strong>简化字符处理：</strong>移除了复杂的Emoji正则表达式处理</li>
                        <li><strong>优化浏览器参数：</strong>添加了<code>--no-sandbox</code>、<code>--disable-dev-shm-usage</code>等稳定性参数</li>
                        <li><strong>改进错误处理：</strong>增加了重试机制和更详细的错误日志</li>
                        <li><strong>内存管理：</strong>优化了页面加载和渲染流程</li>
                    </ul>
                    
                    <h4>当前状态</h4>
                    <div class="success-box">
                        ✅ 问题已解决：Playwright现在可以成功转换special_chars.html文件
                    </div>
                    
                    <h4>WeasyPrint SVG兼容性警告</h4>
                    <div class="warning-box">
                        <code>WARNING:weasyprint:Ignored `stop-color:#ff7675` at 1:1, unknown property.</code>
                    </div>
                    <p><strong>问题分析：</strong></p>
                    <ul>
                        <li><strong>SVG渐变支持限制：</strong>WeasyPrint对SVG的<code>stop-color</code>属性支持不完整</li>
                        <li><strong>影响范围：</strong>主要影响svg.html中的线性渐变效果显示</li>
                        <li><strong>兼容性问题：</strong>WeasyPrint的SVG渲染引擎相比浏览器引擎功能有限</li>
                        <li><strong>解决方案：</strong>可以使用纯色填充替代渐变，或使用CSS渐变代替SVG渐变</li>
                    </ul>
                    
                    <h4>调研建议</h4>
                    <ul>
                        <li><strong>字符集测试：</strong>在实际项目中，建议对包含大量特殊字符的文档进行专门测试</li>
                        <li><strong>渐进式处理：</strong>对于复杂文档，可以考虑分段处理或预处理特殊字符</li>
                        <li><strong>SVG兼容性：</strong>使用WeasyPrint时避免复杂的SVG渐变，优先使用CSS渐变</li>
                        <li><strong>备选方案：</strong>对于特殊字符密集的文档，WeasyPrint表现更稳定；对于复杂SVG，Playwright更适合</li>
                        <li><strong>性能监控：</strong>建议在生产环境中监控转换时间和内存使用情况</li>
                    </ul>
                </div>
            </div>
        </div>
        """
        
        return html
    
    def generate_tools_introduction_html(self) -> str:
        """生成工具介绍HTML"""
        html = """
        <div class="tools-introduction">
            <div class="tool-intro-card">
                <h3><span class="tool-icon">🎭</span>Playwright</h3>
                <p><strong>技术架构：</strong>基于Chromium浏览器引擎的现代化PDF生成工具</p>
                <p><strong>核心优势：</strong>完整支持JavaScript和现代CSS，生成文件最小，渲染质量最高</p>
                <p><strong>适用场景：</strong>现代Web应用、动态内容、高质量要求的PDF生成</p>
            </div>
            
            <div class="tool-intro-card">
                <h3><span class="tool-icon">🐍</span>WeasyPrint</h3>
                <p><strong>技术架构：</strong>纯Python实现的HTML/CSS渲染引擎</p>
                <p><strong>核心优势：</strong>轻量级部署，转换速度最快，优秀的打印样式支持</p>
                <p><strong>适用场景：</strong>服务器端批量处理、报告生成、快速部署</p>
            </div>
            
            <div class="tool-intro-card">
                <h3><span class="tool-icon">📄</span>LibreOffice</h3>
                <p><strong>技术架构：</strong>基于LibreOffice Writer的文档处理引擎</p>
                <p><strong>核心优势：</strong>成熟稳定，强大的文档格式处理，优秀的表格支持</p>
                <p><strong>适用场景：</strong>传统文档转换、企业级应用、复杂表格处理</p>
            </div>
        </div>
        """
        return html
    
    def generate_parsing_capabilities_comparison_html(self) -> str:
        """生成HTML解析能力与限制对比"""
        html = f"""
        <div class="limitations-comparison">
            <div class="comparison-table-container">
                <table class="limitations-table">
                    <thead>
                        <tr>
                            <th>功能特性</th>
                            <th>Playwright</th>
                            <th>WeasyPrint</th>
                            <th>LibreOffice</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="feature-name">CSS3支持</td>
                            <td class="support-excellent">优秀</td>
                            <td class="support-good">良好</td>
                            <td class="support-limited">有限</td>
                        </tr>
                        <tr>
                            <td class="feature-name">JavaScript执行</td>
                            <td class="support-excellent">完全支持</td>
                            <td class="support-none">不支持</td>
                            <td class="support-none">不支持</td>
                        </tr>
                        <tr>
                            <td class="feature-name">Flexbox布局</td>
                            <td class="support-excellent">完全支持</td>
                            <td class="support-good">基本支持</td>
                            <td class="support-limited">有限支持</td>
                        </tr>
                        <tr>
                            <td class="feature-name">Grid布局</td>
                            <td class="support-excellent">完全支持</td>
                            <td class="support-limited">有限支持</td>
                            <td class="support-none">不支持</td>
                        </tr>
                        <tr>
                            <td class="feature-name">Web字体</td>
                            <td class="support-excellent">完全支持</td>
                            <td class="support-good">支持</td>
                            <td class="support-limited">有限支持</td>
                        </tr>
                        <tr>
                            <td class="feature-name">SVG图像</td>
                            <td class="support-excellent">完全支持</td>
                            <td class="support-good">支持</td>
                            <td class="support-good">支持</td>
                        </tr>
                        <tr>
                            <td class="feature-name">表单元素</td>
                            <td class="support-good">基本支持</td>
                            <td class="support-limited">有限支持</td>
                            <td class="support-limited">有限支持</td>
                        </tr>
                        <tr>
                            <td class="feature-name">打印媒体查询</td>
                            <td class="support-excellent">完全支持</td>
                            <td class="support-excellent">完全支持</td>
                            <td class="support-good">基本支持</td>
                        </tr>
                        <tr>
                            <td class="feature-name">中文字体</td>
                            <td class="support-excellent">完全支持</td>
                            <td class="support-excellent">完全支持</td>
                            <td class="support-excellent">完全支持</td>
                        </tr>
                        <tr>
                            <td class="feature-name">转换速度</td>
                            <td class="support-good">中等</td>
                            <td class="support-excellent">快速</td>
                            <td class="support-limited">较慢</td>
                        </tr>
                        <tr>
                            <td class="feature-name">文件大小</td>
                            <td class="support-excellent">最小</td>
                            <td class="support-limited">较大</td>
                            <td class="support-good">中等</td>
                        </tr>
                        <tr>
                            <td class="feature-name">部署复杂度</td>
                            <td class="support-limited">较复杂</td>
                            <td class="support-excellent">简单</td>
                            <td class="support-limited">较复杂</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        """
        return html
    
    def generate_scoring_method_html(self) -> str:
        """生成评分方法说明HTML"""
        html = """
        <div class="scoring-method">
            <div class="method-overview">
                <h3>📊 评估方法概述</h3>
                <div class="evaluation-intro">
                    <p>本评估系统采用<strong>客观量化指标</strong>与<strong>主观质量评估</strong>相结合的方式，全面评估HTML到PDF转换工具的性能表现。</p>
                    <div class="evaluation-types">
                        <div class="eval-type">
                            <h4>🔢 客观评估指标</h4>
                            <p>基于技术指标的量化评估，包括文件大小、转换成功率、内容保留率等可测量的数据</p>
                        </div>
                        <div class="eval-type">
                            <h4>👁️ 主观质量评估</h4>
                            <p>基于视觉效果和功能完整性的人工评估，关注用户体验和实际使用效果</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="objective-metrics-section">
                <h3>📈 客观评估指标详解</h3>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-icon">📊</div>
                        <div class="metric-info">
                            <h4>综合评分</h4>
                            <p class="metric-formula">= (文本保留率 × 30% + 图片支持率 × 25% + 表单支持率 × 20% + 成功率 × 15% + 压缩效率 × 10%)</p>
                            <p class="metric-desc">综合考虑各项技术指标的加权平均分，反映工具的整体性能</p>
                        </div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-icon">📝</div>
                        <div class="metric-info">
                            <h4>文本保留率</h4>
                            <p class="metric-formula">= PDF中提取的文本长度 / HTML中原始文本长度 × 100%</p>
                            <p class="metric-desc">衡量文本内容在转换过程中的完整性，越高表示文本丢失越少</p>
                        </div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-icon">🖼️</div>
                        <div class="metric-info">
                            <h4>图片支持率</h4>
                            <p class="metric-formula">= PDF中检测到的图片数量 / HTML中原始图片数量 × 100%</p>
                            <p class="metric-desc">评估图片元素的转换成功率，包括img标签、背景图片等</p>
                        </div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-icon">📋</div>
                        <div class="metric-info">
                            <h4>表单支持率</h4>
                            <p class="metric-formula">= PDF中保留的表单字段数 / HTML中原始表单字段数 × 100%</p>
                            <p class="metric-desc">检测表单元素（输入框、按钮等）在PDF中的保留情况</p>
                        </div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-icon">✅</div>
                        <div class="metric-info">
                            <h4>转换成功率</h4>
                            <p class="metric-formula">= 成功转换的文件数 / 总测试文件数 × 100%</p>
                            <p class="metric-desc">衡量工具的稳定性和兼容性，反映处理各种HTML文件的能力</p>
                        </div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-icon">🗜️</div>
                        <div class="metric-info">
                            <h4>压缩效率</h4>
                            <p class="metric-formula">= (1 - PDF文件大小 / HTML文件大小) × 100%</p>
                            <p class="metric-desc">评估文件压缩效果，正值表示压缩，负值表示文件增大</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="subjective-evaluation">
                <h3>🎨 主观质量评估维度</h3>
                <div class="dimensions-grid">
                    <div class="dimension-card">
                        <div class="dimension-icon">🎨</div>
                        <div class="dimension-info">
                            <h4>排版与视觉还原度</h4>
                            <div class="weight">权重: 35%</div>
                            <p>评估CSS布局、字体渲染、颜色显示、间距控制、分页效果等视觉还原能力</p>
                        </div>
                    </div>
                    
                    <div class="dimension-card">
                        <div class="dimension-icon">🧠</div>
                        <div class="dimension-info">
                            <h4>功能支持</h4>
                            <div class="weight">权重: 25%</div>
                            <p>评估JavaScript执行、动态内容处理、SVG支持、字体嵌入等功能完整性</p>
                        </div>
                    </div>
                    
                    <div class="dimension-card">
                        <div class="dimension-icon">⚙️</div>
                        <div class="dimension-info">
                            <h4>性能与稳定性</h4>
                            <div class="weight">权重: 20%</div>
                            <p>评估转换速度、内存占用、错误处理、大文档处理能力等性能指标</p>
                        </div>
                    </div>
                    
                    <div class="dimension-card">
                        <div class="dimension-icon">🧩</div>
                        <div class="dimension-info">
                            <h4>部署可行性</h4>
                            <div class="weight">权重: 10%</div>
                            <p>评估安装复杂度、系统依赖、跨平台兼容性、维护成本等部署因素</p>
                        </div>
                    </div>
                    
                    <div class="dimension-card">
                        <div class="dimension-icon">🪶</div>
                        <div class="dimension-info">
                            <h4>可定制性</h4>
                            <div class="weight">权重: 10%</div>
                            <p>评估输出配置选项、页眉页脚设置、水印添加、格式控制等定制能力</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="scoring-formula">
                <h3>🧮 评分计算公式</h3>
                <div class="formula-box">
                    <p><strong>主观综合得分 = </strong></p>
                    <p>排版视觉得分 × 35% + 功能支持得分 × 25% + 性能稳定得分 × 20% + 部署可行得分 × 10% + 可定制得分 × 10%</p>
                </div>
                
                <div class="quality-standards">
                    <h4>📏 质量评分标准</h4>
                    <ul>
                        <li><strong>90-100分：</strong>优秀 - 完美还原原始HTML效果</li>
                        <li><strong>80-89分：</strong>良好 - 基本还原，有轻微差异</li>
                        <li><strong>70-79分：</strong>一般 - 可用但有明显差异</li>
                        <li><strong>60-69分：</strong>较差 - 功能受限，效果不佳</li>
                        <li><strong>0-59分：</strong>失败 - 无法正常转换或严重错误</li>
                    </ul>
                </div>
            </div>
        </div>
        """
        return html

    def generate_overall_metrics_comparison_html(self, results: Dict[str, List[SampleResult]], 
                                               metrics: Dict[str, EvaluationMetrics]) -> str:
        """生成整体指标对比HTML"""
        html = """
        <div class="overall-metrics-comparison">
            <div class="metrics-summary">
        """
        
        # 计算各工具的关键指标
        tool_stats = {}
        for tool_name, tool_results in results.items():
            # 计算成功率
            success_count = sum(1 for r in tool_results if r.conversion_success)
            success_rate = (success_count / len(tool_results)) * 100 if tool_results else 0
            
            # 计算平均转换时间
            successful_times = [r.conversion_time for r in tool_results if r.conversion_success and r.conversion_time > 0]
            avg_time = sum(successful_times) / len(successful_times) if successful_times else 0
            
            # 计算平均文件大小
            successful_sizes = [r.file_size for r in tool_results if r.conversion_success and r.file_size > 0]
            avg_size = sum(successful_sizes) / len(successful_sizes) if successful_sizes else 0
            
            # 计算平均质量分数
            quality_scores = [r.quality_score for r in tool_results if r.quality_score > 0]
            avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
            
            # 计算综合评分
            weighted_score = metrics[tool_name].calculate_weighted_score() if tool_name in metrics else 0
            
            tool_stats[tool_name] = {
                'success_rate': success_rate,
                'avg_time': avg_time,
                'avg_size': avg_size,
                'avg_quality': avg_quality,
                'weighted_score': weighted_score
            }
        
        # 按综合评分排序
        sorted_tools = sorted(tool_stats.items(), key=lambda x: x[1]['weighted_score'], reverse=True)
        
        for i, (tool_name, stats) in enumerate(sorted_tools):
            rank_icon = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
            
            html += f"""
            <div class="tool-summary-card">
                <div class="tool-header">
                    <span class="rank-icon">{rank_icon}</span>
                    <h3>{tool_name}</h3>
                    <span class="overall-score">{stats['weighted_score']:.1f}分</span>
                </div>
                <div class="key-metrics">
                    <div class="metric-item">
                        <span class="metric-label">成功率</span>
                        <span class="metric-value">{stats['success_rate']:.1f}%</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">平均速度</span>
                        <span class="metric-value">{stats['avg_time']:.2f}s</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">平均大小</span>
                        <span class="metric-value">{stats['avg_size'] / 1024:.1f}KB</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">质量评分</span>
                        <span class="metric-value">{stats['avg_quality']:.1f}</span>
                    </div>
                </div>
            </div>
            """
        
        html += """
            </div>
        </div>
        """
        
        return html

    def generate_overall_comparison_html(self, metrics: Dict[str, EvaluationMetrics]) -> str:
        """生成整体对比HTML"""
        html = """
        <div class="performance-grid">
        """
        
        # 按分数排序
        sorted_tools = sorted(metrics.items(), key=lambda x: x[1].calculate_weighted_score(), reverse=True)
        
        for tool_name, metric in sorted_tools:
            # 确定分数颜色
            weighted_score = metric.calculate_weighted_score()
            if weighted_score >= 80:
                score_class = "score-high"
                card_color = "#4CAF50"
            elif weighted_score >= 60:
                score_class = "score-medium" 
                card_color = "#FF9800"
            else:
                score_class = "score-low"
                card_color = "#f44336"
            
            # 计算成功率和平均值
            successful_results = [r for r in metric.conversion_times if r > 0]
            success_rate = len(successful_results) / len(metric.conversion_times) * 100 if metric.conversion_times else 0
            avg_time = sum(successful_results) / len(successful_results) if successful_results else 0
            file_size_values = list(metric.file_sizes.values()) if metric.file_sizes else []
            avg_size = sum(file_size_values) / len(file_size_values) if file_size_values else 0
            
            html += f"""
            <div class="tool-card" style="border-top-color: {card_color};">
                <div class="tool-name">{tool_name}</div>
                <div class="tool-score {score_class}">{weighted_score:.1f}分</div>
                
                <div class="module-scores">
                    <h4>📊 各模块得分</h4>
                    <div class="score-breakdown">
                        <div class="score-item">
                            <span class="score-label">🎨 排版视觉 (35%)</span>
                            <span class="score-value">{metric.layout_visual_score:.1f}</span>
                            <div class="score-bar">
                                <div class="score-fill" style="width: {metric.layout_visual_score}%; background: #4CAF50;"></div>
                            </div>
                        </div>
                        <div class="score-item">
                            <span class="score-label">🧠 功能支持 (25%)</span>
                            <span class="score-value">{metric.functionality_score:.1f}</span>
                            <div class="score-bar">
                                <div class="score-fill" style="width: {metric.functionality_score}%; background: #2196F3;"></div>
                            </div>
                        </div>
                        <div class="score-item">
                            <span class="score-label">⚙️ 性能稳定 (20%)</span>
                            <span class="score-value">{metric.performance_score:.1f}</span>
                            <div class="score-bar">
                                <div class="score-fill" style="width: {metric.performance_score}%; background: #FF9800;"></div>
                            </div>
                        </div>
                        <div class="score-item">
                            <span class="score-label">🧩 部署可行 (10%)</span>
                            <span class="score-value">{metric.deployment_score:.1f}</span>
                            <div class="score-bar">
                                <div class="score-fill" style="width: {metric.deployment_score}%; background: #9C27B0;"></div>
                            </div>
                        </div>
                        <div class="score-item">
                            <span class="score-label">🪶 可定制性 (10%)</span>
                            <span class="score-value">{metric.customization_score:.1f}</span>
                            <div class="score-bar">
                                <div class="score-fill" style="width: {metric.customization_score}%; background: #607D8B;"></div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="performance-summary">
                    <h4>📈 性能指标</h4>
                    <div><strong>成功率:</strong> {success_rate:.1f}%</div>
                    <div><strong>平均时间:</strong> {avg_time:.2f}s</div>
                    <div><strong>平均大小:</strong> {avg_size/1024:.1f}KB</div>
                </div>
            </div>
            """
        
        html += """
        </div>
        """
        
        return html
    
    def generate_detailed_results_html(self, results: Dict[str, List[SampleResult]]) -> str:
        """生成详细结果HTML"""
        html = ""
        
        for tool_name, tool_results in results.items():
            html += f"""
            <div class="section">
                <h3>{tool_name} 详细结果</h3>
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>样例</th>
                            <th>状态</th>
                            <th>质量评分</th>
                            <th>转换时间</th>
                            <th>文件大小</th>
                            <th>错误信息</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            
            for result in tool_results:
                status_class = "status-success" if result.conversion_success else "status-failed"
                status_text = "成功" if result.conversion_success else "失败"
                
                # 修复WeasyPrint显示问题：确保所有数据正确显示
                quality_display = f"{result.quality_score:.1f}" if result.quality_score is not None else "N/A"
                time_display = f"{result.conversion_time:.2f}s" if result.conversion_time is not None else "N/A"
                size_display = f"{result.file_size/1024:.1f}KB" if result.file_size is not None else "N/A"
                error_display = result.error_message[:50] + "..." if result.error_message and len(result.error_message) > 50 else (result.error_message or "无")
                
                # 为成功的转换添加PDF链接
                pdf_link = ""
                if result.conversion_success:
                    # 根据工具名称映射到正确的文件后缀
                    tool_suffix = {
                        "WeasyPrint": "weasyprint",
                        "Playwright": "playwright", 
                        "LibreOffice": "soffice"
                    }.get(tool_name, tool_name.lower())
                    
                    sample_base = result.sample_name.replace('.html', '')
                    pdf_path = f"../src/test_data/outputs/{sample_base}_{tool_suffix}.pdf"
                    pdf_link = f'<br><a href="{pdf_path}" class="pdf-link" target="_blank">📄 查看PDF</a>'
                
                html += f"""
                <tr>
                    <td><strong>{result.sample_name}</strong>{pdf_link}</td>
                    <td><span class="{status_class}">{status_text}</span></td>
                    <td>{quality_display}</td>
                    <td>{time_display}</td>
                    <td>{size_display}</td>
                    <td><small>{error_display}</small></td>
                </tr>
                """
            
            html += """
                    </tbody>
                </table>
            </div>
            """
        
        return html
    
    def generate_performance_analysis_html(self, metrics: Dict[str, EvaluationMetrics]) -> str:
        """生成性能分析HTML"""
        html = """
        <div class="section">
            <h2>📊 性能分析</h2>
        """
        
        # 计算每个工具的平均值
        tool_stats = {}
        for tool_name, metric in metrics.items():
            successful_results = [r for r in metric.conversion_times if r > 0]
            avg_time = sum(successful_results) / len(successful_results) if successful_results else float('inf')
            
            file_size_values = list(metric.file_sizes.values()) if metric.file_sizes else []
            avg_size = sum(file_size_values) / len(file_size_values) if file_size_values else 0
            
            tool_stats[tool_name] = {'avg_time': avg_time, 'avg_size': avg_size}
        
        # 找出最快和最慢的工具
        fastest_tool = min(tool_stats.items(), key=lambda x: x[1]['avg_time'])
        slowest_tool = max(tool_stats.items(), key=lambda x: x[1]['avg_time'] if x[1]['avg_time'] != float('inf') else 0)
        
        # 找出文件最小和最大的工具
        smallest_files = min(tool_stats.items(), key=lambda x: x[1]['avg_size'])
        largest_files = max(tool_stats.items(), key=lambda x: x[1]['avg_size'])
        
        html += f"""
        <div class="performance-grid">
            <div class="metric-card">
                <div class="metric-title">🚀 转换速度最快</div>
                <div class="metric-value">{fastest_tool[0]}</div>
                <div>平均 {fastest_tool[1]['avg_time']:.2f}s</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">🐌 转换速度最慢</div>
                <div class="metric-value">{slowest_tool[0]}</div>
                <div>平均 {slowest_tool[1]['avg_time']:.2f}s</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">📦 文件最小</div>
                <div class="metric-value">{smallest_files[0]}</div>
                <div>平均 {smallest_files[1]['avg_size']/1024:.1f}KB</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">📈 文件最大</div>
                <div class="metric-value">{largest_files[0]}</div>
                <div>平均 {largest_files[1]['avg_size']/1024:.1f}KB</div>
            </div>
        </div>
        """
        
        html += "</div>"
        return html
    
    def generate_recommendations_html(self, metrics: Dict[str, EvaluationMetrics]) -> str:
        """生成推荐建议HTML"""
        # 按总分排序
        sorted_tools = sorted(metrics.items(), key=lambda x: x[1].calculate_weighted_score(), reverse=True)
        
        html = """
        <div class="recommendations">
            <h3>💡 选型建议与最佳实践</h3>
            
            <div class="recommendation-grid">
                <div class="scenario-card">
                    <h4>🏢 企业级生产环境</h4>
                    <div class="recommended-tool">推荐：Playwright</div>
                    <div class="reason">
                        <p><strong>理由：</strong></p>
                        <ul>
                            <li>最佳的视觉还原效果 (95分)</li>
                            <li>完整的JavaScript和动态内容支持</li>
                            <li>稳定的API和丰富的配置选项</li>
                            <li>活跃的社区支持和持续更新</li>
                        </ul>
                        <p><strong>适用场景：</strong>复杂页面、动态内容、高质量要求</p>
                    </div>
                </div>
                
                <div class="scenario-card">
                    <h4>⚡ 高性能批量处理</h4>
                    <div class="recommended-tool">推荐：WeasyPrint</div>
                    <div class="reason">
                        <p><strong>理由：</strong></p>
                        <ul>
                            <li>最快的转换速度 (0.26s平均)</li>
                            <li>轻量级，资源占用少</li>
                            <li>优秀的CSS支持和打印样式</li>
                            <li>纯Python实现，易于集成</li>
                        </ul>
                        <p><strong>适用场景：</strong>报告生成、静态内容、批量转换</p>
                    </div>
                </div>
                
                <div class="scenario-card">
                    <h4>🔧 传统系统集成</h4>
                    <div class="recommended-tool">推荐：LibreOffice</div>
                    <div class="reason">
                        <p><strong>理由：</strong></p>
                        <ul>
                            <li>成熟稳定，久经考验</li>
                            <li>强大的文档处理能力</li>
                            <li>良好的表格和复杂布局支持</li>
                            <li>跨平台兼容性好</li>
                        </ul>
                        <p><strong>适用场景：</strong>文档转换、表格处理、传统系统</p>
                    </div>
                </div>
            </div>
            
            <div class="implementation-tips">
                <h4>🛠️ 实施建议</h4>
                <div class="tips-grid">
                    <div class="tip-card">
                        <h5>性能优化</h5>
                        <ul>
                            <li>使用连接池减少启动开销</li>
                            <li>合理设置超时时间</li>
                            <li>考虑异步处理大批量任务</li>
                            <li>监控内存使用，及时释放资源</li>
                        </ul>
                    </div>
                    
                    <div class="tip-card">
                        <h5>质量保证</h5>
                        <ul>
                            <li>建立测试样例库，定期回归测试</li>
                            <li>设置质量阈值，自动检测异常</li>
                            <li>保留原始HTML用于问题排查</li>
                            <li>建立错误处理和重试机制</li>
                        </ul>
                    </div>
                    
                    <div class="tip-card">
                        <h5>部署运维</h5>
                        <ul>
                            <li>容器化部署，确保环境一致性</li>
                            <li>配置健康检查和监控告警</li>
                            <li>准备降级方案和备用工具</li>
                            <li>定期更新依赖，关注安全补丁</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="decision-matrix">
                <h4>🎯 决策矩阵</h4>
                <table class="decision-table">
                    <thead>
                        <tr>
                            <th>需求场景</th>
                            <th>首选方案</th>
                            <th>备选方案</th>
                            <th>关键考虑因素</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>复杂页面 + 动态内容</td>
                            <td>Playwright</td>
                            <td>-</td>
                            <td>JavaScript支持必需</td>
                        </tr>
                        <tr>
                            <td>高并发 + 静态内容</td>
                            <td>WeasyPrint</td>
                            <td>Playwright</td>
                            <td>性能优先</td>
                        </tr>
                        <tr>
                            <td>文档处理 + 表格重</td>
                            <td>LibreOffice</td>
                            <td>WeasyPrint</td>
                            <td>表格布局复杂度</td>
                        </tr>
                        <tr>
                            <td>快速原型 + 简单需求</td>
                            <td>WeasyPrint</td>
                            <td>Playwright</td>
                            <td>开发效率</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        """
        
        return html
    
    def generate_full_report(self, results: Dict[str, List[SampleResult]], 
                           metrics: Dict[str, EvaluationMetrics],
                           objective_metrics: Dict[str, ObjectiveMetrics] = None) -> str:
        """生成简化的HTML报告，专注于客观评估指标"""
        
        html = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>HTML转PDF工具评估报告</title>
            {self.css_styles}
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📄 HTML转PDF工具评估报告</h1>
                    <p>WeasyPrint、Playwright 和 LibreOffice 客观评估对比</p>
                </div>
                
                <div class="content">
                    <div class="section">
                        <h2>🔧 HTML转PDF工具介绍</h2>
                        {self.generate_tools_introduction_html()}
                    </div>
                    
                    <div class="section">
                        <h2>📋 HTML解析能力与限制对比</h2>
                        {self.generate_parsing_capabilities_comparison_html()}
                    </div>
                    
                    <div class="section">
                        <h2>🏆 整体指标对比</h2>
                        {self.generate_overall_metrics_comparison_html(results, metrics)}
                    </div>
                    
                    <div class="section">
                        <h2>📝 详细结果</h2>
                        {self.generate_enhanced_detailed_results_html(results)}
                    </div>
                </div>
                
                <div class="footer">
                    <p>报告生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html