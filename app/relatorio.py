"""Gera dados/relatorio_coleta.md a partir de dados/itens.json (etapa E2).

Uso:
    python app/relatorio.py

O relatório responde: o dataset está equilibrado o suficiente para amostrar
os 50 casos de avaliação? Quais campos de metadados são confiáveis (presentes
em quase todos os itens) e quais são raros?
"""
import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import DADOS_DIR

CAMPOS_CHAVE = [
    "Descrição", "Povo", "Categoria", "Matéria-prima", "Técnica de confecção",
    "Dimensões", "Função", "Estado de origem", "Ano de aquisição do objeto",
    "Autoidentificação", "Nome étnico do item",
]


def tabela(contagem: dict, total: int, top: int = 15) -> list[str]:
    linhas = ["| Valor | Itens | % |", "|---|---:|---:|"]
    for valor, qtd in list(contagem.items())[:top]:
        linhas.append(f"| {valor} | {qtd} | {qtd / total:.0%} |")
    resto = sum(list(contagem.values())[top:])
    if resto:
        linhas.append(f"| *(outros {len(contagem) - top} valores)* | {resto} | {resto / total:.0%} |")
    return linhas


def main() -> None:
    with open(os.path.join(DADOS_DIR, "itens.json"), encoding="utf-8") as f:
        itens = json.load(f)
    total = len(itens)

    def contar(campo: str) -> dict:
        c: dict[str, int] = {}
        for it in itens:
            v = it["metadados"].get(campo, "(vazio)")
            c[v] = c.get(v, 0) + 1
        return dict(sorted(c.items(), key=lambda kv: -kv[1]))

    presenca = {
        campo: sum(1 for it in itens if it["metadados"].get(campo))
        for campo in CAMPOS_CHAVE
    }
    todos_campos: dict[str, int] = {}
    for it in itens:
        for campo in it["metadados"]:
            todos_campos[campo] = todos_campos.get(campo, 0) + 1

    por_categoria = contar("Categoria")
    por_povo = contar("Povo")
    maior_cat = max(por_categoria.values()) / total

    desc_tamanhos = sorted(
        len(it["metadados"].get("Descrição", "")) for it in itens
    )
    mediana_desc = desc_tamanhos[total // 2]

    L: list[str] = []
    L.append(f"# Relatório de inspeção do dataset — E2 ({date.today().isoformat()})")
    L.append("")
    L.append(f"**{total} itens** com imagem e metadados, coletados da coleção pública do "
             f"Museu do Índio (Tainacan). Gerado por `python app/relatorio.py`.")
    L.append("")
    L.append("## Presença dos campos-chave")
    L.append("")
    L.append("| Campo | Presente | % |")
    L.append("|---|---:|---:|")
    for campo, qtd in sorted(presenca.items(), key=lambda kv: -kv[1]):
        L.append(f"| {campo} | {qtd}/{total} | {qtd / total:.0%} |")
    L.append("")
    L.append(f"Descrição curatorial (a baseline): mediana de **{mediana_desc} caracteres**; "
             f"menor {desc_tamanhos[0]}, maior {desc_tamanhos[-1]}.")
    L.append("")
    L.append("## Distribuição por categoria")
    L.append("")
    L.extend(tabela(por_categoria, total))
    L.append("")
    verif = "✅ ok" if maior_cat <= 0.5 else "⚠️ categoria dominante acima de 50% — estratificar a amostra dos casos"
    L.append(f"**Verificação da E2** (nenhuma categoria >50%): maior categoria = {maior_cat:.0%} → {verif}")
    L.append("")
    L.append("## Distribuição por povo")
    L.append("")
    L.extend(tabela(por_povo, total))
    L.append("")
    L.append(f"Povos distintos: **{len(por_povo)}** · Estados: **{len(contar('Estado de origem'))}**")
    L.append("")
    L.append("## Campos raros (presentes em <10% dos itens)")
    L.append("")
    raros = {c: q for c, q in sorted(todos_campos.items(), key=lambda kv: kv[1])
             if q / total < 0.10}
    if raros:
        L.append(", ".join(f"{c} ({q})" for c, q in raros.items()))
    else:
        L.append("Nenhum.")
    L.append("")

    destino = os.path.join(DADOS_DIR, "relatorio_coleta.md")
    with open(destino, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"OK: {destino}")
    print(f"    categorias: {len(por_categoria)} (maior: {maior_cat:.0%})")
    print(f"    povos: {len(por_povo)}")


if __name__ == "__main__":
    main()
