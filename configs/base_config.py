MODEL_CONFIG = {
    "base_model": "Qwen/Qwen-7B-Chat",
    "embedding_model": "BAAI/bge-large-zh",
    "max_length": 4096
}

RETRIEVAL_CONFIG = {
    "chunk_size": 512,
    "chunk_overlap": 50,
    "top_k": 5
}

DOMAIN_CONFIG = {
    "field": "battery_electrolyte",
    "key_concepts": [
        "solvation structure", "SEI formation", "ionic conductivity",
        "electrochemical window", "Li+ transference number", "Coulombic efficiency"
    ]
}