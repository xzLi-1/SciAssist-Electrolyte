import sys
import os

# 更可靠的路径添加方式
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)  # 使用insert(0)确保优先搜索

try:
    from data_processing.electrolyte_pdf_processor import ElectrolytePDFProcessor
    print("✅ 导入成功！")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"尝试添加的路径: {src_dir}")
    print(f"该路径是否存在: {os.path.exists(src_dir)}")
    if os.path.exists(src_dir):
        print(f"src目录内容: {os.listdir(src_dir)}")
    sys.exit(1)


def test_processor():
    """测试PDF处理器的基本功能"""
    processor = ElectrolytePDFProcessor()
    
    # 测试文本分析功能
    test_text = """
    We prepared the electrolyte with 1 M LiPF6 in EC/EMC (3:7 by volume) 
    and 2 wt% VC additive. The Coulombic efficiency reached 99.8% after 
    100 cycles, with ionic conductivity of 12.3 mS cm⁻¹. The electrochemical 
    window was stable between 3.0 V and 4.8 V.
    """
    
    print("🔬 测试电解液PDF处理器...")
    
    # 测试配方提取
    formulations = processor.extract_electrolyte_formulations(test_text)
    print(f"✅ 提取到 {len(formulations)} 个电解液配方:")
    for i, formula in enumerate(formulations, 1):
        print(f"  {i}. {formula['component']} - {formula['concentration']}")
    
    # 测试性能指标提取
    metrics = processor.extract_performance_metrics(test_text)
    print(f"✅ 提取到 {len(metrics)} 个性能指标:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    print("🎉 所有测试通过！PDF处理器工作正常。")

if __name__ == "__main__":
    test_processor()