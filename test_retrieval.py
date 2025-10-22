# 不使用任何可能引起冲突的库
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from retrieval.retrieval_manager import PurePythonRetrievalManager

def test_final_retrieval_system():
    """测试最终检索系统"""
    print("🔍 测试纯Python电解液专业检索系统...")
    print("✅ 无OpenMP冲突风险")
    
    # 初始化检索管理器
    retrieval_manager = PurePythonRetrievalManager()
    
    # 创建测试文档
    test_documents = [
        {
            'content': """
            High voltage electrolytes are crucial for next-generation lithium-ion batteries.
            We developed an electrolyte with 1.2 M LiPF6 in FEC/EMC (3:7) that exhibits
            excellent stability up to 4.8V. The Coulombic efficiency reached 99.7% and
            ionic conductivity was 11.5 mS cm⁻¹. This formulation shows great promise
            for high-energy-density batteries.
            """,
            'metadata': {
                'title': 'High Voltage Electrolyte for Li-ion Batteries',
                'section': 'abstract',
                'authors': ['John Doe', 'Jane Smith']
            }
        },
        {
            'content': """
            Solid electrolyte interphase (SEI) formation is critical for battery performance.
            Using 2 wt% VC additive in 1M LiPF6/EC-DEC electrolyte significantly improves
            SEI stability. The cycling performance shows 95% capacity retention after
            500 cycles at 1C rate. The interface characterization reveals uniform SEI layer.
            This electrolyte formulation provides excellent Coulombic efficiency of 99.5%.
            """,
            'metadata': {
                'title': 'SEI Formation with VC Additive',
                'section': 'results', 
                'authors': ['Alice Johnson', 'Bob Wilson']
            }
        },
        {
            'content': """
            Lithium metal batteries require electrolytes with high Li+ transference number.
            We studied LiFSI-based electrolytes in ether solvents. The transference number
            reached 0.78, with ionic conductivity of 8.9 mS cm⁻¹. Coulombic efficiency
            was maintained at 99.3% over 200 cycles in Li||Cu cells. The electrolyte
            composition was 1 M LiFSI in DME/DOL (1:1) with LiNO3 additive.
            """,
            'metadata': {
                'title': 'LiFSI Electrolytes for Li Metal Batteries',
                'section': 'conclusion',
                'authors': ['Charlie Brown', 'Diana Lee']
            }
        },
        {
            'content': """
            高电压电解液对于下一代锂离子电池至关重要。我们开发了一种1.2 M LiPF6在FEC/EMC (3:7)
            中的电解液，其在4.8V以下表现出优异的稳定性。库伦效率达到99.7%，离子电导率为11.5 mS cm⁻¹。
            该配方在高能量密度电池中显示出巨大潜力。
            """,
            'metadata': {
                'title': '高电压锂离子电池电解液研究',
                'section': '摘要',
                'authors': ['张三', '李四']
            }
        }
    ]
    
    # 构建知识库
    retrieval_manager.build_from_documents(test_documents)
    
    print("✅ 知识库构建完成")
    
    # 测试查询
    test_queries = [
        "high voltage electrolyte stability",
        "VC additive SEI formation", 
        "ionic conductivity LiFSI",
        "库伦效率 电解液",
        "LiPF6 high voltage"
    ]
    
    for query in test_queries:
        print(f"\n📝 查询: '{query}'")
        results = retrieval_manager.search(query, top_k=2)
        
        print(f"找到 {len(results)} 个相关结果:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. 相似度: {result['similarity']:.3f}")
            print(f"     标题: {result['metadata']['title']}")
            print(f"     内容: {result['content'][:80]}...")
            
            # 提取并显示配方信息
            formulations = retrieval_manager.retriever.extract_formulations_from_text(result['content'])
            if formulations:
                print(f"     配方: {formulations}")
            
            # 提取并显示性能指标
            metrics = retrieval_manager.retriever.extract_metrics_from_text(result['content'])
            if metrics:
                print(f"     指标: {metrics}")
    
    # 显示统计信息
    stats = retrieval_manager.get_statistics()
    print(f"\n📊 系统统计:")
    print(f"  文档数量: {stats['document_count']}")
    print(f"  词汇表大小: {stats['vocabulary_size']}")
    


if __name__ == "__main__":
    test_final_retrieval_system()