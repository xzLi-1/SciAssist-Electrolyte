import logging
from typing import List, Dict, Any
from .electrolyte_analyst import ElectrolyteAnalyst

logger = logging.getLogger(__name__)

class AnalystManager:
    """
    分析智能体管理器 - 协调分析功能
    """
    
    def __init__(self):
        self.analyst = ElectrolyteAnalyst()
        logger.info("分析智能体管理器初始化完成")
    
    def comprehensive_analysis(self, formulation: str, search_results: List[Dict] = None) -> Dict[str, Any]:
        """
        执行综合分析
        
        Args:
            formulation: 电解液配方描述
            search_results: 相关的检索结果（可选）
            
        Returns:
            综合分析结果
        """
        logger.info(f"执行综合分析: {formulation}")
        
        analysis_result = {
            'formulation_analysis': {},
            'research_insights': {},
            'recommendations': {},
            'timestamp': self._get_timestamp()
        }
        
        # 配方分析
        formulation_analysis = self.analyst.analyze_formulation(formulation)
        analysis_result['formulation_analysis'] = formulation_analysis
        
        # 研究洞察（如果有检索结果）
        if search_results:
            research_insights = self.analyst.generate_research_insights(search_results)
            analysis_result['research_insights'] = research_insights
        
        # 综合建议
        comprehensive_recommendations = self._generate_comprehensive_recommendations(
            formulation_analysis, 
            research_insights if search_results else {}
        )
        analysis_result['recommendations'] = comprehensive_recommendations
        
        return analysis_result
    
    def _generate_comprehensive_recommendations(self, formulation_analysis: Dict, research_insights: Dict) -> Dict[str, Any]:
        """生成综合建议"""
        recommendations = {
            'immediate_actions': [],
            'research_directions': [],
            'performance_optimizations': []
        }
        
        # 基于配方分析的建议
        if formulation_analysis.get('risk_factors'):
            recommendations['immediate_actions'].extend(
                f"注意: {risk}" for risk in formulation_analysis['risk_factors']
            )
        
        if formulation_analysis.get('recommendations'):
            recommendations['performance_optimizations'].extend(
                formulation_analysis['recommendations']
            )
        
        # 基于研究洞察的建议
        if research_insights.get('research_gaps'):
            recommendations['research_directions'].extend(
                research_insights['research_gaps']
            )
        
        return recommendations
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def batch_analyze_formulations(self, formulations: List[str]) -> List[Dict[str, Any]]:
        """
        批量分析多个配方
        
        Args:
            formulations: 配方描述列表
            
        Returns:
            分析结果列表
        """
        results = []
        for formulation in formulations:
            try:
                analysis = self.analyst.analyze_formulation(formulation)
                results.append({
                    'formulation': formulation,
                    'analysis': analysis
                })
            except Exception as e:
                logger.error(f"分析配方失败 '{formulation}': {e}")
                results.append({
                    'formulation': formulation,
                    'error': str(e)
                })
        
        return results