"""Monta o material do juiz (E10) a partir do resultado do Notebook 06.

Dois materiais, para duas perguntas diferentes:

  1. DOSSIÊ por caso — o que o juiz precisa para conferir os critérios do caso: a foto
     em resolução máxima, o registro COMPLETO (todos os campos, regra do protocolo desde
     a revisão do v7), a observação, os textos gerados, as flags, os critérios e a
     anotação humana da E3.
  2. A/B CEGO — a descrição curatorial (baseline) e o alt-text gerado, em ordem
     sorteada com seed fixa, sem dizer qual é qual. Cada par recebe um código opaco
     (P01, P02...) e a foto é copiada com esse nome: quem julga não tem como chegar ao
     id do item. O gabarito do sorteio vai para um arquivo à parte, que o juiz não recebe.

Uso:
    python avaliacao/montar_painel.py --gabarito CAMINHO --lotes-dir PASTA

As fotos ficam em dados/imagens/ (cache local, fora do git).
"""
import argparse
import json
import os
import random
import shutil
import sys

import requests

try:
    # mesma saída de app/tainacan.py: no Windows o Python não enxerga a cadeia de
    # certificados pelo certifi; truststore usa o repositório do sistema operacional
    import truststore

    truststore.inject_into_ssl()
except ImportError:
    pass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import DADOS_DIR, IMAGENS_DIR

AVAL_DIR = os.path.dirname(os.path.abspath(__file__))
PAINEL_DIR = os.path.join(AVAL_DIR, "painel")
RESULTADOS_DIR = os.path.join(os.path.dirname(AVAL_DIR), "resultados")
SEED = 42


def ler_json(caminho):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def ler_jsonl(caminho):
    with open(caminho, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def gravar(caminho, dado):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        json.dump(dado, f, ensure_ascii=False, indent=2)
        f.write("\n")


def baixar_foto(item_pool):
    """Foto em resolução máxima (o arquivo original, não a versão reduzida da página)."""
    os.makedirs(IMAGENS_DIR, exist_ok=True)
    destino = os.path.join(IMAGENS_DIR, f"{item_pool['id']}.jpg")
    if not os.path.exists(destino):
        r = requests.get(item_pool["imagem_url"], timeout=90)
        r.raise_for_status()
        with open(destino, "wb") as f:
            f.write(r.content)
    return destino.replace("\\", "/")


def em_lotes(lista, tamanho):
    return [lista[i:i + tamanho] for i in range(0, len(lista), tamanho)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--casos", default=os.path.join(RESULTADOS_DIR, "06_lote_casos.json"))
    ap.add_argument("--holdout", default=os.path.join(RESULTADOS_DIR, "06_lote_holdout.json"))
    ap.add_argument("--saida", default=PAINEL_DIR, help="pasta dos arquivos versionados")
    ap.add_argument("--gabarito", required=True,
                    help="onde gravar o gabarito do A/B — fora do alcance de quem julga")
    ap.add_argument("--lotes-dir", required=True, help="pasta de trabalho com os lotes do juiz")
    ap.add_argument("--por-lote", type=int, default=10, help="dossiês por lote de critérios")
    ap.add_argument("--por-lote-ab", type=int, default=25, help="pares por lote do A/B")
    args = ap.parse_args()

    pool = {it["id"]: it for it in ler_json(os.path.join(DADOS_DIR, "itens.json"))}
    casos = {c["item_id"]: c for c in ler_jsonl(os.path.join(AVAL_DIR, "casos.jsonl"))
             + ler_jsonl(os.path.join(AVAL_DIR, "holdout.jsonl"))}
    itens = ler_json(args.casos)["itens"] + ler_json(args.holdout)["itens"]
    assert len(itens) == 50 and {it["id"] for it in itens} == set(casos), "lote incompleto"

    dossies, pares = [], []
    for it in itens:
        caso, foto = casos[it["id"]], baixar_foto(pool[it["id"]])
        gerou = bool(it["resolucao_ok"] and it["json_valido"] and it["alt_text"])
        dossies.append({
            "id": it["id"], "conjunto": it["conjunto"],
            "visto_no_desenvolvimento": it["visto_no_desenvolvimento"],
            "titulo": caso["titulo"], "povo": caso["povo"],
            "foto": foto, "foto_url": pool[it["id"]]["imagem_url"],
            "resolucao_vista_pelo_modelo": it["resolucao"],
            "situacao": ("descrição gerada" if gerou else
                         "sem resolução: flag, nenhum texto" if not it["resolucao_ok"] else
                         "falha de geração"),
            "categorias_borda": caso["categorias_borda"],
            "criterios": caso["criterios"],
            "anotacao_humana_e3": caso.get("notas", ""),
            "baseline": caso["baseline"],
            "registro_completo": pool[it["id"]]["metadados"],
            "observacao": it["observacao"],
            "alt_text": it["alt_text"],
            "descricao_objeto": it["descricao_objeto"],
            "flags": it["flags"],
            "passou_pelo_retry": it["retry"],
        })
        if gerou:
            pares.append({"id": it["id"], "foto": foto, "baseline": caso["baseline"],
                          "gerado": it["alt_text"]})

    # A/B cego: a ordem dos pares e o lado de cada texto saem do mesmo sorteio
    sorteio = random.Random(SEED)
    sorteio.shuffle(pares)
    pasta_fotos_ab = os.path.join(IMAGENS_DIR, "ab")
    shutil.rmtree(pasta_fotos_ab, ignore_errors=True)
    os.makedirs(pasta_fotos_ab)
    cego, gabarito = [], {}
    for n, par in enumerate(pares, 1):
        codigo = f"P{n:02d}"
        lado_baseline = sorteio.choice("AB")
        lado_gerado = "B" if lado_baseline == "A" else "A"
        foto_ab = os.path.join(pasta_fotos_ab, f"{codigo}.jpg").replace("\\", "/")
        shutil.copyfile(par["foto"], foto_ab)
        cego.append({"codigo": codigo, "foto": foto_ab,
                     f"texto_{lado_baseline}": par["baseline"],
                     f"texto_{lado_gerado}": par["gerado"]})
        gabarito[codigo] = {"id": par["id"], lado_baseline: "baseline", lado_gerado: "gerado"}
    cego = [dict(sorted(p.items())) for p in cego]  # texto_A sempre antes de texto_B

    gravar(os.path.join(args.saida, "dossies.json"), dossies)
    gravar(os.path.join(args.saida, "ab_cego.json"), cego)
    gravar(args.gabarito, {"seed": SEED, "pares": gabarito})
    for nome, material, tamanho in (("criterios", dossies, args.por_lote),
                                    ("ab", cego, args.por_lote_ab)):
        for n, lote in enumerate(em_lotes(material, tamanho), 1):
            gravar(os.path.join(args.lotes_dir, f"{nome}_{n:02d}.json"), lote)

    lados = [g["A"] for g in gabarito.values()]
    print(f"dossiês: {len(dossies)} casos → {os.path.relpath(os.path.join(args.saida, 'dossies.json'))}")
    print(f"A/B cego: {len(cego)} pares (baseline no lado A em {lados.count('baseline')}, "
          f"no lado B em {lados.count('gerado')})")
    print(f"sem par no A/B (não geraram texto): "
          f"{[d['id'] for d in dossies if d['situacao'] != 'descrição gerada']}")
    print(f"lotes do juiz em {args.lotes_dir}: "
          f"{len(em_lotes(dossies, args.por_lote))} de critérios, "
          f"{len(em_lotes(cego, args.por_lote_ab))} de A/B")


if __name__ == "__main__":
    main()
