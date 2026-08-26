# Proposta para revisão: observação v3 + redação v9 + divisão prompt/rubrica/código

*26/08/2026 · para revisão do Eduardo ANTES de gerar o novo notebook. Contexto e evidências em
`analise_prompt_rubrica.md`. Após aprovação: novo teste no Qwen com este conjunto.*

## A divisão de trabalho (o sistema inteiro, não só o prompt)

| Camada | O que carrega | Por quê |
|---|---|---|
| **Prompt de observação v3** | Observação em SEÇÕES nomeadas (todas parseáveis), com contexto guardado ("reconhecer materiais, não adivinhar significado") | Decisões visuais são tomadas por quem vê a foto; seções eliminam divagação e pergunta que induz resposta |
| **Prompt de redação v9** | Contrato de fontes + regras universais, hierarquizadas | Regra que vale para todo objeto não pode depender de sorteio do RAG |
| **Rubrica v1.2 (RAG)** | Só diretrizes por categoria + glossário | O que o `recuperar()` realmente entrega (k=3 por semelhança) |
| **Código do notebook** | Garantias mecânicas: cada item de `ARTEFATOS:` vira flag automaticamente; `ENQUADRAMENTO:` parseado e injetado no prompt (as duas linhas saem do texto da observação antes da redação); consulta do RAG montada das seções `OBJETO:` + `PADRÕES:`; pós-processamento remove "sobre fundo [cor]" residual do alt | O que precisa de 100% de garantia não se pede a modelo |
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
2. Incerteza se herda: o que estiver na seção LEGIBILIDADE da observação, ou vier com hesitação ("parece", "talvez", "possivelmente"), sai do texto ou vira o termo genérico — nunca vira afirmação.
3. Divergência não se resolve no texto: quando observação e registro conflitam (nome, cor, quantidade, material, dimensão), não escolha um lado nem harmonize — registre em flags como divergencia_imagem_catalogo; no texto, o fato não visível fica com o registro e a aparência fica com a observação.
4. Os exemplos deste prompt mostram a FORMA das frases, com lacunas [assim]; preencha sempre com o conteúdo deste objeto, nunca com as palavras do exemplo.

PRODUZA TRÊS SAÍDAS:

A) alt_text — o que a fotografia mostra, para quem não a vê.
   Uma frase, no máximo 30 palavras, começando pelo objeto (nomeado pelo TÍTULO do registro) e pelo povo.
   Contém: o material, quando natural e sem tingimento; as cores, onde a cor informa (penas, miçangas, pinturas, tingimentos); a forma dos padrões (faixas, xadrez, losangos, geométrico); as quantidades da seção PARTES E QUANTIDADES da observação.
   As seções FUNDO E ESTÚDIO e ARTEFATOS da observação nunca alimentam este texto nem o B — são insumo exclusivo das flags.
   Se o ENQUADRAMENTO diz "detalhe", comece com "Detalhe de [objeto]"; se diz "inteiro", não mencione enquadramento nem orientação que não informa.
   O fundo do estúdio não existe para este texto. Pintura ou decoração aplicada sobre a base da peça se descreve nesta ordem: primeiro a decoração e suas cores, depois a base — "pintura [tipo] em [cores] sobre [material da base]"; a base nunca aparece sozinha ("sobre a [material]") sem dizer o que está sobre ela.
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
   no prompt v9. Ficam **23 trechos: 13 de categoria (10 categorias) + 10 de glossário**.
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

---

# O que a implementação acrescentou à proposta (26/08/2026)

A proposta acima foi revisada pelo Eduardo e implementada no **Notebook 04 v6**. Cinco coisas
mudaram ou nasceram durante a implementação — todas na mesma direção: **o que dá para garantir
em código sai do prompt**.

## 1. `FUNDO E ESTÚDIO` também é consumida pelo código

A proposta dizia que as seções `FUNDO E ESTÚDIO` e `ARTEFATOS` "nunca alimentam" os textos, mas
deixava a primeira viajar no prompt de redação com a instrução de ignorá-la. Isso é o mecanismo
1b do próprio diagnóstico: mandar "há um fundo branco e uma etiqueta" e pedir que o modelo não
use é plantar a palavra proibida no contexto. **A seção agora sai da observação antes da
redação**, junto com `ENQUADRAMENTO` e `ARTEFATOS`. Medida de referência: nos alts da v5, "sobre
fundo [cor]" aparecia em 15 de 20.

## 2. RAG híbrido — a categoria deixou de depender de sorteio

O campo `Categoria` existe em 100% dos itens e usa exatamente os mesmos nomes dos trechos da
rubrica (conferido nos 555 itens do acervo). A diretriz da categoria passou a ser **escolhida
pelo registro**, e só o glossário é recuperado por similaridade (k=2). A mesma regra que tirou
as regras universais da rubrica ("regra universal não pode depender de sorteio do RAG") vale
para a diretriz de categoria. Categoria fora da rubrica cai no modo semântico antigo.

Dois ajustes técnicos junto: o embedder passou a rodar na **CPU** (23 trechos e 20 consultas são
trabalho trivial, e a T4 fica inteira para o modelo 4-bit), e a consulta passou a ser codificada
com o **prompt de query** da família Qwen3-Embedding, que é instruída — os documentos vão sem.

## 3. Escala, plausibilidade e contradição saíram do prompt

Três defeitos resistiram a todas as versões do prompt: a escala pela medida de uma parte, a
miniatura não declarada e `metadado_suspeito` em zero por três lotes. Nenhum é tarefa de escrita:

- **Escala** = maior dimensão do registro, com rótulo, ignorando medidas "com cordel/alça
  esticada". A redação recebe a frase pronta e é proibida de recalcular.
- **Plausibilidade** = teto por categoria calculado como **Q3 + 3×IQR das dimensões do próprio
  acervo** (547 itens com medida parseável), com piso de 150 cm. Dispara em 2 dos 547: o abano de
  290 cm e uma capa de pele de onça de 223 cm, que é grande de verdade. Taxa de alarme 0,4%.
- **Contradição entre campos** continua sendo trabalho de modelo, mas como **pergunta isolada**,
  fora da tarefa de escrita.

## 4. O alt bruto fica salvo ao lado do alt final

Sem ele, um "sobre fundo X" zerado não distingue o que o prompt v9 resolveu do que o
pós-processamento escondeu — e é exatamente essa diferença que o lote v6 está medindo. O
pós-processamento também ficou **conservador**: só remove quando o trecho termina em pontuação
dentro de duas palavras. Em "sobre fundo bege e boca larga" ele não mexe, e a verificação acusa —
amputar a frase seria pior que deixar passar.

## 5. A régua virou código compartilhado, e mede os lotes antigos

`avaliacao/checar_lote.py` roda as checagens de hoje sobre qualquer lote salvo. Os dois blocos
que importam (registro e verificação) são **o mesmo texto** no script e no notebook — o notebook
é montado a partir do script, então as duas cópias não divergem.

As checagens ganharam **fronteira de palavra**: a régua anterior procurava o termo como pedaço
de texto e confundia "aparece" com "parece", "profundo" com "fundo", "decoração" com "coração" —
o mesmo casamento raso que o projeto diagnosticou nos modelos estava na régua que os media.
Checagens novas: coerência de enquadramento, medida que não existe no registro, escala pela
medida errada, miniatura não declarada, jargão de fotografia no alt ("close-up", "plano médio") e
teto de escuta do nível 2.
