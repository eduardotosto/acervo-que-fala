#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Mede qualquer lote contra o GABARITO EDITORIAL — a consolidacao das revisoes do Eduardo.

A regua (checar_lote.py) ve padroes genericos; este script ve outra coisa: os defeitos
ESPECIFICOS que a revisao humana ja apontou, item a item. A metrica e reincidencia —
defeito ja apontado que volta num lote novo. E a resposta a pergunta "estamos avancando?"
nos termos de quem revisa, nao nos termos da regua.

Uso:
    python avaliacao/checar_gabarito.py resultados/04_pipeline_completo_v7.json ...
"""
import io, json, re, sys

RE_CM = re.compile(r"\d+(?:[.,]\d+)?\s*cm", re.I)


def avaliar(entrada, item):
    """True = defeito PRESENTE neste lote."""
    alt = (item.get("alt_text") or "").lower()
    n2 = (item.get("descricao_objeto") or "").lower()
    texto = alt + "\n" + n2
    tipo, padrao = entrada["tipo"], entrada.get("padrao", "")
    if tipo == "proibe":
        return re.search(padrao, texto, re.I) is not None
    if tipo == "proibe_alt":
        return re.search(padrao, alt, re.I) is not None
    if tipo == "exige_alt":
        return re.search(padrao, alt, re.I) is None
    if tipo == "exige":
        return re.search(padrao, texto, re.I) is None
    if tipo == "exige_flag":
        return not any(re.search(padrao, f.get("tipo", ""), re.I)
                       for f in (item.get("flags") or []))
    if tipo == "medidas_2mais":
        return len(RE_CM.findall(n2)) >= 2 or "dimensões:" in n2
    if tipo == "medidas_3mais":
        return len(RE_CM.findall(n2)) >= 3 or "dimensões:" in n2
    if tipo == "proibe_abertura":
        return re.search(padrao, n2.strip(), re.I) is not None
    raise ValueError(tipo)


def main():
    gab = json.load(io.open("avaliacao/gabarito_editorial.json", encoding="utf-8"))
    lotes = []
    for caminho in sys.argv[1:]:
        with io.open(caminho, encoding="utf-8") as f:
            itens = {i["id"]: i for i in json.load(f)["itens"]}
        nome = caminho.rsplit("/", 1)[-1].replace(".json", "").replace("04_pipeline_completo", "v1").replace("v1_", "").replace("05_bakeoff_", "")
        lotes.append((nome, itens))

    linhas = []          # (rotulo, origem, [presenca por lote])
    for e in gab["globais"]:
        for nome, itens in lotes[:1]:
            pass
        presencas = []
        for nome, itens in lotes:
            afetados = [i for i, it in itens.items() if avaliar(e, it)]
            presencas.append(afetados)
        linhas.append((f"[global] {e['slug']}", e["origem"], presencas, None))
    for e in gab["por_item"]:
        presencas = []
        for nome, itens in lotes:
            it = itens.get(e["item"])
            presencas.append([e["item"]] if (it and avaliar(e, it)) else [])
        linhas.append((f"{e['item']} {e['slug']}", e["origem"], presencas, e.get("politica")))

    larg = max(8, max(len(n) for n, _ in lotes) + 2)
    print("\nGABARITO EDITORIAL — reincidência dos defeitos apontados pelo Eduardo, lote a lote")
    print("(número = itens afetados; '·' = defeito ausente; conferir = fidelidade pendente de olho humano)\n")
    print(f"{'defeito':38}" + "".join(f"{n:>{larg}}" for n, _ in lotes))
    print("-" * (38 + larg * len(lotes)))
    for rotulo, origem, presencas, politica in linhas:
        marca = " (conferir)" if politica == "conferir" else ""
        print(f"{(rotulo + marca)[:38]:38}" +
              "".join(f"{len(p) if p else '·':>{larg}}" for p in presencas))
    print("-" * (38 + larg * len(lotes)))
    totais = [sum(len(p) for _, _, pres, _ in linhas for p in [pres[j]]) for j in range(len(lotes))]
    print(f"{'TOTAL de reincidências':38}" + "".join(f"{t:>{larg}}" for t in totais))
    n_def = len(linhas)
    ativos = [sum(1 for _, _, pres, _ in linhas if pres[j]) for j in range(len(lotes))]
    print(f"{'defeitos distintos presentes':38}" +
          "".join(f"{a}/{n_def}".rjust(larg) for a in ativos))


if __name__ == "__main__":
    main()
