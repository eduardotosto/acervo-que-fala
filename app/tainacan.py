"""Coleta reprodutível do acervo digital do Museu do Índio (API pública do Tainacan).

Uso:
    python app/tainacan.py --n 60                  # amostra smoke
    python app/tainacan.py --n 500                 # dataset da PoC
    python app/tainacan.py --n 60 --baixar-imagens # também baixa as fotos p/ dados/imagens/

Saída:
    dados/itens.json         — um registro por item com imagem: id, título, URL,
                               URL da imagem e os metadados (nome do campo → valor)
    dados/estatisticas.json  — contagens para o relatório de inspeção (E2)
"""
import argparse
import json
import os
import re
import sys
import time

import requests

try:
    # No Windows, o Python não enxerga a cadeia de certificados gov.br via certifi;
    # truststore usa o repositório de certificados do sistema operacional.
    import truststore

    truststore.inject_into_ssl()
except ImportError:
    pass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import COLECAO_ID, DADOS_DIR, IMAGENS_DIR, TAINACAN_BASE

RE_IMG_SRC = re.compile(r'src="([^"]+)"')


def extrair_url_imagem(document_as_html: str) -> str | None:
    m = RE_IMG_SRC.search(document_as_html or "")
    return m.group(1) if m else None


def coletar(n: int, pausa: float, baixar_imagens: bool) -> list[dict]:
    sessao = requests.Session()
    itens, pagina, vistos = [], 1, set()
    while len(itens) < n:
        r = sessao.get(
            f"{TAINACAN_BASE}/collection/{COLECAO_ID}/items",
            params={"perpage": 96, "paged": pagina, "orderby": "modified", "order": "DESC"},
            timeout=60,
        )
        r.raise_for_status()
        lote = r.json().get("items", [])
        if not lote:
            break  # acabou o acervo antes de atingir n
        for it in lote:
            if len(itens) >= n:
                break
            if it.get("document_type") != "attachment" or it["id"] in vistos:
                continue  # borda: item sem imagem (≈27% do acervo) ou repetido
            vistos.add(it["id"])
            imagem = extrair_url_imagem(it.get("document_as_html"))
            if not imagem:
                det = sessao.get(f"{TAINACAN_BASE}/items/{it['id']}", timeout=60).json()
                imagem = extrair_url_imagem(det.get("document_as_html"))
            if not imagem:
                continue
            meta_raw = sessao.get(
                f"{TAINACAN_BASE}/item/{it['id']}/metadata", timeout=60
            ).json()
            metadados = {
                m["metadatum"]["name"]: m["value_as_string"]
                for m in meta_raw
                if m.get("value_as_string")
            }
            itens.append(
                {
                    "id": it["id"],
                    "titulo": it["title"],
                    "url": it["url"],
                    "imagem_url": imagem,
                    "metadados": metadados,
                }
            )
            if baixar_imagens:
                os.makedirs(IMAGENS_DIR, exist_ok=True)
                destino = os.path.join(IMAGENS_DIR, f"{it['id']}.jpg")
                if not os.path.exists(destino):
                    img = sessao.get(imagem, timeout=90)
                    img.raise_for_status()
                    with open(destino, "wb") as f:
                        f.write(img.content)
            if len(itens) % 20 == 0:
                print(f"  {len(itens)}/{n} itens coletados...")
            time.sleep(pausa)
        pagina += 1
    return itens


def estatisticas(itens: list[dict]) -> dict:
    def contar(campo: str) -> dict:
        contagem: dict[str, int] = {}
        for it in itens:
            v = it["metadados"].get(campo, "(vazio)")
            contagem[v] = contagem.get(v, 0) + 1
        return dict(sorted(contagem.items(), key=lambda kv: -kv[1]))

    return {
        "total": len(itens),
        "com_descricao_curatorial": sum(
            1 for it in itens if it["metadados"].get("Descrição")
        ),
        "por_categoria": contar("Categoria"),
        "por_povo": contar("Povo"),
        "por_estado": contar("Estado de origem"),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, default=300, help="itens com imagem a coletar")
    ap.add_argument("--pausa", type=float, default=0.25, help="segundos entre chamadas")
    ap.add_argument("--baixar-imagens", action="store_true")
    args = ap.parse_args()

    os.makedirs(DADOS_DIR, exist_ok=True)
    print(f"Coletando {args.n} itens da coleção {COLECAO_ID}...")
    itens = coletar(args.n, args.pausa, args.baixar_imagens)

    with open(os.path.join(DADOS_DIR, "itens.json"), "w", encoding="utf-8") as f:
        json.dump(itens, f, ensure_ascii=False, indent=2)
    stats = estatisticas(itens)
    with open(os.path.join(DADOS_DIR, "estatisticas.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"OK: {stats['total']} itens em {DADOS_DIR}/itens.json")
    print(f"    com descrição curatorial: {stats['com_descricao_curatorial']}")
    print(f"    categorias distintas: {len(stats['por_categoria'])}")
    print(f"    povos distintos: {len(stats['por_povo'])}")


if __name__ == "__main__":
    main()
