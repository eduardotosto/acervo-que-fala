"""Gera avaliacao/painel/relatorio_juiz.md a partir do julgamento consolidado (E10).

O relatório é o material de ADJUDICAÇÃO: o juiz aponta, o Eduardo decide. Entram só os
itens que pedem decisão humana — achados de gravidade alta, vereditos `conferir` e os
pares do A/B em que a baseline venceu. O julgamento completo (todos os achados, todas as
evidências) está em juiz_criterios.json e juiz_ab.json.

Uso:
    python avaliacao/gerar_relatorio_juiz.py
"""
import collections
import json
import os
import re

AVAL_DIR = os.path.dirname(os.path.abspath(__file__))
PAINEL_DIR = os.path.join(AVAL_DIR, "painel")
CAMADA = {"observacao": "observação", "redacao": "redação", "registro": "registro", "codigo": "código"}
TEXTO = {"alt_text": "alt-text", "descricao_objeto": "descrição", "flags": "flags",
         "observacao": "observação"}


def ler(nome):
    with open(os.path.join(PAINEL_DIR, nome), encoding="utf-8") as f:
        return json.load(f)


def limpo(texto):
    return re.sub(r"\s+", " ", texto or "").replace("|", "/").strip()


def itens_para_adjudicar(criterios):
    """Os itens que pedem decisão humana, na ordem e com a numeração do relatório:
    primeiro os achados de gravidade alta, caso a caso; depois os vereditos `conferir`.
    A página de adjudicação usa a mesma função — os números são os mesmos nos dois."""
    itens = []
    for j in criterios:
        for a in j["achados"]:
            if a["gravidade"] == "alta":
                itens.append({"tipo": "achado_grave", "id": j["id"], **a})
    for j in criterios:
        for c in j["criterios"]:
            if c["veredito"] == "conferir":
                itens.append({"tipo": "conferir", "id": j["id"], **c})
    return [dict(it, numero=n) for n, it in enumerate(itens, 1)]


def main():
    dossies = {d["id"]: d for d in ler("dossies.json")}
    criterios, ab = ler("juiz_criterios.json"), ler("juiz_ab.json")
    rotulo = lambda i: (f"{dossies[i]['titulo']} {dossies[i]['povo']} ({i}, "
                        f"{dossies[i]['conjunto']})")

    itens = itens_para_adjudicar(criterios)
    caminho_adj = os.path.join(PAINEL_DIR, "adjudicacao.json")
    adj = ler("adjudicacao.json") if os.path.exists(caminho_adj) else None
    decisoes = {d["numero"]: d for d in adj["itens"]} if adj else {}
    def decisao(numero):
        d = decisoes.get(numero, {})
        return (d.get("decisao") or "") + (f" — {d['nota']}" if d.get("nota") else "")
    graves = [(it["id"], it) for it in itens if it["tipo"] == "achado_grave"]
    conferir = [(it["id"], it) for it in itens if it["tipo"] == "conferir"]
    perdidos = [p for p in ab if p["descreve_melhor"] == "baseline"]
    todos = [a for j in criterios for a in j["achados"]]

    L = ["# Relatório do juiz — lote de avaliação (29/09/2026)", "",
         "Gerado por `avaliacao/gerar_relatorio_juiz.py` a partir de `juiz_criterios.json` e "
         "`juiz_ab.json`. Protocolo em [protocolo_juiz.md](protocolo_juiz.md).", "",
         "**Como usar:** cada item numerado pede uma decisão — *concordo*, *discordo* ou "
         "*parcial*. Achado adjudicado vira dado do projeto; discordância calibra o juiz.", "",
         (f"**Adjudicado por {adj['adjudicado_por']} em {adj['data']}:** "
          + ", ".join(f"{n} {d}" for d, n in collections.Counter(
              x["decisao"] or "sem decisão" for x in adj["itens"]).most_common())
          + f", de {len(adj['itens'])} itens. Origem do registro: {adj.get('origem', 'página de adjudicação')}"
          if adj else
          "**Ainda não adjudicado.** Os números abaixo são a leitura do juiz, com a margem medida "
          "em 27/08 (concordância de ~95%, recall de ~89%)."), "",
         "## O julgamento em números", "",
         "| | Total |", "|---|---|",
         f"| Casos julgados | {len(criterios)} |",
         f"| Achados | {len(todos)} |",
         f"| Achados de gravidade alta | {len(graves)}, em "
         f"{len({i for i, _ in graves})} casos |",
         f"| Vereditos `conferir` | {len(conferir)} |",
         f"| Pares do A/B | {len(ab)} |",
         f"| Pares em que a baseline descreve melhor | {len(perdidos)} |", "",
         "Camada dos achados de gravidade alta: " + ", ".join(
             f"{CAMADA[c]} {n}" for c, n in collections.Counter(
                 a["camada"] for _, a in graves).most_common()) + ".", "",
         "## 1. Achados de gravidade alta", "",
         "Informação falsa ou inventada, segundo o juiz. A camada diz onde o erro nasceu.", ""]
    for caso in criterios:
        do_caso = [a for i, a in graves if i == caso["id"]]
        if not do_caso:
            continue
        L += [f"### {rotulo(caso['id'])}", ""]
        for a in do_caso:
            L += [f"**{a['numero']}.** {limpo(a['descricao'])}",
                  f"   - Onde: {TEXTO.get(a['texto'], a['texto'])} · camada: {CAMADA[a['camada']]}",
                  f"   - Evidência: {limpo(a['evidencia'])}",
                  f"   - Adjudicação: {decisao(a['numero'])}", ""]

    L += ["## 2. Vereditos que pedem olho humano", "",
          "O juiz não decidiu: depende de tonalidade, leitura de padrão ou nitidez da foto.", ""]
    for i, c in conferir:
        L += [f"**{c['numero']}.** {rotulo(i)} — critério: *{limpo(c['criterio'])}*",
              f"   - O que o juiz viu: {limpo(c['evidencia'])}",
              f"   - Adjudicação: {decisao(c['numero'])}", ""]

    L += ["## 3. A/B cego: pares em que a descrição curatorial descreve melhor", "",
          "No motivo, A e B são os lados do sorteio; a coluna ao lado diz qual era o texto gerado.", "",
          "| Caso | Lado do gerado | Critério decisivo | Motivo do juiz |", "|---|---|---|---|"]
    for p in perdidos:
        L.append(f"| {rotulo(p['id'])} | {p['lado_do_gerado']} | {limpo(p['criterio_decisivo'])} | "
                 f"{limpo(p['motivo'])} |")
    L.append("")

    with open(os.path.join(PAINEL_DIR, "relatorio_juiz.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L))
    print(f"relatorio_juiz.md: {len(graves)} achados graves, {len(conferir)} conferir, "
          f"{len(perdidos)} pares perdidos — {len(itens)} itens para adjudicar")


if __name__ == "__main__":
    main()
