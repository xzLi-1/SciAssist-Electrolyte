import os
import re
import math
import logging
from typing import List, Dict, Any, Tuple
from collections import Counter, defaultdict
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PurePythonRetriever:
    """
    纯Python实现的电解液检索系统 - 完全避免OpenMP冲突
    """
    
    def __init__(self):
        self.documents = []
        self.vocab = set()
        self.doc_vectors = []
        self.idf = {}
        self.is_trained = False
        
        # 电解液领域关键词
        self.domain_terms = [
            'electrolyte', 'lithium', 'battery', 'ionic', 'conductivity',
            'coulombic', 'efficiency', 'voltage', 'cycle', 'stability',
            'SEI', 'interface', 'solvent', 'salt', 'additive', 'formation',
            'performance', 'capacity', 'retention', 'density', 'energy',
            'anode', 'cathode', 'cell', 'cycling', 'decomposition',
            'LiPF6', 'LiTFSI', 'LiFSI', 'EC', 'DEC', 'DMC', 'EMC', 'FEC', 'VC',
            '库伦效率', '离子电导率', '电化学窗口', '界面稳定性'
        ]
        
        logger.info("初始化纯Python电解液检索系统")
    
    def preprocess_text(self, text: str) -> List[str]:
        """文本预处理"""
        # 转换为小写
        text = text.lower()
        # 移除特殊字符，保留字母、数字和基本标点
        text = re.sub(r'[^\w\s.,;:!?]', '', text)
        # 分词
        words = text.split()
        return words
    
    def build_vocabulary(self, documents: List[Dict]) -> None:
        """构建词汇表"""
        all_words = set()
        for doc in documents:
            words = self.preprocess_text(doc['content'])
            all_words.update(words)
        
        # 添加领域术语
        all_words.update([term.lower() for term in self.domain_terms])
        self.vocab = all_words
        logger.info(f"词汇表构建完成，共 {len(self.vocab)} 个词")
    
    def compute_tf(self, words: List[str]) -> Dict[str, float]:
        """计算词频"""
        word_count = len(words)
        if word_count == 0:
            return {}
        
        tf = {}
        word_freq = Counter(words)
        
        for word, freq in word_freq.items():
            if word in self.vocab:
                tf[word] = freq / word_count
        
        return tf
    
    def compute_idf(self, documents: List[Dict]) -> None:
        """计算逆文档频率"""
        doc_count = len(documents)
        doc_freq = defaultdict(int)
        
        for doc in documents:
            words = set(self.preprocess_text(doc['content']))
            for word in words:
                if word in self.vocab:
                    doc_freq[word] += 1
        
        self.idf = {}
        for word, freq in doc_freq.items():
            self.idf[word] = math.log(doc_count / (1 + freq))
    
    def build_tfidf_vectors(self, documents: List[Dict]) -> None:
        """构建TF-IDF向量"""
        self.doc_vectors = []
        
        for doc in documents:
            words = self.preprocess_text(doc['content'])
            tf = self.compute_tf(words)
            
            vector = {}
            for word, tf_value in tf.items():
                if word in self.idf:
                    vector[word] = tf_value * self.idf[word]
            
            self.doc_vectors.append(vector)
    
    def build_knowledge_base(self, documents: List[Dict[str, Any]]) -> None:
        """构建知识库"""
        if not documents:
            raise ValueError("文档列表不能为空")
        
        logger.info(f"开始构建知识库，共 {len(documents)} 个文档")
        
        self.documents = documents
        self.build_vocabulary(documents)
        self.compute_idf(documents)
        self.build_tfidf_vectors(documents)
        self.is_trained = True
        
        logger.info("知识库构建完成")
    
    def cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """计算余弦相似度"""
        # 获取所有唯一的词
        all_words = set(vec1.keys()) | set(vec2.keys())
        
        dot_product = 0
        norm1 = 0
        norm2 = 0
        
        for word in all_words:
            v1 = vec1.get(word, 0)
            v2 = vec2.get(word, 0)
            dot_product += v1 * v2
            norm1 += v1 * v1
            norm2 += v2 * v2
        
        if norm1 == 0 or norm2 == 0:
            return 0
        
        return dot_product / (math.sqrt(norm1) * math.sqrt(norm2))
    
    def search(self, query: str, top_k: int = 5, min_score: float = 0.1) -> List[Dict]:
        """搜索相关文档"""
        if not self.is_trained:
            raise ValueError("检索系统尚未训练，请先构建知识库")
        
        # 处理查询
        query_words = self.preprocess_text(query)
        query_tf = self.compute_tf(query_words)
        
        # 构建查询向量
        query_vector = {}
        for word, tf_value in query_tf.items():
            if word in self.idf:
                query_vector[word] = tf_value * self.idf[word]
        
        # 计算相似度
        similarities = []
        for i, doc_vector in enumerate(self.doc_vectors):
            similarity = self.cosine_similarity(query_vector, doc_vector)
            if similarity >= min_score:
                similarities.append((i, similarity))
        
        # 排序并返回top_k结果
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for doc_idx, similarity in similarities[:top_k]:
            doc = self.documents[doc_idx]
            results.append({
                'content': doc['content'],
                'similarity': similarity,
                'metadata': doc['metadata']
            })
        
        return results
    
    def extract_formulations_from_text(self, text: str) -> List[Dict]:
        """从文本中提取电解液配方"""
        formulations = []
        
        patterns = [
            r'(\d+\.?\d*)\s*[Mm]\s*(LiPF6|LiTFSI|LiFSI|LiBOB)',
            r'(\d+)\s*[Mm]\s*(LiPF6|LiTFSI|LiFSI|LiBOB)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                formulations.append({
                    'type': 'salt',
                    'component': match.group(2),
                    'concentration': match.group(1)
                })
        
        return formulations
    
    def extract_metrics_from_text(self, text: str) -> Dict:
        """从文本中提取性能指标"""
        metrics = {}
        
        ce_match = re.search(r'CE\s*[=:]\s*(\d+\.?\d*)%?', text, re.IGNORECASE)
        if ce_match:
            try:
                metrics['coulombic_efficiency'] = float(ce_match.group(1))
            except ValueError:
                pass
        
        cond_match = re.search(r'(\d+\.?\d*)\s*mS\s*cm', text, re.IGNORECASE)
        if cond_match:
            try:
                metrics['ionic_conductivity'] = float(cond_match.group(1))
            except ValueError:
                pass
        
        return metrics