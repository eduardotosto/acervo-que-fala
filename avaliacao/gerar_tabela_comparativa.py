"""Gera resultados/tabela_comparativa.html — os 20 objetos, lado a lado, em três sistemas.

Para cada objeto: a foto (clique abre resolução máxima), a descrição curatorial que o
museu usa hoje (o baseline do projeto) e, em três colunas, o alt-text, a descrição do
objeto e as flags de cada lote — v5 (Qwen, sistema antigo), v6 (Qwen, sistema
redesenhado) e o Gemma do bake-off. Os problemas de cada texto vêm de
avaliacao/checar_lote.py, a mesma régua nos três.

Uso:
    python avaliacao/gerar_tabela_comparativa.py
"""
import html
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

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "avaliacao"))
from app.config import TAINACAN_BASE
import checar_lote as CL

LOTES = [
    ("v5", "Qwen · sistema antigo", "resultados/04_pipeline_completo_v5.json",
     "prompt v8, 25 regras no mesmo contexto"),
    ("v6", "Qwen · sistema redesenhado", "resultados/04_pipeline_completo_v6.json",
     "observação v3 em seções + contrato de fontes + garantias em código"),
    ("gemma", "Gemma 3 12B · bake-off", "resultados/05_bakeoff_gemma.json",
     "mesmo prompt v8 do v5, redator diferente"),
    ("v7", "Qwen · v7 (correções medidas no v6)", "resultados/04_pipeline_completo_v7.json",
     "varredura de artefatos + escala/plausibilidade em código + marca de atribuição variada"),
]

CSS = """
:root { --terra:#8a4b2c; --terra-soft:#f3ddd0; --terra-ink:#341000; --indigo:#2f5d8f;
  --indigo-soft:#dfe9f4; --ocre:#7d6000; --ocre-soft:#f2e5ba; --erro:#8c2f2f;
  --erro-soft:#f6dcdc; --ok:#2b6b45; --ok-soft:#d9ecdf;
  --bg:#f7f4ee; --card:#fbf9f4; --line:#d8cfc0; --ink:#231f18; --muted:#5c5546; }
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Google Sans Flex','Segoe UI',system-ui,sans-serif; background:var(--bg);
  color:var(--ink); line-height:1.55; padding:2.2rem 1.25rem 4rem; }
.wrap { max-width:1900px; margin:0 auto; }
h1 { font-weight:700; font-size:1.8rem; }
.resumo { background:var(--indigo-soft); border-radius:16px; padding:1rem 1.3rem;
  margin:1rem 0 1.2rem; font-size:.92rem; }
.placar { display:flex; gap:.8rem; flex-wrap:wrap; margin:.8rem 0 0; }
.placar div { background:var(--card); border:1px solid var(--line); border-radius:12px;
  padding:.5rem .9rem; font-size:.85rem; }
.placar b { font-size:1.15rem; color:var(--terra); }
.controles { position:sticky; top:0; z-index:5; background:var(--bg); padding:.7rem 0 1rem;
  border-bottom:1px solid var(--line); margin-bottom:1.4rem; font-size:.85rem;
  display:flex; gap:1.1rem; flex-wrap:wrap; align-items:center; }
.controles label { cursor:pointer; user-select:none; }
.card { background:var(--card); border:1px solid var(--line); border-radius:14px;
  margin-bottom:1.6rem; overflow:hidden; }
.topo { display:flex; align-items:baseline; gap:.6rem; padding:.9rem 1.2rem .5rem; flex-wrap:wrap; }
.num { font-weight:700; color:var(--terra); font-size:1.05rem; }
h2 { font-size:1.05rem; font-weight:600; display:inline; }
.tag { font-weight:600; font-size:.64rem; letter-spacing:.05em; text-transform:uppercase;
  background:var(--terra-soft); color:var(--terra-ink); padding:.15rem .5rem; border-radius:999px; }
.corpo { display:grid; grid-template-columns:minmax(200px,270px) repeat(4,1fr); gap:0; }
@media (max-width:1200px) { .corpo { grid-template-columns:1fr 1fr; } }
@media (max-width:760px) { .corpo { grid-template-columns:1fr; } }
.esq { padding:.4rem .6rem 1rem; }
.foto { display:block; background:#e3ddd1; cursor:zoom-in; border-radius:10px; overflow:hidden; }
.foto img { display:block; width:100%; max-height:340px; object-fit:contain; padding:.4rem; }
.base { margin-top:.7rem; font-size:.8rem; color:var(--muted); }
.base b { color:var(--ink); font-size:.68rem; letter-spacing:.1em; text-transform:uppercase;
  display:block; margin-bottom:.2rem; }
.escala { margin-top:.6rem; font-size:.75rem; color:var(--indigo); }
.col { padding:.9rem 1.1rem 1.2rem; border-left:1px solid var(--line); }
.col h3 { font-size:.72rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase;
  color:var(--indigo); margin-bottom:.5rem; }
.rot { font-size:.62rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase;
  color:var(--muted); margin:.7rem 0 .15rem; }
.alt { background:var(--indigo-soft); border-radius:8px; padding:.5rem .7rem; font-size:.87rem; }
.nivel2 { font-size:.83rem; color:var(--muted); }
.flag { background:var(--ocre-soft); color:var(--ocre); border-radius:8px;
  padding:.3rem .5rem; font-size:.74rem; margin-top:.25rem; }
.probs { margin-top:.6rem; display:flex; gap:.3rem; flex-wrap:wrap; }
.chip { background:var(--erro-soft); color:var(--erro); border-radius:999px;
  padding:.12rem .5rem; font-size:.68rem; font-weight:600; }
.limpo { background:var(--ok-soft); color:var(--ok); border-radius:999px;
  padding:.12rem .5rem; font-size:.68rem; font-weight:600; }
.oculto { display:none; }
"""


def melhor_imagem(det, sessao):
    doc = det.get("document_as_html", "")
    m = re.search(r'<img[^>]+src="([^"]+)"', doc)
    src = m.group(1) if m else ""
    m = re.search(r'<a[^>]+href="([^"]+\.(?:jpe?g|png|webp))"', doc, re.IGNORECASE)
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


def e(texto):
    return html.escape(str(texto or ""))


def coluna(chave, item):
    """Uma coluna do card: alt, nível 2, flags e os problemas da régua única."""
    if item is None:
        return f'<div class="col {chave}"><h3>—</h3><div class="nivel2">lote sem este item</div></div>'
    problemas = CL.verificar(item)
    chips = "".join(f'<span class="chip" title="{e(v)}">{e(k)}</span>' for k, v in problemas) \
        or '<span class="limpo">sem problemas</span>'
    flags = "".join(f'<div class="flag">⚑ {e(f.get("tipo"))}: {e(f.get("detalhe"))}</div>'
                    for f in (item.get("flags") or [])) \
        or '<div class="nivel2" style="margin-top:.25rem">— sem flags</div>'
    nivel2 = e(item.get("descricao_objeto", "")).replace("\n\n", "<br><br>").replace("\n", "<br>")
    bruto = ""
    if item.get("alt_bruto") and item["alt_bruto"] != item["alt_text"]:
        bruto = (f'<div class="rot">Alt bruto (antes do pós-processamento)</div>'
                 f'<div class="nivel2">{e(item["alt_bruto"])}</div>')
    return (f'<div class="col {chave}">'
            f'<h3>{e(TITULOS[chave])}</h3>'
            f'<div class="probs">{chips}</div>'
            f'<div class="rot">Alt-text · {len(item.get("alt_text", "").split())} palavras</div>'
            f'<div class="alt">{e(item.get("alt_text"))}</div>{bruto}'
            f'<div class="rot">Descrição do objeto · '
            f'{len(item.get("descricao_objeto", "").split())} palavras</div>'
            f'<div class="nivel2">{nivel2}</div>'
            f'<div class="rot">Flags</div>{flags}</div>')


TITULOS = {chave: rotulo for chave, rotulo, _, _ in LOTES}


def main():
    lotes = {}
    for chave, _, caminho, _ in LOTES:
        with open(os.path.join(REPO, caminho), encoding="utf-8") as f:
            lotes[chave] = {i["id"]: i for i in json.load(f)["itens"]}

    limpos = {}
    for chave, itens in lotes.items():
        limpos[chave] = sum(1 for it in itens.values() if not CL.verificar(
            it if it.get("escala") else dict(it, escala=CL.analisar_registro(it["registro"])[0])))

    sessao = requests.Session()
    ordem = list(lotes["v7"])
    cards = []
    for n, iid in enumerate(ordem, 1):
        det = sessao.get(f"{TAINACAN_BASE}/items/{iid}", timeout=60).json()
        src, cheia = melhor_imagem(det, sessao)
        ref = lotes["v7"][iid]
        reg = ref["registro"]
        escala = CL.analisar_registro(reg)[0]
        colunas = ""
        for chave, _, _, _ in LOTES:
            it = lotes[chave].get(iid)
            if it is not None and not it.get("escala"):
                it = dict(it, escala=escala)
            colunas += coluna(chave, it)
        cards.append(f"""
<div class="card" id="i{iid}">
  <div class="topo"><span class="num">#{n}</span> <h2>{e(ref['titulo'])}</h2>
    <span class="tag">{e(reg.get('Povo', '?'))}</span>
    <span class="tag">{e(reg.get('Categoria', '?'))}</span>
    <span class="tag">item {iid}</span></div>
  <div class="corpo">
    <div class="esq">
      <a class="foto" href="{e(cheia)}" target="_blank" rel="noopener" title="Abrir em resolução máxima">
        <img src="{e(src)}" alt="{e(ref['titulo'])}" loading="lazy"></a>
      <div class="base"><b>Baseline — descrição curatorial</b>{e(reg.get('Descrição') or '(o registro não traz descrição)')}</div>
      <div class="escala">Escala calculada do registro: {e(escala)}</div>
    </div>{colunas}
  </div>
</div>""")
        print(f"  [{n}/{len(ordem)}] {ref['titulo']}")

    placar = "".join(
        f"<div><b>{limpos[chave]}/{len(lotes[chave])}</b> sem problemas<br>{e(rotulo)}"
        f"<br><span style='font-size:.76rem;color:var(--muted)'>{e(nota)}</span></div>"
        for chave, rotulo, _, nota in LOTES)
    toggles = "".join(
        f'<label><input type="checkbox" checked data-col="{chave}"> {e(rotulo)}</label>'
        for chave, rotulo, _, _ in LOTES)

    html_final = f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Comparativo por objeto — v5 × v6 × Gemma</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@400;600;700&display=swap">
<style>{CSS}</style></head><body><div class="wrap">
<h1>Comparativo por objeto — alt-text e descrição do objeto</h1>
<div class="resumo">Os mesmos 20 objetos em três sistemas. <b>v5</b> e <b>v6</b> usam o mesmo modelo
(Qwen3-VL-8B): a diferença entre as duas colunas é só o sistema de instruções. O <b>Gemma</b> rodou
o prompt antigo, e está aqui como referência do bake-off. As etiquetas vermelhas são os problemas
apontados por <code>avaliacao/checar_lote.py</code> — a mesma régua nos três lotes; passe o mouse
para ver o detalhe. Clique na foto para a resolução máxima.
<div class="placar">{placar}</div></div>
<div class="controles"><span>Mostrar:</span>{toggles}</div>
{''.join(cards)}
</div>
<script>
document.querySelectorAll('.controles input').forEach(cb => cb.addEventListener('change', () => {{
  document.querySelectorAll('.col.' + cb.dataset.col).forEach(c => c.classList.toggle('oculto', !cb.checked));
}}));
</script>
</body></html>"""

    destino = os.path.join(REPO, "resultados", "tabela_comparativa.html")
    with open(destino, "w", encoding="utf-8") as f:
        f.write(html_final)
    print(f"\nOK: {destino} ({len(cards)} objetos) | sem problemas: " +
          ", ".join(f"{c} {limpos[c]}/20" for c, _, _, _ in LOTES))


if __name__ == "__main__":
    main()
