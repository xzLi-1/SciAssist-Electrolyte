import re
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ElectrolyteAnalyst:
    """
    电解液分析智能体 - 提供专业分析和建议
    """
    
    def __init__(self):
        self.performance_standards = {
            'coulombic_efficiency': {
                'excellent': 99.5,
                'good': 99.0,
                'poor': 98.0
            },
            'ionic_conductivity': {
                'excellent': 10.0,
                'good': 5.0,
                'poor': 1.0
            },
            'cycle_life': {
                'excellent': 1000,
                'good': 500,
                'poor': 100
            },
            'voltage_window': {
                'excellent': 4.5,
                'good': 4.3,
                'poor': 4.0
            }
        }
        
        # 电解液配方知识库
        self.formulation_knowledge = {
            'high_voltage': {
                'description': '高电压电解液体系',
                'recommended_salts': ['LiPF6', 'LiTFSI'],
                'recommended_solvents': ['FEC', 'EMC', 'EC'],
                'recommended_additives': ['VC', 'LiPO2F2'],
                'typical_concentrations': ['1.0-1.5 M'],
                'key_considerations': ['抗氧化稳定性', '铝集流体兼容性']
            },
            'lithium_metal': {
                'description': '锂金属电池电解液',
                'recommended_salts': ['LiFSI', 'LiTFSI'],
                'recommended_solvents': ['DME', 'DOL', 'TTE'],
                'recommended_additives': ['LiNO3', 'CsPF6'],
                'typical_concentrations': ['1.0-4.0 M'],
                'key_considerations': ['锂枝晶抑制', '界面稳定性']
            },
            'silicon_anode': {
                'description': '硅负极电解液',
                'recommended_salts': ['LiPF6', 'LiFSI'],
                'recommended_solvents': ['FEC', 'EC', 'EMC'],
                'recommended_additives': ['FEC', 'VC', 'SA'],
                'typical_concentrations': ['1.0-1.2 M'],
                'key_considerations': ['体积膨胀适应', 'SEI稳定性']
            }
        }
        
        logger.info("电解液分析智能体初始化完成")
    
    def analyze_formulation(self, formulation_text: str) -> Dict[str, Any]:
        """
        分析电解液配方
        
        Args:
            formulation_text: 配方文本描述
            
        Returns:
            分析结果字典
        """
        logger.info(f"分析电解液配方: {formulation_text}")
        
        analysis = {
            'components_identified': [],
            'performance_predictions': [],
            'recommendations': [],
            'compatibility_assessment': {},
            'risk_factors': []
        }
        
        # 识别组分
        components = self._identify_components(formulation_text)
        analysis['components_identified'] = components
        
        # 性能预测
        performance = self._predict_performance(components, formulation_text)
        analysis['performance_predictions'] = performance
        
        # 提供建议
        recommendations = self._generate_recommendations(components, performance)
        analysis['recommendations'] = recommendations
        
        # 兼容性评估
        compatibility = self._assess_compatibility(components)
        analysis['compatibility_assessment'] = compatibility
        
        # 风险评估
        risks = self._identify_risks(components, formulation_text)
        analysis['risk_factors'] = risks
        
        return analysis
    
    def _identify_components(self, text: str) -> List[Dict]:
        """识别电解液组分"""
        components = []
        
        # 识别锂盐
        salt_patterns = {
            'LiPF6': r'(\d+\.?\d*)\s*[Mm]?\s*LiPF6',
            'LiTFSI': r'(\d+\.?\d*)\s*[Mm]?\s*LiTFSI',
            'LiFSI': r'(\d+\.?\d*)\s*[Mm]?\s*LiFSI',
            'LiBOB': r'(\d+\.?\d*)\s*[Mm]?\s*LiBOB'
        }
        
        for salt, pattern in salt_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                concentration = match.group(1) if match.group(1) else "未知"
                components.append({
                    'type': 'salt',
                    'name': salt,
                    'concentration': concentration,
                    'role': '导电锂盐'
                })
        
        # 识别溶剂
        solvent_patterns = {
            'EC': r'EC',
            'DEC': r'DEC',
            'DMC': r'DMC', 
            'EMC': r'EMC',
            'FEC': r'FEC',
            'PC': r'PC',
            'DME': r'DME',
            'DOL': r'DOL'
        }
        
        for solvent, pattern in solvent_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                components.append({
                    'type': 'solvent',
                    'name': solvent,
                    'role': self._get_solvent_role(solvent)
                })
        
        # 识别添加剂
        additive_patterns = {
            'VC': r'VC|vinylene\s+carbonate',
            'FEC': r'FEC|fluoroethylene\s+carbonate',
            'LiNO3': r'LiNO3|lithium\s+nitrate',
            'CsPF6': r'CsPF6'
        }
        
        for additive, pattern in additive_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                components.append({
                    'type': 'additive',
                    'name': additive,
                    'role': self._get_additive_role(additive)
                })
        
        return components
    
    def _get_solvent_role(self, solvent: str) -> str:
        """获取溶剂作用描述"""
        roles = {
            'EC': '高介电常数溶剂，促进盐解离',
            'DEC': '低粘度溶剂，改善离子电导率',
            'DMC': '低粘度溶剂，优化低温性能',
            'EMC': '平衡溶剂，兼顾溶解性和粘度',
            'FEC': '成膜溶剂，改善SEI稳定性',
            'PC': '高电压稳定性溶剂',
            'DME': '醚类溶剂，适用于锂金属电池',
            'DOL': '醚类溶剂，改善锂金属兼容性'
        }
        return roles.get(solvent, '有机溶剂')
    
    def _get_additive_role(self, additive: str) -> str:
        """获取添加剂作用描述"""
        roles = {
            'VC': 'SEI成膜添加剂，改善首次效率',
            'FEC': '锂金属电池专用成膜添加剂',
            'LiNO3': '锂金属电池界面稳定剂',
            'CsPF6': '阳离子添加剂，抑制枝晶生长'
        }
        return roles.get(additive, '功能添加剂')
    
    def _predict_performance(self, components: List[Dict], text: str) -> List[Dict]:
        """预测性能指标"""
        predictions = []
        
        # 提取文本中的实际性能数据
        extracted_metrics = self._extract_metrics_from_text(text)
        
        # 基于组分进行预测
        salt_concentrations = [float(comp['concentration']) for comp in components 
                             if comp['type'] == 'salt' and comp['concentration'] != '未知']
        avg_concentration = sum(salt_concentrations) / len(salt_concentrations) if salt_concentrations else 1.0
        
        # 电导率预测
        conductivity_pred = self._predict_conductivity(components, avg_concentration)
        predictions.append({
            'metric': 'ionic_conductivity',
            'predicted_value': conductivity_pred,
            'confidence': 'medium',
            'explanation': self._explain_conductivity_prediction(components, conductivity_pred)
        })
        
        # 库伦效率预测
        ce_pred = self._predict_coulombic_efficiency(components)
        predictions.append({
            'metric': 'coulombic_efficiency',
            'predicted_value': ce_pred,
            'confidence': 'medium', 
            'explanation': self._explain_ce_prediction(components, ce_pred)
        })
        
        # 添加提取的实际数据
        for metric, value in extracted_metrics.items():
            predictions.append({
                'metric': metric,
                'actual_value': value,
                'source': 'extracted_from_text',
                'assessment': self._assess_performance(metric, value)
            })
        
        return predictions
    
    def _extract_metrics_from_text(self, text: str) -> Dict[str, float]:
        """从文本中提取性能指标"""
        metrics = {}
        
        # 库伦效率
        ce_match = re.search(r'CE\s*[=:]\s*(\d+\.?\d*)%?', text, re.IGNORECASE)
        if ce_match:
            try:
                metrics['coulombic_efficiency'] = float(ce_match.group(1))
            except ValueError:
                pass
        
        # 离子电导率
        cond_match = re.search(r'(\d+\.?\d*)\s*mS\s*cm', text, re.IGNORECASE)
        if cond_match:
            try:
                metrics['ionic_conductivity'] = float(cond_match.group(1))
            except ValueError:
                pass
        
        return metrics
    
    def _predict_conductivity(self, components: List[Dict], concentration: float) -> float:
        """预测离子电导率"""
        base_conductivity = 8.0  # 基准电导率 mS/cm
        
        # 根据盐类型调整
        salts = [comp['name'] for comp in components if comp['type'] == 'salt']
        if 'LiFSI' in salts:
            base_conductivity += 2.0
        elif 'LiTFSI' in salts:
            base_conductivity += 1.5
        
        # 根据浓度调整
        if concentration > 1.5:
            base_conductivity -= 1.0
        elif concentration < 0.8:
            base_conductivity += 0.5
        
        return round(base_conductivity, 1)
    
    def _predict_coulombic_efficiency(self, components: List[Dict]) -> float:
        """预测库伦效率"""
        base_ce = 99.0  # 基准库伦效率 %
        
        # 根据添加剂调整
        additives = [comp['name'] for comp in components if comp['type'] == 'additive']
        if 'VC' in additives or 'FEC' in additives:
            base_ce += 0.5
        if 'LiNO3' in additives:
            base_ce += 0.3
        
        return round(base_ce, 1)
    
    def _explain_conductivity_prediction(self, components: List[Dict], value: float) -> str:
        """解释电导率预测"""
        salts = [comp['name'] for comp in components if comp['type'] == 'salt']
        
        if value >= 10.0:
            return f"预测电导率较高({value} mS/cm)，可能由于高效的锂盐和优化的溶剂比例"
        elif value >= 6.0:
            return f"中等电导率({value} mS/cm)，适用于大多数应用场景"
        else:
            return f"较低电导率({value} mS/cm)，建议优化盐浓度或溶剂体系"
    
    def _explain_ce_prediction(self, components: List[Dict], value: float) -> str:
        """解释库伦效率预测"""
        if value >= 99.5:
            return f"优异的库伦效率({value}%)，表明良好的界面稳定性"
        elif value >= 99.0:
            return f"良好的库伦效率({value}%)，适合实际应用"
        else:
            return f"库伦效率({value}%)有待提升，建议添加成膜添加剂"
    
    def _assess_performance(self, metric: str, value: float) -> Dict[str, str]:
        """评估性能水平"""
        standards = self.performance_standards.get(metric, {})
        
        if value >= standards.get('excellent', 0):
            return {'level': 'excellent', 'description': '性能优异'}
        elif value >= standards.get('good', 0):
            return {'level': 'good', 'description': '性能良好'}
        else:
            return {'level': 'poor', 'description': '需要改进'}
    
    def _generate_recommendations(self, components: List[Dict], performance: List[Dict]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        salts = [comp['name'] for comp in components if comp['type'] == 'salt']
        additives = [comp['name'] for comp in components if comp['type'] == 'additive']
        
        # 基于组分的建议
        if not any(additive in ['VC', 'FEC'] for additive in additives):
            recommendations.append("建议添加VC或FEC成膜添加剂以改善首次库伦效率和循环稳定性")
        
        if 'LiPF6' in salts:
            recommendations.append("LiPF6在高温下可能分解，如应用环境温度较高建议考虑LiTFSI或LiFSI")
        
        # 基于性能预测的建议
        for pred in performance:
            if pred.get('predicted_value'):
                if pred['metric'] == 'ionic_conductivity' and pred['predicted_value'] < 5.0:
                    recommendations.append("离子电导率偏低，建议优化溶剂比例或增加盐浓度")
                elif pred['metric'] == 'coulombic_efficiency' and pred['predicted_value'] < 99.0:
                    recommendations.append("库伦效率有待提升，建议添加界面稳定添加剂")
        
        return recommendations
    
    def _assess_compatibility(self, components: List[Dict]) -> Dict[str, Any]:
        """评估组分兼容性"""
        compatibility = {
            'overall': 'good',
            'issues': [],
            'strengths': []
        }
        
        salts = [comp['name'] for comp in components if comp['type'] == 'salt']
        solvents = [comp['name'] for comp in components if comp['type'] == 'solvent']
        
        # 检查铝集流体兼容性
        if 'LiTFSI' in salts or 'LiFSI' in salts:
            if 'EC' not in solvents:
                compatibility['issues'].append("LiTFSI/LiFSI与铝集流体可能存在腐蚀风险，建议添加EC溶剂")
        
        # 检查高电压兼容性
        if 'PC' in solvents:
            compatibility['strengths'].append("PC溶剂提供良好的高电压稳定性")
        
        # 检查锂金属兼容性
        if 'DME' in solvents or 'DOL' in solvents:
            compatibility['strengths'].append("醚类溶剂适合锂金属电池应用")
        
        if compatibility['issues']:
            compatibility['overall'] = 'needs_attention'
        
        return compatibility
    
    def _identify_risks(self, components: List[Dict], text: str) -> List[str]:
        """识别潜在风险"""
        risks = []
        
        salts = [comp['name'] for comp in components if comp['type'] == 'salt']
        
        # LiPF6的热稳定性风险
        if 'LiPF6' in salts:
            risks.append("LiPF6在高温(>60°C)下可能分解产生HF，影响电池寿命")
        
        # 检测高浓度风险
        salt_conc = [float(comp['concentration']) for comp in components 
                    if comp['type'] == 'salt' and comp['concentration'] != '未知']
        if any(conc > 2.0 for conc in salt_conc):
            risks.append("高盐浓度可能导致粘度增加和电导率下降")
        
        return risks
    
    def generate_research_insights(self, search_results: List[Dict]) -> Dict[str, Any]:
        """
        基于检索结果生成研究洞察
        
        Args:
            search_results: 检索系统返回的结果列表
            
        Returns:
            研究洞察字典
        """
        logger.info(f"基于 {len(search_results)} 个检索结果生成研究洞察")
        
        insights = {
            'trends': [],
            'common_formulations': [],
            'performance_benchmarks': {},
            'research_gaps': [],
            'key_findings': []
        }
        
        # 分析常见配方
        all_formulations = []
        for result in search_results:
            if result['metadata'].get('electrolyte_formulations'):
                all_formulations.extend(result['metadata']['electrolyte_formulations'])
        
        # 统计常见配方模式
        formulation_stats = {}
        for formula in all_formulations:
            key = f"{formula.get('component', '')}_{formula.get('concentration', '')}"
            formulation_stats[key] = formulation_stats.get(key, 0) + 1
        
        insights['common_formulations'] = [
            {'formulation': k, 'frequency': v} 
            for k, v in formulation_stats.items() 
            if v > 1
        ]
        
        # 提取性能基准
        performance_data = {'coulombic_efficiency': [], 'ionic_conductivity': []}
        for result in search_results:
            metrics = result['metadata'].get('performance_metrics', {})
            for metric, value in metrics.items():
                if metric in performance_data:
                    performance_data[metric].append(value)
        
        for metric, values in performance_data.items():
            if values:
                insights['performance_benchmarks'][metric] = {
                    'average': sum(values) / len(values),
                    'max': max(values),
                    'min': min(values),
                    'count': len(values)
                }
        
        # 生成研究趋势
        if len(search_results) >= 3:
            insights['trends'].append("高电压电解液体系是当前研究热点")
            insights['trends'].append("多功能添加剂的使用越来越受到关注")
        
        # 识别研究空白
        salts_mentioned = set()
        for result in search_results:
            for formula in result['metadata'].get('electrolyte_formulations', []):
                if formula.get('type') == 'salt':
                    salts_mentioned.add(formula.get('component', ''))
        
        if 'LiBOB' not in salts_mentioned:
            insights['research_gaps'].append("LiBOB盐体系的研究相对较少")
        
        insights['key_findings'] = [
            f"分析了 {len(search_results)} 篇相关文献",
            f"识别出 {len(insights['common_formulations'])} 种常见配方模式",
            f"建立了主要性能指标的基准数据"
        ]
        
        return insights