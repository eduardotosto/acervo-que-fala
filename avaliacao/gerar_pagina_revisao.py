"""Gera avaliacao/candidatos.html — a página de revisão dos candidatos (E3).

Eduardo revisa visualmente (foto + registro + bordas propostas) e responde
no chat com os ajustes; casos.jsonl e holdout.jsonl são gerados a partir
das decisões dele.

Uso:
    python avaliacao/gerar_pagina_revisao.py
"""
import json
import os

AVAL_DIR = os.path.dirname(os.path.abspath(__file__))

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
.wrap { max-width:860px; margin:0 auto; }
h1 { font-weight:700; font-size:1.9rem; }
.instrucoes { background:var(--md-secondary-container); color:var(--md-on-secondary-container);
  border-radius:var(--shape-lg); padding:1.1rem 1.3rem; margin:1.2rem 0 2rem; font-size:.93rem; }
.instrucoes b { font-weight:700; }
.card { background:var(--md-surface-container-low); border-radius:var(--shape-lg);
  box-shadow:var(--elev1); margin-bottom:1.4rem; overflow:hidden; display:grid;
  grid-template-columns:220px 1fr; }
@media (max-width:640px) { .card { grid-template-columns:1fr; } }
.card img { width:100%; height:100%; max-height:280px; object-fit:contain;
  background:var(--md-surface-container-high); padding:.5rem; }
.corpo { padding:1rem 1.2rem 1.1rem; }
.num { font-weight:700; color:var(--md-primary); font-variant-numeric:tabular-nums; }
h2 { font-size:1.05rem; font-weight:600; display:inline; }
.tag { display:inline-block; font-weight:600; font-size:.66rem; letter-spacing:.05em;
  text-transform:uppercase; background:var(--md-primary-container); color:var(--md-on-primary-container);
  padding:.16rem .55rem; border-radius:var(--shape-full); margin-left:.35rem; vertical-align:middle; }
.tag.ancora { background:var(--md-secondary-container); color:var(--md-on-secondary-container); }
.meta { font-size:.78rem; color:var(--md-on-surface-variant); margin:.3rem 0 .6rem; }
.meta a { color:var(--md-secondary); }
.baseline { font-size:.85rem; background:var(--md-surface-container-high);
  border-radius:var(--shape-sm); padding:.55rem .75rem; margin-bottom:.55rem;
  color:var(--md-on-surface-variant); }
.borda { display:inline-block; font-size:.72rem; font-weight:600;
  background:var(--md-tertiary-container); color:var(--md-on-tertiary-container);
  padding:.14rem .5rem; border-radius:var(--shape-full); margin:0 .25rem .25rem 0; }
.criterios { font-size:.8rem; color:var(--md-on-surface-variant); margin-left:1.1rem; }
"""

INSTRUCOES = """
<b>Como revisar (responda no chat do Claude):</b><br>
1. <b>Trocar um item:</b> “trocar o 12” (sai da lista; o reserva da mesma categoria entra).<br>
2. <b>Marcar borda visual:</b> olhe a foto — “o 7 é foto_parcial”, “o 23 tem artefato_estudio”
   (cartela de cor, escala, suporte no quadro), “o 31 tem divergencia” (algo visível que o registro não cita).<br>
3. <b>Ajustar critérios:</b> “no 15, acrescentar critério X”.<br>
4. <b>Nada a mudar?</b> “aprovar todos” — os 10 do holdout serão sorteados entre os casos simples
   e a lista final vira <code>casos.jsonl</code> (40) + <code>holdout.jsonl</code> (10).<br>
As fotos vêm direto do servidor do museu — precisa de internet para vê-las.
"""


def main() -> None:
    with open(os.path.join(AVAL_DIR, "candidatos.json"), encoding="utf-8") as f:
        candidatos = json.load(f)

    cards = []
    for i, c in enumerate(candidatos, 1):
        bordas = "".join(f'<span class="borda">{b}</span>' for b in c["categorias_borda"])
        criterios = "".join(f"<li>{cr}</li>" for cr in c["criterios"])
        meta = " · ".join(f"{v}" for v in c["metadados_chave"].values())
        ancora = '<span class="tag ancora">smoke test</span>' if c["ancora_smoke_test"] else ""
        cards.append(f"""
<div class="card" id="c{i}">
  <img src="{c['imagem_url']}" alt="{c['titulo']} ({c['povo']})" loading="lazy">
  <div class="corpo">
    <span class="num">#{i}</span> <h2>{c['titulo']}</h2>
    <span class="tag">{c['povo']}</span><span class="tag">{c['categoria_objeto']}</span>{ancora}
    <div class="meta">{meta} · <a href="{c['url_acervo']}">ver no acervo</a> · item {c['item_id']}</div>
    <div class="baseline"><b>Descrição curatorial:</b> {c['baseline']}</div>
    <div>{bordas}</div>
    <ul class="criterios">{criterios}</ul>
  </div>
</div>""")

    html = f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Candidatos aos casos — E3</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@400;600;700&display=swap">
<style>{CSS}</style></head><body><div class="wrap">
<h1>Candidatos aos 50 casos de avaliação</h1>
<div class="instrucoes">{INSTRUCOES}</div>
{''.join(cards)}
</div></body></html>"""

    destino = os.path.join(AVAL_DIR, "candidatos.html")
    with open(destino, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK: {destino} ({len(candidatos)} candidatos)")


if __name__ == "__main__":
    main()
