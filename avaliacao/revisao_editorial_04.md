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
