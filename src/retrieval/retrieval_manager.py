import os
import logging
from typing import List, Dict, Any
from .electrolyte_retriever import PurePythonRetriever

logger = logging.getLogger(__name__)

class PurePythonRetrievalManager:
    """
    纯Python检索系统管理器
    """
    
    def __init__(self):
        self.retriever = PurePythonRetriever()
        self.is_ready = False
    
    def build_from_documents(self, documents: List[Dict]) -> None:
        """从文档构建知识库"""
        if documents:
            self.retriever.build_knowledge_base(documents)
            self.is_ready = True
            logger.info(f"知识库构建完成，共处理 {len(documents)} 个文档")
        else:
            logger.warning("没有成功处理任何文档")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """搜索文档"""
        if not self.is_ready:
            raise ValueError("检索系统尚未准备好，请先构建知识库")
        
        return self.retriever.search(query, top_k)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取系统统计信息"""
        if not self.is_ready:
            return {"status": "not_ready"}
        
        return {
            "status": "ready",
            "document_count": len(self.retriever.documents),
            "vocabulary_size": len(self.retriever.vocab)
        }