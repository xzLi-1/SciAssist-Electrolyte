import fitz  # PyMuPDF
import re
import os
from typing import List, Dict, Tuple
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ElectrolytePDFProcessor:
    """
    专门处理电池电解液领域学术论文的PDF处理器
    """
    
    def __init__(self):
        self.section_keywords = {
            'abstract': [r'abstract', r'摘要'],
            'introduction': [r'introduction', r'引言'],
            'experimental': [r'experimental', r'methods?', r'方法', r'实验部分'],
            'results': [r'results', r'结果', r'results and discussion'],
            'discussion': [r'discussion', r'讨论'],
            'conclusion': [r'conclusion', r'结论']
        }
        
        # 电解液相关术语模式（已修复中文逗号、缺失逗号及重复项）
        self.electrolyte_patterns = {
            'salts': [
                r'LiPF6', r'LiTFSI', r'LiFSI', r'LiBOB', r'LiDFOB', r'LiClO4', r'LiAsF6',
                r'LiNO3', r'LiBF4', r'LiPOF2', r'LiBETI', r'LiDFB', r'LiFNFSI', r'LiTFPFB'
            ],
            'solvents': [
                r'EC', r'DEC', r'DMC', r'EMC', r'FEMC', r'FEC', r'DFEC', r'DME', r'TTE',
                r'PC', r'GBL', r'THF', r'CPME', r'THP', r'1,3-Dioxolane', r'DOL', r'DMAc',
                r'NMP', r'EG', r'PG', r'PEG', r'DMA', r'DMF', r'BC', r'MA', r'EP', r'DPC',
                r'GDE', r'DMSO', r'AN', r'DPhC', r'HFE', r'MEC', r'MP', r'PPC', r'VC', r'VEC',
                r'FPC', r'DMEe', r'BM', r'EE', r'EGDME', r'DEGDME', r'TEGDME', r'SL', r'MeSL',
                r'DMS', r'DES', r'PN', r'BN', r'PhCN', r'DFEC', r'TFEC', r'DFDMC', r'FMEC',
                r'DPrC', r'DBuC', r'MPC', r'EPrC', r'EA', r'MF', r'EB', r'MB', r'EGC', r'GC',
                r'TMC', r'HMPA', r'TMP', r'FEMC', r'DFDEC', r'CP', r'VPC', r'PFA', r'BTFE', r'P3TE'
            ],
            'additives': [r'VC', r'FEC', r'LiNO3', r'CsPF6', r'TMSP', r'TTE']
        }
    
    def extract_structured_content(self, pdf_path: str) -> Dict[str, str]:
        """
        提取结构化的论文内容，按章节组织
        
        Args:
            pdf_path: PDF文件路径
            
        Returns:
            按章节组织的字典，键为章节名，值为章节内容
        """
        try:
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
                
            doc = fitz.open(pdf_path)
            structured_content = {}
            current_section = "header"  # 从文件头开始
            
            logger.info(f"开始处理PDF: {os.path.basename(pdf_path)}")
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                
                if not text.strip():
                    continue
                
                # 检测章节标题（检查每页的前几行）
                lines = text.split('\n')[:5]  # 只检查前5行
                section_found = False
                
                for line in lines:
                    line_clean = line.strip().lower()
                    for section, patterns in self.section_keywords.items():
                        for pattern in patterns:
                            if re.search(pattern, line_clean, re.IGNORECASE):
                                # 确保不是正文中的偶然匹配
                                if len(line_clean) < 100:  # 假设标题不会太长
                                    current_section = section
                                    section_found = True
                                    logger.debug(f"检测到章节: {section} - {line}")
                                    break
                        if section_found:
                            break
                    if section_found:
                        break
                
                # 按章节组织内容
                if current_section not in structured_content:
                    structured_content[current_section] = ""
                structured_content[current_section] += text + "\n"
            
            doc.close()
            logger.info(f"PDF处理完成，共识别 {len(structured_content)} 个章节")
            return structured_content
            
        except Exception as e:
            logger.error(f"PDF处理错误: {e}")
            return {}
    
    def extract_electrolyte_formulations(self, text: str) -> List[Dict]:
        """
        专门提取电解液配方信息
        
        Args:
            text: 要分析的文本
            
        Returns:
            提取到的电解液配方列表
        """
        formulations = []
        
        # 更精确的电解液组成匹配模式
        patterns = [
            # 盐浓度匹配: 1 M LiPF6, 1.5 m LiTFSI
            r'(\d+\.?\d*)\s*[Mm]\s*(LiPF6|LiTFSI|LiFSI|LiBOB|LiClO4)',
            # 溶剂比例匹配: EC:DEC (1:1, v/v), EC/DMC (3:7)
            r'(EC|DEC|DMC|EMC|FEC|DME|PC)[:\/]\s*(EC|DEC|DMC|EMC|FEC|DME|PC)?\s*\(?\s*(\d+)\s*[:：]\s*(\d+)',
            # 添加剂匹配: 2 wt% VC, 5 vol% FEC
            r'(\d+\.?\d*)\s*(wt%|vol%|%)\s*(VC|FEC|LiNO3|CsPF6|TMSP)',
            # 简单的组分提及
            r'\b(\d+\.?\d*\s*[Mm]?)\s*(EC|DEC|DMC|EMC|FEC|DME|PC|VC|LiPF6|LiTFSI|LiFSI)\b'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                formulation = {
                    'component': match.group(2) if match.lastindex >= 2 else match.group(1),
                    'concentration': match.group(1),
                    'context': text[max(0, match.start()-100):match.end()+100],
                    'pattern_used': pattern
                }
                
                # 去重：检查是否已经存在相似的配方
                is_duplicate = False
                for existing in formulations:
                    if (existing['component'] == formulation['component'] and 
                        existing['concentration'] == formulation['concentration']):
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    formulations.append(formulation)
        
        logger.info(f"从文本中提取到 {len(formulations)} 个电解液配方")
        return formulations
    
    def extract_performance_metrics(self, text: str) -> Dict[str, float]:
        """
        提取电池性能指标
        
        Args:
            text: 要分析的文本
            
        Returns:
            性能指标字典
        """
        metrics = {}
        
        # 库伦效率匹配
        ce_patterns = [
            r'CE\s*[=:]\s*(\d+\.?\d*)%?',
            r'coulombic\s+efficiency\s*[=:]\s*(\d+\.?\d*)%?',
            r'库伦效率\s*[=:]\s*(\d+\.?\d*)%?'
        ]
        
        for pattern in ce_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    metrics['coulombic_efficiency'] = float(match.group(1))
                    break
                except ValueError:
                    continue
        
        # 离子电导率匹配
        conductivity_patterns = [
            r'(\d+\.?\d*)\s*mS\s*cm⁻¹',  # mS cm⁻¹
            r'(\d+\.?\d*)\s*mS/cm',
            r'ionic conductivity\s*[=:]\s*(\d+\.?\d*)',
            r'离子电导率\s*[=:]\s*(\d+\.?\d*)'
        ]
        
        for pattern in conductivity_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    metrics['ionic_conductivity'] = float(match.group(1))
                    break
                except ValueError:
                    continue
        
        # 电压窗口匹配
        voltage_patterns = [
            r'(\d+\.?\d*)\s*[Vv]\s*[–\-~]\s*(\d+\.?\d*)\s*[Vv]',
            r'voltage window\s*[=:]\s*(\d+\.?\d*)\s*[Vv]',
            r'电化学窗口\s*[=:]\s*(\d+\.?\d*)\s*[Vv]'
        ]
        
        for pattern in voltage_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    if len(matches[0]) == 2:  # 范围
                        metrics['voltage_window_min'] = float(matches[0][0])
                        metrics['voltage_window_max'] = float(matches[0][1])
                    else:  # 单个值
                        metrics['voltage_window'] = float(matches[0][0])
                    break
                except ValueError:
                    continue
        
        return metrics
    
    def analyze_paper_metadata(self, pdf_path: str) -> Dict:
        """
        分析论文的元数据信息
        
        Args:
            pdf_path: PDF文件路径
            
        Returns:
            论文元数据字典
        """
        try:
            doc = fitz.open(pdf_path)
            first_page_text = doc[0].get_text()
            doc.close()
            
            metadata = {
                'title': self._extract_title(first_page_text),
                'authors': self._extract_authors(first_page_text),
                'abstract': self._extract_abstract(first_page_text),
                'page_count': len(doc)
            }
            
            return metadata
            
        except Exception as e:
            logger.error(f"元数据提取错误: {e}")
            return {}
    
    def _extract_title(self, text: str) -> str:
        """提取论文标题"""
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if line.strip() and len(line.strip()) > 10:  # 假设标题有一定长度
                # 检查是否包含常见的标题特征
                if not any(keyword in line.lower() for keyword in ['abstract', 'introduction', 'author']):
                    return line.strip()
        return "标题未识别"
    
    def _extract_authors(self, text: str) -> List[str]:
        """提取作者信息"""
        lines = text.split('\n')
        authors = []
        
        for i, line in enumerate(lines):
            if any(name_indicator in line.lower() for name_indicator in ['university', 'institute', 'college', '@']):
                # 前一行可能是作者行
                if i > 0 and lines[i-1].strip():
                    potential_authors = lines[i-1].strip()
                    if len(potential_authors) > 5:  # 作者名应该有一定长度
                        authors = [author.strip() for author in potential_authors.split(',')]
                        break
        
        return authors if authors else ["作者未识别"]
    
    def _extract_abstract(self, text: str) -> str:
        """提取摘要"""
        lines = text.split('\n')
        abstract_lines = []
        in_abstract = False
        
        for line in lines:
            if 'abstract' in line.lower() or '摘要' in line:
                in_abstract = True
                continue
            if in_abstract:
                if any(section in line.lower() for section in ['introduction', 'keywords', '1.']):
                    break
                if line.strip():
                    abstract_lines.append(line.strip())
        
        return ' '.join(abstract_lines) if abstract_lines else "摘要未识别"


# 测试代码
if __name__ == "__main__":
    # 测试处理器
    processor = ElectrolytePDFProcessor()
    print("✅ 电解液PDF处理器初始化成功！")
    
    # 测试文本分析
    test_text = """
    The electrolyte was composed of 1 M LiPF6 in EC/DMC (1:1, v/v) with 2 wt% VC additive.
    The Coulombic efficiency was 99.5% and ionic conductivity was 10.5 mS cm⁻¹.
    The voltage window was 3.0-4.5 V.
    """
    
    formulations = processor.extract_electrolyte_formulations(test_text)
    metrics = processor.extract_performance_metrics(test_text)
    
    print(f"提取到配方: {formulations}")
    print(f"提取到性能指标: {metrics}")