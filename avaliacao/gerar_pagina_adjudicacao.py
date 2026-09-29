"""Gera avaliacao/painel/adjudicacao.html — a página em que o Eduardo adjudica o juiz (E10).

O juiz aponta, o Eduardo decide. Cada item traz a foto, os textos gerados, o que o juiz
disse e a evidência; a decisão é concordo, discordo ou parcial, com nota opcional. A
numeração é a mesma de relatorio_juiz.md.

As decisões ficam guardadas no navegador a cada clique. No fim, o botão "Baixar" gera
adjudicacao.json, que vai para avaliacao/painel/.

Uso:
    python avaliacao/gerar_pagina_adjudicacao.py
"""
import html
import json
import os

from gerar_relatorio_juiz import CAMADA, PAINEL_DIR, TEXTO, itens_para_adjudicar, ler

CSS = """
:root { --md-primary:#8a4b2c; --md-primary-container:#ffdbc6; --md-on-primary-container:#341000;
  --md-secondary:#2f5d8f; --md-secondary-container:#d3e4ff; --md-on-secondary-container:#001b3d;
  --md-tertiary-container:#ffe9b3; --md-on-tertiary-container:#271900;
  --md-surface:#f7f4ee; --md-surface-container-low:#f1ede3; --md-surface-container-high:#e3ddd1;
  --md-on-surface:#1e1b16; --md-on-surface-variant:#4d463b; --md-outline-variant:#d8cfc0;
  --ok:#2b6b45; --erro:#8c2f2f; --meio:#7d6000;
  --shape-sm:8px; --shape-lg:16px; --shape-full:999px;
  --elev1:0 1px 2px rgba(30,20,10,.09), 0 1px 4px rgba(30,20,10,.07); }
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Google Sans Flex','Segoe UI',system-ui,sans-serif; background:var(--md-surface);
  color:var(--md-on-surface); line-height:1.55; padding:0 1.25rem 5rem; }
.wrap { max-width:980px; margin:0 auto; }
header.topo { position:sticky; top:0; z-index:5; background:var(--md-surface);
  padding:1rem 0 .8rem; border-bottom:1px solid var(--md-outline-variant); margin-bottom:1.5rem;
  display:flex; gap:1rem; align-items:center; flex-wrap:wrap; }
h1 { font-weight:700; font-size:1.25rem; flex:1 1 16rem; }
.progresso { font-weight:600; font-variant-numeric:tabular-nums; color:var(--md-primary); }
button { font:inherit; font-weight:600; border:0; cursor:pointer; border-radius:var(--shape-full);
  padding:.5rem 1.1rem; background:var(--md-secondary); color:#fff; }
button.leve { background:var(--md-surface-container-high); color:var(--md-on-surface); }
.aviso { background:var(--md-tertiary-container); color:var(--md-on-tertiary-container);
  border-radius:var(--shape-lg); padding:.8rem 1.3rem; margin-bottom:1rem; font-size:.93rem;
  font-weight:600; }
.instrucoes { background:var(--md-secondary-container); color:var(--md-on-secondary-container);
  border-radius:var(--shape-lg); padding:1rem 1.3rem; margin-bottom:2rem; font-size:.93rem; }
section.caso { background:var(--md-surface-container-low); border-radius:var(--shape-lg);
  box-shadow:var(--elev1); margin-bottom:1.6rem; overflow:hidden; }
.cabeca { display:grid; grid-template-columns:300px 1fr; }
@media (max-width:720px) { .cabeca { grid-template-columns:1fr; } }
.cabeca img { width:100%; max-height:340px; object-fit:contain;
  background:var(--md-surface-container-high); padding:.5rem; display:block; }
.textos { padding:1rem 1.2rem; min-width:0; }
h2 { font-size:1.05rem; font-weight:600; }
.meta { font-size:.78rem; color:var(--md-on-surface-variant); margin:.15rem 0 .7rem; }
.rotulo { font-size:.68rem; font-weight:700; letter-spacing:.05em; text-transform:uppercase;
  color:var(--md-secondary); margin-top:.6rem; }
.texto { font-size:.9rem; }
details { font-size:.82rem; color:var(--md-on-surface-variant); margin-top:.6rem; }
summary { cursor:pointer; font-weight:600; }
details pre { white-space:pre-wrap; font:inherit; margin-top:.4rem; }
.item { border-top:1px solid var(--md-outline-variant); padding:1rem 1.2rem; }
.item.decidido { background:var(--md-surface-container-high); }
.num { font-weight:700; color:var(--md-primary); font-variant-numeric:tabular-nums; }
.tag { display:inline-block; font-weight:600; font-size:.66rem; letter-spacing:.05em;
  text-transform:uppercase; background:var(--md-primary-container); color:var(--md-on-primary-container);
  padding:.16rem .55rem; border-radius:var(--shape-full); margin-left:.35rem; vertical-align:middle; }
.tag.conferir { background:var(--md-tertiary-container); color:var(--md-on-tertiary-container); }
.achado { font-size:.95rem; margin:.35rem 0; }
.evidencia { font-size:.85rem; color:var(--md-on-surface-variant); }
fieldset { border:0; display:flex; gap:.5rem; flex-wrap:wrap; align-items:center; margin-top:.7rem; }
legend { font-size:.68rem; font-weight:700; letter-spacing:.05em; text-transform:uppercase;
  color:var(--md-on-surface-variant); margin-bottom:.3rem; }
fieldset label { border:1.5px solid var(--md-outline-variant); border-radius:var(--shape-full);
  padding:.3rem .9rem; font-size:.85rem; font-weight:600; cursor:pointer; }
fieldset input[type=radio] { position:absolute; opacity:0; }
fieldset input:focus-visible + span { outline:2px solid var(--md-secondary); outline-offset:4px; }
label.concordo:has(input:checked) { background:var(--ok); border-color:var(--ok); color:#fff; }
label.discordo:has(input:checked) { background:var(--erro); border-color:var(--erro); color:#fff; }
label.parcial:has(input:checked) { background:var(--meio); border-color:var(--meio); color:#fff; }
input.nota { flex:1 1 14rem; font:inherit; font-size:.85rem; padding:.35rem .7rem;
  border:1.5px solid var(--md-outline-variant); border-radius:var(--shape-sm); background:#fff; }
"""

JS = """
const CHAVE = 'acervo-que-fala-adjudicacao-2026-09-29';
let estado = {};
let guardando = true;  // navegador com armazenamento bloqueado: a página segue, e avisa
try { estado = JSON.parse(localStorage.getItem(CHAVE) || '{}'); } catch (erro) { guardando = false; }
const total = document.querySelectorAll('.item').length;

function pintar() {
  let feitos = 0;
  document.querySelectorAll('.item').forEach(el => {
    const d = estado[el.dataset.numero];
    const decidido = !!(d && d.decisao);
    el.classList.toggle('decidido', decidido);
    if (decidido) feitos++;
  });
  document.getElementById('progresso').textContent = feitos + ' de ' + total + ' decididos';
  document.getElementById('aviso').hidden = guardando;
}

document.querySelectorAll('.item').forEach(el => {
  const n = el.dataset.numero;
  const d = estado[n] || {};
  el.querySelectorAll('input[type=radio]').forEach(r => {
    r.checked = d.decisao === r.value;
    r.addEventListener('change', () => guardar(n, {decisao: r.value}));
  });
  const nota = el.querySelector('input.nota');
  nota.value = d.nota || '';
  nota.addEventListener('input', () => guardar(n, {nota: nota.value}));
});

function guardar(n, mudanca) {
  estado[n] = Object.assign({}, estado[n], mudanca);
  try { localStorage.setItem(CHAVE, JSON.stringify(estado)); } catch (erro) { guardando = false; }
  pintar();
}

function resultado() {
  const itens = [];
  document.querySelectorAll('.item').forEach(el => {
    const d = estado[el.dataset.numero] || {};
    itens.push({numero: Number(el.dataset.numero), id: Number(el.dataset.id), tipo: el.dataset.tipo,
                decisao: d.decisao || null, nota: d.nota || ''});
  });
  return JSON.stringify({adjudicado_por: 'Eduardo Tosto', data: new Date().toISOString().slice(0, 10),
                         itens: itens}, null, 2);
}

document.getElementById('baixar').addEventListener('click', () => {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([resultado()], {type: 'application/json'}));
  a.download = 'adjudicacao.json';
  a.click();
});
document.getElementById('copiar').addEventListener('click', async () => {
  await navigator.clipboard.writeText(resultado());
  document.getElementById('copiar').textContent = 'Copiado';
});
pintar();
"""

INSTRUCOES = """
<b>Como adjudicar.</b> Cada item é algo que o juiz apontou. Olhe a foto, leia os textos e decida:
<b>concordo</b> (o juiz tem razão), <b>discordo</b> (o juiz errou) ou <b>parcial</b> (tem razão em
parte — diga em quê na nota). A nota é opcional. As decisões ficam guardadas neste navegador a cada
clique: dá para fechar a página e voltar. No fim, <b>Baixar</b> gera <code>adjudicacao.json</code>
— salve em <code>avaliacao/painel/</code> ou cole o conteúdo no chat do Claude.
As fotos vêm direto do servidor do museu: precisa de internet.
"""

e = html.escape


def bloco_item(it):
    if it["tipo"] == "achado_grave":
        tag = '<span class="tag">gravidade alta</span>'
        corpo = (f'<p class="achado">{e(it["descricao"])}</p>'
                 f'<p class="evidencia"><b>Onde:</b> {TEXTO.get(it["texto"], it["texto"])} · '
                 f'<b>camada:</b> {CAMADA[it["camada"]]}<br><b>Evidência:</b> {e(it["evidencia"])}</p>')
    else:
        tag = '<span class="tag conferir">pede olho humano</span>'
        corpo = (f'<p class="achado">Critério: <i>{e(it["criterio"])}</i></p>'
                 f'<p class="evidencia"><b>O que o juiz viu:</b> {e(it["evidencia"])}</p>')
    n = it["numero"]
    opcoes = "".join(
        f'<label class="{v}"><input type="radio" name="d{n}" value="{v}"><span>{v}</span></label>'
        for v in ("concordo", "discordo", "parcial"))
    return (f'<div class="item" data-numero="{n}" data-id="{it["id"]}" data-tipo="{it["tipo"]}">'
            f'<span class="num">{n}.</span>{tag}{corpo}'
            f'<fieldset><legend>Decisão do item {n}</legend>{opcoes}'
            f'<input class="nota" type="text" aria-label="Nota do item {n}" '
            f'placeholder="nota (opcional)"></fieldset></div>')


def main():
    dossies = {d["id"]: d for d in ler("dossies.json")}
    itens = itens_para_adjudicar(ler("juiz_criterios.json"))

    por_caso = {}
    for it in itens:
        por_caso.setdefault(it["id"], []).append(it)

    casos = []
    for id_, do_caso in por_caso.items():
        d = dossies[id_]
        registro = "\n".join(f"{k}: {v}" for k, v in d["registro_completo"].items())
        flags = "\n".join(f"{f['tipo']}: {f['detalhe']}" for f in d["flags"]) or "nenhuma"
        casos.append(
            f'<section class="caso"><div class="cabeca">'
            f'<a href="{e(d["foto_url"])}" target="_blank" rel="noopener">'
            f'<img src="{e(d["foto_url"])}" alt="Fotografia do objeto: {e(d["titulo"])}" loading="lazy"></a>'
            f'<div class="textos"><h2>{e(d["titulo"])} — {e(d["povo"])}</h2>'
            f'<p class="meta">item {id_} · {d["conjunto"]}'
            f'{" · visto no desenvolvimento" if d["visto_no_desenvolvimento"] else ""}</p>'
            f'<p class="rotulo">Alt-text gerado</p><p class="texto">{e(d["alt_text"]) or "—"}</p>'
            f'<p class="rotulo">Descrição do objeto gerada</p>'
            f'<p class="texto">{e(d["descricao_objeto"]) or "—"}</p>'
            f'<details><summary>Observação do modelo de visão</summary><pre>{e(d["observacao"])}</pre></details>'
            f'<details><summary>Registro completo do catálogo</summary><pre>{e(registro)}</pre></details>'
            f'<details><summary>Flags emitidas</summary><pre>{e(flags)}</pre></details>'
            f'</div></div>' + "".join(bloco_item(it) for it in do_caso) + '</section>')

    pagina = (
        '<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>Adjudicação do juiz — Acervo que Fala</title>\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@400;500;600;700'
        '&display=swap" rel="stylesheet">\n'
        f'<style>{CSS}</style>\n</head>\n<body>\n<div class="wrap">\n'
        '<header class="topo"><h1>Adjudicação do juiz — lote de avaliação</h1>'
        '<span class="progresso" id="progresso" aria-live="polite"></span>'
        '<button class="leve" id="copiar" type="button">Copiar resultado</button>'
        '<button id="baixar" type="button">Baixar adjudicacao.json</button></header>\n'
        '<main>\n<p class="aviso" id="aviso" role="alert" hidden>Este navegador não está guardando '
        'as decisões. Baixe o resultado antes de fechar a página.</p>\n'
        f'<div class="instrucoes">{INSTRUCOES}</div>\n' + "\n".join(casos) +
        f'\n</main>\n</div>\n<script>{JS}</script>\n</body>\n</html>\n')

    destino = os.path.join(PAINEL_DIR, "adjudicacao.html")
    with open(destino, "w", encoding="utf-8", newline="\n") as f:
        f.write(pagina)
    print(f"adjudicacao.html: {len(itens)} itens em {len(casos)} casos, {len(pagina)} caracteres")


if __name__ == "__main__":
    main()
