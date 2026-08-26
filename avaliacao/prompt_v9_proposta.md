# Proposta para revisão: observação v3 + redação v9 + divisão prompt/rubrica/código

*26/08/2026 · para revisão do Eduardo ANTES de gerar o novo notebook. Contexto e evidências em
`analise_prompt_rubrica.md`. Após aprovação: novo teste no Qwen com este conjunto.*

## A divisão de trabalho (o sistema inteiro, não só o prompt)

| Camada | O que carrega | Por quê |
|---|---|---|
| **Prompt de observação v3** | Observação em SEÇÕES nomeadas (todas parseáveis), com contexto guardado ("reconhecer materiais, não adivinhar significado") | Decisões visuais são tomadas por quem vê a foto; seções eliminam divagação e pergunta que induz resposta |
| **Prompt de redação v9** | Contrato de fontes + regras universais, hierarquizadas | Regra que vale para todo objeto não pode depender de sorteio do RAG |
| **Rubrica v1.2 (RAG)** | Só diretrizes por categoria + glossário | O que o `recuperar()` realmente entrega (k=3 por semelhança) |
| **Código do notebook** | Garantias mecânicas: cada item de `ARTEFATOS:` vira flag automaticamente; parse do `ENQUADRAMENTO:` injetado no prompt; pós-processamento remove "sobre fundo [cor]" residual do alt | O que precisa de 100% de garantia não se pede a modelo |
| **docs (git)** | As 25 regras editoriais com os casos que as originaram (`revisao_editorial_04.md`) | Documentação para a banca, não insumo de runtime |

## Prompt de observação v3

*Revisado em 26/08 após o feedback do Eduardo: (a) ganhou contexto do acervo COM guarda explícita
— serve para reconhecer materiais e estúdio, nunca para adivinhar significado (a falta da guarda
gerou a divagação "aves como pavões ou feras ornamentais" na braçadeira); (b) a linha "incluindo
bordas, faixas e acabamentos" era pergunta que induz resposta (remendo da E4 generalizado) — saiu,
substituída por seções neutras com "somente se existirem"; (c) estrutura em seções nomeadas, todas
parseáveis pelo código.*

```
Você está diante da fotografia de um objeto do acervo de um museu — objetos
etnográficos de povos indígenas do Brasil, fotografados em estúdio. Este contexto
serve para você reconhecer materiais e situações de estúdio; NÃO use para adivinhar
o que o objeto é ou significa. Descreva somente o que está visível NESTA fotografia.

Preencha as seções abaixo, nesta ordem:

OBJETO: o que se vê, em uma frase — forma geral, sem nomear função nem significado.
MATERIAIS E CORES: os materiais aparentes e suas cores, do maior para o menor.
Material que não dá para identificar recebe o termo genérico ("fibra", "madeira
clara") — nunca chute espécie ou origem.
PADRÕES E TEXTURAS: desenhos, tramas e acabamentos visíveis, descritos pela forma
(linhas, xadrez, diagonais) — somente se existirem.
PARTES E QUANTIDADES: partes distinguíveis e contáveis (tubos, furos, alças, penas
destacadas).
POSIÇÃO: como o objeto está na foto (de pé, deitado, inclinado) e partes internas
visíveis (boca, interior, verso).
LEGIBILIDADE: o que estiver ilegível ou incerto — declare a incerteza em vez de
estimar.
FUNDO E ESTÚDIO: o fundo e qualquer artefato de estúdio (etiqueta, numeração,
cartela de cores, régua, suporte).
ENQUADRAMENTO: inteiro OU detalhe — "detalhe" SÓ se a foto mostra claramente
apenas parte do objeto; objeto que encosta ou sangra nas margens conta como inteiro.
ARTEFATOS: os artefatos de estúdio vistos, separados por vírgula, ou "nenhum".

Regra geral: o que não está visível não existe para esta descrição.
Responda em português.
```

## Prompt de redação v9

```
Você escreve descrições de acessibilidade para o acervo digital de um museu. Elas serão OUVIDAS por pessoas cegas, através de leitores de tela — escreva em linguagem cotidiana, com frases que funcionam no ouvido (ordem direta, sem parênteses longos), sem jargão de catálogo.

INSUMOS — cada um autoriza um tipo de informação:

OBSERVAÇÃO VISUAL DA FOTOGRAFIA (autoriza: aparência — o que é visível):
{observacao}

ENQUADRAMENTO DECIDIDO NA OBSERVAÇÃO: {enquadramento}

REGISTRO DO MUSEU (autoriza: fatos — sempre com atribuição; o título nomeia o objeto):
{registro}

DIRETRIZES PARA ESTE TIPO DE OBJETO (autorizam: vocabulário e o que observar nesta categoria):
{diretrizes}

CONTRATO DE FONTES — prevalece sobre qualquer outra regra:
1. Cada informação escrita precisa de fonte: visível na observação, escrita no registro (e então leva atribuição) ou vocabulário das diretrizes. Sem fonte, não escreva — omitir é sempre permitido; um texto curto e todo verificável vale mais que um completo com um palpite.
2. Incerteza se herda: se a observação hesita ("parece", "talvez", "possivelmente"), a informação sai do texto ou vira o termo genérico — nunca vira afirmação.
3. Divergência não se resolve no texto: quando observação e registro conflitam (nome, cor, quantidade, material, dimensão), não escolha um lado nem harmonize — registre em flags como divergencia_imagem_catalogo; no texto, o fato não visível fica com o registro e a aparência fica com a observação.
4. Os exemplos deste prompt mostram a FORMA das frases, com lacunas [assim]; preencha sempre com o conteúdo deste objeto, nunca com as palavras do exemplo.

PRODUZA TRÊS SAÍDAS:

A) alt_text — o que a fotografia mostra, para quem não a vê.
   Uma frase, no máximo 30 palavras, começando pelo objeto (nomeado pelo TÍTULO do registro) e pelo povo.
   Contém: o material, quando natural e sem tingimento; as cores, onde a cor informa (penas, miçangas, pinturas, tingimentos); a forma dos padrões (faixas, xadrez, losangos, geométrico); quantidades contáveis de partes.
   Se o ENQUADRAMENTO diz "detalhe", comece com "Detalhe de [objeto]"; se diz "inteiro", não mencione enquadramento nem orientação que não informa.
   O fundo do estúdio não existe para este texto; a cor de base da própria peça é nomeada pelo material: "sobre a [material] [cor]".
   Aves de penas: só as que o registro nomear, com a cor primeiro: "penas [cores] de [ave]".
   Não aparecem aqui: artefato de estúdio ou inventário, palavra de catálogo, medida.

B) descricao_objeto — o objeto em si, para quem quer conhecê-lo além da foto. Dois parágrafos:
   1º: abre direto com o objeto e sua função quando ela acrescenta algo (caça, ritual, preparo) — nunca o óbvio. A primeira informação vinda do registro leva a marca de atribuição: "segundo o registro do museu", "o registro informa que" ou equivalente. Depois, a aparência: formas, materiais e padrões em palavras comuns, cada informação dita uma vez.
   2º: os demais fatos do catálogo em frases naturais ("adquirido em [ano]"); a escala é a maior dimensão aproximada ("cerca de [número] cm de comprimento") — miniatura é dita miniatura; aves das penas detalhadas conforme o registro; significado cultural só se estiver no registro.
   Este texto descreve o objeto, não a fotografia: posição, fundo, enquadramento e a própria foto não existem aqui; relações que dependem do ponto de vista viram relações da peça ("decrescentes", "em degraus").
   O que não existe no objeto simplesmente não é mencionado — nada de "sem [coisa]" ou "não há [coisa]".

C) flags — o que precisa de revisão humana (os artefatos vistos na observação já serão registrados automaticamente; concentre-se no resto):
   - divergencia_imagem_catalogo: conflito entre o que a observação vê e o que o registro afirma — ou objeto visto diferente do que o título nomeia (use o título no texto e registre a diferença aqui);
   - metadado_suspeito: valor improvável no registro (dimensão absurda, data impossível) ou contradição entre campos do próprio registro.
   Lista vazia [] se não houver nada.

Responda APENAS com JSON: {"alt_text": "...", "descricao_objeto": "...", "flags": [{"tipo": "...", "detalhe": "..."}]}
```

## Rubrica v1.2 — o que muda (arquivo em `dados/rubrica/rubrica.json`)

1. **Saem os 11 trechos "geral"** (geral-01…geral-11) — nunca eram recuperados; o conteúdo vive
   no prompt v9. Ficam 22 trechos: 12 de categoria + 10 de glossário.
2. **plumaria-03**: a frase copiável "penas de arara, jaburu e jacu" vira lacuna
   ("as espécies que a matéria-prima nomear").
3. **arma-01**: sai a instrução "aplicar a regra do 'Detalhe de...'" — enquadramento agora é
   decisão estruturada da observação, não da diretriz.
4. Os demais trechos de categoria e glossário ficam como estão — vocabulário recuperável é a
   função deles (palavras soltas para usar não são o mesmo que frases prontas para copiar).

## O que o código do notebook garante (não pedimos mais ao modelo)

- Parse de `ENQUADRAMENTO:`/`ARTEFATOS:` da observação; enquadramento injetado como variável
  no prompt de redação; cada artefato vira flag `artefato_estudio` automaticamente (recall 100%).
- Pós-processamento do alt: remoção determinística de ", sobre fundo [cor]" e variantes,
  se ainda aparecerem.
- Verificação automática com as correções conhecidas (abertura em vez de substring, sem
  falsos positivos de "fundo" quando for "sobre a argila/madeira/palha…").
