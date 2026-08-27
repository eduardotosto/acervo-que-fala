# Revisão editorial do lote da E7 — anotações do Eduardo

Feedback card a card sobre `resultados/tabela_lote_04.html` (24/08/2026, em curso).
Ao final, destila em **rubrica v1.1** + **prompt v5** (abertura da E8).

## #1 — Pote Karajá (9196)

**Alt-text**
- "Globular" = jargão de catálogo → formas em palavras comuns ("de corpo arredondado").
- Padrões só como cores, sem forma ("padrões vermelho-alaranjado e preto") → dizer a forma dos padrões.

**Nível 2**
- Abertura "O objeto é um pote…" soa artificial → abrir direto: "Um pote cerâmico…".
- "Globular" de novo (jargão).
- **Vazamento da foto**: "posicionado em pé e inclinado levemente para a direita" — nível 2 descreve o OBJETO, nunca posição/fundo/enquadramento da foto. (Dúvida do Eduardo respondida: nível 2 é independente da fotografia; vira regra dura no prompt v5.)
- Padronagem "cruzes e padrões reticulados" parece equivocada (conferir contra a foto em alta).
- "Segundo o registro do museu" sempre igual nos 20 textos → manter UMA atribuição por texto, variar a formulação, integrar à frase (a fronteira de auditoria fica).
- Material repetido: "material é cerâmica" + "feita em argila" → dizer uma vez.
- Medidas em 3 dimensões = ficha técnica → uma noção de escala basta ("peça pequena, cerca de 6 cm de altura").
- "Foi aquisição em 1977" = português quebrado (colou o nome do campo) → "foi adquirido em 1977" ou cortar.
- **Uso/função deve abrir o texto** (gera interesse): "Um pote cerâmico Karajá usado no preparo e serviço de alimentos…".

## #2 — Faixa frontal emplumada Kalapalo (665)

**Alt-text**
- "Chapéu plumário": jargão E nome errado (título do registro = "Faixa frontal emplumada") → o alt nomeia o objeto pelo título do registro, em linguagem comum.
- Dúvida do Eduardo sobre "cocar" (respondida): não é ofensivo, mas é impreciso aqui — evoca coroa radial; esta peça é faixa de testa. Nome do museu comanda + aposto cotidiano ("adorno de cabeça"); "cocar" só quando o registro usar.
- Eduardo aprova citar as aves das penas — no alt, espécies em conjunto vindas da matéria-prima ("penas de arara, jaburu e jacu"), no lugar da lista de cores vagas.

**Nível 2**
- Vazamento da foto de novo ("posicionado de forma equilibrada, de pé, com a face frontal visível") — reincidência da regra 1.
- Medidas: reincidência (escala, não ficha técnica).
- "A função é…" = frase-etiqueta, mesma família de "O objeto é…" → sem molduras; função integrada à primeira frase.

## Regras candidatas acumuladas (rubrica v1.1 / prompt v5)

1. Nível 2 nunca menciona a fotografia (posição, fundo, enquadramento, inclinação).
2. Abrir o nível 2 direto com o objeto + função ("Um pote cerâmico Karajá usado para…"), sem frases-etiqueta ("O objeto é…", "A função é…", "Trata-se de…").
3. Sem jargão de catálogo no texto público (globular, reticulado, plumário…) — formas em palavras comuns.
4. Padrões: dizer forma além da cor.
5. Uma atribuição ao registro por texto, com formulação variada.
6. Material dito uma vez (não repetir entre metade visual e metade do registro).
7. Escala em vez de ficha técnica de medidas.
8. Datas/aquisição em frase natural ("adquirido em 1977") ou omitidas.
9. Alt nomeia o objeto pelo título do registro (nunca rebatiza pela aparência); nomenclatura cultural sempre da fonte do museu.
10. **Aprovada e refinada (#4):** cor implícita nos materiais naturais (madeira, palha, cerâmica, cipó) — citar só se houver tingimento; cor importa onde informa: penas, miçangas, pinturas, padronagens.
11. **Aprovada (#2):** aves das penas citadas a partir da matéria-prima — no alt, as espécies em conjunto ("penas de arara, jaburu e jacu"); no nível 2, o mapa ave→cor quando o registro traz, com atribuição.
12. Texto público nunca afirma ausências ("sem etiquetas", "não há evidência de tingimento…") — o que não existe não aparece. (Registrar ausência é papel da observação interna, não do texto final.)
13. Fidelidade visual pendente de conferência humana no lote v5: padronagem do #1 ("cruzes e reticulados"?) e "superfície lisa" num trançado (#4).

## #3 — Flauta de pã Tukano (51023)

- Alt: ok (aprovado pelo Eduardo).
- Nível 2: vazamento da foto ("posição vertical… inclinado para a direita"; "fundo é preto") — reincidência; e afirmação de ausência ("sem artefatos de estúdio ou etiquetas") → regra 12.

## #4 — Abano trançado Fulni-ô (63283)

- Alt: preferir material a "fitas marrom claro" — origem da regra 10 refinada (cor implícita em material natural).
- Nível 2: "superfície é lisa" parece errado para trançado de palha (fidelidade visual → regra 13); "Não há evidência de tingimento, costura ou reforços visíveis" = ruído de ausência → regra 12.

## Decisão de processo (24/08/2026)

Eduardo perguntou se seguimos card a card ou aplicamos as regras e "sentimos" o resultado.
**Decisão: parar a revisão de estilo no #4** — achados repetindo (foto no nível 2 3×, medidas 2×, ausências 2×). Aplicar regras 1–12 em rubrica v1.1 + prompt v5, regenerar o lote (notebook 04 v2), e a segunda revisão foca só em fidelidade visual + o que sobrar.

---

# Segunda revisão — lote v2, todos os 20 cards (25/08/2026)

Eduardo revisou os 20 cards do lote v2 (`tabela_lote_04_v2.html`), foco em fidelidade visual.
Feedback verbatim consolidado abaixo por card; regras novas 14–25 no final.

- **#1 Pote (9196):** "fundo bege" no alt é a base da própria cerâmica → nomear pelo material. Nível 2: agrupar informações do mesmo gênero (material repetido: abre com cerâmica, fecha com "feita em argila"); concordância "cinza-escura" para acabamento; 6 cm de altura questionado → **checado: as 3 dimensões do registro são coerentes (4,3/5,5/6,0) = miniatura genuína; o texto deve DIZER "miniatura"**.
- **#2 Faixa (665):** no alt, prioridade são as CORES das penas (visual); aves qualificam — ideal em pares ("penas vermelhas de arara"); "texturas variadas e padrões naturais de coloração" = vago demais.
- **#3 Flauta de pã (51023):** alt deve contar os tubos. Nível 2: "mais curtos no topo, mais longos na base" depende do ponto de vista — "em cascata" basta; "formato vertical, textura natural, sem pinturas ou decorações visíveis" = vago + ausência (já vetada).
- **#4 Abano (63283):** "em ângulo agudo" não descreve — "diagonais alternadas" é o certo. Nível 2: "estrutura retangular" e "roseta com fitas tingidas de azul e verde" NÃO verificáveis (foto é detalhe) → invenção; "trançado"/"fibra vegetal" repetidos; "porte médio, comprimento suficiente para uso prático" = frase vazia.
- **#5 Tanga (78838):** não é detalhe — objeto sangra as margens (≈ inteiro). Nível 2: "sobre fundo branco" confundiu cor do objeto com fundo da FOTO; "miçangas" repetida demais.
- **#6 Braçadeira (1376):** "composição rica e texturizada" = subjetivo; "se curva suavemente" = descrição da foto. 76 cm questionado → **checado: registro menciona "alças soltas"; comprimento deve incluir os cordões → flag**. Registro tem pares cor↔ave ("amarelo, verde e vermelha (Arara)") — modelo nem usou o verde.
- **#7 Pulseira (84811):** alt confuso; faltou o preto; fundo branco da foto contaminou as cores; pulseira não tem "bordas". Nível 2: "destinada a ser usada no pulso" = óbvio; "motivos florais e corações" = interpretação subjetiva de padrão abstrato/geométrico; perdeu o fecho; comprimento irrelevante (escala de pulseira é conhecida).
- **#8 Zarabatana (883523):** brinquedo ou caça? → **checado: contradição interna do registro (Descrição: "brinquedo em miniatura" × Função: "utilizado para caça") = metadado_suspeito**. "Cabo" vem do registro, mas zarabatana tem TUBO (vocabulário fisicamente correto vence). Escala: dizer a MAIOR dimensão (comprimento), não o bocal.
- **#9 Pote (2081):** "fundo creme" = argila; "superfície bege clara" → nomear material.
- **#10 Fuso (5011):** "sugerindo uso frequente" = inferência indevida (textura felpuda é própria do algodão cru); **"tortual" não existe** (registro: "Entalhe | Modelado") = palavra inventada; "forma é funcional, bordas suaves, sem detalhes ornamentais" = frase sem sentido.
- **#11 Argila (200648):** nível 2 focou no tubo de ensaio quando o que importa é o CONTEÚDO; leu como alt.
- **#12 Flauta de osso (210680):** "instrumento musical usado para sons ritmados" = redundante (sabemos para que serve flauta; contexto cultural sim); "sua forma sugere uso em rituais sonoros" = especulação — só afirmações.
- **#13 Pião (5146):** "parecendo cerâmica ou madeira" = especulação — ou sabemos (registro: cabaça + madeira) ou termo genérico.
- **#14 Abano de tucum (500179):** alt: faltou descrição visual da forma e complexidade. Nível 2: "arredondada e simétrica, como uma pequena esteira" = impreciso.
- **#15 Remo (3411):** "inteiro e horizontal" — remo não é horizontal nem vertical; "inteiro" não é descrição (só marcar quando é detalhe).
- **#16 Braçadeira (1366):** "material das penas é natural, sem tingimento artificial" — não é do registro + afirmação de ausência; "Kalapalo" repetido.
- **#17 Estojo (4156):** fundo da foto confundindo de novo; "sem detalhes de acabamento visíveis" = negativa E contradiz a pintura citada acima.
- **#18 Arco (205095):** "mostra sinais de uso" = inferência imprecisa (todo objeto de museu parece desgastado).
- **#19 Panela (905):** "o que a torna pequena para uso doméstico" = inferência desnecessária.
- **#20 Bolsa (500322):** "Peça pequena, com formato retangular e bordas suaves" = vago; por que foco nas bordas?; "peça pequena" sozinho não informa.

## Regras novas da segunda revisão (14–25)

14. **Fundo fotográfico nunca contamina o objeto**: o fundo do estúdio não entra em nenhum texto nem empresta cor ao objeto (#5, #7, #17); quando a "cor de fundo" é a base da própria peça, nomear pelo material ("sobre a argila bege"), nunca como "fundo" (#1, #9).
15. **Só afirmações verificáveis**: proibido "sugere", "parece", "parecendo X ou Y", "possivelmente"; sem inferências de uso/desgaste ("sinais de uso", "uso frequente", "pequena para uso doméstico"); sem juízo estético ("composição rica"); padrão abstrato é "geométrico/abstrato", nunca vira flores/corações; na dúvida de material, termo genérico OU a matéria-prima do registro (#6, #7, #10, #12, #13, #18, #19).
16. **Frases vazias cortadas**: "porte médio", "comprimento suficiente para uso prático", "forma funcional", "bordas suaves" sem função descritiva, "peça pequena" sozinho (#4, #10, #20).
17. **Pares cor↔ave no alt** — cor primeiro (é o visual), ave qualifica: "penas vermelhas e amarelas de arara"; nunca "texturas variadas e padrões naturais" (#2, #6).
18. **Quantidades contáveis entram** quando distinguíveis (tubos da flauta) (#3).
19. **Relações dependentes de ponto de vista só no alt**; nível 2 usa relações da própria peça ("em cascata", "decrescentes") (#3).
20. **Enquadramento refinado**: objeto que sangra as margens ≈ completo (sem "Detalhe de"); "Detalhe" só para fragmento claro; nunca escrever "inteiro"/"horizontal"/"vertical" quando não informa (#5, #15).
21. **Não explicar o óbvio**: função tautológica não entra ("pulseira usada no pulso", "flauta para sons"); função entra quando acrescenta (caça, ritual, preparo) (#7, #12).
22. **Sem redundância lexical**: não repetir a mesma palavra-chave várias vezes (trançado, miçangas, nome do povo) (#4, #5, #16).
23. **Conteúdo antes do recipiente** em amostras (argila, resina): o nível 2 abre pelo conteúdo (#11).
24. **Vocabulário fisicamente correto e existente**: zarabatana tem tubo (mesmo que o registro diga "cabo"); palavra inventada ("tortual") é defeito — termo técnico só do registro ou glossário (#8, #10).
25. **Escala = maior dimensão aproximada** ("cerca de 40 cm de comprimento"), nunca medida de parte (bocal); miniatura é declarada ("miniatura de 6 cm — cabe na palma da mão"); detalhes redundantes de escala conhecida (pulseira) podem ser omitidos (#1, #7, #8).

**Aplicação:** regras 14–25 → prompt v7 (Notebook 04 v4) + checagens novas (especulação, frases vazias, "fundo" no alt). Fidelidade dos casos #4 (roseta inventada) e #14 será reavaliada no lote v4.

---

# Resultado do lote v4 (25/08/2026) — o teto do controle por prompt

Rodado com prompt v7 (25 regras). **Resultado misto: 4/20 sem problemas.** O que aconteceu é
o achado técnico mais importante da E7.

## Ganhou

- **Atribuição ao registro: 5/20 → 20/20** — a correção da v6 funcionou integralmente.
- Regra 18 (contagem): Flauta agora diz **"seis tubos"**.
- Regra 14 onde a base É o material: Pote e Panela dizem **"sobre a argila bege"** ✓.
- Invenções da v2 que sumiram: "corações e flores" na pulseira; "tortual" no fuso; "ângulo agudo"
  virou "espinha-de-peixe" no Abano.
- Par cor↔ave correto na Braçadeira 1366: "penas vermelhas e amarelas de arara".

## Regras que produziram efeito colateral (o achado central)

1. **Regra 17 (pares cor↔ave) CAUSOU uma alucinação nova.** Item 210680 (Flauta de osso): o
   registro não tem Matéria-prima, não nomeia ave nenhuma, e a observação não menciona arara —
   mas o alt da v4 diz **"penas vermelhas de arara"**. Na v2 o modelo tinha acertado justamente
   por NÃO inventar a ave. A regra empurrou o modelo a completar o par mesmo sem fonte.
2. **Regra 5 (uma atribuição por texto) quebrou a auditabilidade.** No Abano, a "roseta de fitas
   tingidas em azul e verde" **está no registro** (verificado: campo Descrição) — não era invenção,
   como parecia na revisão. Mas o texto a apresenta sem marca de atribuição, misturada à descrição
   visual, e por isso lê como se fosse visível na foto. Com fatos de catálogo espalhados pelo texto,
   uma atribuição só no começo não basta.

## Regressões

- **"foi aquisição em"** voltou em 4 itens (883523, 210680, 1366, 4156) — estava corrigido na v2.
- **Povo sumiu do alt** no 200648 (estava presente na v2).
- **Ruído de flags**: 18 flags, mas 12 são só "existe um fundo" — e várias afirmam ausência dentro
  da flag ("Fundo branco, sem artefatos visíveis"), que é a regra 12 violada por dentro. A regra
  "todo artefato vira flag" super-corrigiu.

## Regras que simplesmente não pegaram

- Regra 25 (miniatura declarada): o Pote de 6 cm continua sem dizer que é miniatura.
- Regra 24 (vocabulário físico): a zarabatana continua com "cabo", não "tubo".
- `metadado_suspeito` **zero vezes**, apesar de dois casos claros no lote: o Abano de **290 cm**
  (reproduzido como "cerca de 3 metros" sem flag) e a contradição do 883523 (Descrição diz
  "brinquedo em miniatura", Função diz "caça") — que o modelo **harmonizou** em vez de sinalizar.

## Conclusão metodológica

O Qwen3-VL-8B chegou ao **teto de obediência a prompt**: com 25 regras concorrendo no mesmo
contexto, cada regra nova passou a custar uma regra antiga, e duas regras produziram defeitos que
não existiam. Não é falha de método — é limite de capacidade do modelo, e é um resultado
tecnicamente defensável para a banca. Consequências práticas:

- **Parar de extrair regras**; congelar o prompt v7 e ir para a avaliação (E8–E10), onde o painel
  humano julga com os critérios oficiais do projeto, não o olho editorial.
- Defeitos residuais são exatamente o que as **flags + interface de revisão humana (E11)** existem
  para capturar — o sistema nunca foi desenhado para dispensar revisão.
- Duas correções pontuais valem a pena antes de congelar (ver E8): regra 17 exige fonte explícita
  no registro para nomear a ave; regra 5 vira "cada fato de catálogo carrega marca de atribuição".

---

# ERRATA (26/08/2026) — a "alucinação da arara" não era alucinação

Durante a análise do bake-off descobriu-se que o campo **Descrição** do registro do item 210680
diz textualmente: *"Possui decoração formada por **tufos de penas de arara de cor vermelhas**,
amarradas ao fio de fibra"*. O diagnóstico da v4/v5 ("o modelo inventa a arara sem fonte") estava
**errado**: a verificação da época leu a Descrição truncada em 200 caracteres — o corte caía
exatamente em "decoração formada por t…" — e checou apenas Matéria-prima (vazia) e a observação.
O fato estava no registro que viaja no prompt; o Qwen estava ancorado, e a regra 17 não induziu
erro nenhum neste caso.

**O que a errata NÃO muda:** a conclusão de saturação do prompt permanece, sustentada pelas
regressões verificadas ("foi aquisição em" voltou em 4 itens na v4, povo sumiu de um alt,
etiqueta vazou na v5, "sobre fundo X" persistiu em 15/20 apesar da regra).

**Lição de método (para o texto da banca):** o erro nasceu de evidência truncada pela própria
ferramenta de análise — mais um caso, ao lado do gabarito das duas penas azuis, de que cada
camada da avaliação também precisa ser auditável.

## Análise da v2 (24/08/2026) — achada por código, sem revisão visual do Eduardo

O prompt v5 acertou quase tudo das 12 regras (fotografia sumiu do nível 2 em 20/20, ficha técnica virou escala, aves das penas citadas, "todo artefato vira flag" gerou 8 flags vs. 1 antes). Mas 2 problemas objetivos apareceram, achados sem precisar da revisão visual:

1. **Artefato ainda vazou para o nível 2** (Flauta 51023: "apresenta uma marcação numérica, que não é parte do objeto original") — a regra "artefato nunca aparece" só estava escrita no prompt v5 para a saída A (alt-text), não repetida para a saída B (nível 2).
2. **Atribuição ao registro sumiu em 15/20 textos** — o prompt só garantia isso via um exemplo específico (o Pote, que foi o único a manter "segundo o registro do museu"); o modelo não generalizou a regra para os outros 19 objetos, que passaram a narrar fatos do catálogo sem nenhuma marca de atribuição.

E 2 falsos positivos na própria checagem automática (não no texto do modelo): "o objeto é" estava sendo procurado em qualquer posição (pegou "...e o objeto é pequeno..." e "...do objeto é auxiliar..."), quando a regra só proíbe abrir o texto assim; "sobre fundo X" foi confundido com fotografia, quando é vocabulário legítimo de padronagem ("padrões geométricos sobre fundo bege" descreve a peça, não a foto).

**Prompt v6 fecha os 2 bugs reais** (regra do artefato repetida para as duas saídas, com exemplo errado×certo cada; atribuição virou exigência explícita, não mais dependente de um único exemplo) **e a checagem corrigiu os 2 falsos positivos** (abertura de frase-etiqueta só conta no início do texto; termos de fundo saíram da lista de "foto no nível 2"). Notebook 04 v3 no Drive, aguardando Eduardo rodar.

---

# Régua única: os cinco lotes medidos pelo mesmo critério (26/08/2026)

Cada lote foi gerado com uma versão diferente da verificação automática — inclusive com bugs
conhecidos, como o casamento de substring que confundia "aparece" com "parece". Comparar o
"n/20 sem problemas" de dois lotes medidos por réguas diferentes não diz nada, e o projeto já
tinha caído nessa armadilha uma vez (os falsos positivos da v2).

`avaliacao/checar_lote.py` aplica as checagens de hoje a qualquer lote salvo, pulando sozinho as
que dependem de campos que o lote antigo não tem. Rodando nos cinco lotes existentes:



```
Problemas por checagem — itens afetados, a mesma régua em todos os lotes

checagem                                    04             04_v2             04_v4             04_v5  05_bakeoff_gemma
----------------------------------------------------------------------------------------------------------------------
fundo_no_alt                                 5                13                14                15                 1
especulacao                                  9                 4                 3                 2                 2
frase_etiqueta                              17                 -                 2                 -                 -
nivel2_sem_atribuicao                        -                15                 -                 -                 -
flag_de_fundo                                -                 1                10                 -                 3
foto_no_nivel2                              11                 -                 1                 1                 -
artefato_no_nivel2                           5                 1                 2                 3                 -
escala_errada                                2                 4                 1                 2                 1
aquisicao_em                                 2                 2                 4                 1                 -
afirmacao_de_ausencia                        6                 -                 2                 1                 -
flag_de_ausencia                             -                 2                 6                 -                 -
miniatura_nao_declarada                      1                 1                 1                 1                 1
frase_vazia                                  -                 5                 -                 -                 -
jargao_de_foto_no_alt                        -                 -                 1                 2                 1
alt_longo                                    -                 -                 -                 2                 2
medida_fora_do_registro                      -                 1                 -                 1                 -
artefato_no_alt                              -                 -                 -                 1                 1
povo_ausente_no_alt                          -                 -                 1                 -                 -
----------------------------------------------------------------------------------------------------------------------
itens sem problema                        1/20              0/20              2/20              3/20             11/20
flags: artefato_estudio                      1                 8                18                 5                12
flags: divergencia_imagem_catalogo                 -                 -                 -                 -                 7
flags: metadado_suspeito                     -                 -                 -                 -                 1
```

**Como ler.** As linhas são checagens, não itens: um item pode falhar em várias. Três leituras:

- **O que a régua confirma do que já estava documentado:** `nivel2_sem_atribuicao` = 15 só na v2 é
  exatamente o achado registrado à época ("a atribuição sumiu em 15/20"); `frase_etiqueta` = 17 no
  primeiro lote é a "abertura em rótulo"; `fundo_no_alt` sobe 5 → 13 → 14 → 15 na linha do Qwen e
  fica em 1 no Gemma. A régua reproduz os achados que vieram de leitura humana.
- **O que ninguém estava medindo:** `escala_errada` aparece em todos os cinco lotes (2, 4, 1, 2, 1)
  e `miniatura_nao_declarada` em todos (1 cada) — defeitos que existiam desde o começo e que
  nenhuma versão da verificação enxergava, porque exigem comparar o texto com o registro.
  `jargao_de_foto_no_alt` mostra o "close-up"/"plano médio" entrando como vocabulário novo a partir
  da v4, depois que a regra proibiu "inteiro/horizontal/vertical".
- **O placar do bake-off muda de número, não de sentido:** com a régua única, Gemma **11/20** ×
  Qwen v5 **3/20** (as checagens de hoje são mais estritas; o placar original era 13 × 3).

A comparação **v5 × v6** vai usar esta mesma tabela — é o que separa o efeito do sistema
redesenhado do efeito de ter trocado a régua no meio do caminho.

---

# Lote v6 (26/08/2026) — a hipótese do Eduardo se confirma

Mesmo modelo (Qwen3-VL-8B), mesmos 20 objetos, mesma régua. Só o sistema de instruções mudou:
observação v3 em seções, redação v9 com Contrato de Fontes, rubrica v1.2, enquadramento decidido
no código. **Sem problemas: 3/20 (v5) → 11/20 (v6)** — o mesmo placar do Gemma no bake-off.

*Nota de escopo: a rodada usou o notebook v6 como estava no Drive pela manhã (rubrica 1.2). As
garantias acrescentadas na revisão técnica da tarde — escala injetada, teto de plausibilidade,
contradição isolada, alt bruto salvo — **não estavam nesta rodada**.*

## O que o redesenho resolveu

| Checagem | v5 | v6 |
|---|---|---|
| `fundo_no_alt` | 15 | **0** |
| `jargao_de_foto_no_alt` ("close-up", "plano médio") | 2 | **0** |
| `artefato_no_alt` | 1 | **0** |
| `foto_no_nivel2` | 1 | **0** |
| `artefato_no_nivel2` | 3 | 1 |
| `especulacao` | 2 | 1 |

O fundo do estúdio era o resíduo mais teimoso do projeto — sobreviveu a três versões de prompt que
o proibiam explicitamente, e neste lote foi a zero. **Errata (ver o fim desta seção): o crédito
não é da remoção da seção `FUNDO E ESTÚDIO`, que não chegou a acontecer.**

Ganho de qualidade junto: a Flauta de pã (51023) gerou uma flag de divergência **real** — "a
observação indica sete tubos, o registro menciona seis" —, o mesmo achado que o Gemma tinha feito
no bake-off. Era a primeira divergência legítima produzida pelo Qwen.

## O que o redesenho custou

1. **Frase-etiqueta voltou: 0 → 4** (665, 51023, 5146, 500322). O prompt v9 enxugou as proibições
   e a lista explícita ("PROIBIDO abrir com 'O objeto é…', anunciar 'A função é…'") saiu junto.
   Duas abrem com rótulo, duas trazem "A função é" no meio. É o preço de trocar regra negativa por
   checklist positivo — e mostra que algumas proibições não têm equivalente positivo.
2. **A observação v3 perdeu artefatos: 5 → 2 flags** — e a causa é outra, ver a errata. A
   observação **viu** os dois artefatos: a marcação numérica da Flauta está escrita em `PARTES E
   QUANTIDADES` e em `LEGIBILIDADE`, e a etiqueta do 200648 está escrita em `FUNDO E ESTÚDIO`. Nos
   dois casos a seção `ARTEFATOS` respondeu "nenhum": o modelo não repete o que já disse. A cartela
   da Faixa (665) e a etiqueta da Braçadeira (1376) continuaram detectadas.
3. **Escala: 2 → 3.** Esperado — esta rodada não tinha a escala calculada. Dos três, dois são erro
   claro (o Pote 2081 escreveu 7,3 cm de altura em vez dos 10,3 cm do bojo; a Bolsa 500322 escreveu
   83 cm, que é a altura *com a alça esticada*) e um é juízo em disputa (a Tanga 78838 escreveu 75 cm
   com cordel; o registro chama os 50 cm de "medida maior").
4. **Nível 2 mais longo: 79 → 102 palavras** em média. Ainda dentro do teto de 180.

## O que continua igual

`miniatura_nao_declarada` em 1 item, `aquisicao_em` em 1, `afirmacao_de_ausencia` em 1. E a
vantagem do Gemma em **flags de divergência (7 × 1)** não foi tocada pelo redesenho — é diferença
de modelo, não de instrução. O bake-off continua de pé.

---

# Terceira revisão editorial (26/08/2026) — o lote v6, lido pelo Eduardo

Oito observações sobre o lote v6, todas confirmadas nos dados. **Três delas a régua automática
não estava vendo** — o "11/20 sem problemas" do v6 era otimista porque a régua era cega para elas.

| # | Observação do Eduardo | O que os dados mostram | Onde a correção entra |
|---|---|---|---|
| 1 | Repetição de "segundo o registro do museu" | A fórmula abre **20 dos 20** textos, e 13 têm 2+ marcas. É papagaio de exemplo: era o primeiro exemplo do prompt | **Código**: 5 fórmulas em rodízio por item. Prompt: uma marca por bloco de fatos, não por fato |
| 2 | Descrições longas demais | Máximo 143 palavras; o teto do prompt era 180 | Teto baixado para **120** no prompt, checagem em 140 |
| 3 | Padrão geométrico descrito como letras ("G ou C invertidos") | Confirmado no 84811 — e são **gregas**, termo que o glossário do RAG entrega. Também "em forma de coroa" (665) e "forma de pequena esteira" (500179, regressão da regra 14) | Prompt: padrão sempre pela geometria, nunca por semelhança. Régua: checagem `padrao_por_analogia` |
| 4 | "pequeno rótulo branco" no #6 (1376) | Confirmado — e a régua **não pegava**: "rótulo", "inscrição" e "tombo" faltavam na lista de artefatos | Régua corrigida |
| 5 | Função óbvia | 4 casos: flauta = "instrumento musical", pulseira = "cingir o pulso", bolsa = "guardar e transportar" | Prompt: função só quando diz algo que o **nome** já não diz. Régua: `funcao_obvia` |
| 6 | Afirmação de ausência | **14 dos 20** textos. A régua acusava **1** — cobria seis frases fixas | Régua com padrão amplo (exceto o hedge legítimo "não identificado", que vem do registro). Prompt: nem a ausência de informação vira frase |
| 7 | Contagem errada de tubos no #3 | A observação contou sete, o registro enumera **seis** medidas de tubo. A flag de divergência saiu ✓, mas o texto afirmou "sete". Enumeração de partes existe em **1 dos 555** itens — não compensa código | Prompt: conflito de QUANTIDADE → o texto não escreve número |
| 8 | Imprecisão das cores no alt do #2 (665) | O alt cita preto, amarelo e vermelho; a observação viu também **azul** — as duas penas azuis, o achado fundador do projeto — e o registro não as menciona. Não virou flag | Prompt: todas as cores que a observação nomeia. **Código**: cor vista e não registrada vira flag automática |

## O item 8 fecha um ciclo

A comparação automática entre as cores da observação e as do registro **reencontra sozinha as duas
penas azuis da Faixa Kalapalo** — o caso em que o modelo corrigiu o gabarito humano, em agosto,
por leitura de uma pessoa. Agora é uma flag que o código gera. Dispara em 3 dos 20 itens (665,
1376, 1366), sempre como pedido de conferência: só considera cores informativas — bege, marrom e
cinza são a cor natural do material, que o catálogo nunca nomeia — e só quando o registro
descreve alguma cor.

## O retrato honesto, com a régua corrigida

Com as checagens novas ligadas, os três lotes caem para **1/20 sem problemas**. O número não diz
que a qualidade caiu: diz que a régua anterior era cega para defeitos presentes em todos eles.
`atribuicao_repetida` atinge 11, 15 e 16 dos 20 textos de v5, v6 e Gemma; `afirmacao_de_ausencia`
atinge 7, 12 e 1. São defeitos que existiam desde o primeiro lote e que ninguém tinha medido.

O "sem problemas" deixa de ser a métrica útil quando a régua tem vinte checagens — qualquer
tropeço desqualifica o item inteiro. A comparação passa a ser a **tabela por checagem**.

---

# Lote v7 (27/08/2026) — o prompt assumiu o que o código garantia, e a régua nova é outra

Rodado com o notebook v7 (prompt de redação v10 + garantias em código + as correções dos 8 achados
da terceira revisão). **Atenção ao ler o placar**: a régua desta rodada tem as checagens novas dos
8 achados (`atribuicao_repetida`, `funcao_obvia`, `padrao_por_analogia`, ausências endurecidas), que
punem TODOS os lotes retroativamente — por isso o "itens sem problema" despencou em todas as
colunas (v6: 11/20 na régua antiga → 1/20 nesta). A comparação honesta é por checagem, e pela
média: **v5 2,7 → v6 2,5 → v7 2,2 problemas/item** (Gemma 2,0, ainda com o prompt antigo).

## O número mais importante da rodada

**O pós-processamento do fundo agiu em 0/20 alts.** Na v5, "sobre fundo X" estava em 15 de 20; no
v7 o prompt resolveu sozinho os 20 — o regex que existia de rede de segurança ficou ocioso. É a
resposta à pergunta que o alt bruto foi criado para responder: o código não está maquiando o texto;
o texto que a pessoa cega ouve saiu inteiro do modelo.

## O que zerou (e por quê)

| Checagem | v5 | v7 | O que mudou |
|---|---|---|---|
| `fundo_no_alt` | 15 | **0** | prompt v10 (pós-processamento não precisou agir) |
| `escala_errada` | 2 | **0** | escala calculada em código e injetada |
| `miniatura_nao_declarada` | 1 | **0** | idem — o Pote agora diz "miniatura" |
| `atribuicao_repetida` | 11 | **0** | marca variada por item (mas ver regressão 1) |
| `frase_etiqueta`, `especulacao`, `jargao_de_foto` | — | **0** | regras reafirmadas no v10 |
| `artefato_visto_sem_flag` | — | **0** | varredura de todas as seções (4/4 itens, como validado) |

E as **flags de cor** estrearam funcionando: a Faixa 665 gerou "a foto mostra azul e o registro
nomeia só amarelo, preto, vermelho" — **as penas azuis do smoke test, redescobertas pelo Qwen**
(antes só o Gemma as tinha achado). Braçadeiras 1376 (laranja) e 1366 (branco/laranja) idem. O
abano de 290 cm virou `metadado_suspeito` pela primeira vez (via código). A contradição
brinquedo×caça do 883523 seguiu não detectada **mesmo como pergunta isolada** — o modelo harmonizou
de novo ("não há contradição, pois..."); este resíduo fica para a revisão humana.

## Duas regressões, as duas nascidas das correções

1. **A marca de atribuição saiu do texto audível (13/20).** A correção do achado nº 1 (repetição de
   "segundo o registro do museu") pediu ao modelo a marca variada num campo próprio
   (`marca_atribuicao`) — e o modelo entendeu que o campo substitui o texto: escolheu formulações
   variadas ("conforme o catálogo do museu", "de acordo com a ficha do museu"...), preencheu o
   campo e **escreveu o nível 2 sem marca nenhuma**. Quem ouve perdeu a fronteira de auditoria — a
   contribuição central do projeto. Correção candidata (v8): o CÓDIGO sorteia a formulação por item
   e a injeta no prompt como variável ("use exatamente esta marca: ..."), como já se faz com
   enquadramento e escala — variedade determinística, marca dentro do texto.
2. **O teto de 30 palavras quebrou em 10/20 alts (31–53).** As exigências novas de cor e material
   somaram palavras e o limite perdeu a disputa. Correção candidata: reafirmar o teto como
   prioridade que vence qualquer outra exigência da seção A.

Persistem: `afirmacao_de_ausencia` (9 — "sem pintura", "etiqueta sem caracteres legíveis"; inclui
1 falso positivo da régua: o 78838 colou o texto de Dimensões do registro, com "(sem cordel)" —
defeito real, mas de ficha técnica, não de ausência) e `funcao_obvia` (4). Artefato vazou para o
texto em itens onde a menção vive em PARTES/LEGIBILIDADE, que continuam viajando para a redação.

---

# Quarta revisão editorial (27/08/2026) — lote v7, cards #1–#3 (parcial) e a métrica que faltava

O Eduardo revisou os três primeiros cards do v7 e interrompeu com uma constatação: **defeitos já
apontados em revisões anteriores estão voltando** — e o veredito otimista da régua ("2,2
problemas/item, avanço") não os via. O pedido: reunir TODAS as revisões e usá-las como métrica.
Todos os achados foram conferidos no dado bruto:

- **#1 Pote 9196:** "marrom-escuríssimo" (o superlativo da 2ª revisão, de volta); "decoração em
  relevo" — **invenção**: o registro diz "pintados"; "cruzes e elementos que lembram raios"
  (analogia + as cruzes não conferidas desde a 1ª revisão); "cerâmica bege-clara" (cor de material
  natural, regra 10); **"possui uma única alça lateral" — alucinação** (o pote não tem alça; o v6
  já a tinha); "borda extrovertida" e "globular" (jargão, regra 3 — o glossário manda "boca que se
  abre para fora"); e a miniatura de 6 cm deveria pedir conferência como o abano de 290 cm.
- **#2 Faixa 665:** o registro diz penas **"costuradas em couro de onça"**; o texto escreveu
  "bordadas" — técnica errada, termo sem fonte. E o alt segue sem o azul (achado nº 8 da 3ª).
- **#3 Flauta 51023:** "sete tubos" pela quarta rodada seguida — o registro diz **"seis tubos ...
  dispostos paralelamente"**. Duas decisões novas do Eduardo: **a contagem do catálogo prevalece
  sempre** (substitui a política da 3ª revisão, que mandava omitir o número) e "paralelamente" — que
  é palavra do próprio registro — é o termo certo para a disposição.

## O gabarito editorial vira métrica permanente

`avaliacao/gabarito_editorial.json` consolida as quatro revisões em 29 padrões verificáveis
(5 globais + 24 por item); `avaliacao/checar_gabarito.py` mede qualquer lote contra eles.
A métrica é **reincidência**: defeito já apontado que volta. Nos sete lotes:

| Lote | v1 | v2 | v4 | v5 | Gemma | v6 | v7 |
|---|---|---|---|---|---|---|---|
| Defeitos distintos presentes (de 29) | 12 | 17 | **8** | **8** | 9 | 14 | **14** |

**A leitura muda o veredito do v7.** Na métrica do gabarito, v7 = v6, e ambos estão PIORES que
v4/v5. O mecanismo é o teto de saturação visto de outro ângulo: o prompt de 25 regras (v4/v5)
segurava jargão, cor de material natural e analogias **porque as proibia por extenso**; o
redesenho enxuto (v9/v10) ganhou nos padrões estruturais (fundo, escala, atribuição — o que a
régua genérica mede) e **devolveu o que tinha saído do prompt**. As duas métricas discordam porque
medem coisas diferentes — e a métrica editorial é a que decide qualidade de texto público.

Defeitos presentes em TODOS os sete lotes: **"cabo" na zarabatana** (regra 24, nunca cumprida por
nenhum modelo sob nenhum prompt), **contradição brinquedo×caça sem flag**, **dimensão pequena sem
flag**. Quase-onipresentes: o azul fora do alt da Faixa (5/7) e os sete tubos (4 lotes seguidos).
Alucinações novas que o gabarito agora vigia: relevo (v7), alça (v6+v7), bordadas (v7).

## O que já virou código nesta sessão

1. **Dimensão atipicamente pequena → flag** `metadado_suspeito` ("miniatura genuína ou erro de
   registro; conferir") — mesma lógica do teto de 290 cm, agora com piso.
2. **Contagem do registro prevalece**: `contagens()` extrai pares número+substantivo da Descrição
   ("seis tubos") e a régua acusa `contagem_diverge_do_registro` quando o texto conta diferente —
   dispara na Flauta em v5, v6, Gemma e v7. A injeção no prompt ("CONTAGEM DO REGISTRO: ...")
   fica para o próximo notebook, se houver.
3. O gabarito entra no fluxo de fechamento de lote junto com a régua.

**Nota de método:** ao escrever o gabarito, o padrão `\b` em JSON virou backspace e silenciou duas
linhas da matriz — o MESMO bug do RE_ANALOGIA de ontem, pego porque "cabo ausente em 7/7 lotes"
era bom demais. Terceira aparição da classe; padrões novos não usam mais barra invertida.

## A matriz completa

```
GABARITO EDITORIAL — reincidência dos defeitos apontados pelo Eduardo, lote a lote
(número = itens afetados; '·' = defeito ausente; conferir = fidelidade pendente de olho humano)

defeito                                     v1      v2      v4      v5   gemma      v6      v7
----------------------------------------------------------------------------------------------
[global] cor_superlativa                     1       ·       2       2       ·       ·       1
[global] analogia_lembra                     3       1       ·       ·       1       1       1
[global] jargao_catalogo                     3       ·       1       ·       1       2       3
[global] cor_material_natural                1       1       ·       ·       ·       2       3
[global] ficha_tecnica                      17       ·       7      10      15       5       6
9196 decoracao_em_relevo                     ·       ·       ·       ·       ·       ·       1
9196 alca_inexistente                        ·       ·       ·       ·       ·       1       1
9196 cruzes_nao_conferidas (conferir)        1       ·       ·       ·       ·       ·       1
9196 dimensao_pequena_sem_flag               1       1       1       1       1       1       1
665 rebatizado_chapeu                        1       ·       ·       ·       ·       ·       ·
665 bordado_nao_costurado                    ·       ·       ·       ·       ·       ·       1
665 coroa_analogia                           ·       ·       ·       ·       ·       1       ·
665 azul_ausente_do_alt                      ·       1       1       1       ·       1       1
51023 sete_tubos                             ·       ·       ·       1       1       1       1
63283 trancado_liso                          1       ·       ·       ·       ·       ·       ·
63283 angulo_agudo                           ·       1       ·       ·       ·       ·       ·
84811 coracoes_flores                        ·       1       ·       ·       ·       ·       ·
84811 letras_G_C                             ·       ·       ·       ·       ·       1       ·
84811 bordas_de_pulseira                     1       1       1       1       ·       ·       ·
883523 cabo_de_zarabatana                    1       1       1       1       1       1       1
883523 contradicao_sem_flag                  1       1       1       1       1       1       1
5011 tortual                                 ·       1       ·       ·       1       1       ·
200648 recipiente_antes_do_conteudo          ·       1       ·       ·       ·       ·       ·
210680 sons_ritmados                         ·       1       ·       ·       ·       ·       ·
500179 esteira_analogia                      ·       1       ·       ·       1       1       ·
3411 inteiro_horizontal                      ·       1       ·       ·       ·       ·       ·
905 pequena_para_uso                         ·       1       ·       ·       ·       ·       ·
500322 bordas_suaves                         ·       1       ·       ·       ·       ·       ·
1376 curva_suave_foto                        ·       1       ·       ·       ·       ·       ·
----------------------------------------------------------------------------------------------
TOTAL de reincidências                      32      17      15      18      23      20      23
defeitos distintos presentes             12/29   17/29    8/29    8/29    9/29   14/29   14/29
```

---

# Lote v8 (27/08/2026) — as políticas funcionaram; sobrou uma família de defeito

Rodado com as 8 políticas da adjudicação + validação com retry. **Régua mecânica: 3,1 → 0,5
problemas/item (11/20 sem problema); gabarito de reincidência: 25 → 2 defeitos distintos.**
Antes do veredito, a revisão dos resíduos encontrou e corrigiu **4 falsos positivos da régua**
(lição repetida: o avaliador também se avalia): a fórmula "de acordo com a ficha do museu" —
sorteada pelo nosso próprio rodízio — não era reconhecida como atribuição; "padrões gregos"
não casava com o padrão exigido "grega"; o "em forma de X" da Panela vem do próprio registro
(exceção que a política catálogo-manda prevê, agora codificada); e o item sem resolução era
punido por checagens de texto que a política mandou não gerar.

## O que as políticas entregaram (medido)

- **Zeraram**: fundo, medida/ausência no alt, molde de variável, colagem de registro, escala
  errada, contagem divergente, atribuição repetida, afirmações de ausência, alt longo,
  jargão de foto, especulação, artefato nos textos, estado sem fonte, "aquisição em".
- **Quarentena em ação**: 4 medidas suspeitas fora do texto (9196, 63283, 1376, 1366); o azul
  da Faixa e o laranja das Braçadeiras em flag e fora do texto; as cores do registro dentro.
- **Contagem injetada**: a Flauta finalmente diz **seis tubos** — defeito de 4 lotes, resolvido.
- **"Costuradas"** na Faixa (catálogo-manda) ✓; **espinha-de-peixe** no Abano ✓ (2×); ritual
  sem fonte da Braçadeira sumiu ✓; o Pião 5146 foi barrado pelo porteiro de resolução e virou
  flag de dataset ✓.
- **Retry**: 5 textos precisaram da segunda volta — o número que mede o que o prompt sozinho
  não segura.

## O que sobrou (9 problemas, uma família dominante)

1. **Jargão do catálogo não traduzido** — a única reincidência real do gabarito: "globular"
   (9196, 2081), "extrovertida" (9196; 905 só no alt — o nível 2 traduziu "boca que se abre
   para fora"), "zoomorfos" sem virar "figuras de animais" (4156). O glossário entrega a
   tradução; o 8B usa às vezes.
2. **Função óbvia** (5): o modelo escreveu até os exemplos proibidos textualmente no prompt
   ("remo... deslocar", "panela... cozinhar e servir").
3. **Povo ausente do alt** (2) e **observação sem linha ENQUADRAMENTO válida** (2, fallback
   correto nos dois).

## Encaminhamento — v9, mudança de UMA função

Os resíduos 1–3 têm a mesma causa: o validador do retry não os cobria. O **v9 muda só a função
`validar_rascunho`** (prompt e observação intocados): jargão conhecido, povo no alt e função
óbvia entram na checagem, e o retry cobra a correção. Se o padrão do v8 se repetir (o retry
resolveu o que cobria), o critério de saída — zero reincidência adjudicada — fica ao alcance.

---

# 6ª adjudicação (27/08/2026) — revisão editorial do Eduardo sobre o v8

Revisão card a card do lote v8, com decisões novas de política. Cada achado foi conferido no dado
bruto antes de virar regra:

- **Global — frases em minúscula**: a marca de atribuição sorteada em minúscula ("de acordo com a
  ficha do museu, foi adquirido...") abria frase sem maiúscula. Correção em CÓDIGO (tipografia é
  determinística): `capitalizar_frases()` no pós-processamento, e a régua ganhou `frase_em_minuscula`.
- **Global — "não existe base bege" (erro grave)**: material natural (madeira, fibra, argila,
  algodão, couro) NUNCA recebe nome de cor — no máximo "clara/escura"; procedência (tipo de
  madeira/fibra) só quando o catálogo der. Isso aposenta de vez a velha muleta "sobre a argila
  bege". Régua nova `cor_em_material_natural` (exceção: cor de pintura/tingimento).
- **#1 Pote**: povo fora do nível 2 → política: povo, ano de aquisição e origem SEMPRE entram na
  descrição quando o registro os tem (régua: `povo/ano/origem_ausente_no_n2`).
- **#2 Faixa**: a estrutura sumiu — o ouvinte imaginou base de couro aparente, quando o catálogo
  diz penas COSTURADAS no couro (base coberta). Caso em que o catálogo explica a imagem melhor que
  o alt: a construção do catálogo estrutura a descrição (gabarito: exige "costurad").
- **#4 Abano**: o alt citou a roseta azul/verde, que NÃO está visível na foto (detalhe da trama) —
  elemento só-catálogo nunca entra no alt, apenas na descrição (gabarito: proibe_alt azul|verde).
- **#5 Tanga**: "miçangas sobre linha" → miçangas são "confeccionadas com [linha]"; e a repetição
  literal alt↔descrição voltou ("franjas e cordel de amarração" igual nos dois). Régua nova
  `repeticao_alt_n2` (5 palavras idênticas).
- **#6 Braçadeira**: penas "compostas por", nunca "sobre"; aquisição/origem faltando — conferido:
  **o texto estava TRUNCADO** (terminava na marca de atribuição; o 200648 também). Régua nova
  `nivel2_truncado` + validador exige os fatos depois da marca. E a cor da ETIQUETA (branco) não
  pode gerar flag de cor — `cores_divergentes` agora exclui frases com artefato.
- **#8 Zarabatana**: cores enumeradas soltas perdem o vínculo com as partes → política: cor presa
  à parte que a exibe ("cabo escuro, bocal claro").
- **#11 Argila**: procedência (Igarapé Ucuqui) e tipo ("dekai") sumiram — catálogo manda, entram;
  e o contenedor (tubo, tampa) fica SÓ no alt — a descrição é do conteúdo (régua:
  `contenedor_no_nivel2` para Etnobotânica; gabarito exige dekai/ucuqui).
- **#12 Flauta de osso**: "osso" 3× — redundância (regra 22 reforçada no prompt).
- **#14 Abano de talo — checagem de procedência RESOLVIDA**: "pá para virar beiju e atiçar fogo"
  TEM fonte — é o campo **Função** do registro, textual. A confusão era da TABELA comparativa, que
  só mostrava o campo Descrição como baseline; agora mostra Descrição + Função + Matéria-prima.
- **#20 Bolsa — recalibração de `funcao_obvia`**: função descrita no campo Função do registro PODE
  entrar (catálogo manda) — a checagem só dispara quando a função não tem fonte. Nota: pela mesma
  lógica, remo/panela/flauta (que têm Função no registro) deixam de ser defeito; se o Eduardo
  preferir manter o veto para esses casos, a checagem volta a ser incondicional.

**Notebook v10** (prompt v13): todas as políticas acima + capitalização em código + validador
ampliado (cor-material, povo/ano/origem na descrição, truncamento, repetição do alt, contenedor).
O v9 fica superado sem rodar — suas mudanças estão contidas no v10.
