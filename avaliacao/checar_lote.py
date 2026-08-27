#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Mede QUALQUER lote de resultados com a régua de hoje.

Cada lote (v1, v2, v4, v5, bake-off Gemma, v6) foi gerado com uma versão diferente da
verificação automática — inclusive com bugs conhecidos, como o casamento de substring
que confundia "aparece" com "parece". Comparar o "n/20 sem problemas" de dois lotes
medidos por réguas diferentes não diz nada. Este script aplica as MESMAS checagens a
todos, e pula sozinho as que dependem de campos que o lote antigo não tem.

Os dois blocos marcados abaixo são o mesmo texto que roda no Notebook 04 (etapas 5b e
7) — o notebook é montado a partir daqui, então as duas cópias não divergem.

Uso:
    python avaliacao/checar_lote.py resultados/04_pipeline_completo_v5.json
    python avaliacao/checar_lote.py --itens resultados/04_pipeline_completo_v5.json
"""
import argparse, collections, io, json, os, re, sys

# --- INICIO BLOCO REGISTRO (compartilhado com o Notebook 04, etapa 5b) ---
ROTULOS = r"(comprimento|altura|largura|di[âa]metro|espessura|profundidade)"
RE_ROTULO, RE_NUM = re.compile(ROTULOS, re.I), re.compile(r"\d+(?:[.,]\d+)?")
# medida "com cordel / com a alça esticada" mede o objeto pendurado, não a peça
RE_COM_CORDA = re.compile(
    r"com\s+(a\s+|o\s+)?(cordel|cord[aã]o|al[çc]a|amarra)|esticad|\+\s*(cordel|cord[aã]o|al[çc]a)", re.I)

# Teto de plausibilidade por categoria = Q3 + 3xIQR das dimensões do PRÓPRIO acervo
# (547 dos 555 itens de dados/itens.json têm medida parseável), com piso de 150 cm —
# abaixo disso, peça grande é plausível em qualquer categoria. No acervo inteiro o teto
# dispara 2 vezes: o abano de 290 cm (dimensão improvável, caso conhecido do projeto) e
# a capa de pele de onça de 223 cm (peça genuinamente grande). Flag é pedido de
# conferência humana, não veredito — a taxa de alarme é o que importa, e é de 0,4%.
TETOS_CATEGORIA = {
    "Adornos Plumários": 156,
    "Adornos de Materiais Ecléticos, Indumentária e Toucador": 106,
    "Armas": 491,
    "Cerâmica": 56,
    "Cordões e Tecidos": 103,
    "Etnobotânica": 33,
    "Instrumentos musicais e de sinalização": 76,
    "Objetos rituais, mágicos e lúdicos": 144,
    "Trançados": 181,
    "Utensílios e implementos de materiais ecléticos": 75,
}
PISO_SUSPEITA = 150
# miniatura: peça bem menor que o comum da categoria, em categorias de objeto grande
MEDIANAS_CATEGORIA = {"Cerâmica": 14.0, "Trançados": 41.5, "Armas": 212.5,
                      "Instrumentos musicais e de sinalização": 41.0,
                      "Utensílios e implementos de materiais ecléticos": 19.5}

def escala_do_registro(dimensoes):
    """Maior dimensão do objeto, em cm, com o rótulo — a regra editorial 25 ("escala é a
    maior dimensão, nunca a medida de uma parte"), resolvida em código. Trata a lista
    enumerada ("29,5; 21,5; ... e 9,5 cm de comprimento") herdando o rótulo do segmento
    seguinte. Devolve (valor, rótulo) ou None."""
    if not dimensoes or "cm" not in dimensoes.lower():
        return None
    segmentos = [s for s in re.split(r";|\s-\s", dimensoes) if s.strip()]
    candidatos = []
    for i, seg in enumerate(segmentos):
        if RE_COM_CORDA.search(seg):
            continue
        rot = RE_ROTULO.search(seg) or next(
            (RE_ROTULO.search(s) for s in segmentos[i + 1:] if RE_ROTULO.search(s)), None)
        rotulo = rot.group(1).lower() if rot else ""
        candidatos += [(float(m.group(0).replace(",", ".")), rotulo) for m in RE_NUM.finditer(seg)]
    return max(candidatos) if candidatos else None


def numero_pt(v):
    return f"{v:.0f}" if v >= 20 else f"{v:.1f}".replace(".", ",").replace(",0", "")


def analisar_registro(registro):
    """Devolve a linha ESCALA pronta para o prompt + as flags de metadado que a
    aritmética já resolve (dimensão fora do teto da categoria, ano impossível)."""
    cat, flags = registro.get("Categoria", ""), []
    e = escala_do_registro(registro.get("Dimensões", ""))
    if not e:
        escala = "não informada no registro — não escreva medida nenhuma"
    else:
        valor, rotulo = e
        escala = f"cerca de {numero_pt(valor)} cm" + (f" de {rotulo}" if rotulo else "")
        mediana = MEDIANAS_CATEGORIA.get(cat)
        if mediana and valor < 10 and valor < mediana / 2:
            escala += " — miniatura (bem menor que o comum na categoria): diga que é miniatura"
            # 4a revisao editorial: dimensao atipicamente pequena tambem pede conferencia
            # humana, pelo mesmo motivo do abano de 290 cm — pode ser miniatura genuina
            # (as 3 dimensoes do Pote 9196 sao coerentes) ou erro de registro
            flags.append({"tipo": "metadado_suspeito", "detalhe":
                          f"dimensão atipicamente pequena para {cat} ({numero_pt(valor)} cm; "
                          f"mediana da categoria {numero_pt(mediana)} cm) — miniatura genuína "
                          f"ou erro de registro; conferir"})
        teto = TETOS_CATEGORIA.get(cat)
        if teto and valor > max(teto, PISO_SUSPEITA):
            flags.append({"tipo": "metadado_suspeito", "detalhe":
                          f"{numero_pt(valor)} cm de {rotulo or 'dimensão'} está acima do teto de "
                          f"plausibilidade da categoria {cat} ({teto} cm, calculado do acervo)"})
    if re.search(r"al[çc]as? soltas?", registro.get("Descrição", "") or "", re.I) and e:
        flags.append({"tipo": "metadado_suspeito", "detalhe":
                      "a Descrição menciona alças soltas — o comprimento pode incluí-las; conferir"})
    ano = (registro.get("Ano de aquisição do objeto") or "").strip()
    if ano.isdigit() and not (1850 <= int(ano) <= 2026):
        flags.append({"tipo": "metadado_suspeito", "detalhe": f"ano de aquisição improvável: {ano}"})
    return escala, flags
# --- FIM BLOCO REGISTRO ---

# --- INICIO BLOCO OBSERVACAO (compartilhado com o Notebook 04, etapa 5) ---
# A secao ARTEFATOS sozinha nao basta. Medido no lote v6: em 2 dos 4 itens com artefato
# real, o modelo descreveu o artefato na secao onde o viu (PARTES E QUANTIDADES,
# LEGIBILIDADE, FUNDO E ESTUDIO) e respondeu "nenhum" em ARTEFATOS - ele nao repete o
# que ja disse. A varredura le todas as secoes e descarta as mencoes sob negacao
# ("nao ha etiquetas", "sem numeracao"), que sao a maioria. No lote v6: 4/4 itens
# corretos, 0 falso positivo, contra 2/4 da secao sozinha.
# "suporte" ficou de fora: nomeia tanto a base de estudio quanto uma parte do proprio
# objeto (a peca central da bracadeira 1366) - ambiguidade que nao da para resolver aqui.
FAMILIAS_ARTEFATO = [("etiqueta", r"etiqueta\w*|r[óo]tulo\w*"),
                     ("inscrição", r"numera[çc]\w*|marca[çc][ãa]o\w*|inscri[çc]\w*"),
                     ("cartela de cores", r"cartela\w*|escala\s+de\s+cores?"),
                     ("régua", r"r[ée]gua\w*")]
RE_TERMO_ARTEFATO = re.compile(
    r"(?<![a-zà-ú])(" + "|".join(p for _, p in FAMILIAS_ARTEFATO) + ")", re.I)
RE_NEGACAO = re.compile(r"(?<![a-zà-ú])(n[ãa]o\s|nenhum\w*|sem\s|nada\s|aus[êe]ncia)", re.I)


def artefatos_da_observacao(obs):
    """Uma flag por familia de artefato citada na observacao fora de contexto de
    negacao, com a frase mais curta como detalhe."""
    por_familia = {}
    for m in RE_TERMO_ARTEFATO.finditer(obs):
        ini = max(obs.rfind(".", 0, m.start()), obs.rfind("\n", 0, m.start())) + 1
        if RE_NEGACAO.search(obs[ini:m.start()]):
            continue
        fim = obs.find(".", m.end())
        frase = re.sub(r"\s+", " ", obs[ini:fim if fim > 0 else m.end() + 60]).strip(" .;,")
        frase = re.sub(r"^[#*\s]*[A-ZÀ-Ú ]{4,}[#*\s]*:[#*\s]*", "", frase)
        nome = next(n for n, pat in FAMILIAS_ARTEFATO if re.match(pat, m.group(0), re.I))
        if nome not in por_familia or len(frase) < len(por_familia[nome]):
            por_familia[nome] = frase
    return [{"tipo": "artefato_estudio", "detalhe": f"{n}: {t}"} for n, t in por_familia.items()]

# Cor vista na foto que o registro nao nomeia. Reencontra automaticamente o achado
# fundador do projeto: as duas penas AZUIS da Faixa Kalapalo (665), que o registro
# nao menciona. So dispara quando o registro DESCREVE cores (registro que nao fala de
# cor nao autoriza divergencia) e so para cores informativas - bege, marrom, cinza e
# afins sao a cor natural do material, que o catalogo nunca nomeia.
CORES_INFORMATIVAS = {"azul": r"azu[lm]|azulad", "verde": r"verde|esverdead",
                      "vermelho": r"vermelh|avermelhad", "amarelo": r"amarel",
                      "laranja": r"laranj", "roxo": r"rox|violet", "rosa": r"rosa",
                      "preto": r"pret", "branco": r"branc"}
CORES_DE_MATERIAL = r"bege|marrom|castanh|cinza|creme|ocre|dourad|prate|amarronzad"


def cores_do_texto(texto):
    return {nome for nome, pat in CORES_INFORMATIVAS.items()
            if re.search(rf"(?<![a-zà-ú])(?:{pat})\w*", texto or "", re.I)}


def cores_divergentes(observacao, registro, secao_fn):
    """Cores que a observacao nomeia e o registro nao. Devolve lista de flags."""
    texto_reg = " ".join(str(registro.get(c, "")) for c in
                         ("Descrição", "Matéria-prima", "Técnica de confecção", "Nome do item"))
    no_registro = cores_do_texto(texto_reg)
    if not no_registro:
        return []
    na_foto = cores_do_texto(secao_fn(observacao, "MATERIAIS E CORES") + " " +
                             secao_fn(observacao, "PADRÕES E TEXTURAS"))
    so_na_foto = sorted(na_foto - no_registro)
    if not so_na_foto:
        return []
    return [{"tipo": "divergencia_imagem_catalogo",
             "detalhe": f"a foto mostra {', '.join(so_na_foto)} e o registro nomeia só "
                        f"{', '.join(sorted(no_registro))}"}]
# --- FIM BLOCO OBSERVACAO ---

# --- INICIO BLOCO VERIFICACAO (compartilhado com o Notebook 04, etapa 7) ---
# Todos os termos são procurados com FRONTEIRA DE PALAVRA. A versão anterior usava
# "termo in texto": "parece" casava com "aparece", "fundo" com "profundo", "coração"
# com "decoração" — o mesmo casamento raso de texto que o projeto diagnosticou nos
# modelos aparecia na própria régua que os media.
B = lambda termos: re.compile(r"(?<![a-zà-úA-ZÀ-Ú])(?:" + "|".join(termos) + r")", re.I)
RE_ARTEFATO = B(["cartela", "paleta", "numeraç", "marcaç", "etiqueta", "régua", "suporte",
                 "rótulo", "rotulo", "inscriç", "tombo"])
RE_AUSENCIA = re.compile(
    r"(?<![a-zà-ú])(?:n[ãa]o (?:h[áa]|é|s[ãa]o|est[áa]|apresenta|possui|tem|cont[ée]m|traz|"
    r"exibe|permite|menciona|descrev\w+|inform\w+|registr\w+|visív\w+)|sem \w+|nenhum\w*|"
    r"aus[êe]ncia de)(?!\s*\w{0,12}identificad)", re.I)
RE_ESPECULACAO = B(["sugere", "sugerindo", "parece", "parecendo", "possivelmente", "talvez"])
RE_VAZIA = B(["porte médio", "uso prático", "uso frequente", "sinais de uso", "forma funcional",
              "forma é funcional"])
RE_FUNDO_TXT = B(["fundo"])
RE_FOTO = re.compile(r"(?<![a-zà-ú])(?:posicionad|enquadr|fotografia|[dn]a imagem|ao fundo|"
                     r"plano (?:médio|geral|fechado|aberto)|close|"
                     r"inclinad\w*\s+(?:levemente\s+)?(?:para\s+)?[aà]?\s*"
                     r"(?:direita|esquerda|frente|trás))", re.I)
# jargão de fotografia no alt: "close-up" e "plano médio" apareceram como
# vocabulário novo de enquadramento na v5, depois que a regra proibiu
# "inteiro/horizontal/vertical". "Detalhe de..." continua sendo a marca sancionada.
RE_JARGAO_FOTO = re.compile(r"(?<![a-zà-ú])(?:close|plano (?:médio|geral|fechado|aberto)|primeiro plano)", re.I)
# funcao tautologica: a que so repete o que o nome do objeto ja diz (regra 21)
RE_FUNCAO_OBVIA = re.compile(
    r"(pulseira|bracelete)[^.]{0,45}(pulso|braço)|(flauta|instrumento)[^.]{0,50}(som|sonor|músic|music)"
    r"|(bolsa|cesto|cesta)[^.]{0,45}(guardar|transportar|carregar)|(pote|panela|vasilha|tigela)"
    r"[^.]{0,50}(armazenar|guardar|conter)|(remo)[^.]{0,35}(remar|navega)|(arco)[^.]{0,35}(atirar|flecha)"
    r"|(colar|cinto|tanga)[^.]{0,40}(pescoço|cintura|corpo)", re.I)
# padrao descrito por semelhanca em vez de geometria: as gregas do 84811 viraram
# "elementos em forma de G ou C invertidos" com o termo certo disponivel no glossario
RE_ANALOGIA = re.compile(
    r"(?<![a-zà-ú])(?:em forma de\s+[\"“‘']?[A-Z][\"”’']?(?![a-zà-ú])|letra\s+[A-Z]\b"
    r"|(?:em )?forma de (?:flor|coração|estrela|coroa|esteira|pétala|folha|animal|ave|leque)"
    r"|lembra(?:ndo)? um|semelhante a um|parecid\w+ com)", re.I)
# marca de atribuicao: uma por bloco de fatos do catalogo, nao uma por fato
RE_MARCA_ATRIB = re.compile(
    r"segundo o registro(?: do museu)?|o registro(?: do museu)? (?:informa|menciona|indica|descreve|diz)"
    r"|conforme o (?:registro|cat[áa]logo)|de acordo com o (?:registro|cat[áa]logo)"
    r"|segundo o cat[áa]logo|o cat[áa]logo (?:informa|registra|descreve)", re.I)
ABERTURAS_ETIQUETA = ("o objeto é", "trata-se de")
RE_MEDIDA_TXT = re.compile(r"(\d+(?:[.,]\d+)?)\s*cm", re.I)


NUMEROS_PT = {"um": 1, "uma": 1, "dois": 2, "duas": 2, "três": 3, "tres": 3,
              "quatro": 4, "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9,
              "dez": 10, "onze": 11, "doze": 12}
RE_NUM_SUBST = re.compile(r"(?<![a-zà-ú])(" + "|".join(NUMEROS_PT) + r"|[2-9]|1[0-2])\s+([a-zà-ú]{3,}s)(?![a-zà-ú])", re.I)


def contagens(texto):
    """Pares (substantivo plural, número) escritos num texto: 'seis tubos' -> (tubos, 6)."""
    pares = {}
    for m in RE_NUM_SUBST.finditer(texto or ""):
        n = NUMEROS_PT.get(m.group(1).lower()) or int(m.group(1))
        pares.setdefault(m.group(2).lower(), n)
    return pares


def tem_atribuicao(texto):
    return re.search(r"(?<![a-zà-ú])(registro|catálogo|catalogo)", texto or "", re.I) is not None


def verificar(item):
    """Devolve os problemas como pares (chave, detalhe). A chave é estável, para somar o
    mesmo problema entre lotes; o detalhe é o que muda de item para item.

    As checagens que dependem de campos que só a v6 produz (o enquadramento decidido na
    observação) são puladas quando o campo não existe — é o que permite medir os lotes
    antigos sem inventar dado que eles não têm. A escala, por ser função só do registro,
    vale para todos."""
    p = []
    alt = item.get("alt_text", "") or ""
    d = item.get("descricao_objeto", "") or ""
    a, dl = alt.lower(), d.lower().strip()
    registro = item.get("registro", {}) or {}

    if item.get("json_valido") is False:
        p.append(("json_invalido", ""))
    if "enquadramento_ok" in item and not item["enquadramento_ok"]:
        p.append(("obs_sem_enquadramento", ""))

    povo = (registro.get("Povo") or "").strip()
    if povo and povo.split()[0].lower() not in a:
        p.append(("povo_ausente_no_alt", povo))
    if RE_ARTEFATO.search(a):
        p.append(("artefato_no_alt", RE_ARTEFATO.search(a).group(0)))
    if RE_FUNDO_TXT.search(a):
        p.append(("fundo_no_alt", ""))
    if RE_JARGAO_FOTO.search(a):
        p.append(("jargao_de_foto_no_alt", RE_JARGAO_FOTO.search(a).group(0)))
    if len(alt.split()) > 30:
        p.append(("alt_longo", f"{len(alt.split())} palavras"))
    # a revisao do juiz sobre o v7 achou os tres abaixo passando limpos pelo alt:
    if RE_AUSENCIA.search(a):
        p.append(("ausencia_no_alt", RE_AUSENCIA.search(a).group(0)[:30]))
    if RE_MEDIDA_TXT.search(alt):
        p.append(("medida_no_alt", RE_MEDIDA_TXT.search(alt).group(0)))
    if re.search(r"em escala de|escala\s*:", a + chr(10) + (item.get("descricao_objeto") or "").lower()):
        p.append(("molde_de_escala_no_texto", "a moldura da variável ESCALA vazou"))
    if item.get("enquadramento"):
        alt_detalhe = a.strip().startswith("detalhe")
        if alt_detalhe and item["enquadramento"] != "detalhe":
            p.append(("enquadramento_incoerente", "alt diz Detalhe, observação diz inteiro"))
        if not alt_detalhe and item["enquadramento"] == "detalhe":
            p.append(("enquadramento_incoerente", "observação diz detalhe, alt não marca"))
    return p + _verificar_nivel2(item, d, dl, a, registro)


def _verificar_nivel2(item, d, dl, a, registro):
    p = []
    if d:
        if not tem_atribuicao(d):
            p.append(("nivel2_sem_atribuicao", ""))
        if any(dl.startswith(ab) for ab in ABERTURAS_ETIQUETA):
            p.append(("frase_etiqueta", dl[:18]))
        if "a função é" in dl:
            p.append(("frase_etiqueta", "a função é"))
        if "aquisição em" in dl:
            p.append(("aquisicao_em", ""))
        if RE_ARTEFATO.search(dl):
            p.append(("artefato_no_nivel2", RE_ARTEFATO.search(dl).group(0)))
        if RE_AUSENCIA.search(dl):
            p.append(("afirmacao_de_ausencia", RE_AUSENCIA.search(dl).group(0)))
        if RE_FOTO.search(dl):
            p.append(("foto_no_nivel2", RE_FOTO.search(dl).group(0)))
        if len(d.split()) > 140:
            p.append(("nivel2_longo", f"{len(d.split())} palavras"))
        # colagem do registro bruto: nomes de campo com dois-pontos dentro do texto
        # (o 78838 do v7 colou a ficha inteira — e a palavra "Registro" da colagem
        # ainda comprava a checagem de atribuicao)
        m_colagem = re.search(r"(matéria-prima|técnica de confecção|categoria|dimensões)\s*:", dl)
        if m_colagem:
            p.append(("colagem_do_registro", m_colagem.group(1)))
        # estado da federacao citado sem estar em nenhum campo do registro — o modelo
        # preenche por conhecimento de mundo (Kaxinawa -> Acre) quando o campo esta vazio
        reg_txt = " ".join(str(v) for v in registro.values()).lower()
        for uf in ("acre", "amazonas", "pará", "maranhão", "mato grosso", "tocantins",
                   "pernambuco", "rondônia", "roraima", "amapá", "amazônia"):
            if re.search(rf"(?<![a-zà-ú]){uf}(?![a-zà-ú])", dl) and uf not in reg_txt:
                p.append(("estado_sem_fonte", uf))
        marcas = RE_MARCA_ATRIB.findall(d)
        if len(marcas) > 1:
            p.append(("atribuicao_repetida", f"{len(marcas)} marcas no mesmo texto"))
        if RE_FUNCAO_OBVIA.search(dl):
            p.append(("funcao_obvia", RE_FUNCAO_OBVIA.search(dl).group(0)[:40]))
        # medidas: toda medida escrita tem que estar no registro, e a escala é a maior
        nums_txt = [float(x.replace(",", ".")) for x in RE_MEDIDA_TXT.findall(d)]
        nums_reg = [float(x.replace(",", ".")) for x in
                    re.findall(r"\d+(?:[.,]\d+)?", registro.get("Dimensões", "") or "")]
        for t in nums_txt:
            if nums_reg and not any(abs(r - t) <= 1.0 for r in nums_reg):
                p.append(("medida_fora_do_registro", f"{t:g} cm"))
        # 4a revisao: a contagem do CATALOGO prevalece sempre — o modelo nao e bom nisso
        reg_desc = registro.get("Descrição", "") or ""
        cont_reg, cont_txt = contagens(reg_desc), contagens(a + " " + d)
        for palavra, n_reg in cont_reg.items():
            n_txt = cont_txt.get(palavra)
            if n_txt is not None and n_txt != n_reg:
                p.append(("contagem_diverge_do_registro",
                          f"{palavra}: texto diz {n_txt}, registro diz {n_reg}"))
        escala = item.get("escala") or ""
        if escala and nums_txt:
            m = re.search(r"(\d+(?:[.,]\d+)?)", escala)
            if m:
                esc = float(m.group(1).replace(",", "."))
                if not any(abs(esc - t) <= 1.0 for t in nums_txt):
                    p.append(("escala_errada", f"a maior é {esc:g} cm"))
        if "miniatura" in escala and "miniatura" not in dl:
            p.append(("miniatura_nao_declarada", ""))

    for nome, texto in [("alt", a), ("nível 2", d)]:
        if RE_ANALOGIA.search(texto):
            p.append(("padrao_por_analogia", f"{nome}: {RE_ANALOGIA.search(texto).group(0)[:34]}"))

    for nome, texto in [("alt", a), ("nível 2", dl)]:
        if RE_ESPECULACAO.search(texto):
            p.append(("especulacao", f"{nome}: {RE_ESPECULACAO.search(texto).group(0)}"))
        if RE_VAZIA.search(texto):
            p.append(("frase_vazia", f"{nome}: {RE_VAZIA.search(texto).group(0)}"))

    obs = item.get("observacao") or ""
    if obs and artefatos_da_observacao(obs) and not any(
            f.get("tipo") == "artefato_estudio" for f in (item.get("flags") or [])):
        p.append(("artefato_visto_sem_flag", artefatos_da_observacao(obs)[0]["detalhe"][:40]))

    for f in item.get("flags", []) or []:
        det = (f.get("detalhe") or "").lower()
        if (f.get("tipo") == "artefato_estudio" and RE_FUNDO_TXT.search(det)
                and not RE_ARTEFATO.search(det)):
            p.append(("flag_de_fundo", ""))
        if RE_AUSENCIA.search(det):
            p.append(("flag_de_ausencia", ""))
    return p
# --- FIM BLOCO VERIFICACAO ---


def medir(caminho):
    with io.open(caminho, encoding="utf-8") as f:
        lote = json.load(f)
    itens = lote["itens"]
    contagem, por_item = collections.Counter(), []
    for it in itens:
        # a escala usada na medição é SEMPRE a do código atual (não a que foi injetada
        # na época): mede-se o texto contra a política de hoje. Caso concreto: a Flauta
        # 210680 recebeu "41 cm" de uma versão com o filtro de cordel furado; o texto
        # que repetiu 41 passa a acusar escala_errada, como deve.
        if it.get("registro"):
            it = dict(it, escala=analisar_registro(it["registro"])[0])
        problemas = verificar(it)
        por_item.append((it["id"], it.get("titulo", ""), problemas))
        for chave, _ in problemas:
            contagem[chave] += 1
    flags = collections.Counter(f.get("tipo") for it in itens for f in (it.get("flags") or []))
    return {"nome": os.path.basename(caminho).replace(".json", "").replace("_pipeline_completo", ""),
            "n": len(itens), "limpos": sum(1 for _, _, p in por_item if not p),
            "contagem": contagem, "por_item": por_item, "flags": flags}


def main():
    ap = argparse.ArgumentParser(description="Mede lotes de resultados com a régua da v6.")
    ap.add_argument("arquivos", nargs="+")
    ap.add_argument("--itens", action="store_true", help="lista os problemas item a item")
    args = ap.parse_args()

    lotes = [medir(c) for c in args.arquivos]
    chaves = sorted({k for l in lotes for k in l["contagem"]},
                    key=lambda k: -sum(l["contagem"][k] for l in lotes))
    larg = max(12, max(len(l["nome"]) for l in lotes) + 2)

    print("\nProblemas por checagem — itens afetados, a mesma régua em todos os lotes\n")
    print(f"{'checagem':28}" + "".join(f"{l['nome']:>{larg}}" for l in lotes))
    print("-" * (28 + larg * len(lotes)))
    for k in chaves:
        print(f"{k:28}" + "".join(f"{l['contagem'][k] or '-':>{larg}}" for l in lotes))
    print("-" * (28 + larg * len(lotes)))
    print(f"{'total de problemas':28}" +
          "".join(f"{sum(l['contagem'].values()):>{larg}}" for l in lotes))
    print(f"{'problemas por item':28}" +
          "".join(f"{sum(l['contagem'].values()) / l['n']:>{larg}.1f}" for l in lotes))
    print(f"{'itens sem problema':28}" +
          "".join(f"{str(l['limpos']) + '/' + str(l['n']):>{larg}}" for l in lotes))
    for t in sorted({t for l in lotes for t in l["flags"] if t}):
        print(f"{'flags: ' + t:28}" + "".join(f"{l['flags'][t] or '-':>{larg}}" for l in lotes))

    if args.itens:
        for l in lotes:
            print(f"\n=== {l['nome']} ===")
            for id_, titulo, problemas in l["por_item"]:
                marca = "ok" if not problemas else "; ".join(
                    f"{k}{' (' + v + ')' if v else ''}" for k, v in problemas)
                print(f"{id_:>7} {titulo[:26]:26} {marca}")


if __name__ == "__main__":
    main()
