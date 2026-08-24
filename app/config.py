"""Configurações centrais — tudo que é ajustável vive aqui (§8.4 do curso).

Sem segredos: o projeto usa apenas APIs públicas e modelos locais.
"""
import os

# API do acervo (Tainacan / Museu do Índio)
TAINACAN_BASE = os.environ.get(
    "TAINACAN_BASE", "https://tainacan.museudoindio.gov.br/wp-json/tainacan/v2"
)
COLECAO_ID = int(os.environ.get("COLECAO_ID", "471"))  # Museu do Índio: 20.965 itens

# Modelos (parâmetros de configuração — trocar aqui não altera a arquitetura)
MODELO_VLM = os.environ.get("MODELO_VLM", "qwen3-vl:8b")        # visão (Ollama)
MODELO_REDATOR = os.environ.get("MODELO_REDATOR", "qwen3:8b")   # redação (Ollama)
MODELO_EMBEDDINGS = os.environ.get(
    "MODELO_EMBEDDINGS", "Qwen/Qwen3-Embedding-0.6B"
)

# Caminhos
DADOS_DIR = os.environ.get("DADOS_DIR", "dados")
IMAGENS_DIR = os.path.join(DADOS_DIR, "imagens")  # cache local, fora do git
