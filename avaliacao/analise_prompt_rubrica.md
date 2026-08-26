# Análise: erros induzidos pelo próprio prompt e pela rubrica

*26/08/2026 · disparada pela observação do Eduardo antes do julgamento A/B: "alguns erros estão
sendo gerados por instruções e regras mal desenhadas" — confirmada com evidência abaixo.*

## 1. Evidência: três mecanismos de erro induzido

### 1a. Papagaio de exemplo — frases concretas do prompt vazam para a saída

O prompt v8 ensina regras COM exemplos literais. Os modelos copiam o exemplo, não a regra:

| Frase de exemplo no prompt | Vazou para (Qwen v5) | Vazou para (Gemma) |
|---|---|---|
| "sobre a argila bege" | Pote 9196 ✓cerâmica, **Fuso 5011 (madeira!)**, **Bolsa 500322 (fio de tucum!)** | Pote 9196, Pote 2081, Panela 905 ✓, **Pulseira 84811 (miçangas!)** |
| "em cascata" | Flauta 51023 | Flauta 51023 |
| "penas vermelhas e amarelas de arara" | Braçadeira 1366 (verbatim) | — |
| "cerca de 40 cm" | 210680 (registro: 41 cm — talvez legítimo), **500179** | — |

O caso da Bolsa/Fuso/Pulseira é prova: a frase aparece onde o material nem é argila.
**"Sobre a argila bege" sem contexto do que está sobre** — o incômodo original do Eduardo — é
o exemplo do prompt colado no lugar da descrição.

### 1b. Palavra-gatilho sem negação — o "Detalhe de" em excesso

O Gemma marcou "Detalhe de" em 13/20 alts. Nos itens 9196, 1366 e 5146, a observação afirma
textualmente **"o objeto aparece inteiro"** — e ainda assim o alt saiu como detalhe. A observação
desses itens contém as palavras "close"/"detalhe" em contexto NEGADO ("não há close-up nem
detalhe isolado"); o redator associa por palavra, sem processar a negação. A checagem automática
do projeto teve a mesma doença em outra escala ("de**coraç**ão" → falso positivo de "coração";
"flor**ais**" → falso positivo de "LoRA" numa busca). Padrão raso de texto é um modo de falha
do sistema inteiro, não de um modelo.

### 1c. Sobrecarga de regra negativa — a saturação já documentada

25+ regras majoritariamente negativas ("proibido X", "nunca Y") competindo no mesmo contexto:
regressões medidas nas v4/v5 (seção anterior deste arquivo). Regra negativa também **planta a
palavra proibida no contexto** — dizer "nunca escreva 'porte médio'" coloca "porte médio" na
frente do modelo 20 vezes por lote.

## 2. Achado estrutural: as regras "gerais" da rubrica NUNCA chegam ao modelo

A função `recuperar()` **pula os trechos de categoria "geral"** (por desenho — eles deveriam
viver no prompt). Consequência: os trechos geral-01…geral-11 da rubrica v1.1 são peso morto em
runtime — documentação que parece regra ativa. A rubrica só entrega ao modelo os trechos de
categoria (cerâmica, plumária…) e o glossário, k=3 por item.

## 3. Proposta — prompt v9: um contrato epistêmico positivo antes das regras de estilo

O pedido do Eduardo: garantir o básico — não inventar, não especular, registrar inconsistências,
e **eliminar o que tem confiança baixa**. Redação proposta (abre o prompt, antes de A/B/C):

> **CONTRATO DE FONTES — vale para as duas descrições:**
> 1. Cada informação que você escrever precisa de uma fonte: ou está VISÍVEL na observação, ou
>    está ESCRITA no registro (e então leva atribuição), ou é vocabulário das diretrizes. Se você
>    não consegue apontar a fonte, NÃO ESCREVA — omitir é sempre permitido; inventar, nunca.
>    Um texto mais curto e todo verificável vale mais que um texto completo com um palpite.
> 2. Incerteza se herda: se a observação hesita ("parece", "talvez", "possivelmente"), a
>    informação OU sai do texto OU vira o termo genérico da categoria — nunca vira afirmação.
> 3. Divergência não se resolve no texto: quando observação e registro conflitam (nome, cor,
>    quantidade, material, dimensão), você NÃO escolhe um lado nem harmoniza — registra a flag
>    `divergencia_imagem_catalogo` e, no texto, o fato não-visível fica com o registro e a
>    aparência fica com a observação.
> 4. Os exemplos deste prompt ilustram a FORMA das frases. NUNCA copie as palavras de um
>    exemplo: substitua sempre pelo conteúdo do objeto em questão.

E duas mudanças mecânicas que tiram decisões semânticas do redator:

5. **Enquadramento decidido na observação, não na redação.** O prompt de observação passa a
   terminar com duas linhas estruturadas, sempre presentes:
   `ENQUADRAMENTO: inteiro` ou `ENQUADRAMENTO: detalhe`
   `ARTEFATOS: [lista, ou "nenhum"]`
   A redação obedece mecanicamente: "Detalhe de..." se e somente se `ENQUADRAMENTO: detalhe`;
   cada item de `ARTEFATOS` vira uma flag `artefato_estudio`. (Elimina o 1b por construção.)
6. **Exemplos com lacunas.** Onde um exemplo for indispensável, usar placeholder:
   "sobre a [material] [cor]" em vez de "sobre a argila bege". (Elimina o 1a por construção.)

As 25 regras de estilo continuam valendo, mas: agrupadas por saída, enxugadas, sem frases
copiáveis, e com as proibições formuladas positivamente onde possível ("escala = a maior
dimensão aproximada" em vez de listar todas as frases vazias proibidas).

## 4. Proposta — rubrica v1.2

- **Remover os trechos "geral"** (mortos em runtime); o conteúdo deles já vive no prompt. A
  versão de documentação vai para `docs/` como guia editorial do projeto.
- Manter categoria + glossário (o que o RAG realmente entrega), revisando cada trecho pelos
  critérios do contrato: sem frase de exemplo copiável, sem lista de palavras proibidas.

## 5. O que isto NÃO invalida

O bake-off atual segue comparável: os dois modelos rodaram com o MESMO prompt v8 — o handicap
foi idêntico. O julgamento cego do Eduardo continua válido para escolher o redator; o prompt v9
entra depois, para o vencedor.

## 6. Encaminhamento

1. Eduardo revisa o prompt v8 (íntegra abaixo) e a rubrica (`dados/rubrica/rubrica.json`),
   marcando o que mais quiser mudar;
2. Julgamento A/B cego (página já gerada);
3. Prompt v9 + rubrica v1.2 escritos com o contrato acima, para o redator vencedor;
4. E8 roda as métricas nos 40 casos já com o conjunto congelado.

---

## Anexo — prompt v8 na íntegra (como viajou nos dois modelos)

```
Você escreve descrições de acessibilidade para o acervo digital de um museu, lidas por pessoas cegas via leitor de tela. Escreva em linguagem cotidiana — NUNCA jargão de catálogo ('globular' → 'arredondado'), NUNCA palavras inventadas; termo técnico só se vier do registro ou do glossário. Só afirmações verificáveis: proibido 'sugere', 'parece', 'parecendo X ou Y', 'possivelmente'; proibido inferir uso ou desgaste ('sinais de uso', 'uso frequente'); proibido juízo estético ('composição rica') e frases vazias ('porte médio', 'forma funcional', 'comprimento para uso prático'). Não repita a mesma palavra-chave várias vezes.

OBSERVAÇÃO VISUAL DA FOTOGRAFIA (única fonte do que é visível):
{observacao}

REGISTRO DO MUSEU (fatos do catálogo — o título nomeia o objeto):
{registro}

DIRETRIZES PARA ESTE TIPO DE OBJETO (recuperadas da base do projeto):
{diretrizes}

PRODUZA TRÊS SAÍDAS:

A) alt_text — uma frase, máx. 30 palavras, descrevendo a FOTOGRAFIA. Começa pelo objeto (nomeado pelo TÍTULO do registro — nunca rebatize pela aparência) e pelo povo — o nome do povo SEMPRE aparece no alt_text. Enquadramento: marque 'Detalhe de...' SÓ quando a foto mostra claramente um fragmento; objeto que encosta ou sangra nas margens conta como completo; NUNCA escreva 'inteiro', 'horizontal' ou 'vertical' — não informam. O fundo do estúdio NUNCA aparece nem empresta cor ao objeto; quando a cor de base é da própria peça, nomeie pelo material ('sobre a argila bege'), nunca como 'fundo'. Cores: nomeie onde informam (penas, miçangas, pinturas — proibido 'colorido', 'tons variados'); em material natural sem tingimento, nomeie o MATERIAL em vez da cor. Padrões têm FORMA além de cor (faixas, xadrez, losangos); padrão abstrato é 'geométrico' — nunca vire flores ou corações. Conte partes distinguíveis (ex.: 'sete tubos'). Penas: par cor+ave SOMENTE quando a Matéria-prima ou a Descrição do registro NOMEIA a ave ('penas vermelhas e amarelas de arara'); se o registro não nomeia nenhuma ave, descreva só as cores — citar espécie sem fonte é o pior erro possível. Na dúvida de material: termo genérico OU a matéria-prima do registro — nunca 'parecendo cerâmica ou madeira'. ARTEFATO DE ESTÚDIO/INVENTÁRIO NUNCA APARECE (vale também para a saída B) — ERRADO: '...com marcação numérica na base.' CERTO: terminar a frase sem citar a marcação (ela vira flag).

B) descricao_objeto — descreve o OBJETO, não a fotografia: PROIBIDO posição, inclinação, fundo, enquadramento ou a foto; relação que depende do ponto de vista ('mais curtos no topo') vira relação da própria peça ('em cascata', 'decrescentes'). PROIBIDO citar artefato de estúdio/inventário — ERRADO: 'A base apresenta uma marcação numérica, que não é parte do objeto original.' CERTO: a frase termina sem citar a marcação (ela já virou flag). Em amostras e conteúdos (argila, resina, sementes), o CONTEÚDO vem antes do recipiente. Dois parágrafos:
   1º: abre direto com o objeto e sua função — mas só função que ACRESCENTA (caça, ritual, preparo de alimentos); nunca o óbvio ('pulseira usada no pulso'). Ex.: 'Um pote cerâmico Karajá que, segundo o registro do museu, era usado no preparo e serviço de alimentos.' PROIBIDO abrir com 'O objeto é...', 'Trata-se de...' ou anunciar 'A função é...'. Depois, a aparência: formas, materiais e padrões em palavras comuns, informações do mesmo gênero agrupadas (material dito UMA vez, num lugar só).
   2º: os demais fatos do catálogo. Escala: a MAIOR dimensão aproximada ('cerca de 40 cm de comprimento'); miniatura é declarada ('miniatura de 6 cm, cabe na palma da mão'); escala óbvia (pulseira) pode ser omitida. Aves das penas: detalhe cor a cor conforme o registro. Significado cultural: só se estiver no registro.
   REGRA DE ATRIBUIÇÃO (vale para o texto todo): TODO fato que vem do catálogo e NÃO é visível na foto — função, técnica, origem, ano, medidas, decorações que o registro descreve — carrega uma marca de atribuição na própria frase, com formulação variada: 'segundo o registro do museu', 'o registro informa', 'conforme o catálogo', 'de acordo com o registro'. O que a observação viu não leva marca. Sem a marca, quem ouve não distingue o que a foto mostra do que o museu documentou. Datas sempre em frase natural: 'adquirido em 1977' — NUNCA 'foi aquisição em'.
   NUNCA afirme ausências ('sem etiquetas', 'não há sinais de...') — o que não existe simplesmente não aparece no texto.

C) flags — lista do que precisa de revisão humana:
   - tipo 'artefato_estudio': etiqueta, numeração, cartela, régua ou suporte que a observação notou — cada um vira uma flag. O FUNDO LISO DE ESTÚDIO NÃO É ARTEFATO e não vira flag. Uma flag descreve o que EXISTE — nunca escreva flag afirmando ausência ('sem etiquetas visíveis');
   - tipo 'divergencia_imagem_catalogo': algo claramente visível que o registro não menciona, ou objeto visto diferente do que o título nomeia (nesse caso, use o título no texto e registre a divergência aqui);
   - tipo 'metadado_suspeito': valor do registro que parece improvável (dimensão absurda para o tipo de objeto, data impossível) ou contradição entre campos do registro (ex.: Descrição diz 'brinquedo em miniatura' e Função diz 'utilizado para caça').
   Lista vazia [] se não houver nada.

Responda APENAS com JSON: {{"alt_text": "...", "descricao_objeto": "...", "flags": [{{"tipo": "...", "detalhe": "..."}}]}}

