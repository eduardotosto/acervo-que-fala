"""Monta site/dados.json — o lote pré-computado que o site serve.

O site não roda modelo nenhum: ele mostra o que o Notebook 06 gerou e o que a avaliação
mediu. Este script junta, por objeto, o resultado do lote, o caso de avaliação, a leitura
do juiz e, quando existir, a adjudicação do Eduardo.

Uso:
    python site/montar_dados.py
"""
import json
import os

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(SITE_DIR)
PAINEL = os.path.join(RAIZ, "avaliacao", "painel")


def ler(*partes):
    with open(os.path.join(RAIZ, *partes), encoding="utf-8") as f:
        return json.load(f)


def ler_jsonl(*partes):
    with open(os.path.join(RAIZ, *partes), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def main():
    lotes = [ler("resultados", f"06_lote_{c}.json") for c in ("casos", "holdout")]
    pool = {it["id"]: it for it in ler("dados", "itens.json")}
    casos = {c["item_id"]: c for c in ler_jsonl("avaliacao", "casos.jsonl")
             + ler_jsonl("avaliacao", "holdout.jsonl")}
    juiz = {j["id"]: j for j in ler("avaliacao", "painel", "juiz_criterios.json")}
    ab = {p["id"]: p for p in ler("avaliacao", "painel", "juiz_ab.json")}

    adjudicacao = {}
    caminho_adj = os.path.join(PAINEL, "adjudicacao.json")
    if os.path.exists(caminho_adj):
        for d in ler("avaliacao", "painel", "adjudicacao.json")["itens"]:
            adjudicacao[d["numero"]] = d

    # a numeração dos itens adjudicáveis é a do relatório do juiz
    import sys
    sys.path.insert(0, os.path.join(RAIZ, "avaliacao"))
    from gerar_relatorio_juiz import itens_para_adjudicar
    numerados = itens_para_adjudicar(list(juiz.values()))

    objetos = []
    for lote in lotes:
        for it in lote["itens"]:
            caso, j = casos[it["id"]], juiz[it["id"]]
            graves = [{"numero": n["numero"], "descricao": n["descricao"], "camada": n["camada"],
                       "onde": n["texto"], "evidencia": n["evidencia"],
                       "adjudicacao": adjudicacao.get(n["numero"], {}).get("decisao"),
                       "nota": adjudicacao.get(n["numero"], {}).get("nota", "")}
                      for n in numerados if n["id"] == it["id"] and n["tipo"] == "achado_grave"]
            par = ab.get(it["id"])
            objetos.append({
                "id": it["id"], "conjunto": it["conjunto"],
                "visto_no_desenvolvimento": it["visto_no_desenvolvimento"],
                "titulo": caso["titulo"], "povo": caso["povo"],
                "categoria": caso["categoria_objeto"],
                "foto_url": pool[it["id"]]["imagem_url"], "pagina_no_acervo": pool[it["id"]]["url"],
                "baseline": caso["baseline"],
                "alt_text": it["alt_text"], "descricao_objeto": it["descricao_objeto"],
                "flags": it["flags"], "resolucao": it["resolucao"],
                "gerou_texto": bool(it["alt_text"]),
                "passou_pelo_retry": bool(it["retry"]),
                "observacao": it["observacao"],
                "registro": {k: v for k, v in it["registro"].items() if v},
                "juiz": {
                    "fidelidade_visual": j["fidelidade_visual"], "resumo": j["resumo"],
                    "achados": {g: sum(1 for a in j["achados"] if a["gravidade"] == g)
                                for g in ("alta", "media", "baixa")},
                    "graves": graves,
                    "criterios": [{"criterio": c["criterio"], "veredito": c["veredito"]}
                                  for c in j["criterios"]],
                },
                "ab": None if par is None else {
                    "descreve_melhor": par["descreve_melhor"], "publicaria": par["publicaria"],
                    "lado_do_gerado": par["lado_do_gerado"], "motivo": par["motivo"],
                    "notas_gerado": par["notas_gerado"], "notas_baseline": par["notas_baseline"]},
            })

    metricas = ler("resultados", "06_metricas.json")
    dados = {
        "sistema": {"modelo": lotes[0]["modelo"], "rubrica": lotes[0]["rubrica_versao"],
                    "executado_em_utc": lotes[0]["executado_em_utc"],
                    "minutos_de_geracao": sum(l["minutos_de_geracao"] for l in lotes)},
        "adjudicado": bool(adjudicacao),
        "recortes": {nome: {k: v for k, v in r.items() if k != "regua_por_item"}
                     for nome, r in metricas["recortes"].items()},
        "objetos": objetos,
    }
    destino = os.path.join(SITE_DIR, "dados.json")
    with open(destino, "w", encoding="utf-8", newline="\n") as f:
        json.dump(dados, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"site/dados.json: {len(objetos)} objetos, {os.path.getsize(destino) // 1024} KB, "
          f"adjudicação {'incluída' if adjudicacao else 'ainda não existe'}")


if __name__ == "__main__":
    main()
