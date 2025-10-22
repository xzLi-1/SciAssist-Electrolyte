import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agents.analyst_manager import AnalystManager

def test_analyst_system():
    """测试分析智能体系统"""
    print("🔬 测试电解液分析智能体系统...")
    
    # 初始化分析管理器
    analyst_manager = AnalystManager()
    
    # 测试配方
    test_formulations = [
        "1.2 M LiPF6 in EC/EMC (3:7) with 2% VC additive for high voltage applications",
        "1 M LiFSI in DME/DOL (1:1) with 0.5 M LiNO3 for lithium metal batteries",
        "1 M LiPF6 in EC/DEC (1:1) for silicon anode batteries"
    ]
    
    for i, formulation in enumerate(test_formulations, 1):
        print(f"\n{'='*60}")
        print(f"配方 {i} 分析: {formulation}")
        print(f"{'='*60}")
        
        # 执行分析
        analysis_result = analyst_manager.comprehensive_analysis(formulation)
        
        # 显示分析结果
        formulation_analysis = analysis_result['formulation_analysis']
        
        print(f"\n📋 组分识别:")
        for component in formulation_analysis.get('components_identified', []):
            print(f"  - {component['name']} ({component['type']}): {component.get('concentration', 'N/A')} - {component['role']}")
        
        print(f"\n📊 性能预测:")
        for prediction in formulation_analysis.get('performance_predictions', []):
            if prediction.get('predicted_value'):
                print(f"  - {prediction['metric']}: {prediction['predicted_value']} - {prediction.get('explanation', '')}")
            elif prediction.get('actual_value'):
                assessment = prediction.get('assessment', {})
                print(f"  - {prediction['metric']}: {prediction['actual_value']} ({assessment.get('description', '')})")
        
        print(f"\n💡 改进建议:")
        for recommendation in formulation_analysis.get('recommendations', []):
            print(f"  - {recommendation}")
        
        print(f"\n⚠️ 风险评估:")
        for risk in formulation_analysis.get('risk_factors', []):
            print(f"  - {risk}")
        
        print(f"\n🔍 兼容性评估:")
        compatibility = formulation_analysis.get('compatibility_assessment', {})
        print(f"  - 总体评估: {compatibility.get('overall', '未知')}")
        for strength in compatibility.get('strengths', []):
            print(f"  - 优势: {strength}")
        for issue in compatibility.get('issues', []):
            print(f"  - 问题: {issue}")
    
    print(f"\n🎉 分析智能体系统测试完成！")

def test_batch_analysis():
    """测试批量分析功能"""
    print(f"\n{'='*60}")
    print("测试批量分析功能")
    print(f"{'='*60}")
    
    analyst_manager = AnalystManager()
    
    formulations = [
        "1 M LiPF6 in EC/DMC",
        "LiFSI in ether solvents for LMB",
        "High concentration electrolyte with 3 M LiTFSI"
    ]
    
    batch_results = analyst_manager.batch_analyze_formulations(formulations)
    
    for result in batch_results:
        if 'error' in result:
            print(f"❌ 分析失败: {result['formulation']} - {result['error']}")
        else:
            components_count = len(result['analysis'].get('components_identified', []))
            print(f"✅ 分析完成: {result['formulation']} - 识别到 {components_count} 个组分")

if __name__ == "__main__":
    test_analyst_system()
    test_batch_analysis()