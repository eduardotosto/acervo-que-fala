# Acervo que Fala: descrições de acessibilidade para o acervo digital do Museu do Índio

#### Aluno: [Eduardo Tosto Campos](https://github.com/eduardotosto)
#### Orientadora: Manoela Kohler

---

Trabalho apresentado ao curso [Inteligência Artificial Generativa & Large Language Models](https://ica.ele.puc-rio.br/cursos/ia-generativa-large-language-models/) como pré-requisito para conclusão de curso.

- [Link para o código](https://github.com/eduardotosto/acervo-que-fala): este repositório. O andamento, etapa por etapa, está em [docs/ETAPAS.md](docs/ETAPAS.md).

- Trabalhos relacionados:
    - [W3C WAI — Images Tutorial](https://www.w3.org/WAI/tutorials/images/).
    - [WCAG 2.2, critério 1.1.1 — conteúdo não textual](https://www.w3.org/TR/WCAG22/#non-text-content).
    - Cooper Hewitt Guidelines for Image Description, Coyote (MCA Chicago) e DIAGRAM Center: o cotejo com as regras deste projeto está em [docs/protocolos-acessibilidade.md](docs/protocolos-acessibilidade.md).

---

### Resumo

O acervo digital do Museu do Índio publica 20.965 itens com o texto alternativo das fotografias vazio. Para quem navega com leitor de tela, a imagem não existe.

Este trabalho é uma prova de conceito (PoC): um sistema que usa só modelos abertos, em GPU gratuita, para gerar dois textos por objeto. O primeiro é o alt-text, que descreve a fotografia. O segundo é a descrição do objeto, que serve de audioguia. Junto com eles saem flags, que dizem a um revisor humano onde olhar.

O sistema foi desenvolvido sobre 20 objetos, congelado, e depois medido em 50 objetos que não participaram dos ajustes. O alt-text gerado cumpre os critérios objetivos em 47 de 49 casos e foi avaliado como mais claro ao ouvido do que a descrição do catálogo. Em fidelidade ao que a foto mostra, os dois ficam próximos. Em 20 dos 49 textos gerados a avaliação encontrou informação falsa ou inventada.

O que a PoC entrega, então, não é um texto pronto para publicar. É um primeiro rascunho auditável, com a indicação de onde cada erro nasceu.

### 1. Introdução

**O problema.** No site do acervo, cada fotografia é publicada com `alt=""`. O texto alternativo é o que o leitor de tela fala no lugar da imagem, e ele é exigido pelo critério mais básico das diretrizes de acessibilidade (WCAG 1.1.1) e pela Lei Brasileira de Inclusão para sites de órgãos públicos.

**A baseline.** *Baseline* é o ponto de comparação: o que existiria sem o sistema. Aqui, é a descrição curatorial do catálogo usada como alt-text, porque é o que o acervo tem à mão. Ela foi escrita para especialistas:

> Pote de borda extrovertida e base plana apresentando superfície decorada com motivos geometrizantes pintados em vermelho e preto

**A proposta.** Três saídas por objeto:

| Saída | O que é | Regra principal |
|---|---|---|
| Nível 1, alt-text | Descreve a fotografia | Até 30 palavras, começa pelo objeto e pelo povo |
| Nível 2, descrição do objeto | Descreve o objeto, independente da foto | Todo fato do catálogo entra com atribuição: "segundo o registro do museu" |
| Flags | O que pede revisão humana | Artefato de estúdio, divergência entre foto e catálogo, metadado improvável |

**As restrições que assumi.** Só modelos abertos. Infraestrutura gratuita (Google Colab, GPU T4). Revisão humana obrigatória. Significado cultural só quando o catálogo do museu o registra.

**A pergunta.** As descrições geradas servem melhor a quem ouve do que a descrição curatorial usada como alt-text?

### 2. Modelagem

#### Os dados

A coleta usa a API pública do acervo (Tainacan): 555 itens com fotografia e registro, em 10 categorias de objeto. Antes de qualquer ajuste no sistema, separei 40 casos de avaliação e 10 de *holdout*, revisados um a um. *Holdout* é o conjunto que fica fora de todo o desenvolvimento e roda uma única vez, no fim.

#### O pipeline

| Etapa | Quem faz | O que acontece |
|---|---|---|
| 1. Observação | Modelo de visão | Recebe só a fotografia e descreve o que vê, em seções nomeadas |
| 2. Garantias | Código | Calcula a escala, a contagem de partes e as flags. Informação com flag não entra no texto |
| 3. Redação | Modelo de linguagem | Recebe só texto: a observação, o registro do catálogo e as diretrizes recuperadas por RAG |
| 4. Validação | Código | Confere o rascunho e, se ele falha, devolve o diagnóstico ao modelo uma vez (*retry*) |
| 5. Revisão | Pessoa | As flags dizem onde olhar |

O modelo é o Qwen3-VL-8B, quantizado em 4-bit para caber na GPU gratuita. RAG (*retrieval-augmented generation*) é buscar trechos de uma base de conhecimento e entregá-los ao modelo junto com a tarefa. A base aqui é uma rubrica escrita à mão, com diretrizes por categoria de objeto e um glossário.

A separação entre olhar e escrever existe por um motivo: poder dizer, de cada erro, se ele nasceu na observação ou na redação.

#### O caminho

1. **Primeiro objeto e *smoke test*.** Um objeto de ponta a ponta, depois cinco. *Smoke test* é a menor execução possível, só para saber se o caminho inteiro funciona. Logo aí o modelo corrigiu o meu gabarito: a faixa Kalapalo tem duas penas azuis, e eu tinha anotado uma.
2. **Lote de 20 e revisão editorial.** Eu revisava os textos, e cada correção virava regra no prompt. Foram seis rodadas de revisão; as duas primeiras geraram 25 regras.
3. **O prompt saturou.** Perto de 25 regras, cada regra nova passou a derrubar uma antiga.
4. **Parte dos erros vinha do próprio prompt.** Uma frase de exemplo era copiada ao pé da letra: "sobre a argila bege" apareceu numa bolsa de fio de tucum.
5. **O que precisa de garantia foi para código.** Escala, contagem, teto de plausibilidade das medidas, flags e validação saíram do prompt. Entre os lotes v8 e v10, medidos pela mesma régua, os problemas por objeto caíram de 4,0 para 1,7.
6. **Comparação de redatores (*bake-off*).** Testei o Gemma 3 12B no lugar do Qwen. Com o prompt antigo ele rodou e foi melhor nas checagens. Com o sistema atual, não coube na memória da GPU gratuita. Segui com o Qwen e registrei a limitação.
7. **Congelamento e avaliação.** O sistema foi congelado em 28/08/2026. A avaliação rodou em 29/09/2026, nos 50 objetos.

O histórico completo, com as versões de cada prompt e cada lote, está em [docs/ETAPAS.md](docs/ETAPAS.md) e [docs/VERSOES.md](docs/VERSOES.md).

#### A avaliação

| Instrumento | O que mede | Onde está |
|---|---|---|
| Régua mecânica | Checagens automáticas sobre o texto | [avaliacao/checar_lote.py](avaliacao/checar_lote.py) |
| Critérios objetivos do alt-text | Gerado e baseline, nos mesmos 5 critérios | [avaliacao/rodar.py](avaliacao/rodar.py) |
| Flags × anotação humana | Se o sistema sinalizou o que eu tinha anotado em cada caso | [avaliacao/rodar.py](avaliacao/rodar.py) |
| Juiz | Um modelo confere cada texto contra a foto e o registro | [avaliacao/painel/](avaliacao/painel/) |
| A/B cego | O juiz recebe a foto e dois textos, sem saber qual é qual | [avaliacao/painel/](avaliacao/painel/) |

O juiz segue a técnica *LLM-as-judge*: um modelo de linguagem avalia a saída de outro contra critérios escritos. Usei o Claude (Opus). Os 57 apontamentos mais graves passaram por mim, um a um, e concordei com todos.

#### Nota de método

O projeto foi construído em par com LLMs. O código e os notebooks foram escritos pelo Claude (Anthropic), a partir das minhas decisões de arquitetura, de revisão e de critério. Vários achados deste trabalho são dele, e estão registrados assim no ETAPAS. O juiz da avaliação também é o Claude. Nenhum modelo proprietário participa da geração das descrições.

### 3. Resultados

Um comando imprime todas as métricas: `python avaliacao/rodar.py`.

#### Os números

| Medida | Desenvolvimento (20) | Casos (40) | Holdout (10) |
|---|---|---|---|
| Objetos com descrição gerada | 19 | 39 | 10 |
| Problemas por objeto, régua mecânica | 1,7 | 1,6 | 1,7 |
| Alt-text atende aos 5 critérios objetivos (gerado / baseline) | — | 37 / 0, de 39 | 10 / 0, de 10 |
| O mesmo, sem o critério "cita o povo" | — | 37 / 26, de 39 | 10 / 3, de 10 |
| Critérios do caso atendidos, segundo o juiz | — | 58% | 56% |
| Textos com informação falsa ou inventada | — | 16 de 39 | 4 de 10 |
| A/B cego: qual descreve melhor (gerado / baseline) | — | 27 / 12 | 4 / 6 |
| Nota de clareza ao ouvido, de 1 a 5 (gerado / baseline) | — | 4,08 / 2,85 | 4,0 / 2,4 |
| Nota de fidelidade à foto, de 1 a 5 (gerado / baseline) | — | 3,85 / 3,49 | 3,7 / 4,0 |

A rodada processou os 50 objetos sem falha de geração, em 93 minutos. Um objeto ficou sem texto: a foto tem 154×106 pixels, e o sistema emite uma flag em vez de descrever.

#### O que eles dizem

- **O sistema se comporta igual fora do desenvolvimento.** A régua mede 1,7 problema por objeto no lote em que o sistema foi ajustado e de 1,6 a 1,7 nos objetos que ele nunca tinha visto.
- **O texto gerado ganha no ouvido.** Clareza e concisão ficam mais de um ponto acima da baseline nos dois conjuntos.
- **No olho, não ganha.** A fidelidade fica próxima nos casos, e no holdout a baseline descreve melhor em 6 dos 10 pares.
- **A baseline zera nos critérios objetivos por um motivo só.** A descrição curatorial não cita o povo em nenhum dos 49 casos, porque no catálogo o povo fica em outro campo. Por isso a tabela traz a linha sem esse critério.

#### Onde o erro nasce

Dos 37 apontamentos de gravidade alta, 17 nasceram na observação e 20 na redação. Na observação, o erro típico é de material: cabaça vista como cerâmica, osso visto como madeira. Na redação, é de invenção: um padrão que a foto não mostra.

Cinco dos 17 erros de observação não chegaram ao texto publicado. Em dois objetos do holdout o modelo viu o material errado, e a redação usou o material do catálogo.

#### Um erro que o próprio sistema induz

Os termos "gregas" e "espinha-de-peixe" aparecem em 12 textos sem estar na observação nem no registro. Eles só existem no trecho do glossário que o RAG entregou ao redator. Em 7 desses 12, a foto não mostra o padrão. No lote de desenvolvimento isso não aparecia, porque os objetos de lá tinham esses padrões de fato.

#### Dois exemplos

Moringa Terena, em que o alt-text gerado foi avaliado como correto:

| | Texto |
|---|---|
| Baseline | Moringa de base plana, com dois gargalos de bordas direta, separados por uma alça. Apresenta decoração no bojo com motivos naturalistas fitomorfos (vegetais) pintados na cor branco |
| Alt-text gerado | Moringa, cerâmica da etnia Terena, com corpo esférico, alça circular e dois gargalos, pintada com motivos vegetais em branco. |

Recipiente de cabaça Guarani Nhandeva, em que o alt-text gerado erra duas vezes:

| | Texto |
|---|---|
| Baseline | Recipiente de cabaça com alça, tampa de sabugo de milho e revestida com cipó gwaimbé "djawóá" |
| Alt-text gerado | Recipiente de cabaça do povo Guarani Nhandeva, com tampa de sabugo de milho e corpo envolto por corda trançada em padrão de espinha-de-peixe, em cerâmica marrom avermelhada. |

O objeto é de cabaça, e a foto não mostra espinha-de-peixe. O primeiro erro nasceu na observação. O segundo, na redação, induzido pelo glossário.

#### O que as flags pegaram

| O que eu tinha anotado no caso | O sistema sinalizou |
|---|---|
| Foto parcial | 6 de 7 |
| Artefato de estúdio (etiqueta, numeração, cartela) | 9 de 14 |
| Divergência entre foto e catálogo | 4 de 11 |
| Metadado suspeito | 1 de 1 |

As flags viraram também uma auditoria do catálogo. O abano registrado com 290 cm foi sinalizado, e o juiz apontou 23 inconsistências que são do registro, não do texto.

#### O que a régua não vê

A régua mecânica foi construída com os defeitos do lote de desenvolvimento. Nos objetos novos apareceram defeitos que ela não mede: em 12 de 49 textos o modelo inventa um particípio para "adquirir" ("aquisido", "aquisitado"). Em 24 de 49, a descrição do objeto omite o povo, embora o validador cobre.

### 4. Conclusões

**O que a PoC mostra.** Com modelos abertos e GPU gratuita, dá para gerar um primeiro rascunho que o ouvido entende melhor do que a descrição de catálogo, e que chega ao revisor com a indicação do que conferir.

**O que ela não mostra.** Que esse rascunho possa ser publicado sem revisão. Em 20 de 49 textos há informação falsa ou inventada.

**O que aprendi sobre o desenho.** O que precisa de garantia não se pede ao modelo, se resolve em código. Onde o código garante, o resultado ficou estável. Onde só o prompt pede, o modelo oscila. E cada camada que eu acrescentei para ajudar (exemplo no prompt, glossário no RAG, validador) também trouxe um tipo novo de erro.

**Limites.**

- Não houve avaliação com pessoas cegas nem com curadores do museu. A avaliação é automática e por um modelo juiz.
- O A/B com avaliadores humanos saiu do escopo. O teste com leitor de tela (NVDA) está preparado em [avaliacao/painel/](avaliacao/painel/) e ainda não foi feito.
- O juiz é um modelo proprietário, usado só para medir. Na calibração de 27/08, ele deixou passar cerca de um defeito em cada dez.
- São 50 objetos de um acervo de 20.965. Custo em escala e aceitação pelo museu não foram medidos.
- O projeto não passou por consulta às comunidades indígenas. Os nomes dos povos seguem a grafia do registro do museu.
- A comparação entre redatores sob o sistema atual não coube na GPU gratuita. Se o teto de obediência é do tamanho do modelo, fica em aberto.
- O site de demonstração está pronto em [site/](site/), sem a interface de revisão humana que estava no plano. A publicação ainda não foi feita.

**O que fica em aberto.** Se o texto gerado é mais claro, igualmente fiel e inventa em 4 de cada 10 objetos, revisar custa menos do que escrever do zero? A PoC não responde. Ela deixa o custo visível, objeto a objeto.

---

### Como reproduzir

```
pip install -r requirements.txt
python app/tainacan.py --n 60      # coleta pela API pública do acervo
python avaliacao/rodar.py          # valida os casos e imprime as métricas
```

A geração roda no Colab, com GPU T4: [abrir o Notebook 06](https://colab.research.google.com/github/eduardotosto/acervo-que-fala/blob/main/notebooks/06_lote_avaliacao.ipynb).

| Pasta | O que tem |
|---|---|
| [app/](app/) | Coleta e configuração |
| [dados/](dados/) | Itens coletados e a rubrica do RAG |
| [notebooks/](notebooks/) | Os notebooks executados no Colab, com cada etapa explicada |
| [resultados/](resultados/) | A saída de cada lote, com os prompts embutidos, e as métricas |
| [avaliacao/](avaliacao/) | Casos, holdout, régua, juiz e adjudicação |
| [site/](site/) | Site de demonstração (Gradio) |
| [docs/](docs/) | Etapas, versões e protocolos de acessibilidade |

A API do acervo é pública, sem autenticação: não há segredos neste repositório.

---

Matrícula: 252.100.045

Pontifícia Universidade Católica do Rio de Janeiro

Curso de Pós Graduação *Inteligência Artificial Generativa & Large Language Models*
