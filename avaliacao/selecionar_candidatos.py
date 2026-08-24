"""Seleção estratificada de candidatos aos 50 casos de avaliação (E3).

Aplica as quotas decididas na E2 (dados/relatorio_coleta.md) sobre o pool
de dados/itens.json e gera avaliacao/candidatos.json — a lista que Eduardo
revisa (na página gerada por gerar_pagina_revisao.py) antes de virar
casos.jsonl + holdout.jsonl.

Determinístico: random.seed(42). Rodar de novo produz a mesma lista.

Uso:
    python avaliacao/selecionar_candidatos.py
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import DADOS_DIR

AVAL_DIR = os.path.dirname(os.path.abspath(__file__))

# Quota final (50 casos) por categoria de objeto + margem de candidatos extras
# para Eduardo poder trocar. Total das quotas = 50.
QUOTAS = {
    "Cerâmica": 9,
    "Adornos de Materiais Ecléticos, Indumentária e Toucador": 8,
    "Objetos rituais, mágicos e lúdicos": 6,
    "Adornos Plumários": 6,
    "Utensílios e implementos de materiais ecléticos": 5,
    "Trançados": 5,
    "Cordões e Tecidos": 4,
    "Instrumentos musicais e de sinalização": 3,
    "Armas": 3,
    "Etnobotânica": 1,
}
EXTRAS_POR_CATEGORIA = 2  # candidatos além da quota, quando o pool permitir

# Os 5 objetos do smoke test entram garantidos, com as bordas já conhecidas.
ANCORAS = {
    9196: ["jargao_catalogo"],
    665: ["divergencia_imagem_catalogo", "artefato_estudio"],
    51023: ["jargao_catalogo"],
    63283: ["foto_parcial", "metadado_suspeito"],
    78838: ["texto_sem_hierarquia"],
}

CRITERIOS_POR_BORDA = {
    "jargao_catalogo": [
        "alt-text em linguagem simples, sem jargão de catalogação",
        "termos técnicos só na descrição do objeto, explicados ou atribuídos ao museu",
    ],
    "divergencia_imagem_catalogo": [
        "elemento visível ausente do catálogo é descrito",
        "divergência sinalizada em flag para revisão, não omitida",
    ],
    "artefato_estudio": [
        "artefatos de estúdio (cartela de cor, escala, suporte) excluídos da descrição",
    ],
    "foto_parcial": [
        "alt-text avisa que a foto é detalhe/parcial",
        "descrição do objeto completa vem do registro, com atribuição",
    ],
    "metadado_suspeito": [
        "valor improvável do registro sinalizado em flag, não repetido como fato",
    ],
    "texto_sem_hierarquia": [
        "alt-text conciso (≤30 palavras), objeto primeiro",
        "informação do registro reorganizada com hierarquia na descrição do objeto",
    ],
    "caso_simples": [
        "alt-text descreve a fotografia (enquadramento incluído)",
        "descrição do objeto ancorada: todo fato não-visível tem fonte no registro",
        "nenhum elemento inventado",
    ],
}


def bordas_preliminares(item: dict) -> list[str]:
    if item["id"] in ANCORAS:
        return ANCORAS[item["id"]]
    descricao = item["metadados"].get("Descrição", "")
    if len(descricao) > 400:
        return ["texto_sem_hierarquia"]
    return ["caso_simples"]


def main() -> None:
    with open(os.path.join(DADOS_DIR, "itens.json"), encoding="utf-8") as f:
        pool = json.load(f)

    random.seed(42)
    por_categoria: dict[str, list[dict]] = {}
    for it in pool:
        por_categoria.setdefault(it["metadados"].get("Categoria", "(vazio)"), []).append(it)

    candidatos: list[dict] = []
    povos_usados: set[str] = set()
    for categoria, quota in QUOTAS.items():
        disponiveis = list(por_categoria.get(categoria, []))
        random.shuffle(disponiveis)
        alvo = min(quota + EXTRAS_POR_CATEGORIA, len(disponiveis))
        # âncoras da categoria entram primeiro
        escolhidos = [it for it in disponiveis if it["id"] in ANCORAS]
        # depois, gulosamente, preferindo povos ainda não representados
        restantes = [it for it in disponiveis if it["id"] not in ANCORAS]
        restantes.sort(key=lambda it: it["metadados"].get("Povo", "") in povos_usados)
        escolhidos.extend(restantes[: alvo - len(escolhidos)])
        for it in escolhidos:
            povos_usados.add(it["metadados"].get("Povo", ""))
            bordas = bordas_preliminares(it)
            criterios = []
            for b in bordas:
                criterios.extend(CRITERIOS_POR_BORDA[b])
            candidatos.append(
                {
                    "item_id": it["id"],
                    "titulo": it["titulo"],
                    "povo": it["metadados"].get("Povo", ""),
                    "categoria_objeto": categoria,
                    "quota_categoria": quota,
                    "imagem_url": it["imagem_url"],
                    "url_acervo": it["url"],
                    "baseline": it["metadados"].get("Descrição", ""),
                    "metadados_chave": {
                        k: it["metadados"].get(k, "")
                        for k in ["Matéria-prima", "Técnica de confecção", "Dimensões",
                                  "Função", "Estado de origem", "Ano de aquisição do objeto"]
                        if it["metadados"].get(k)
                    },
                    "categorias_borda": bordas,
                    "criterios": criterios,
                    "ancora_smoke_test": it["id"] in ANCORAS,
                }
            )

    destino = os.path.join(AVAL_DIR, "candidatos.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(candidatos, f, ensure_ascii=False, indent=2)

    n_por_cat = {c: sum(1 for x in candidatos if x["categoria_objeto"] == c) for c in QUOTAS}
    print(f"OK: {len(candidatos)} candidatos em {destino}")
    print(f"    povos distintos: {len({c['povo'] for c in candidatos})}")
    for cat, n in n_por_cat.items():
        marca = "" if n >= QUOTAS[cat] else "  ⚠ pool insuficiente p/ quota"
        print(f"    {cat}: {n} candidatos (quota final {QUOTAS[cat]}){marca}")


if __name__ == "__main__":
    main()
