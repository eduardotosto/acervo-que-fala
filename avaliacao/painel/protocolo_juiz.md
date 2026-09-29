# Protocolo do juiz — E10 (29/09/2026)

**LLM-as-judge**: um modelo de linguagem avalia a saída de outro contra critérios escritos. Aqui o
juiz é o Claude (Opus), e o avaliado é o sistema congelado (Qwen3-VL-8B, observação v3.1 +
redação v13), rodado no Notebook 06 sobre os 40 casos de avaliação e os 10 de holdout.

O juiz fica **fora do pipeline**: nenhuma descrição publicada passa por ele. Ele só mede.

## Por que este juiz

O mesmo juiz, com o mesmo protocolo, revisou o lote v7 em 27/08/2026, e o Eduardo adjudicou os 48
achados um a um (5ª adjudicação). Dessa conferência saíram os dois números que sustentam o uso
dele aqui:

| Medida | Valor | O que diz |
|---|---|---|
| Concordância | ~95% | dos 48 achados do juiz, 2 discordâncias e 1 concordância parcial |
| Recall | ~89% | 6 defeitos que só a revisão humana viu |

O juiz erra pouco no que aponta e deixa passar cerca de um defeito em cada dez. Os resultados da
E10 devem ser lidos com essa margem.

## Duas perguntas, dois juízes separados

| | Juiz de critérios | Juiz do A/B cego |
|---|---|---|
| Pergunta | O texto cumpre os critérios do caso e a régua editorial? | Qual dos dois textos serve melhor a quem não vê a foto? |
| Recebe | Dossiê completo do caso | Só a foto e dois textos, A e B |
| Sabe qual texto é o gerado? | Sim | Não |
| Material | `dossies.json` | `ab_cego.json` |
| Saída | `juiz_criterios.json` | `juiz_ab.json` |

Os dois rodam em sessões separadas, sem contexto compartilhado. O juiz do A/B não recebe o
dossiê, o id do item nem o gabarito do sorteio (`ab_gabarito.json`), que só entra no repositório
depois do julgamento.

## Regras do protocolo

1. **O juiz vê todos os campos do registro**, não só os dez que o sistema usa. Regra nascida de um
   erro do próprio juiz na revisão do v7: ele ia reportar "estado alucinado" em 5 cards porque o
   material que lia omitia o campo `Estado de origem`.
2. **Todo veredito traz evidência**: o trecho do texto, o campo do registro ou o que a foto mostra.
   Veredito sem evidência não conta.
3. **Todo achado aponta a camada onde o erro nasceu**: `observacao` (o modelo viu errado),
   `redacao` (viu certo e escreveu errado), `registro` (o catálogo erra ou se contradiz) ou
   `codigo` (flag, escala ou quarentena calculadas errado). É a separação que dá sentido ao
   pipeline em duas etapas.
4. **Na dúvida, `conferir`**. O que depende de olho humano (tonalidade, leitura de padrão) não vira
   veredito do juiz: vira pedido de conferência.
5. **O juiz não reescreve**. Ele mede o texto que existe.
6. **Foto sem resolução e falha de geração também são julgadas**: o juiz confere se a decisão de
   não gerar texto se sustenta diante da foto.

## A régua editorial

As 25 regras das duas primeiras revisões, na forma em que ficaram depois das seis adjudicações.
Onde uma decisão posterior mudou a regra, vale a posterior.

**Fontes e fidelidade**
- Cada informação tem fonte: visível na foto, escrita no registro (com atribuição) ou vocabulário
  do glossário. Nenhum elemento inventado.
- Só afirmações verificáveis: sem "sugere", "parece", "possivelmente"; sem inferência de uso ou
  desgaste; sem juízo estético (regra 15).
- Espécie de animal ou planta só quando o registro nomeia; "motivos zoomorfos" vira "figuras de
  animais" (5ª adjudicação).
- A contagem do catálogo prevalece sobre a contagem visual; divergência vira flag (4ª revisão).
- Informação com flag não entra no texto: cor vista que o registro não nomeia, medida suspeita,
  contradição entre campos (5ª adjudicação, quarentena).

**Alt-text (nível 1) — descreve a fotografia**
- Até 30 palavras; começa pelo objeto, nomeado pelo título do registro, e pelo povo (regra 9).
- Só o visível: fato de catálogo que não aparece na foto fica para a descrição (6ª adjudicação).
- "Detalhe de" só para fragmento claro; objeto que encosta nas margens conta como inteiro; nunca
  "inteiro", "horizontal", "vertical" (regra 20).
- Fora do alt: fundo de estúdio, artefato de inventário, medida, frase de ausência.

**Descrição do objeto (nível 2) — descreve o objeto, não a foto**
- Nunca menciona a fotografia: posição, fundo, enquadramento, inclinação (regra 1).
- Abre pelo nome do objeto, sem "O objeto é", "Trata-se de" (regra 2).
- Marca de atribuição uma vez, ao entrar nos fatos do catálogo; povo, ano de aquisição e estado de
  origem sempre que o registro os tem; o texto não termina na marca (6ª adjudicação).
- Escala é a maior dimensão, com o número literal do catálogo; nunca ficha técnica de medidas,
  nunca medida de alça ou cordel (regras 7 e 25, 5ª adjudicação).
- Relações de ponto de vista viram relações da peça: "decrescentes", "dispostos paralelamente"
  (regra 19).
- Em amostras, o contenedor só existe no alt; a descrição é do conteúdo (regra 23, 6ª adjudicação).

**Vocabulário**
- O catálogo manda nas palavras: termo não técnico do registro se usa como está (cabo, pá,
  algodão). A regra 24, que mandava trocar "cabo" por "tubo" na zarabatana, foi revertida na 5ª
  adjudicação.
- Jargão de catálogo sai pelo glossário: globular, borda extrovertida, reticulado, gameliforme
  (regra 3).
- Material natural não tem nome de cor: madeira, fibra, argila, algodão e couro são no máximo
  "clara" ou "escura". Cor nomeada só em pintura, tingimento, penas e miçangas (6ª adjudicação,
  substitui a regra 10).
- Cor presa à parte que a exibe; padrão descrito pela geometria ou pelo termo do glossário, nunca
  por semelhança ("em forma de G", "lembra uma coroa").
- Miçangas são "confeccionadas com"; peças plumárias são "compostas por"; nunca "[material] sobre
  [material]" (6ª adjudicação).

**Economia do texto**
- Nada de frase de ausência ("sem X", "não há X") (regra 12).
- Nada de frase vazia: "porte médio", "forma funcional", "textura natural" (regra 16).
- Função só quando acrescenta ou quando está no campo Função do registro (regra 21, recalibrada na
  6ª adjudicação).
- Cada informação uma vez; o nível 2 não repete frases do alt (regras 6 e 22).

**Flags**
- Artefato de estúdio visto na foto vira flag `artefato_estudio` e não entra em texto nenhum.
- Fundo de estúdio, sozinho, não é flag.
- Flag nunca afirma ausência.

## Prompt do juiz de critérios

> Você é o juiz de uma avaliação de descrições de acessibilidade para o acervo digital de um
> museu. As descrições serão ouvidas por pessoas cegas, por leitor de tela.
>
> Leia `avaliacao/painel/protocolo_juiz.md` (regras do protocolo e régua editorial) e o arquivo de
> lote indicado. Para cada caso do lote: abra a foto em `foto`, leia o `registro_completo`, a
> `observacao`, o `alt_text`, a `descricao_objeto` e as `flags`.
>
> Para cada item de `criterios`, dê um veredito (`atende`, `nao_atende`, `nao_se_aplica` ou
> `conferir`) com a evidência. Depois liste os achados contra a régua editorial, cada um com a
> camada onde nasceu (`observacao`, `redacao`, `registro` ou `codigo`), a gravidade (`alta` =
> informação falsa ou inventada; `media` = regra editorial quebrada; `baixa` = estilo) e a
> evidência. Registre também o que o texto acerta quando o caso tem uma dificuldade conhecida
> (`categorias_borda`, `anotacao_humana_e3`).
>
> Não reescreva os textos. Não consulte outros arquivos do repositório. Grave a saída como JSON no
> caminho indicado, uma entrada por caso:
>
> ```json
> {"id": 0,
>  "criterios": [{"criterio": "", "veredito": "", "evidencia": ""}],
>  "achados": [{"camada": "", "gravidade": "", "texto": "alt_text | descricao_objeto | flags | observacao", "descricao": "", "evidencia": ""}],
>  "acertos": [""],
>  "fidelidade_visual": "fiel | fiel_com_ressalva | infiel | conferir",
>  "resumo": ""}
> ```

## Prompt do juiz do A/B cego

> Você avalia textos alternativos (alt-text) de fotografias de objetos de museu. O texto será
> ouvido por uma pessoa cega, por leitor de tela, no lugar da imagem.
>
> Leia o arquivo de lote indicado. Cada par tem um `codigo`, uma `foto` e dois textos, `texto_A` e
> `texto_B`, escritos por autores diferentes. Você não sabe quem escreveu qual, e a ordem foi
> sorteada. Abra a foto e julgue os dois textos só pelo que a foto mostra e pelo que cada texto
> diz.
>
> Para cada texto, dê notas de 1 a 5 em três critérios: `fidelidade` (o que o texto afirma está na
> foto?), `clareza_ao_ouvido` (palavras comuns, ordem direta, entende-se ouvindo uma vez?) e
> `concisao` (diz o necessário sem sobrar?). Depois responda: qual dos dois descreve melhor a
> fotografia para quem não a vê (`A`, `B` ou `empate`), e qual você publicaria num site público
> (`A`, `B` ou `nenhum`).
>
> Não consulte nenhum outro arquivo além do lote e das fotos. Grave a saída como JSON no caminho
> indicado, uma entrada por par:
>
> ```json
> {"codigo": "",
>  "notas": {"A": {"fidelidade": 0, "clareza_ao_ouvido": 0, "concisao": 0},
>            "B": {"fidelidade": 0, "clareza_ao_ouvido": 0, "concisao": 0}},
>  "descreve_melhor": "", "publicaria": "", "criterio_decisivo": "", "motivo": ""}
> ```

## Limites declarados

- **O juiz é um modelo proprietário.** O pipeline usa só modelos abertos; a avaliação, não. O
  juiz não gera nem corrige descrição alguma.
- **A cegueira do A/B é imperfeita.** A descrição curatorial tem estilo de catálogo, e um leitor
  atento pode reconhecê-la. O sorteio tira a pista da posição, não a do estilo.
- **A baseline não foi escrita para ser alt-text.** Ela é comparada como alt-text porque é o que
  o acervo teria à mão para preencher o campo hoje vazio.
- **Não há avaliadores humanos nesta etapa.** O projeto não teve acesso a pessoas cegas nem a
  curadores do museu, e o A/B com avaliadores leigos saiu do escopo em 29/09/2026. A validação
  com usuários de leitor de tela fica como trabalho futuro.
- **O juiz não vê tudo**: recall de ~89% na calibração. Defeito ausente do relatório não é
  defeito ausente do texto.
