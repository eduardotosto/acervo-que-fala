"""Consolida as saídas do juiz (E10) e abre o gabarito do A/B.

O juiz trabalha em lotes, em sessões separadas. Este script confere cada saída contra o
material que foi entregue ao juiz e só então grava os arquivos versionados:

    avaliacao/painel/juiz_criterios.json  — vereditos e achados, um por caso
    avaliacao/painel/juiz_ab.json         — A/B com os lados já traduzidos (gerado/baseline)
    avaliacao/painel/ab_gabarito.json     — o sorteio, publicado depois do julgamento

Saída que não fecha com a entrada (caso faltando, critério sem veredito, valor fora do
vocabulário) interrompe a consolidação: resultado de avaliação não se completa no chute.

Uso:
    python avaliacao/consolidar_juiz.py --saidas PASTA --gabarito CAMINHO
"""
import argparse
import glob
import json
import os

AVAL_DIR = os.path.dirname(os.path.abspath(__file__))
PAINEL_DIR = os.path.join(AVAL_DIR, "painel")

VEREDITOS = {"atende", "nao_atende", "nao_se_aplica", "conferir"}
CAMADAS = {"observacao", "redacao", "registro", "codigo"}
GRAVIDADES = {"alta", "media", "baixa"}
FIDELIDADES = {"fiel", "fiel_com_ressalva", "infiel", "conferir", "nao_se_aplica"}
NOTAS = ("fidelidade", "clareza_ao_ouvido", "concisao")


def ler(caminho):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def gravar(nome, dado):
    caminho = os.path.join(PAINEL_DIR, nome)
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        json.dump(dado, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return os.path.relpath(caminho)


def juntar(pasta, prefixo):
    itens = []
    for arq in sorted(glob.glob(os.path.join(pasta, f"{prefixo}_*.json"))):
        itens += ler(arq)
    return itens


def conferir_criterios(saida, dossies):
    erros = []
    por_id = {e["id"]: e for e in saida}
    if len(por_id) != len(saida):
        erros.append("caso julgado mais de uma vez")
    for d in dossies:
        e = por_id.get(d["id"])
        if e is None:
            erros.append(f"{d['id']}: caso sem julgamento")
            continue
        julgados = {c["criterio"].strip() for c in e["criterios"]}
        for c in d["criterios"]:
            if c.strip() not in julgados:
                erros.append(f"{d['id']}: critério sem veredito: {c[:50]}")
        for c in e["criterios"]:
            if c["veredito"] not in VEREDITOS:
                erros.append(f"{d['id']}: veredito fora do vocabulário: {c['veredito']!r}")
            if not c.get("evidencia", "").strip():
                erros.append(f"{d['id']}: veredito sem evidência: {c['criterio'][:50]}")
        for a in e["achados"]:
            if a["camada"] not in CAMADAS:
                erros.append(f"{d['id']}: camada fora do vocabulário: {a['camada']!r}")
            if a["gravidade"] not in GRAVIDADES:
                erros.append(f"{d['id']}: gravidade fora do vocabulário: {a['gravidade']!r}")
        if e["fidelidade_visual"] not in FIDELIDADES:
            erros.append(f"{d['id']}: fidelidade fora do vocabulário: {e['fidelidade_visual']!r}")
    sobra = set(por_id) - {d["id"] for d in dossies}
    if sobra:
        erros.append(f"casos julgados que não estavam no painel: {sorted(sobra)}")
    return erros, [por_id[d["id"]] for d in dossies if d["id"] in por_id]


def abrir_ab(saida, cego, gabarito):
    erros, aberto = [], []
    por_codigo = {e["codigo"]: e for e in saida}
    for par in cego:
        e = por_codigo.get(par["codigo"])
        if e is None:
            erros.append(f"{par['codigo']}: par sem julgamento")
            continue
        g = gabarito["pares"][par["codigo"]]
        lado = {g["A"]: "A", g["B"]: "B"}  # "gerado" -> lado, "baseline" -> lado
        traduz = lambda v: g.get(v, v)     # "A"/"B" viram gerado/baseline; o resto passa
        if e["descreve_melhor"] not in ("A", "B", "empate"):
            erros.append(f"{par['codigo']}: descreve_melhor inválido: {e['descreve_melhor']!r}")
        if e["publicaria"] not in ("A", "B", "nenhum"):
            erros.append(f"{par['codigo']}: publicaria inválido: {e['publicaria']!r}")
        for l in "AB":
            for n in NOTAS:
                if e["notas"][l].get(n) not in (1, 2, 3, 4, 5):
                    erros.append(f"{par['codigo']}: nota inválida em {l}.{n}")
        aberto.append({
            "codigo": par["codigo"], "id": g["id"], "lado_do_gerado": lado["gerado"],
            "notas_gerado": e["notas"][lado["gerado"]],
            "notas_baseline": e["notas"][lado["baseline"]],
            "descreve_melhor": traduz(e["descreve_melhor"]),
            "publicaria": traduz(e["publicaria"]),
            "criterio_decisivo": e["criterio_decisivo"], "motivo": e["motivo"],
        })
    return erros, aberto


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--saidas", required=True, help="pasta com criterios_NN.json e ab_NN.json")
    ap.add_argument("--gabarito", required=True, help="o gabarito gravado por montar_painel.py")
    args = ap.parse_args()

    dossies = ler(os.path.join(PAINEL_DIR, "dossies.json"))
    cego = ler(os.path.join(PAINEL_DIR, "ab_cego.json"))
    gabarito = ler(args.gabarito)

    erros_c, criterios = conferir_criterios(juntar(args.saidas, "criterios"), dossies)
    erros_ab, ab = abrir_ab(juntar(args.saidas, "ab"), cego, gabarito)
    if erros_c or erros_ab:
        print(f"NÃO CONSOLIDADO: {len(erros_c) + len(erros_ab)} problema(s)")
        for e in erros_c + erros_ab:
            print(f"  - {e}")
        raise SystemExit(1)

    print("critérios:", len(criterios), "casos →", gravar("juiz_criterios.json", criterios))
    print("A/B:", len(ab), "pares →", gravar("juiz_ab.json", ab))
    print("gabarito do A/B publicado →", gravar("ab_gabarito.json", gabarito))


if __name__ == "__main__":
    main()
