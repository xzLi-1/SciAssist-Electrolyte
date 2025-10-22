"""
电解液领域专业配置
"""

ELECTROLYTE_DOMAIN_CONFIG = {
    # 关键概念和术语
    "key_concepts": [
        "solvation structure", "SEI formation", "ionic conductivity", 
        "electrochemical window", "Li+ transference number", "Coulombic efficiency",
        "anode stability", "cathode stability", "interface engineering",
        "弱溶剂化", "界面稳定性", "库伦效率", "离子电导率", "电化学窗口"
    ],
    
    # 常见材料
    "common_materials": {
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
    },
    
    # 表征技术
    "characterization_techniques": [
        "XPS", "SEM", "TEM", "XRD", "FTIR", "Raman", "NMR", 
        "EIS", "CV", "LSV", "in-situ characterization",
        "同步辐射", "原位测试", "电化学阻抗"
    ],
    
    # 性能指标阈值
    "performance_thresholds": {
        "coulombic_efficiency": {"excellent": 99.5, "good": 99.0, "poor": 98.0},
        "ionic_conductivity": {"excellent": 10.0, "good": 5.0, "poor": 1.0},
        "cycle_life": {"excellent": 1000, "good": 500, "poor": 100}
    }
}

# 检索增强配置
RETRIEVAL_CONFIG = {
    "chunk_size": 512,
    "chunk_overlap": 50,
    "top_k": 5,
    "similarity_threshold": 0.7
}

# 模型配置
MODEL_CONFIG = {
    "embedding_model": "sentence-transformers/all-mpnet-base-v2",
    "llm_model": "Qwen/Qwen-7B-Chat",
    "max_length": 4096
}