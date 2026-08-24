"""Avaliação do Acervo que Fala — valida e (a partir da E8) mede o conjunto fixo.

Uso:
    python avaliacao/rodar.py --so-validar    # E3: valida schema e quotas dos casos
    python avaliacao/rodar.py                 # E8+: roda as métricas automáticas

Arquivos:
    avaliacao/casos.jsonl     — 40 casos fixos (1 JSON por linha)
    avaliacao/holdout.jsonl   — 10 casos reservados; NÃO abrir/rodar antes da E12
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import DADOS_DIR

AVAL_DIR = os.path.dirname(os.path.abspath(__file__))

CATEGORIAS_BORDA = {
    "jargao_catalogo",
    "divergencia_imagem_catalogo",
    "artefato_estudio",
    "foto_parcial",
    "metadado_suspeito",
    "texto_sem_hierarquia",
    "caso_simples",
}
CAMPOS_OBRIGATORIOS = [
    "item_id", "titulo", "povo", "categoria_objeto",
    "categorias_borda", "criterios", "baseline",
]
MAX_CERAMICA_AVALIACAO = 10  # quota decidida na E2 (dados/relatorio_coleta.md)


def carregar_jsonl(caminho: str) -> list[dict]:
    casos = []
    with open(caminho, encoding="utf-8") as f:
        for n, linha in enumerate(f, 1):
            linha = linha.strip()
            if not linha:
                continue
            try:
                casos.append(json.loads(linha))
            except json.JSONDecodeError as e:
                raise SystemExit(f"ERRO {os.path.basename(caminho)} linha {n}: JSON inválido ({e})")
    return casos


def validar(casos: list[dict], nome: str, pool_ids: set[int]) -> list[str]:
    erros = []
    ids_vistos = set()
    for i, caso in enumerate(casos, 1):
        ref = f"{nome}#{i}"
        for campo in CAMPOS_OBRIGATORIOS:
            if not caso.get(campo):
                erros.append(f"{ref}: campo obrigatório vazio: {campo}")
        if caso.get("item_id") in ids_vistos:
            erros.append(f"{ref}: item_id repetido: {caso['item_id']}")
        ids_vistos.add(caso.get("item_id"))
        if caso.get("item_id") not in pool_ids:
            erros.append(f"{ref}: item_id {caso.get('item_id')} não está em dados/itens.json")
        for borda in caso.get("categorias_borda", []):
            if borda not in CATEGORIAS_BORDA:
                erros.append(f"{ref}: categoria de borda desconhecida: {borda}")
        if not isinstance(caso.get("criterios"), list) or len(caso.get("criterios", [])) < 2:
            erros.append(f"{ref}: mínimo de 2 critérios por caso")
    return erros


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--so-validar", action="store_true", help="valida schema/quotas, sem métricas")
    args = ap.parse_args()

    with open(os.path.join(DADOS_DIR, "itens.json"), encoding="utf-8") as f:
        pool_ids = {it["id"] for it in json.load(f)}

    casos = carregar_jsonl(os.path.join(AVAL_DIR, "casos.jsonl"))
    holdout_path = os.path.join(AVAL_DIR, "holdout.jsonl")
    holdout = carregar_jsonl(holdout_path) if os.path.exists(holdout_path) else []

    erros = validar(casos, "casos", pool_ids) + validar(holdout, "holdout", pool_ids)

    if len(casos) != 40:
        erros.append(f"casos.jsonl deve ter 40 casos (tem {len(casos)})")
    if holdout and len(holdout) != 10:
        erros.append(f"holdout.jsonl deve ter 10 casos (tem {len(holdout)})")
    ceramicas = sum(1 for c in casos if c.get("categoria_objeto") == "Cerâmica")
    if ceramicas > MAX_CERAMICA_AVALIACAO:
        erros.append(f"quota E2 violada: {ceramicas} Cerâmica em casos.jsonl (máx {MAX_CERAMICA_AVALIACAO})")
    bordas_cobertas = {b for c in casos for b in c.get("categorias_borda", [])}
    faltando = CATEGORIAS_BORDA - bordas_cobertas
    if faltando:
        erros.append(f"categorias de borda sem caso: {sorted(faltando)}")

    if erros:
        print(f"FALHOU: {len(erros)} problema(s)")
        for e in erros:
            print(f"  - {e}")
        raise SystemExit(1)

    povos = {c["povo"] for c in casos + holdout}
    categorias = {c["categoria_objeto"] for c in casos + holdout}
    print(f"OK: {len(casos)} casos + {len(holdout)} holdout")
    print(f"    povos distintos: {len(povos)} | categorias de objeto: {len(categorias)}")
    print(f"    Cerâmica em casos: {ceramicas}/{MAX_CERAMICA_AVALIACAO} | bordas cobertas: {len(bordas_cobertas)}/7")

    if not args.so_validar:
        print("\nMétricas automáticas: implementação na E8 (ver docs/ETAPAS.md).")


if __name__ == "__main__":
    main()
