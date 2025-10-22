import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import streamlit as st
import sys
import os
import tempfile
from pathlib import Path

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# 设置页面配置
st.set_page_config(
    page_title="电解液研究智能助手",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 导入自定义模块
from data_processing.electrolyte_pdf_processor import ElectrolytePDFProcessor
from retrieval.pure_python_manager import PurePythonRetrievalManager
from agents.analyst_manager import AnalystManager

class ElectrolyteExpertApp:
    """
    电解液研究智能助手 - Streamlit应用主类
    """
    
    def __init__(self):
        self.pdf_processor = ElectrolytePDFProcessor()
        self.retrieval_manager = PurePythonRetrievalManager()
        self.analyst_manager = AnalystManager()
        self.setup_session_state()
    
    def setup_session_state(self):
        """初始化会话状态"""
        if 'knowledge_base_ready' not in st.session_state:
            st.session_state.knowledge_base_ready = False
        if 'uploaded_files' not in st.session_state:
            st.session_state.uploaded_files = []
        if 'analysis_history' not in st.session_state:
            st.session_state.analysis_history = []
        if 'search_results' not in st.session_state:
            st.session_state.search_results = []
    
    def run(self):
        """运行主应用"""
        # 页面标题和介绍
        st.title("🔋 电解液研究智能助手")
        st.markdown("""
        **基于人工智能的电池电解液研究分析与推荐系统**  
        上传电解液领域学术论文，获取智能分析、配方推荐和研究洞察。
        """)
        
        # 侧边栏
        self.render_sidebar()
        
        # 主内容区域 - 标签页
        tab1, tab2, tab3, tab4 = st.tabs(["📚 文献管理", "🔍 智能检索", "🧪 配方分析", "📊 系统信息"])
        
        with tab1:
            self.render_literature_management()
        
        with tab2:
            self.render_retrieval_interface()
        
        with tab3:
            self.render_analysis_interface()
        
        with tab4:
            self.render_system_info()
    
    def render_sidebar(self):
        """渲染侧边栏"""
        with st.sidebar:
            st.header("⚙️ 系统状态")
            
            # 知识库状态
            if st.session_state.knowledge_base_ready:
                st.success("✅ 知识库已就绪")
                stats = self.retrieval_manager.get_statistics()
                st.info(f"文档数量: {stats['document_count']}")
            else:
                st.warning("📚 知识库未就绪")
            
            st.header("🔧 工具")
            
            # 快速操作
            if st.button("🔄 清除所有数据", use_container_width=True):
                self.clear_all_data()
            
            if st.button("📊 加载示例数据", use_container_width=True):
                self.load_example_data()
            
            # 分析历史
            if st.session_state.analysis_history:
                st.header("📝 分析历史")
                for i, analysis in enumerate(st.session_state.analysis_history[-3:]):
                    with st.expander(f"分析 {i+1}: {analysis['formulation'][:30]}..."):
                        st.write(f"时间: {analysis['timestamp']}")
                        st.write(f"组分: {len(analysis['results']['formulation_analysis']['components_identified'])} 个")
    
    def clear_all_data(self):
        """清除所有数据"""
        st.session_state.knowledge_base_ready = False
        st.session_state.uploaded_files = []
        st.session_state.analysis_history = []
        st.session_state.search_results = []
        st.rerun()
    
    def load_example_data(self):
        """加载示例数据"""
        example_documents = [
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
            }
        ]
        
        self.retrieval_manager.build_from_documents(example_documents)
        st.session_state.knowledge_base_ready = True
        st.success("✅ 示例数据加载完成！")
        st.rerun()
    
    def render_literature_management(self):
        """渲染文献管理界面"""
        st.header("📚 文献管理")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("上传论文PDF")
            uploaded_files = st.file_uploader(
                "选择电解液领域论文PDF文件",
                type="pdf",
                accept_multiple_files=True,
                help="支持多个PDF文件同时上传"
            )
            
            if uploaded_files:
                st.session_state.uploaded_files = uploaded_files
                st.success(f"已选择 {len(uploaded_files)} 个文件")
                
                if st.button("处理论文并构建知识库", type="primary"):
                    self.process_uploaded_files(uploaded_files)
        
        with col2:
            st.subheader("快速开始")
            st.markdown("""
            **没有PDF文件？**
            
            点击下方按钮加载示例数据，
            立即体验系统功能：
            - 高电压电解液
            - 锂金属电池电解液  
            - 界面改性研究
            """)
            
            if st.button("🚀 加载示例数据", use_container_width=True):
                self.load_example_data()
        
        # 显示处理状态
        if st.session_state.knowledge_base_ready:
            st.success("✅ 知识库已构建完成，可以开始检索和分析！")
    
    def process_uploaded_files(self, uploaded_files):
        """处理上传的PDF文件"""
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        documents = []
        
        for i, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"处理文件中 {i+1}/{len(uploaded_files)}: {uploaded_file.name}")
            
            try:
                # 创建临时文件
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                # 处理PDF
                structured_content = self.pdf_processor.extract_structured_content(tmp_path)
                metadata = self.pdf_processor.analyze_paper_metadata(tmp_path)
                
                # 清理临时文件
                os.unlink(tmp_path)
                
                # 为每个章节创建文档
                for section, content in structured_content.items():
                    if content.strip():
                        documents.append({
                            'content': content,
                            'metadata': {
                                'file_name': uploaded_file.name,
                                'section': section,
                                'title': metadata.get('title', 'Unknown'),
                                'authors': metadata.get('authors', [])
                            }
                        })
                
                st.success(f"✅ 成功处理: {uploaded_file.name}")
                
            except Exception as e:
                st.error(f"❌ 处理文件 {uploaded_file.name} 时出错: {e}")
            
            progress_bar.progress((i + 1) / len(uploaded_files))
        
        # 构建知识库
        if documents:
            status_text.text("构建知识库中...")
            self.retrieval_manager.build_from_documents(documents)
            st.session_state.knowledge_base_ready = True
            status_text.text("完成!")
            st.success(f"🎉 知识库构建完成! 共处理 {len(documents)} 个文档片段。")
            st.rerun()
        else:
            st.error("未能处理任何文档。")
    
    def render_retrieval_interface(self):
        """渲染检索界面"""
        st.header("🔍 智能检索")
        
        if not st.session_state.knowledge_base_ready:
            st.warning("请先构建知识库（在文献管理标签页上传PDF或加载示例数据）")
            return
        
        # 搜索界面
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input(
                "输入检索关键词",
                placeholder="例如：high voltage electrolyte stability, VC additive SEI formation, 库伦效率 电解液"
            )
        
        with col2:
            top_k = st.number_input("返回结果数量", min_value=1, max_value=10, value=5)
        
        if st.button("🔎 开始搜索", type="primary") and search_query:
            with st.spinner("搜索中..."):
                results = self.retrieval_manager.search(search_query, top_k=top_k)
                st.session_state.search_results = results
            
            self.display_search_results(results)
    
    def display_search_results(self, results):
        """显示搜索结果"""
        st.subheader(f"检索结果 ({len(results)} 个)")
        
        for i, result in enumerate(results):
            with st.expander(f"📄 结果 {i+1} - 相似度: {result['similarity']:.3f}", expanded=i==0):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write("**内容:**")
                    st.write(result['content'])
                
                with col2:
                    st.write("**元数据:**")
                    st.write(f"**标题:** {result['metadata']['title']}")
                    st.write(f"**作者:** {', '.join(result['metadata']['authors'])}")
                    st.write(f"**章节:** {result['metadata']['section']}")
                    st.write(f"**来源:** {result['metadata']['file_name']}")
                
                # 提取并显示配方信息
                formulations = self.retrieval_manager.retriever.extract_formulations_from_text(result['content'])
                if formulations:
                    st.write("**🔬 识别配方:**")
                    for formula in formulations:
                        st.write(f"- {formula['component']} ({formula.get('concentration', 'N/A')})")
                
                # 提取并显示性能指标
                metrics = self.retrieval_manager.retriever.extract_metrics_from_text(result['content'])
                if metrics:
                    st.write("**📊 性能指标:**")
                    for metric, value in metrics.items():
                        st.write(f"- {metric}: {value}")
    
    def render_analysis_interface(self):
        """渲染分析界面"""
        st.header("🧪 配方分析")
        
        st.markdown("""
        输入电解液配方描述，获取专业分析和改进建议。
        """)
        
        # 配方输入区域
        col1, col2 = st.columns([3, 1])
        
        with col1:
            formulation = st.text_area(
                "电解液配方描述",
                placeholder="例如：1.2 M LiPF6 in EC/EMC (3:7) with 2% VC additive for high voltage applications",
                height=100
            )
        
        with col2:
            st.write("**分析选项**")
            include_research = st.checkbox("包含文献调研", value=True)
            show_details = st.checkbox("显示详细分析", value=True)
        
        if st.button("🔬 开始分析", type="primary") and formulation:
            self.perform_analysis(formulation, include_research, show_details)
    
    def perform_analysis(self, formulation, include_research, show_details):
        """执行配方分析"""
        with st.spinner("分析中..."):
            # 获取相关文献（如果启用）
            search_results = None
            if include_research and st.session_state.knowledge_base_ready:
                search_results = self.retrieval_manager.search(formulation, top_k=3)
            
            # 执行分析
            analysis_result = self.analyst_manager.comprehensive_analysis(
                formulation, 
                search_results
            )
            
            # 保存到历史
            st.session_state.analysis_history.append({
                'formulation': formulation,
                'results': analysis_result,
                'timestamp': analysis_result['timestamp']
            })
        
        # 显示分析结果
        self.display_analysis_results(analysis_result, show_details)
    
    def display_analysis_results(self, analysis_result, show_details):
        """显示分析结果"""
        st.success("✅ 分析完成！")
        
        formulation_analysis = analysis_result['formulation_analysis']
        research_insights = analysis_result.get('research_insights', {})
        recommendations = analysis_result['recommendations']
        
        # 使用标签页组织结果
        tab1, tab2, tab3, tab4 = st.tabs(["📋 组分分析", "📊 性能评估", "💡 改进建议", "🔍 研究洞察"])
        
        with tab1:
            self.display_component_analysis(formulation_analysis)
        
        with tab2:
            self.display_performance_analysis(formulation_analysis)
        
        with tab3:
            self.display_recommendations(recommendations, formulation_analysis)
        
        with tab4:
            self.display_research_insights(research_insights)
    
    def display_component_analysis(self, formulation_analysis):
        """显示组分分析"""
        st.subheader("📋 组分识别")
        
        components = formulation_analysis.get('components_identified', [])
        
        if not components:
            st.warning("未识别到明确的电解液组分")
            return
        
        # 按类型分组显示
        salts = [c for c in components if c['type'] == 'salt']
        solvents = [c for c in components if c['type'] == 'solvent']
        additives = [c for c in components if c['type'] == 'additive']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if salts:
                st.write("**🧂 锂盐:**")
                for salt in salts:
                    concentration = salt.get('concentration', '未知')
                    st.write(f"- {salt['name']} ({concentration})")
                    st.caption(f"作用: {salt['role']}")
        
        with col2:
            if solvents:
                st.write("**🧪 溶剂:**")
                for solvent in solvents:
                    st.write(f"- {solvent['name']}")
                    st.caption(f"作用: {solvent['role']}")
        
        with col3:
            if additives:
                st.write("**⚗️ 添加剂:**")
                for additive in additives:
                    st.write(f"- {additive['name']}")
                    st.caption(f"作用: {additive['role']}")
        
        # 兼容性评估
        compatibility = formulation_analysis.get('compatibility_assessment', {})
        if compatibility:
            st.subheader("🔍 兼容性评估")
            
            if compatibility.get('overall') == 'good':
                st.success("✅ 总体兼容性良好")
            else:
                st.warning("⚠️ 兼容性需要注意")
            
            for strength in compatibility.get('strengths', []):
                st.info(f"✅ {strength}")
            
            for issue in compatibility.get('issues', []):
                st.error(f"❌ {issue}")
    
    def display_performance_analysis(self, formulation_analysis):
        """显示性能分析"""
        st.subheader("📊 性能预测与评估")
        
        predictions = formulation_analysis.get('performance_predictions', [])
        
        if not predictions:
            st.info("暂无性能预测数据")
            return
        
        # 使用指标卡片显示关键性能
        cols = st.columns(3)
        
        for i, prediction in enumerate(predictions[:3]):  # 显示前3个指标
            with cols[i % 3]:
                if prediction.get('predicted_value'):
                    value = prediction['predicted_value']
                    metric_name = prediction['metric'].replace('_', ' ').title()
                    
                    # 根据数值范围设置表情符号
                    if 'efficiency' in prediction['metric'] and value >= 99.5:
                        emoji = "🎯"
                    elif 'conductivity' in prediction['metric'] and value >= 10:
                        emoji = "⚡"
                    else:
                        emoji = "📈"
                    
                    st.metric(
                        label=f"{emoji} {metric_name}",
                        value=f"{value}",
                        help=prediction.get('explanation', '')
                    )
        
        # 显示详细预测解释
        st.subheader("详细分析")
        for prediction in predictions:
            if prediction.get('predicted_value'):
                with st.expander(f"{prediction['metric'].replace('_', ' ').title()} 分析"):
                    st.write(prediction.get('explanation', ''))
    
    def display_recommendations(self, recommendations, formulation_analysis):
        """显示改进建议"""
        st.subheader("💡 改进建议")
        
        # 立即行动建议
        immediate_actions = recommendations.get('immediate_actions', [])
        if immediate_actions:
            st.warning("🚨 需要注意的事项:")
            for action in immediate_actions:
                st.write(f"• {action}")
        
        # 性能优化建议
        performance_optimizations = recommendations.get('performance_optimizations', [])
        if performance_optimizations:
            st.info("🎯 性能优化建议:")
            for optimization in performance_optimizations:
                st.write(f"• {optimization}")
        
        # 研究方向建议
        research_directions = recommendations.get('research_directions', [])
        if research_directions:
            st.success("🔬 研究方向:")
            for direction in research_directions:
                st.write(f"• {direction}")
        
        # 风险评估
        risks = formulation_analysis.get('risk_factors', [])
        if risks:
            st.error("⚠️ 潜在风险:")
            for risk in risks:
                st.write(f"• {risk}")
    
    def display_research_insights(self, research_insights):
        """显示研究洞察"""
        if not research_insights:
            st.info("🔍 启用'包含文献调研'选项可获得研究洞察")
            return
        
        st.subheader("📚 研究洞察")
        
        # 常见配方模式
        common_formulations = research_insights.get('common_formulations', [])
        if common_formulations:
            st.write("**常见配方模式:**")
            for formula in common_formulations:
                st.write(f"- {formula['formulation']} (出现频次: {formula['frequency']})")
        
        # 性能基准
        performance_benchmarks = research_insights.get('performance_benchmarks', {})
        if performance_benchmarks:
            st.write("**📊 性能基准:**")
            for metric, data in performance_benchmarks.items():
                metric_name = metric.replace('_', ' ').title()
                st.write(f"- {metric_name}: 平均 {data['average']:.2f} (范围: {data['min']}-{data['max']})")
        
        # 研究趋势
        trends = research_insights.get('trends', [])
        if trends:
            st.write("**📈 研究趋势:**")
            for trend in trends:
                st.info(f"• {trend}")
        
        # 研究空白
        research_gaps = research_insights.get('research_gaps', [])
        if research_gaps:
            st.write("**🎯 研究空白:**")
            for gap in research_gaps:
                st.warning(f"• {gap}")
    
    def render_system_info(self):
        """渲染系统信息页面"""
        st.header("📊 系统信息")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🛠️ 技术架构")
            st.markdown("""
            **核心模块:**
            - 📄 PDF处理器 - 提取论文内容和配方
            - 🔍 检索系统 - 基于TF-IDF的智能检索
            - 🧪 分析智能体 - 专业分析和建议
            - 🌐 Web界面 - Streamlit交互界面
            
            **技术特点:**
            - 💪 纯Python实现，无外部依赖冲突
            - 🎯 电解液领域专业化
            - 🔄 实时分析和反馈
            - 📚 支持多文档知识库
            """)
        
        with col2:
            st.subheader("📈 系统统计")
            
            if st.session_state.knowledge_base_ready:
                stats = self.retrieval_manager.get_statistics()
                st.metric("文档数量", stats['document_count'])
                st.metric("词汇表大小", stats['vocabulary_size'])
            else:
                st.info("知识库未就绪")
            
            st.metric("分析历史", len(st.session_state.analysis_history))
            st.metric("上传文件", len(st.session_state.uploaded_files))
        
        st.subheader("🎯 使用指南")
        st.markdown("""
        1. **📚 文献管理** - 上传PDF论文或加载示例数据构建知识库
        2. **🔍 智能检索** - 搜索相关研究文献和配方信息  
        3. **🧪 配方分析** - 获取专业分析和改进建议
        4. **📊 研究洞察** - 查看领域趋势和研究空白
        
        **💡 提示:** 使用具体的电解液配方描述可以获得更准确的分析结果。
        """)

def main():
    """主函数"""
    try:
        app = ElectrolyteExpertApp()
        app.run()
    except Exception as e:
        st.error(f"应用运行出错: {e}")
        st.info("请确保所有依赖已正确安装")

if __name__ == "__main__":
    main()