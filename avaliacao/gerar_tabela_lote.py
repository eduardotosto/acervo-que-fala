"""Gera resultados/tabela_lote_04.html — revisão editorial do lote da E7.

Página com os 20 objetos do Notebook 04: foto grande (clique abre a
resolução máxima no servidor do museu), alt-text e descrição do objeto
lado a lado, flags e matéria-prima do registro. Serve para Eduardo
comparar texto × imagem e apontar ajustes de rubrica.

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
.wrap { max-width:1180px; margin:0 auto; }
h1 { font-weight:700; font-size:1.8rem; }
.resumo { background:var(--md-secondary-container); color:var(--md-on-secondary-container);
  border-radius:var(--shape-lg); padding:1rem 1.3rem; margin:1rem 0 2rem; font-size:.92rem; }
.card { background:var(--md-surface-container-low); border-radius:var(--shape-lg);
  box-shadow:var(--elev1); margin-bottom:1.6rem; display:grid;
  grid-template-columns:minmax(320px, 480px) 1fr; overflow:hidden; }
@media (max-width:860px) { .card { grid-template-columns:1fr; } }
.foto { display:block; background:var(--md-surface-container-high); cursor:zoom-in; }
.foto img { display:block; width:100%; height:100%; max-height:560px; object-fit:contain; padding:.6rem; }
.corpo { padding:1.15rem 1.4rem 1.25rem; }
.num { font-weight:700; color:var(--md-primary); font-size:1.05rem; }
h2 { font-size:1.1rem; font-weight:600; display:inline; }
.tag { display:inline-block; font-weight:600; font-size:.64rem; letter-spacing:.05em;
  text-transform:uppercase; background:var(--md-primary-container); color:var(--md-on-primary-container);
  padding:.15rem .5rem; border-radius:var(--shape-full); margin-left:.3rem; vertical-align:middle; }
.materia { font-size:.78rem; color:var(--md-on-surface-variant); margin:.3rem 0 .6rem; }
.rot { font-size:.66rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase;
  color:var(--md-secondary); margin:.65rem 0 .2rem; }
.alt { background:var(--md-secondary-container); color:var(--md-on-secondary-container);
  border-radius:var(--shape-sm); padding:.55rem .75rem; font-size:.95rem; }
.nivel2 { font-size:.9rem; color:var(--md-on-surface-variant); }
.flag { background:var(--md-tertiary-container); color:var(--md-on-tertiary-container);
  border-radius:var(--shape-sm); padding:.4rem .6rem; font-size:.8rem; margin-top:.3rem; }
"""


def melhor_imagem(det: dict, sessao: requests.Session) -> tuple[str, str]:
    """Retorna (url_exibicao, url_resolucao_maxima) para o item."""
    html = det.get("document_as_html", "")
    src = ""
    m = re.search(r'<img[^>]+src="([^"]+)"', html)
    if m:
        src = m.group(1)
    cheia = ""
    m = re.search(r'<a[^>]+href="([^"]+\.(?:jpe?g|png|webp))"', html, re.IGNORECASE)
    if m:
        cheia = m.group(1)
    if not cheia and src:
        candidata = re.sub(r"-\d+x\d+(?=\.\w+$)", "", src)
        if candidata != src:
            try:
                r = sessao.head(candidata, timeout=30)
                if r.status_code == 200:
                    cheia = candidata
            except requests.RequestException:
                pass
    return src, (cheia or src)


def main() -> None:
    with open(os.path.join(REPO, "resultados", "04_pipeline_completo.json"), encoding="utf-8") as f:
        resultado = json.load(f)

    sessao = requests.Session()
    cards = []
    for i, it in enumerate(resultado["itens"], 1):
        det = sessao.get(f"{TAINACAN_BASE}/items/{it['id']}", timeout=60).json()
        src, cheia = melhor_imagem(det, sessao)
        reg = it["registro"]
        flags = "".join(
            f'<div class="flag">⚑ {f["tipo"]}: {f["detalhe"]}</div>' for f in it["flags"]
        ) or '<div class="materia">— sem flags</div>'
        nivel2 = it["descricao_objeto"].replace("\n\n", "<br><br>").replace("\n", "<br>")
        cards.append(f"""
<div class="card" id="i{it['id']}">
  <a class="foto" href="{cheia}" target="_blank" rel="noopener"
     title="Abrir em resolução máxima">
    <img src="{src}" alt="{it['titulo']} ({reg.get('Povo', '')})" loading="lazy"></a>
  <div class="corpo">
    <span class="num">#{i}</span> <h2>{it['titulo']}</h2>
    <span class="tag">{reg.get('Povo', '?')}</span><span class="tag">{reg.get('Categoria', '?')}</span>
    <div class="materia"><b>Matéria-prima (registro):</b> {reg.get('Matéria-prima') or '(vazio)'} · item {it['id']}</div>
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
<div class="resumo"><b>Clique na foto para abrir em resolução máxima</b> (numa nova aba, direto do
servidor do museu).<br>
<b>Como revisar (responda no chat, pelo número):</b> 1) o alt mente ou esconde algo que a foto
mostra? 2) o nível 2 respeita o registro? 3) preferências editoriais — ex.: "no #20, material antes
da cor", "no #6, citar a arara no alt". Suas impressões viram a rubrica v1.1.</div>
{''.join(cards)}
</div></body></html>"""

    destino = os.path.join(REPO, "resultados", "tabela_lote_04.html")
    with open(destino, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK: {destino} ({len(resultado['itens'])} objetos)")


if __name__ == "__main__":
    main()
