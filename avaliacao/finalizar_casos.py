"""Gera casos.jsonl (40) + holdout.jsonl (10) a partir da revisão do Eduardo (E3).

A revisão humana dos 70 candidatos (24/08/2026, card a card na página
candidatos.html) está codificada em REVISAO — este arquivo é o registro
versionado do julgamento que definiu o conjunto de avaliação.

Regras de fechamento:
- itens marcados "trocar" saem; cada categoria é cortada para a quota da E2,
  priorizando âncoras do smoke test > casos com borda marcada > diversidade
  de povos (determinístico, seed 42);
- holdout: 10 itens só-caso_simples, máx. 2 por categoria, sorteio seed 42;
  não se abre até a E12.

Uso:
    python avaliacao/finalizar_casos.py
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

AVAL_DIR = os.path.dirname(os.path.abspath(__file__))

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

# Critérios base: valem para TODO caso; as bordas acrescentam os específicos.
CRITERIOS_BASE = [
    "alt-text descreve a fotografia (enquadramento incluído)",
    "descrição do objeto ancorada: todo fato não-visível tem fonte no registro",
    "nenhum elemento inventado",
]

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
        "artefatos de estúdio/inventário (etiqueta, numeração, cartela, borda, suporte) excluídos da descrição",
    ],
    "foto_parcial": [
        "alt-text avisa que a foto é detalhe/parcial",
        "descrição do objeto completa vem do registro, com atribuição",
    ],
    "enquadramento_distante": [
        "descrição não inventa detalhes ilegíveis pela distância do enquadramento",
        "incerteza declarada quando o enquadramento limita a leitura",
    ],
    "metadado_suspeito": [
        "valor improvável do registro sinalizado em flag, não repetido como fato",
    ],
    "texto_sem_hierarquia": [
        "alt-text conciso (≤30 palavras), objeto primeiro",
        "informação do registro reorganizada com hierarquia na descrição do objeto",
    ],
    "caso_simples": [],  # só os critérios base
}

DIV = "divergencia_imagem_catalogo"
ART = "artefato_estudio"
FP = "foto_parcial"
ENQ = "enquadramento_distante"

# Revisão do Eduardo, card a card (nº na página → decisão). Cards ausentes = ok.
REVISAO: dict[int, dict] = {
    3: {"bordas": [ART], "nota": "foto com borda preta"},
    4: {"bordas": [DIV], "nota": "não cita duas tonalidades de argila e cor branca da decoração marcada com corda"},
    5: {"trocar": "resolução péssima"},
    8: {"bordas": [DIV], "nota": "não cita duas tonalidades de argila e cor branca da decoração marcada com corda"},
    10: {"bordas": [DIV], "nota": "não cita cores ou tonalidades"},
    11: {"trocar": "resolução muito ruim"},
    13: {"bordas": [ENQ], "nota": "objeto ocupa área muito pequena da foto"},
    14: {"trocar": "resolução muito ruim"},
    15: {"bordas": [DIV, FP], "nota": "faltaram cores na descrição; foto parcial"},
    17: {"bordas": [ENQ], "nota": "objeto ocupa área muito pequena da foto"},
    18: {"bordas": [ENQ], "nota": "objeto ocupa área muito pequena da foto"},
    21: {"trocar": "sem resolução"},
    25: {"trocar": "sem resolução"},
    27: {"bordas": [DIV], "nota": "não cita boca pintada"},
    29: {"bordas": [DIV], "nota": "não cita formato nem as cordas que amarram"},
    31: {"bordas": [ART], "nota": "pequena etiqueta"},
    32: {"bordas": [DIV, ART], "nota": "não cita penas com pontas azuis; pequena etiqueta"},
    33: {"bordas": [DIV, ART], "nota": "não cita penas azuis; pequena etiqueta"},
    34: {"bordas": [ART], "nota": "pequena etiqueta"},
    35: {"bordas": [ART], "nota": "pequena etiqueta"},
    37: {"bordas": [ART], "nota": "pequena etiqueta"},
    38: {"bordas": [ART], "nota": "pequena etiqueta e numeração"},
    39: {"bordas": [ART], "nota": "pequena etiqueta e numeração"},
    40: {"bordas": [ART], "nota": "pequena etiqueta e numeração"},
    41: {"bordas": [ART], "nota": "pequena numeração"},
    42: {"bordas": [ART], "nota": "pequena etiqueta e numeração"},
    43: {"bordas": [ART], "nota": "pequena etiqueta e numeração"},
    48: {"bordas": [FP], "nota": "somente detalhe"},
    52: {"bordas": [FP, ART], "nota": "foto parcial; pequena numeração"},
    53: {"bordas": [DIV], "nota": "não cita formato"},
    54: {"bordas": [ART], "nota": "pequena etiqueta"},
    55: {"bordas": [DIV], "nota": "não cita linhas verdes"},
    56: {"bordas": [DIV], "nota": "não cita tingimento na cor azul"},
    57: {"bordas": [DIV], "nota": "não cita forma"},
    63: {"bordas": [FP], "nota": "só vemos detalhe do objeto"},
    64: {"bordas": [FP], "nota": "só vemos detalhe do objeto"},
    65: {"bordas": [FP], "nota": "só vemos detalhe do objeto"},
    66: {"bordas": [FP], "nota": "só vemos detalhe do objeto"},
    67: {"bordas": [FP], "nota": "só vemos detalhe do objeto"},
    68: {"bordas": [ART], "nota": "garrafa com etiqueta que contém o óleo"},
}


def main() -> None:
    with open(os.path.join(AVAL_DIR, "candidatos.json"), encoding="utf-8") as f:
        candidatos = json.load(f)

    # aplica a revisão
    aptos = []
    for i, c in enumerate(candidatos, 1):
        rev = REVISAO.get(i, {})
        if "trocar" in rev:
            continue
        bordas = list(c["categorias_borda"])
        if rev.get("bordas"):
            bordas = [b for b in bordas if b != "caso_simples"] + [
                b for b in rev["bordas"] if b not in bordas
            ]
        criterios: list[str] = list(CRITERIOS_BASE)
        for b in bordas:
            for cr in CRITERIOS_POR_BORDA[b]:
                if cr not in criterios:
                    criterios.append(cr)
        aptos.append(
            {
                "card": i,
                "item_id": c["item_id"],
                "titulo": c["titulo"],
                "povo": c["povo"],
                "categoria_objeto": c["categoria_objeto"],
                "categorias_borda": bordas,
                "criterios": criterios,
                "baseline": c["baseline"],
                "notas": rev.get("nota", ""),
                "_ancora": c["ancora_smoke_test"],
            }
        )

    # corta cada categoria para a quota: âncora > borda marcada > povo novo
    random.seed(42)
    selecionados: list[dict] = []
    povos_usados: set[str] = set()
    for categoria, quota in QUOTAS.items():
        grupo = [c for c in aptos if c["categoria_objeto"] == categoria]

        def prioridade(c: dict) -> tuple:
            marcado = c["categorias_borda"] != ["caso_simples"]
            return (
                0 if c["_ancora"] else 1,
                0 if marcado else 1,
                0 if c["povo"] not in povos_usados else 1,
                c["card"],
            )

        grupo.sort(key=prioridade)
        for c in grupo[:quota]:
            povos_usados.add(c["povo"])
            selecionados.append(c)

    assert len(selecionados) == 50, f"esperava 50, obtive {len(selecionados)}"

    # holdout: 10 só-caso_simples, máx. 2 por categoria
    simples = [c for c in selecionados if c["categorias_borda"] == ["caso_simples"]]
    random.shuffle(simples)
    holdout, por_cat = [], {}
    for c in simples:
        if len(holdout) == 10:
            break
        if por_cat.get(c["categoria_objeto"], 0) >= 2:
            continue
        por_cat[c["categoria_objeto"]] = por_cat.get(c["categoria_objeto"], 0) + 1
        holdout.append(c)
    assert len(holdout) == 10, f"holdout com {len(holdout)} (precisa de 10 casos simples)"
    ids_holdout = {c["item_id"] for c in holdout}
    casos = [c for c in selecionados if c["item_id"] not in ids_holdout]

    def gravar(nome: str, lista: list[dict]) -> None:
        with open(os.path.join(AVAL_DIR, nome), "w", encoding="utf-8") as f:
            for c in lista:
                registro = {k: v for k, v in c.items() if not k.startswith("_") and k != "card"}
                f.write(json.dumps(registro, ensure_ascii=False) + "\n")

    gravar("casos.jsonl", casos)
    gravar("holdout.jsonl", holdout)

    bordas_ct: dict[str, int] = {}
    for c in casos:
        for b in c["categorias_borda"]:
            bordas_ct[b] = bordas_ct.get(b, 0) + 1
    print(f"OK: {len(casos)} casos + {len(holdout)} holdout")
    print(f"    povos distintos (50): {len({c['povo'] for c in selecionados})}")
    for b, n in sorted(bordas_ct.items(), key=lambda kv: -kv[1]):
        print(f"    {b}: {n} casos")


if __name__ == "__main__":
    main()
