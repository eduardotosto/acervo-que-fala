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
