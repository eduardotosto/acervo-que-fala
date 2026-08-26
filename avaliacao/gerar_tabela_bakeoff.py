"""Gera resultados/tabela_bakeoff.html — comparação CEGA Qwen × Gemma.

Para cada um dos 20 objetos: foto (clique abre resolução máxima) e os textos
dos dois redatores como "Texto A" e "Texto B", com lado sorteado por item
(seed fixa). O mapeamento fica em avaliacao/bakeoff_gabarito.json — não abrir
antes de julgar. Julgamento: responder no chat "#n: A", "#n: B" ou "#n: empate".

Uso:
    python avaliacao/gerar_tabela_bakeoff.py
"""
import json
import os
import random
import re
import sys

import requests

try:
    import truststore

    truststore.inject_into_ssl()
except ImportError:
    pass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import TAINACAN_BASE

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = """
:root { --terra:#8a4b2c; --terra-soft:#f3ddd0; --terra-ink:#341000; --indigo:#2f5d8f;
  --indigo-soft:#dfe9f4; --ocre:#7d6000; --ocre-soft:#f2e5ba;
  --bg:#f7f4ee; --card:#fbf9f4; --line:#d8cfc0; --ink:#231f18; --muted:#5c5546; }
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Google Sans Flex','Segoe UI',system-ui,sans-serif; background:var(--bg);
  color:var(--ink); line-height:1.55; padding:2.5rem 1.25rem 4rem; }
.wrap { max-width:1240px; margin:0 auto; }
h1 { font-weight:700; font-size:1.8rem; }
.resumo { background:var(--indigo-soft); border-radius:16px; padding:1rem 1.3rem;
  margin:1rem 0 2rem; font-size:.92rem; }
.card { background:var(--card); border:1px solid var(--line); border-radius:14px;
  margin-bottom:1.6rem; overflow:hidden; }
.topo { display:flex; align-items:baseline; gap:.6rem; padding:.9rem 1.2rem .4rem; flex-wrap:wrap; }
.num { font-weight:700; color:var(--terra); font-size:1.05rem; }
h2 { font-size:1.05rem; font-weight:600; display:inline; }
.tag { font-weight:600; font-size:.64rem; letter-spacing:.05em; text-transform:uppercase;
  background:var(--terra-soft); color:var(--terra-ink); padding:.15rem .5rem; border-radius:999px; }
.corpo { display:grid; grid-template-columns:minmax(240px,340px) 1fr 1fr; gap:0; }
@media (max-width:980px) { .corpo { grid-template-columns:1fr; } }
.foto { display:block; background:#e3ddd1; cursor:zoom-in; }
.foto img { display:block; width:100%; height:100%; max-height:480px; object-fit:contain; padding:.5rem; }
.col { padding:1rem 1.2rem 1.2rem; border-left:1px solid var(--line); }
.col h3 { font-size:.72rem; font-weight:700; letter-spacing:.12em; text-transform:uppercase;
  color:var(--indigo); margin-bottom:.5rem; }
.rot { font-size:.64rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase;
  color:var(--muted); margin:.6rem 0 .15rem; }
.alt { background:var(--indigo-soft); border-radius:8px; padding:.5rem .7rem; font-size:.9rem; }
.nivel2 { font-size:.85rem; color:var(--muted); }
.flag { background:var(--ocre-soft); color:var(--ocre); border-radius:8px;
  padding:.35rem .55rem; font-size:.76rem; margin-top:.3rem; }
"""


def melhor_imagem(det, sessao):
    html = det.get("document_as_html", "")
    m = re.search(r'<img[^>]+src="([^"]+)"', html)
    src = m.group(1) if m else ""
    m = re.search(r'<a[^>]+href="([^"]+\.(?:jpe?g|png|webp))"', html, re.IGNORECASE)
    cheia = m.group(1) if m else ""
    if not cheia and src:
        candidata = re.sub(r"-\d+x\d+(?=\.\w+$)", "", src)
        if candidata != src:
            try:
                if sessao.head(candidata, timeout=30).status_code == 200:
                    cheia = candidata
            except requests.RequestException:
                pass
    return src, (cheia or src)


def bloco(item):
    flags = "".join(
        f'<div class="flag">⚑ {f["tipo"]}: {f["detalhe"]}</div>' for f in item["flags"]
    ) or '<div class="nivel2" style="margin-top:.3rem">— sem flags</div>'
    nivel2 = item["descricao_objeto"].replace("\n\n", "<br><br>").replace("\n", "<br>")
    return (f'<div class="rot">Alt-text</div><div class="alt">{item["alt_text"]}</div>'
            f'<div class="rot">Descrição do objeto</div><div class="nivel2">{nivel2}</div>'
            f'<div class="rot">Flags</div>{flags}')


def main():
    with open(os.path.join(REPO, "resultados", "04_pipeline_completo_v5.json"), encoding="utf-8") as f:
        qwen = {i["id"]: i for i in json.load(f)["itens"]}
    with open(os.path.join(REPO, "resultados", "05_bakeoff_gemma.json"), encoding="utf-8") as f:
        gemma = {i["id"]: i for i in json.load(f)["itens"]}

    rng = random.Random(42)
    sessao = requests.Session()
    gabarito = {}
    cards = []
    for n, iid in enumerate(qwen, 1):
        det = sessao.get(f"{TAINACAN_BASE}/items/{iid}", timeout=60).json()
        src, cheia = melhor_imagem(det, sessao)
        q, g = qwen[iid], gemma[iid]
        qwen_e_a = rng.random() < 0.5
        a, b = (q, g) if qwen_e_a else (g, q)
        gabarito[str(iid)] = {"num": n, "A": "qwen" if qwen_e_a else "gemma",
                              "B": "gemma" if qwen_e_a else "qwen"}
        reg = q["registro"]
        cards.append(f"""
<div class="card" id="i{iid}">
  <div class="topo"><span class="num">#{n}</span> <h2>{q['titulo']}</h2>
    <span class="tag">{reg.get('Povo', '?')}</span><span class="tag">item {iid}</span></div>
  <div class="corpo">
    <a class="foto" href="{cheia}" target="_blank" rel="noopener" title="Abrir em resolução máxima">
      <img src="{src}" alt="{q['titulo']}" loading="lazy"></a>
    <div class="col"><h3>Texto A</h3>{bloco(a)}</div>
    <div class="col"><h3>Texto B</h3>{bloco(b)}</div>
  </div>
</div>""")

    html = f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bake-off cego — Qwen × Gemma</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@400;600;700&display=swap">
<style>{CSS}</style></head><body><div class="wrap">
<h1>Bake-off cego de redação — 20 objetos</h1>
<div class="resumo"><b>Comparação cega:</b> em cada card, os textos A e B vêm de dois modelos
diferentes, com o lado sorteado por objeto — nem a ordem se repete. <b>Julgue pelo texto</b>
(fidelidade à foto, clareza, as regras da rubrica) e responda no chat: "#1: A", "#2: empate"…
O gabarito só é aberto depois do seu julgamento. Clique na foto para a resolução máxima.</div>
{''.join(cards)}
</div></body></html>"""

    destino = os.path.join(REPO, "resultados", "tabela_bakeoff.html")
    with open(destino, "w", encoding="utf-8") as f:
        f.write(html)
    with open(os.path.join(REPO, "avaliacao", "bakeoff_gabarito.json"), "w", encoding="utf-8") as f:
        json.dump(gabarito, f, ensure_ascii=False, indent=2)
    print(f"OK: {destino} ({len(cards)} objetos) + gabarito guardado")


if __name__ == "__main__":
    main()
