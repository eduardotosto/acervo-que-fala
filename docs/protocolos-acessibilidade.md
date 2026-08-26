# Protocolos de acessibilidade e o que este projeto faz

*26/08/2026 · material de referência para o README da banca (E12). As 25 regras editoriais do
projeto nasceram de revisão humana caso a caso, não de leitura de norma — este documento verifica
onde elas convergem com o que já está publicado, e onde o projeto propõe algo que as normas não
cobrem.*

## 1. A base legal do problema

O acervo digital do Museu do Índio publica hoje 20.965 itens com `alt=""`. Isso não é só uma
lacuna de boa prática:

- **WCAG 2.2, critério 1.1.1 (Conteúdo não textual)** — conteúdo não textual precisa de
  alternativa textual que cumpra a mesma função. Imagem informativa com `alt` vazio falha o
  critério no nível A, o mais básico.
- **Lei Brasileira de Inclusão (Lei 13.146/2015), art. 63** — obrigatoriedade de acessibilidade
  nos sítios da internet mantidos por empresas com sede no país e por **órgãos do poder público**.
  O Museu do Índio é vinculado à Funai.
- **eMAG** (Modelo de Acessibilidade em Governo Eletrônico) — referência da administração pública
  federal brasileira, que reproduz a exigência de alternativa textual.

A motivação do projeto, portanto, não depende de argumento de gosto: é uma não-conformidade
objetiva, em um acervo público, com base legal explícita.

## 2. Onde as 25 regras convergem com protocolos publicados

| Protocolo | O que orienta | Regra do projeto que converge |
|---|---|---|
| **W3C WAI — Images Tutorial** e a árvore de decisão do `alt` | alternativa concisa, informação essencial primeiro, sem prefixo "imagem de" | alt abre pelo objeto e pelo povo, sem prefixo de foto |
| **Cooper Hewitt — Guidelines for Image Description** (Smithsonian) | dois comprimentos (curta e longa), objeto antes de contexto, materiais e cores factuais, avisar recorte | a arquitetura de dois níveis; o "Detalhe de..." |
| **Coyote** (Museum of Contemporary Art Chicago) | descrição em dois comprimentos, escrita e revisada por pessoas | precedente museal direto do pipeline com revisão humana |
| **DIAGRAM Center — Image Description Guidelines** | "descreva, não interprete"; do geral ao específico; brevidade | regra 15 (só afirmações verificáveis) é quase literal |
| **Guia para Produções Audiovisuais Acessíveis** (Ministério da Cultura, audiodescrição no Brasil) | descrever o visível sem interpretar; vocabulário cotidiano; texto pensado para o ouvido | regras 3 e 15; o nível 2 como audioguia |

O que essa convergência diz para a banca: um conjunto de regras extraído por revisão humana de 20
objetos reencontrou, sozinho, boa parte do consenso de duas décadas de prática museal e de
acessibilidade web. As regras não são idiossincrasia — e as fontes acima servem de validação
externa barata para um projeto que não teve acesso a usuários cegos.

## 3. Onde o projeto vai além dos protocolos

**A marca de atribuição é contribuição própria.** Nenhum dos guias acima separa, dentro do texto,
o que a fotografia mostra do que o catálogo documenta. Eles tratam a descrição como um ato só. O
projeto separa: a aparência vem da observação e não leva marca; todo fato de catálogo que não é
visível ("segundo o registro do museu") carrega a marca na própria frase. Quem ouve fica sabendo
de onde vem cada informação — e a fronteira de auditoria fica escrita no produto, não num anexo.

**As flags como subproduto.** O que começou como pedido de revisão humana virou auditoria do
acervo: o abano de 290 cm, a contradição "brinquedo em miniatura" × "utilizado para caça", as
duas penas azuis que o gabarito humano registrava como uma. Nenhum protocolo de acessibilidade
prevê que descrever um acervo devolva correções ao acervo.

**Duas decisões deliberadamente divergentes**, que precisam estar declaradas no README:

1. **Texto visível na imagem.** O W3C orienta transcrever texto que aparece na imagem. O projeto
   **exclui** etiquetas e numerações de inventário do texto público e as transforma em flag. A
   justificativa: são ruído de estúdio, não conteúdo do objeto — quem ouve a descrição de uma peça
   não precisa do número de tombo no meio da frase, e ele continua registrado, na flag.
2. **Limite de 30 palavras no alt.** Não vem do folclore dos "125 caracteres" (que nasceu de
   truncamento em leitores antigos e está superado); vem do critério de escuta — uma frase que
   funciona em voz alta antes de o ouvinte perder o fio.

## 4. Museologia indígena: o que o projeto assume e o que fica declarado como limite

- **Nomes dos povos.** O sistema segue o registro do museu (o título e o campo Povo nomeiam o
  objeto e o povo). É a decisão correta para um sistema de descrição — a fonte comanda —, mas o
  registro usa a grafia do museu, que nem sempre é a autodenominação atual do povo. Divergência a
  declarar, não a corrigir por conta própria.
- **Significado cultural.** O prompt proíbe atribuir significado a partir da imagem: função
  ritual, mágica ou lúdica só entra se estiver no registro, com atribuição. Isso protege contra a
  leitura exotizante que um modelo treinado em imagens ocidentais produz com facilidade.
- **Governança de dados indígenas.** Os princípios **CARE** (Collective Benefit, Authority to
  Control, Responsibility, Ethics) e a infraestrutura de **Local Contexts / TK Labels** são o
  vocabulário estabelecido para dizer quem tem autoridade sobre a descrição de um acervo
  indígena. Este projeto não passou por consulta às comunidades — e é isso que a limitação
  registrada no README ("validação com usuários reais e com as comunidades como trabalho futuro")
  significa em termos concretos. Nomear os frameworks torna a limitação verificável em vez de
  genérica.

## 5. Antes de citar na banca

As fontes da seção 2 são estáveis e localizáveis pelo nome. Duas referências adicionais que
apareceram na revisão precisam ter edição e numeração conferidas antes de entrar numa
bibliografia formal: a norma **ABNT** brasileira de acessibilidade em comunicação digital (há
publicação recente na área, mas o número e o ano devem ser verificados no catálogo da ABNT) e a
**ISO/IEC 20071-11**, sobre orientação para alternativas textuais de imagem. O restante do
argumento não depende delas.
