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

## Análise da v2 (24/08/2026) — achada por código, sem revisão visual do Eduardo

O prompt v5 acertou quase tudo das 12 regras (fotografia sumiu do nível 2 em 20/20, ficha técnica virou escala, aves das penas citadas, "todo artefato vira flag" gerou 8 flags vs. 1 antes). Mas 2 problemas objetivos apareceram, achados sem precisar da revisão visual:

1. **Artefato ainda vazou para o nível 2** (Flauta 51023: "apresenta uma marcação numérica, que não é parte do objeto original") — a regra "artefato nunca aparece" só estava escrita no prompt v5 para a saída A (alt-text), não repetida para a saída B (nível 2).
2. **Atribuição ao registro sumiu em 15/20 textos** — o prompt só garantia isso via um exemplo específico (o Pote, que foi o único a manter "segundo o registro do museu"); o modelo não generalizou a regra para os outros 19 objetos, que passaram a narrar fatos do catálogo sem nenhuma marca de atribuição.

E 2 falsos positivos na própria checagem automática (não no texto do modelo): "o objeto é" estava sendo procurado em qualquer posição (pegou "...e o objeto é pequeno..." e "...do objeto é auxiliar..."), quando a regra só proíbe abrir o texto assim; "sobre fundo X" foi confundido com fotografia, quando é vocabulário legítimo de padronagem ("padrões geométricos sobre fundo bege" descreve a peça, não a foto).

**Prompt v6 fecha os 2 bugs reais** (regra do artefato repetida para as duas saídas, com exemplo errado×certo cada; atribuição virou exigência explícita, não mais dependente de um único exemplo) **e a checagem corrigiu os 2 falsos positivos** (abertura de frase-etiqueta só conta no início do texto; termos de fundo saíram da lista de "foto no nível 2"). Notebook 04 v3 no Drive, aguardando Eduardo rodar.
