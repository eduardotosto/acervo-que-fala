"""Renderização do site em HTML — código puro, sem Gradio.

Fica separado do app.py para poder ser testado em qualquer máquina: aqui se decide o que
aparece e como; o app.py só liga os controles a estas funções.

A fotografia de cada objeto entra na página com o alt-text gerado no atributo `alt` — o
site pratica o que o projeto propõe.
"""
import html
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(AQUI, "dados.json"), encoding="utf-8") as f:
    DADOS = json.load(f)
OBJETOS = {o["id"]: o for o in DADOS["objetos"]}
REPOSITORIO = "https://github.com/eduardotosto/acervo-que-fala"

e = html.escape
CONJUNTOS = {"Todos": None, "Casos de avaliação (40)": "casos", "Holdout (10)": "holdout"}
NOME_FLAG = {"artefato_estudio": "artefato de estúdio",
             "divergencia_imagem_catalogo": "divergência foto × catálogo",
             "metadado_suspeito": "metadado suspeito",
             "falta_de_resolucao": "foto sem resolução"}
NOME_CAMADA = {"observacao": "na observação: o modelo viu errado",
               "redacao": "na redação: viu certo e escreveu errado",
               "registro": "no registro: o catálogo erra",
               "codigo": "no código: flag ou escala calculada errado"}
NOME_FIDELIDADE = {"fiel": "fiel à foto", "fiel_com_ressalva": "fiel, com ressalva",
                   "infiel": "infiel à foto", "conferir": "pede conferência humana",
                   "nao_se_aplica": "não se aplica"}
NOME_LADO = {"gerado": "o alt-text gerado", "baseline": "a descrição curatorial",
             "empate": "empate", "nenhum": "nenhum dos dois"}

CSS = """
.aqf { --md-primary:#8a4b2c; --md-primary-container:#ffdbc6; --md-on-primary-container:#341000;
  --md-secondary:#2f5d8f; --md-secondary-container:#d3e4ff; --md-on-secondary-container:#001b3d;
  --md-tertiary:#7a5a17; --md-tertiary-container:#ffe9b3; --md-on-tertiary-container:#271900;
  --md-surface:#f7f4ee; --md-surface-container-low:#f1ede3; --md-surface-container:#eae5da;
  --md-surface-container-high:#e3ddd1; --md-on-surface:#1e1b16; --md-on-surface-variant:#4d463b;
  --md-outline-variant:#d8cfc0; --ok:#3d6b34; --erro:#8c2f2f;
  --shape-sm:8px; --shape-lg:16px; --shape-full:999px;
  --elev1:0 1px 2px rgba(30,20,10,.09), 0 1px 4px rgba(30,20,10,.07);
  font-family:'Google Sans Flex','Segoe UI',system-ui,sans-serif; color:var(--md-on-surface);
  line-height:1.6; font-size:1rem; }
.dark .aqf { --md-primary:#ffb787; --md-primary-container:#6c3712; --md-on-primary-container:#ffdbc6;
  --md-secondary:#a7c8ff; --md-secondary-container:#114881; --md-on-secondary-container:#d3e4ff;
  --md-tertiary:#e8c16d; --md-tertiary-container:#5c4200; --md-on-tertiary-container:#ffe9b3;
  --md-surface:#17140f; --md-surface-container-low:#1e1a14; --md-surface-container:#221e17;
  --md-surface-container-high:#2c271e; --md-on-surface:#ece5da; --md-on-surface-variant:#cec4b4;
  --md-outline-variant:#4d463b; --ok:#8fbc82; --erro:#f2b8b5;
  --elev1:0 1px 3px rgba(0,0,0,.45), 0 2px 6px rgba(0,0,0,.35); }
.aqf * { box-sizing:border-box; }
.aqf h1 { font-size:1.7rem; font-weight:700; line-height:1.2; margin:0 0 .4rem; color:var(--md-on-surface); }
.aqf h2 { font-size:1.25rem; font-weight:600; margin:0 0 .2rem; color:var(--md-on-surface); }
.aqf h3 { font-size:.72rem; font-weight:700; letter-spacing:.06em; text-transform:uppercase;
  color:var(--md-secondary); margin:1.2rem 0 .3rem; }
.aqf p { margin:0 0 .6rem; color:var(--md-on-surface); }
.aqf a { color:var(--md-secondary); }
.aqf .lead { font-size:1.02rem; max-width:62rem; }
.aqf .aviso { background:var(--md-tertiary-container); color:var(--md-on-tertiary-container);
  border-radius:var(--shape-lg); padding:.8rem 1.1rem; font-size:.92rem; margin:.8rem 0 0; }
.aqf .aviso p { color:inherit; margin:0; }
.aqf .cartao { background:var(--md-surface-container-low); border-radius:var(--shape-lg);
  box-shadow:var(--elev1); display:grid; grid-template-columns:minmax(0,5fr) minmax(0,7fr);
  overflow:hidden; }
@media (max-width:760px) { .aqf .cartao { grid-template-columns:1fr; } }
.aqf .foto { background:var(--md-surface-container-high); padding:1rem; }
.aqf .foto img { width:100%; height:auto; max-height:520px; object-fit:contain; display:block;
  border-radius:var(--shape-sm); }
.aqf .foto .legenda { font-size:.8rem; color:var(--md-on-surface-variant); margin:.6rem 0 0; }
.aqf .corpo { padding:1.1rem 1.3rem 1.4rem; min-width:0; }
.aqf .meta { font-size:.82rem; color:var(--md-on-surface-variant); margin:0 0 .4rem; }
.aqf .caixa { border-radius:var(--shape-sm); padding:.7rem .9rem; font-size:.95rem; }
.aqf .caixa p:last-child { margin-bottom:0; }
.aqf .caixa.baseline { background:var(--md-surface-container-high); }
.aqf .caixa.baseline p { color:var(--md-on-surface-variant); }
.aqf .caixa.gerado { background:var(--md-secondary-container); }
.aqf .caixa.gerado p { color:var(--md-on-secondary-container); }
.aqf .caixa.vazio { background:var(--md-tertiary-container); }
.aqf .caixa.vazio p { color:var(--md-on-tertiary-container); }
.aqf .chip { display:inline-block; font-size:.7rem; font-weight:700; letter-spacing:.04em;
  text-transform:uppercase; border-radius:var(--shape-full); padding:.12rem .6rem;
  background:var(--md-tertiary-container); color:var(--md-on-tertiary-container); margin-right:.4rem; }
.aqf .chip.grave { background:var(--md-primary-container); color:var(--md-on-primary-container); }
.aqf .chip.ok { background:var(--ok); color:var(--md-surface); }
.aqf .chip.nao { background:var(--erro); color:var(--md-surface); }
.aqf ul { margin:0; padding-left:1.1rem; }
.aqf li { margin:0 0 .45rem; font-size:.92rem; color:var(--md-on-surface); }
.aqf li small, .aqf .nota { font-size:.82rem; color:var(--md-on-surface-variant); display:block; }
.aqf details { margin-top:.8rem; font-size:.88rem; color:var(--md-on-surface-variant); }
.aqf summary { cursor:pointer; font-weight:600; color:var(--md-on-surface); }
.aqf pre { white-space:pre-wrap; font:inherit; margin:.4rem 0 0; color:var(--md-on-surface-variant); }
.aqf table { border-collapse:collapse; width:100%; font-size:.92rem; margin:.3rem 0 1.4rem;
  font-variant-numeric:tabular-nums; }
.aqf th, .aqf td { text-align:left; padding:.45rem .7rem; border-bottom:1px solid var(--md-outline-variant);
  color:var(--md-on-surface); vertical-align:top; }
.aqf th { font-size:.72rem; letter-spacing:.05em; text-transform:uppercase;
  color:var(--md-on-surface-variant); font-weight:700; }
.aqf td.num, .aqf th.num { text-align:right; white-space:nowrap; }
.aqf .rolagem { overflow-x:auto; }
.aqf .texto { max-width:50rem; }
"""


def rotulo(o):
    return f"{o['titulo']} — {o['povo']} ({o['id']})"


def opcoes(conjunto):
    alvo = CONJUNTOS[conjunto]
    return [(rotulo(o), o["id"]) for o in DADOS["objetos"] if alvo in (None, o["conjunto"])]


def paragrafos(texto):
    return "".join(f"<p>{e(p.strip())}</p>" for p in texto.split("\n") if p.strip())


# ------------------------------------------------------------------ cabeçalho
def cabecalho():
    return f"""<div class="aqf" lang="pt-BR">
<h1>Acervo que Fala</h1>
<p class="lead">O acervo digital do Museu do Índio tem 20.965 itens publicados com o texto
alternativo vazio: quem usa leitor de tela não ouve descrição nenhuma da fotografia. Este site
mostra o que um sistema de modelos abertos gerou para 50 objetos do acervo, e o que a avaliação
encontrou em cada um.</p>
<div class="aviso" role="note"><p><b>Textos gerados por modelo, sem revisão humana.</b> Eles contêm
erros, e a avaliação os aponta objeto a objeto. Projeto acadêmico independente (ICA/PUC-Rio): não é
um produto do Museu do Índio nem descrição oficial do acervo.
<a href="{REPOSITORIO}">Código, dados e avaliação no repositório</a>.</p></div>
</div>"""


# ------------------------------------------------------------------ cartão do objeto
def bloco_flags(o):
    if not o["flags"]:
        return "<p>Nenhuma flag emitida para este objeto.</p>"
    itens = "".join(f'<li><span class="chip">{e(NOME_FLAG.get(f["tipo"], f["tipo"]))}</span>'
                    f'{e(f["detalhe"])}</li>' for f in o["flags"])
    return f"<ul>{itens}</ul>"


def bloco_juiz(o):
    j = o["juiz"]
    a = j["achados"]
    partes = [f'<p><b>Fidelidade visual:</b> {NOME_FIDELIDADE.get(j["fidelidade_visual"], j["fidelidade_visual"])}. '
              f'<b>Achados:</b> {a["alta"]} de gravidade alta, {a["media"]} média, {a["baixa"]} baixa.</p>',
              f'<p>{e(j["resumo"])}</p>']
    if j["graves"]:
        linhas = []
        for g in j["graves"]:
            decisao = ""
            if g["adjudicacao"]:
                classe = {"concordo": "ok", "discordo": "nao"}.get(g["adjudicacao"], "")
                decisao = (f'<small><span class="chip {classe}">adjudicação: {e(g["adjudicacao"])}</span>'
                           f'{e(g["nota"])}</small>')
            linhas.append(f'<li><span class="chip grave">gravidade alta</span>{e(g["descricao"])}'
                          f'<small>Erro nascido {NOME_CAMADA[g["camada"]]}. {e(g["evidencia"])}</small>'
                          f'{decisao}</li>')
        partes.append(f"<ul>{''.join(linhas)}</ul>")
    ab = o["ab"]
    if ab:
        partes.append(
            f'<p><b>A/B cego:</b> sem saber qual era qual, o juiz achou que '
            f'{NOME_LADO[ab["descreve_melhor"]]} descreve melhor a foto, e publicaria '
            f'{NOME_LADO[ab["publicaria"]]}.</p>'
            f'<p class="nota">Motivo: {e(ab["motivo"])} (Neste par, o texto gerado era o lado '
            f'{ab["lado_do_gerado"]}.)</p>')
    return "".join(partes)


def cartao(id_objeto):
    o = OBJETOS[int(id_objeto)]
    conjunto = "holdout" if o["conjunto"] == "holdout" else "caso de avaliação"
    visto = " · esteve no lote de desenvolvimento" if o["visto_no_desenvolvimento"] else ""
    if o["gerou_texto"]:
        alt_da_imagem = o["alt_text"]
        nivel1 = f'<div class="caixa gerado">{paragrafos(o["alt_text"])}</div>'
        nivel2 = f'<div class="caixa gerado">{paragrafos(o["descricao_objeto"])}</div>'
        legenda = ("O texto alternativo desta imagem, nesta página, é o alt-text gerado abaixo. "
                   "No acervo publicado ele está vazio.")
    else:
        alt_da_imagem = f"Fotografia do objeto {o['titulo']}, sem descrição gerada"
        vazio = ('<div class="caixa vazio"><p>Nenhum texto foi gerado. A foto tem '
                 f'{e(o["resolucao"])} pixels, abaixo do mínimo para descrever: o sistema emite uma '
                 'flag e devolve o item ao acervo.</p></div>')
        nivel1 = nivel2 = vazio
        legenda = "Foto sem resolução mínima: o sistema não descreve."
    registro = "\n".join(f"{k}: {v}" for k, v in o["registro"].items())
    return f"""<div class="aqf" lang="pt-BR"><article class="cartao">
<div class="foto"><img src="{e(o['foto_url'])}" alt="{e(alt_da_imagem)}">
<p class="legenda">{legenda} <a href="{e(o['pagina_no_acervo'])}">Ver o item no site do museu</a>.</p></div>
<div class="corpo">
<h2>{e(o['titulo'])} — {e(o['povo'])}</h2>
<p class="meta">{e(o['categoria'])} · item {o['id']} · {conjunto}{visto}</p>
<h3>Como o acervo descreve hoje (descrição curatorial)</h3>
<div class="caixa baseline">{paragrafos(o['baseline'])}</div>
<h3>Nível 1 — alt-text da fotografia, gerado</h3>
{nivel1}
<h3>Nível 2 — descrição do objeto, gerada</h3>
{nivel2}
<h3>Flags para revisão humana</h3>
{bloco_flags(o)}
<h3>O que a avaliação apontou</h3>
{bloco_juiz(o)}
<details><summary>O que o modelo de visão disse ter visto</summary><pre>{e(o['observacao']) or 'Sem observação.'}</pre></details>
<details><summary>Campos do registro entregues ao redator</summary><pre>{e(registro)}</pre></details>
</div></article></div>"""


# ------------------------------------------------------------------ resultados
def tabela(cabecalhos, linhas):
    th = "".join(f'<th class="{"num" if i else ""}">{e(c)}</th>' for i, c in enumerate(cabecalhos))
    tr = "".join("<tr>" + "".join(f'<td class="{"num" if i else ""}">{e(str(c))}</td>'
                                  for i, c in enumerate(l)) + "</tr>" for l in linhas)
    return f'<div class="rolagem"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def br(valor):
    return str(valor).replace(".", ",")


def resultados():
    r = DADOS["recortes"]
    nomes = [n for n in ("casos", "não vistos", "holdout") if n in r]
    cab = ["Medida"] + [f"{n} ({r[n]['n']})" for n in nomes]
    col = lambda f: [f(r[n]) for n in nomes]
    par = lambda chave: lambda x: (f"{x['alt_criterios']['gerado'].get(chave, 0)} | "
                                   f"{x['alt_criterios']['baseline'].get(chave, 0)} de {x['com_texto']}")
    juiz = lambda f: [f(r[n]["juiz"]) for n in nomes]
    taxa = lambda v: f"{round(100 * v.get('atende', 0) / max(1, v.get('atende', 0) + v.get('nao_atende', 0)))}%"
    adjudicado = ("Os achados de gravidade alta foram adjudicados pelo autor." if DADOS["adjudicado"] else
                  "Os números do juiz ainda não foram adjudicados pelo autor: são a leitura do juiz.")
    return f"""<div class="aqf" lang="pt-BR"><div class="texto">
<h2>O que foi medido</h2>
<p>O sistema foi desenvolvido sobre um lote de 20 objetos e depois congelado. Os números abaixo são
de 50 objetos fixados antes de qualquer ajuste: 40 casos de avaliação e 10 de <i>holdout</i>, o
conjunto reservado que roda uma única vez, no fim. "Não vistos" são os casos sem os 5 objetos que
também estiveram no lote de desenvolvimento.</p>
<p>Modelo: {e(DADOS['sistema']['modelo'])}, em GPU gratuita. Rodada de {e(DADOS['sistema']['executado_em_utc'][:10])},
{br(round(DADOS['sistema']['minutos_de_geracao']))} minutos de geração para os 50 objetos.</p></div>

<h3>Cobertura</h3>
{tabela(cab, [["Objetos com descrição gerada"] + col(lambda x: x["com_texto"]),
              ["Foto sem resolução: flag, nenhum texto"] + col(lambda x: x["sem_resolucao"]),
              ["Falha de geração"] + col(lambda x: x["falha_de_geracao"]),
              ["Textos que passaram pela correção automática"] + col(lambda x: x["retry"])])}

<h3>Verificação automática (régua mecânica)</h3>
{tabela(cab, [["Problemas por objeto"] + col(lambda x: br(x["regua_problemas_por_item"])),
              ["Objetos sem nenhum problema"] + col(lambda x: f"{x['regua_sem_problema']} de {x['n']}")])}
<p class="nota">No lote de desenvolvimento a mesma régua mede 1,7 problema por objeto.</p>

<h3>Alt-text: gerado | descrição curatorial, em critérios objetivos</h3>
{tabela(cab, [[c.capitalize()] + col(par(c)) for c in
              ("até 30 palavras", "começa pelo objeto", "cita o povo", "sem jargão de catálogo", "sem medida")]
             + [["Atende aos 5 critérios"] + col(lambda x: f"{x['alt_todos_os_criterios']['gerado']} | "
                                                 f"{x['alt_todos_os_criterios']['baseline']} de {x['com_texto']}")])}
<p class="nota">A descrição curatorial nunca cita o povo porque, no catálogo, o povo fica em outro campo.
Ela não foi escrita para ser texto alternativo; é comparada como tal porque é o que o acervo teria
à mão para preencher o campo vazio.</p>

<h3>Juiz: um modelo de linguagem confere cada texto contra a foto e o registro</h3>
{tabela(cab, [["Critérios do caso atendidos"] + juiz(lambda j: taxa(j["vereditos"])),
              ["Textos com informação falsa ou inventada"] + [
                  f"{r[n]['juiz']['casos_com_grave_no_texto']} de {r[n]['com_texto']}" for n in nomes],
              ["Erros graves nascidos na observação"] + juiz(lambda j: j["achados_graves_por_camada"].get("observacao", 0)),
              ["Erros graves nascidos na redação"] + juiz(lambda j: j["achados_graves_por_camada"].get("redacao", 0)),
              ["Fiel à foto / com ressalva / infiel"] + juiz(lambda j: " / ".join(
                  str(j["fidelidade_visual"].get(k, 0)) for k in ("fiel", "fiel_com_ressalva", "infiel")))])}
<p class="nota">{adjudicado} Na calibração de 27/08/2026, o autor concordou com cerca de 95% dos
apontamentos do juiz, e o juiz deixou passar cerca de um defeito em cada dez.</p>

<h3>A/B cego: gerado | descrição curatorial</h3>
{tabela(cab, [["Qual descreve melhor a foto"] + juiz(lambda j: f"{j['ab_descreve_melhor'].get('gerado', 0)} | {j['ab_descreve_melhor'].get('baseline', 0)}"),
              ["Qual seria publicado"] + juiz(lambda j: f"{j['ab_publicaria'].get('gerado', 0)} | {j['ab_publicaria'].get('baseline', 0)}"),
              ["Nota de fidelidade, de 1 a 5"] + juiz(lambda j: f"{br(j['ab_notas']['gerado']['fidelidade'])} | {br(j['ab_notas']['baseline']['fidelidade'])}"),
              ["Nota de clareza ao ouvido"] + juiz(lambda j: f"{br(j['ab_notas']['gerado']['clareza_ao_ouvido'])} | {br(j['ab_notas']['baseline']['clareza_ao_ouvido'])}"),
              ["Nota de concisão"] + juiz(lambda j: f"{br(j['ab_notas']['gerado']['concisao'])} | {br(j['ab_notas']['baseline']['concisao'])}")])}
<p class="nota">O juiz recebeu só a foto e os dois textos, em ordem sorteada, sem saber qual era qual.</p>
</div>"""


# ------------------------------------------------------------------ como funciona
def como_funciona():
    return f"""<div class="aqf" lang="pt-BR"><div class="texto">
<h2>Dois textos por objeto</h2>
<p><b>Nível 1, alt-text:</b> descreve a fotografia em até 30 palavras, começando pelo objeto e pelo
povo. É o que o leitor de tela fala no lugar da imagem.</p>
<p><b>Nível 2, descrição do objeto:</b> descreve o objeto em si, independente da foto. Todo fato que
vem do catálogo entra com marca de atribuição, como "segundo o registro do museu".</p>
<p><b>Flags:</b> o que precisa de olho humano antes de publicar: artefato de estúdio na foto,
divergência entre foto e catálogo, metadado improvável.</p>

<h2 style="margin-top:1.4rem">O caminho de cada objeto</h2>
<table><tbody>
<tr><td><b>1. Observação</b></td><td>O modelo de visão recebe só a fotografia e descreve o que vê,
em seções nomeadas.</td></tr>
<tr><td><b>2. Garantias em código</b></td><td>Escala, contagem de partes, teto de plausibilidade das
medidas e flags de cor são calculados, não pedidos ao modelo. Informação com flag não entra no texto.</td></tr>
<tr><td><b>3. Redação</b></td><td>O modelo recebe só texto: a observação, o registro do catálogo e as
diretrizes da rubrica, recuperadas por categoria e por similaridade (RAG).</td></tr>
<tr><td><b>4. Validação</b></td><td>O código confere o rascunho e, se ele falha, devolve o diagnóstico
ao modelo uma única vez.</td></tr>
<tr><td><b>5. Revisão humana</b></td><td>As flags e a avaliação dizem onde olhar. Esta etapa não é
opcional.</td></tr>
</tbody></table>
<p>A separação entre olhar e escrever existe para auditar cada erro: ele nasceu na observação ou
na redação?</p>

<h2 style="margin-top:1.4rem">O que este projeto não prova</h2>
<ul>
<li>Não houve avaliação com pessoas cegas nem com curadores do museu. A avaliação é automática e por
um modelo juiz.</li>
<li>O juiz é um modelo proprietário, usado só para medir. O que gera as descrições é aberto.</li>
<li>São 50 objetos de um acervo de 20.965. Escala, custo e aceitação institucional não foram medidos.</li>
<li>Significado cultural só entra quando o catálogo do museu o registra. O sistema não o infere.</li>
</ul>
<p style="margin-top:1rem">Projeto final da pós em Inteligência Artificial Generativa &amp; Large
Language Models (ICA/PUC-Rio). Autor: Eduardo Tosto. Orientadora: Profa. Manoela Kohler.
<a href="{REPOSITORIO}">Repositório</a>.</p>
</div></div>"""
