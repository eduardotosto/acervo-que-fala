"""Avaliação do Acervo que Fala — valida o conjunto fixo e imprime as métricas.

Uso:
    python avaliacao/rodar.py                 # valida os casos e imprime as métricas
    python avaliacao/rodar.py --so-validar    # só valida schema e quotas dos casos
    python avaliacao/rodar.py --itens         # acrescenta a lista item a item

Arquivos:
    avaliacao/casos.jsonl            — 40 casos fixos (1 JSON por linha)
    avaliacao/holdout.jsonl          — 10 casos reservados, rodados uma única vez
    resultados/06_lote_casos.json    — saída do Notebook 06 para os 40 casos
    resultados/06_lote_holdout.json  — saída do Notebook 06 para o holdout

Os blocos 1 a 5 são o que código consegue medir sem olhar a fotografia. Fidelidade
visual (o texto descreve o que a foto mostra?) é trabalho do juiz: o bloco 6 aparece
quando avaliacao/painel/ tem o julgamento consolidado (E10).
"""
import argparse
import collections
import json
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.config import DADOS_DIR
import checar_gabarito
import checar_lote

AVAL_DIR = os.path.dirname(os.path.abspath(__file__))
PAINEL_DIR = os.path.join(AVAL_DIR, "painel")
NOTAS_AB = ("fidelidade", "clareza_ao_ouvido", "concisao")
RESULTADOS_DIR = os.path.join(os.path.dirname(AVAL_DIR), "resultados")

CATEGORIAS_BORDA = {
    "jargao_catalogo",
    "divergencia_imagem_catalogo",
    "artefato_estudio",
    "foto_parcial",
    "enquadramento_distante",  # descoberta na revisão humana da E3 (24/08/2026)
    "metadado_suspeito",
    "texto_sem_hierarquia",
    "caso_simples",
}
CAMPOS_OBRIGATORIOS = [
    "item_id", "titulo", "povo", "categoria_objeto",
    "categorias_borda", "criterios", "baseline",
]
MAX_CERAMICA_AVALIACAO = 10  # quota decidida na E2 (dados/relatorio_coleta.md)

# Jargão de catálogo: só os termos que o projeto JÁ adjudicou como jargão — a lista do
# validador do Notebook 04 (6ª adjudicação) e o verbete do glossário que manda traduzir.
# Lista curta de propósito: criar termo novo agora seria ajustar a régua ao resultado.
RE_JARGAO = re.compile(r"(?<![a-zà-ú])(globular\w*|extrovertid\w*|reticulad\w*|zoomorf\w*|"
                       r"gameliforme\w*)", re.I)
RE_MEDIDA = re.compile(r"\d+(?:[.,]\d+)?\s*cm", re.I)

# Anotação humana da E3 -> o que o sistema faz com ela. enquadramento_distante não tem
# mecanismo correspondente no sistema: aparece na tabela como lacuna, não como erro.
SINAIS = {
    "artefato_estudio": lambda it: tem_flag(it, "artefato_estudio"),
    "divergencia_imagem_catalogo": lambda it: tem_flag(it, "divergencia_imagem_catalogo"),
    "metadado_suspeito": lambda it: tem_flag(it, "metadado_suspeito"),
    "foto_parcial": lambda it: it.get("enquadramento") == "detalhe",
}


def tem_flag(item, tipo):
    return any(f.get("tipo") == tipo for f in (item.get("flags") or []))


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


# ---------------------------------------------------------------- métricas
def com_texto(item):
    return bool(item.get("resolucao_ok", True) and item.get("json_valido") and item.get("alt_text"))


def criterios_do_alt(alt, titulo, povo):
    """Os critérios do nível 1 que código confere: até 30 palavras, começa pelo objeto,
    cita o povo, sem jargão de catálogo, sem medida. Valem igual para o texto gerado e
    para a baseline (a descrição curatorial usada como alt-text)."""
    a = (alt or "").lower()
    inicio = " ".join(a.split()[:4])
    nome_objeto = titulo.lower().split()[0]
    return {
        "até 30 palavras": len(a.split()) <= 30,
        "começa pelo objeto": nome_objeto in inicio,
        "cita o povo": povo.split()[0].lower() in a if povo else False,
        "sem jargão de catálogo": RE_JARGAO.search(a) is None,
        "sem medida": RE_MEDIDA.search(a) is None,
    }


def medir_regua(itens):
    """A régua mecânica, com a escala recalculada pelo código atual (como em
    checar_lote.medir): mede-se o texto contra a política de hoje."""
    por_item, contagem = [], collections.Counter()
    for it in itens:
        if it.get("registro"):
            it = dict(it, escala=checar_lote.analisar_registro(it["registro"])[0])
        problemas = checar_lote.verificar(it)
        por_item.append((it["id"], it.get("titulo", ""), problemas))
        contagem.update(chave for chave, _ in problemas)
    return por_item, contagem


def medir_recorte(itens, casos_por_id, gabarito):
    gerados = [it for it in itens if com_texto(it)]
    por_item, contagem = medir_regua(itens)

    alt = {"gerado": collections.Counter(), "baseline": collections.Counter()}
    palavras = {"gerado": [], "baseline": []}
    todos = {"gerado": 0, "baseline": 0}
    for it in gerados:
        caso = casos_por_id[it["id"]]
        for lado, texto in (("gerado", it["alt_text"]), ("baseline", caso["baseline"])):
            c = criterios_do_alt(texto, caso["titulo"], caso["povo"])
            alt[lado].update(k for k, ok in c.items() if ok)
            todos[lado] += all(c.values())
            palavras[lado].append(len(texto.split()))

    observados = [it for it in itens if it.get("observacao")]
    sinais = {}
    for borda, sinalizou in SINAIS.items():
        anotados = [it for it in observados if borda in casos_por_id[it["id"]]["categorias_borda"]]
        sinais[borda] = {
            "anotados": len(anotados),
            "sinalizados": sum(1 for it in anotados if sinalizou(it)),
            "nao_sinalizados": [it["id"] for it in anotados if not sinalizou(it)],
            "sem_anotacao": [it["id"] for it in observados
                             if sinalizou(it) and it not in anotados],
        }

    reincidencia = {e["slug"]: [it["id"] for it in gerados if checar_gabarito.avaliar(e, it)]
                    for e in gabarito["globais"]}
    return {
        "n": len(itens),
        "com_texto": len(gerados),
        "sem_resolucao": sum(1 for it in itens if not it.get("resolucao_ok", True)),
        "falha_de_geracao": sum(1 for it in itens if it.get("resolucao_ok", True) and not com_texto(it)),
        "retry": sum(1 for it in itens if it.get("retry")),
        "regua_sem_problema": sum(1 for _, _, p in por_item if not p),
        "regua_problemas_por_item": round(sum(contagem.values()) / len(itens), 2),
        "regua_por_checagem": dict(contagem.most_common()),
        "regua_por_item": [(i, t, [list(p) for p in ps]) for i, t, ps in por_item],
        "alt_criterios": {lado: dict(alt[lado]) for lado in alt},
        "alt_todos_os_criterios": todos,
        "alt_mediana_palavras": {lado: statistics.median(v) if v else 0 for lado, v in palavras.items()},
        "flags_por_tipo": dict(collections.Counter(
            f.get("tipo") for it in itens for f in (it.get("flags") or []))),
        "sinais": sinais,
        "reincidencia_global": reincidencia,
    }


def medir_juiz(itens, juiz):
    """O que o juiz disse sobre os itens deste recorte (E10)."""
    ids = {it["id"] for it in itens}
    casos = [j for j in juiz["criterios"] if j["id"] in ids]
    achados = [a for j in casos for a in j["achados"]]
    pares = [p for p in juiz["ab"] if p["id"] in ids]
    por_criterio = {}
    for j in casos:
        for c in j["criterios"]:
            por_criterio.setdefault(c["criterio"].strip(), collections.Counter())[c["veredito"]] += 1
    conta = lambda valores: dict(collections.Counter(valores))
    return {
        "casos_julgados": len(casos),
        "vereditos": conta(c["veredito"] for j in casos for c in j["criterios"]),
        "por_criterio": {k: dict(v) for k, v in por_criterio.items()},
        "achados_por_gravidade": conta(a["gravidade"] for a in achados),
        "achados_por_camada": conta(a["camada"] for a in achados),
        "achados_graves_por_camada": conta(a["camada"] for a in achados if a["gravidade"] == "alta"),
        "casos_com_achado_grave": sum(1 for j in casos
                                      if any(a["gravidade"] == "alta" for a in j["achados"])),
        "fidelidade_visual": conta(j["fidelidade_visual"] for j in casos),
        "ab_pares": len(pares),
        "ab_descreve_melhor": conta(p["descreve_melhor"] for p in pares),
        "ab_publicaria": conta(p["publicaria"] for p in pares),
        "ab_notas": {lado: {n: round(statistics.mean(p[f"notas_{lado}"][n] for p in pares), 2)
                            for n in NOTAS_AB} if pares else {}
                     for lado in ("gerado", "baseline")},
    }


def imprimir_juiz(recortes):
    nomes = list(recortes)
    j = lambda n: recortes[n]["juiz"]

    def bloco(titulo, campo, pares):
        print(f"   {titulo}")
        for rotulo, chave in pares:
            linha(f"  {rotulo}", [j(n)[campo].get(chave, 0) for n in nomes])

    print()
    print("6. JUIZ (E10) — Claude (Opus); protocolo em avaliacao/painel/protocolo_juiz.md")
    linha("casos julgados", [j(n)["casos_julgados"] for n in nomes])
    bloco("critérios dos casos", "vereditos",
          (("atende", "atende"), ("não atende", "nao_atende"),
           ("conferir (olho humano)", "conferir"), ("não se aplica", "nao_se_aplica")))
    taxa = lambda v: (f"{100 * v.get('atende', 0) / (v.get('atende', 0) + v.get('nao_atende', 0)):.0f}%"
                      if v.get("atende", 0) + v.get("nao_atende", 0) else "—")
    linha("  atende, entre atende e não atende", [taxa(j(n)["vereditos"]) for n in nomes])
    bloco("achados contra a régua editorial, por gravidade", "achados_por_gravidade",
          (("alta (informação falsa ou inventada)", "alta"), ("média (regra quebrada)", "media"),
           ("baixa (estilo)", "baixa")))
    linha("  casos com achado de gravidade alta",
          [f"{j(n)['casos_com_achado_grave']}/{j(n)['casos_julgados']}" for n in nomes])
    camadas = (("observação (viu errado)", "observacao"), ("redação (escreveu errado)", "redacao"),
               ("registro (o catálogo erra)", "registro"), ("código (flag, escala)", "codigo"))
    bloco("achados por camada onde o erro nasceu", "achados_por_camada", camadas)
    bloco("idem, só os de gravidade alta", "achados_graves_por_camada", camadas[:2])
    bloco("fidelidade visual", "fidelidade_visual",
          (("fiel", "fiel"), ("fiel com ressalva", "fiel_com_ressalva"), ("infiel", "infiel"),
           ("conferir", "conferir")))
    print("   A/B cego (alt-text gerado × descrição curatorial)")
    linha("  pares julgados", [j(n)["ab_pares"] for n in nomes])
    for titulo, campo, terceiro in (("descreve melhor", "ab_descreve_melhor", "empate"),
                                    ("publicaria", "ab_publicaria", "nenhum")):
        for lado in ("gerado", "baseline", terceiro):
            linha(f"  {titulo}: {lado}", [j(n)[campo].get(lado, 0) for n in nomes])
    for nota in NOTAS_AB:
        linha(f"  nota {nota.replace('_', ' ')}, de 1 a 5",
              [f"{j(n)['ab_notas']['gerado'].get(nota, '—')} | "
               f"{j(n)['ab_notas']['baseline'].get(nota, '—')}" for n in nomes])
    print("   (notas: gerado | baseline)")


# ---------------------------------------------------------------- impressão
def linha(rotulo, valores, larg=18):
    print(f"   {rotulo:38}" + "".join(f"{str(v):>{larg}}" for v in valores))


def imprimir(lotes, recortes, itens_a_itens):
    nomes = list(recortes)
    cab = lotes[0]
    print(f"\nACERVO QUE FALA — métricas do conjunto fixo")
    print(f"sistema: {cab['modelo']} · rubrica {cab['rubrica_versao']} · "
          f"notebook {cab['notebook']} · executado em {cab.get('executado_em_utc', '?')} UTC")
    print("tempo de geração: " + " · ".join(
        f"{l['conjunto']} {l.get('minutos_de_geracao', '?')} min" for l in lotes))
    print("'não vistos' = os casos sem os 5 objetos do smoke test, que estiveram no "
          "lote de desenvolvimento")

    print("\n1. COBERTURA")
    linha("", [f"{n} ({recortes[n]['n']})" for n in nomes])
    for rotulo, chave in (("com descrição gerada", "com_texto"),
                          ("sem resolução (flag, nenhum texto)", "sem_resolucao"),
                          ("falha de geração", "falha_de_geracao"),
                          ("passaram pelo retry", "retry")):
        linha(rotulo, [recortes[n][chave] for n in nomes])

    print("\n2. RÉGUA MECÂNICA (avaliacao/checar_lote.py)")
    linha("itens sem problema", [f"{recortes[n]['regua_sem_problema']}/{recortes[n]['n']}" for n in nomes])
    linha("problemas por item", [recortes[n]["regua_problemas_por_item"] for n in nomes])
    chaves = sorted({k for n in nomes for k in recortes[n]["regua_por_checagem"]},
                    key=lambda k: -sum(recortes[n]["regua_por_checagem"].get(k, 0) for n in nomes))
    for k in chaves:
        linha(f"  {k}", [recortes[n]["regua_por_checagem"].get(k, "·") for n in nomes])

    print("\n3. ALT-TEXT: GERADO × BASELINE (descrição curatorial usada como alt-text)")
    print("   só itens com descrição gerada; cada célula é gerado | baseline")
    criterios = list(criterios_do_alt("", "x", "x"))
    par = lambda r, g, b: f"{g}/{r['com_texto']} | {b}/{r['com_texto']}"
    for c in criterios:
        linha(c, [par(recortes[n], recortes[n]["alt_criterios"]["gerado"].get(c, 0),
                      recortes[n]["alt_criterios"]["baseline"].get(c, 0)) for n in nomes])
    linha("atende aos 5 critérios", [par(recortes[n], recortes[n]["alt_todos_os_criterios"]["gerado"],
                                         recortes[n]["alt_todos_os_criterios"]["baseline"]) for n in nomes])
    linha("mediana de palavras", [f"{recortes[n]['alt_mediana_palavras']['gerado']:g} | "
                                  f"{recortes[n]['alt_mediana_palavras']['baseline']:g}" for n in nomes])

    print("\n4. FLAGS × ANOTAÇÃO HUMANA (categorias de borda anotadas na E3)")
    print("   cada célula é sinalizados/anotados (+ sinalizados sem anotação humana)")
    for borda in SINAIS:
        linha(borda, [f"{recortes[n]['sinais'][borda]['sinalizados']}/"
                      f"{recortes[n]['sinais'][borda]['anotados']} "
                      f"(+{len(recortes[n]['sinais'][borda]['sem_anotacao'])})" for n in nomes])
    linha("enquadramento_distante", ["sem mecanismo"] * len(nomes))
    todos_tipos = sorted({t for n in nomes for t in recortes[n]["flags_por_tipo"] if t})
    for t in todos_tipos:
        linha(f"  flags emitidas: {t}"[:38], [recortes[n]["flags_por_tipo"].get(t, "·") for n in nomes])

    print("\n5. GABARITO EDITORIAL — padrões globais das revisões humanas (itens afetados)")
    for slug in recortes[nomes[0]]["reincidencia_global"]:
        linha(slug, [len(recortes[n]["reincidencia_global"][slug]) or "·" for n in nomes])

    if itens_a_itens:
        for n in nomes:
            print(f"\n=== {n} — régua item a item ===")
            for id_, titulo, problemas in recortes[n]["regua_por_item"]:
                marca = "ok" if not problemas else "; ".join(
                    f"{k}{' (' + v + ')' if v else ''}" for k, v in problemas)
                print(f"{id_:>7} {titulo[:26]:26} {marca}")


def metricas(args, casos, holdout):
    if not os.path.exists(args.casos):
        raise SystemExit(f"\nMétricas: falta {args.casos} — rode o Notebook 06 no Colab e "
                         f"traga o resultado do Drive (ver docs/ETAPAS.md, E9).")
    with open(args.casos, encoding="utf-8") as f:
        lote_casos = json.load(f)
    lotes = [lote_casos]
    with open(os.path.join(AVAL_DIR, "gabarito_editorial.json"), encoding="utf-8") as f:
        gabarito = json.load(f)
    casos_por_id = {c["item_id"]: c for c in casos + holdout}

    ids_lote = [it["id"] for it in lote_casos["itens"]]
    if sorted(ids_lote) != sorted(c["item_id"] for c in casos):
        raise SystemExit("o lote não contém exatamente os 40 casos de avaliacao/casos.jsonl")

    itens = lote_casos["itens"]
    recortes = {
        "casos": medir_recorte(itens, casos_por_id, gabarito),
        # os 5 objetos do smoke test estiveram no lote de desenvolvimento
        "não vistos": medir_recorte(
            [it for it in itens if not it.get("visto_no_desenvolvimento")], casos_por_id, gabarito),
    }
    if os.path.exists(args.holdout):
        with open(args.holdout, encoding="utf-8") as f:
            lote_holdout = json.load(f)
        if sorted(it["id"] for it in lote_holdout["itens"]) != sorted(c["item_id"] for c in holdout):
            raise SystemExit("o lote de holdout não contém exatamente os 10 casos de holdout.jsonl")
        lotes.append(lote_holdout)
        recortes["holdout"] = medir_recorte(lote_holdout["itens"], casos_por_id, gabarito)

    caminhos_juiz = [os.path.join(PAINEL_DIR, n) for n in ("juiz_criterios.json", "juiz_ab.json")]
    tem_juiz = all(os.path.exists(c) for c in caminhos_juiz)
    if tem_juiz:
        juiz = {}
        for chave, caminho in zip(("criterios", "ab"), caminhos_juiz):
            with open(caminho, encoding="utf-8") as f:
                juiz[chave] = json.load(f)
        por_recorte = {"casos": itens,
                       "não vistos": [it for it in itens if not it.get("visto_no_desenvolvimento")]}
        if "holdout" in recortes:
            por_recorte["holdout"] = lote_holdout["itens"]
        for nome, itens_do_recorte in por_recorte.items():
            recortes[nome]["juiz"] = medir_juiz(itens_do_recorte, juiz)

    imprimir(lotes, recortes, args.itens)
    if tem_juiz:
        imprimir_juiz(recortes)
    with open(args.saida, "w", encoding="utf-8") as f:
        json.dump({"sistema": {k: lote_casos.get(k) for k in
                               ("notebook", "modelo", "rubrica_versao", "executado_em_utc",
                                "versoes_ambiente")},
                   "recortes": recortes}, f, ensure_ascii=False, indent=2)
    print(f"\nmétricas gravadas em {os.path.relpath(args.saida)}")


def main() -> None:
    for saida in (sys.stdout, sys.stderr):  # console do Windows não é UTF-8 por padrão
        if hasattr(saida, "reconfigure"):
            saida.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--so-validar", action="store_true", help="valida schema/quotas, sem métricas")
    ap.add_argument("--itens", action="store_true", help="lista os problemas da régua item a item")
    ap.add_argument("--casos", default=os.path.join(RESULTADOS_DIR, "06_lote_casos.json"))
    ap.add_argument("--holdout", default=os.path.join(RESULTADOS_DIR, "06_lote_holdout.json"))
    ap.add_argument("--saida", default=os.path.join(RESULTADOS_DIR, "06_metricas.json"))
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
    print(f"    Cerâmica em casos: {ceramicas}/{MAX_CERAMICA_AVALIACAO} | bordas cobertas: {len(bordas_cobertas)}/{len(CATEGORIAS_BORDA)}")

    if not args.so_validar:
        metricas(args, casos, holdout)


if __name__ == "__main__":
    main()
