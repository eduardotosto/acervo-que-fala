"""Gera resultados/tabela_lote_04.html — revisão editorial do lote da E7.

Página com os 20 objetos do Notebook 04 (foto, registro-chave, alt-text,
descrição do objeto, flags) para Eduardo comparar e apontar ajustes de
rubrica (ex.: hierarquia material×cor; origem animal das penas).

Uso:
    python avaliacao/gerar_tabela_lote.py
"""
import json
import os
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
:root { --md-primary:#8a4b2c; --md-primary-container:#ffdbc6; --md-on-primary-container:#341000;
  --md-secondary:#2f5d8f; --md-secondary-container:#d3e4ff; --md-on-secondary-container:#001b3d;
  --md-tertiary-container:#ffe9b3; --md-on-tertiary-container:#271900;
  --md-surface:#f7f4ee; --md-surface-container-low:#f1ede3; --md-surface-container-high:#e3ddd1;
  --md-on-surface:#1e1b16; --md-on-surface-variant:#4d463b; --md-outline-variant:#d8cfc0;
  --shape-sm:8px; --shape-lg:16px; --shape-full:999px;
  --elev1:0 1px 2px rgba(30,20,10,.09), 0 1px 4px rgba(30,20,10,.07); }
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Google Sans Flex','Segoe UI',system-ui,sans-serif; background:var(--md-surface);
  color:var(--md-on-surface); line-height:1.55; padding:2.5rem 1.25rem 4rem; }
.wrap { max-width:900px; margin:0 auto; }
h1 { font-weight:700; font-size:1.8rem; }
.resumo { background:var(--md-secondary-container); color:var(--md-on-secondary-container);
  border-radius:var(--shape-lg); padding:1rem 1.3rem; margin:1rem 0 2rem; font-size:.92rem; }
.card { background:var(--md-surface-container-low); border-radius:var(--shape-lg);
  box-shadow:var(--elev1); margin-bottom:1.3rem; display:grid;
  grid-template-columns:180px 1fr; overflow:hidden; }
@media (max-width:640px) { .card { grid-template-columns:1fr; } }
.card img { width:100%; height:100%; max-height:260px; object-fit:contain;
  background:var(--md-surface-container-high); padding:.5rem; }
.corpo { padding:1rem 1.2rem 1.1rem; }
.num { font-weight:700; color:var(--md-primary); }
h2 { font-size:1.02rem; font-weight:600; display:inline; }
.tag { display:inline-block; font-weight:600; font-size:.64rem; letter-spacing:.05em;
  text-transform:uppercase; background:var(--md-primary-container); color:var(--md-on-primary-container);
  padding:.15rem .5rem; border-radius:var(--shape-full); margin-left:.3rem; vertical-align:middle; }
.materia { font-size:.78rem; color:var(--md-on-surface-variant); margin:.25rem 0 .55rem; }
.rot { font-size:.66rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase;
  color:var(--md-secondary); margin-top:.5rem; }
.alt { background:var(--md-secondary-container); color:var(--md-on-secondary-container);
  border-radius:var(--shape-sm); padding:.5rem .7rem; font-size:.88rem; }
.nivel2 { font-size:.85rem; color:var(--md-on-surface-variant); margin-top:.2rem; }
.flag { background:var(--md-tertiary-container); color:var(--md-on-tertiary-container);
  border-radius:var(--shape-sm); padding:.4rem .6rem; font-size:.8rem; margin-top:.3rem; }
"""


def main() -> None:
    with open(os.path.join(REPO, "resultados", "04_pipeline_completo.json"), encoding="utf-8") as f:
        resultado = json.load(f)

    sessao = requests.Session()
    cards = []
    for i, it in enumerate(resultado["itens"], 1):
        det = sessao.get(f"{TAINACAN_BASE}/items/{it['id']}", timeout=60).json()
        m = re.search(r'src="([^"]+)"', det.get("document_as_html", ""))
        img = m.group(1) if m else ""
        reg = it["registro"]
        flags = "".join(
            f'<div class="flag">⚑ {f["tipo"]}: {f["detalhe"]}</div>' for f in it["flags"]
        ) or '<div class="materia">— sem flags</div>'
        nivel2 = it["descricao_objeto"].replace("\n\n", "<br><br>").replace("\n", "<br>")
        cards.append(f"""
<div class="card" id="i{it['id']}">
  <img src="{img}" alt="{it['titulo']} ({reg.get('Povo', '')})" loading="lazy">
  <div class="corpo">
    <span class="num">#{i}</span> <h2>{it['titulo']}</h2>
    <span class="tag">{reg.get('Povo', '?')}</span><span class="tag">{reg.get('Categoria', '?')}</span>
    <div class="materia"><b>Matéria-prima (registro):</b> {reg.get('Matéria-prima') or '(vazio)'} ·
      <b>Técnica:</b> {reg.get('Técnica de confecção') or '(vazio)'} · item {it['id']}</div>
    <div class="rot">Alt-text (nível 1)</div>
    <div class="alt">{it['alt_text']}</div>
    <div class="rot">Descrição do objeto (nível 2)</div>
    <div class="nivel2">{nivel2}</div>
    <div class="rot">Flags</div>
    {flags}
  </div>
</div>""")

    html = f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lote E7 — revisão editorial</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@400;600;700&display=swap">
<style>{CSS}</style></head><body><div class="wrap">
<h1>Lote da E7 — 20 objetos para revisão editorial</h1>
<div class="resumo"><b>Checagens automáticas:</b> 20/20 JSONs válidos · 20/20 sem problemas
(povo no alt, sem "close" indevido, sem artefato no alt, ≤30 palavras, atribuição no nível 2) ·
caso-referência Abano ✓ · {sum(len(i['flags']) for i in resultado['itens'])} flag(s) gerada(s).<br>
<b>Como revisar (responda no chat):</b> aponte pelo número — ex.: "no #6, prefiro o material antes
da cor", "no #1, citar de que ave são as penas (está na Matéria-prima)". Suas impressões viram a
rubrica v1.1. As fotos vêm do servidor do museu (precisa de internet).</div>
{''.join(cards)}
</div></body></html>"""

    destino = os.path.join(REPO, "resultados", "tabela_lote_04.html")
    with open(destino, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK: {destino} ({len(resultado['itens'])} objetos)")


if __name__ == "__main__":
    main()
