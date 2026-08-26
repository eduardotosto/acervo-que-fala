# Acervo que Fala — Execução em etapas

> Regras de ouro (pensadas para os créditos do Claude):
> 1. **1 etapa = 1 sessão = 1 commit.** Nenhuma etapa começa sem estimativa de terminar na mesma sessão.
> 2. **Fim de etapa:** commit + atualizar o status aqui. Se a sessão for interrompida, nada além do commit anterior se perde.
> 3. **Retomada:** toda sessão nova começa lendo este arquivo ("onde paramos").
> 4. **TODA inferência roda no Colab** (decisão de 24/08/2026 — nada de modelo local): notebooks didáticos em `notebooks/`, com passo a passo explicativo voltado à banca — célula markdown antes de cada código, pontos de verificação, 1 item antes de lote. Claude escreve o notebook e analisa os resultados; Eduardo abre no Colab, ativa a GPU e clica "Executar tudo". Não gasta crédito de Claude.
> 5. **Modelo por etapa:** Sonnet 5 para execução mecânica · Opus 5 para pipeline/RAG/código novo · Fable 5 para travamentos e decisões de arquitetura.

## Status

| Etapa | Descrição | Status |
|---|---|---|
| E1 | Fundação: repo + coleta reprodutível + amostra smoke | ✅ 24/08/2026 |
| E2 | Dataset completo (500 itens) + relatório de inspeção | ✅ 24/08/2026 |
| E3 | `casos.jsonl`: 40 casos fixos + 10 holdout (sessão interativa com Eduardo) | ✅ 24/08/2026 |
| E4 | Notebook 01 no Colab: Qwen3-VL-8B (4-bit) + 1 item ponta a ponta | ✅ 24/08/2026 (v3) |
| E5 | Pipeline nível 1 (alt-text) nos 5 objetos do smoke test — Notebook 02 | ✅ 24/08/2026 |
| E6 | RAG: rubrica indexada + recuperação por tipo de objeto — Notebook 03 | ✅ 24/08/2026 |
| E7 | Nível 2 + flags + saída estruturada; lote de 20 (5 smoke + 15 novos) — Notebook 04 | ✅ 24/08/2026 · lote **v6** rodado: 3/20 → 11/20 |
| E8 | `rodar.py` completo: métricas automáticas nos 40 casos | ⬜ |
| E9 | Lote completo no Colab (notebook com markdown explicativo) | ⬜ |
| E10 | Painel humano: material A/B + condução (trabalho de Eduardo; Claude prepara) | ⬜ |
| E11 | Site Gradio + deploy no HF Spaces + interface de revisão | ⬜ |
| E12 | Holdout (roda 1x) + README da banca + texto descritivo + ensaio da demo | ⬜ |
| EP | *(paralela, qualquer momento)* GitHub remoto: instalar `gh`, criar repo, push | ⬜ |

Mapeamento com o plano de 10 semanas: E1–E3 = Fases 0–1 · E4–E7 = Fase 2 · E8–E10 = Fase 3 · E11 = Fase 4 · E12 = Fase 5.

## Detalhe das etapas

### E1 — Fundação ✅
Estrutura do curso (`app/`, `dados/`, `avaliacao/`, `tests/`, `docs/`), `.gitignore`, `requirements.txt`, `app/config.py`, `app/tainacan.py` (coleta reprodutível com argparse), amostra smoke de ~60 itens versionada em `dados/`, git init + primeiros commits.
**Verificação:** `python app/tainacan.py --n 60` termina sem erro e `dados/itens.json` tem itens com metadados e URL de imagem.

### E2 — Dataset completo ✅
500 itens coletados (9 categorias, 49 povos, 100% com descrição curatorial; mediana da descrição: 164 caracteres). Relatório em `dados/relatorio_coleta.md`.
**Resultado da verificação:** Cerâmica = 51% do dataset (viés da ordenação por modificação recente — lotes de digitalização). **Decisão registrada:** os 50 casos da E3 serão estratificados por quota — máx. 10 de Cerâmica, presença garantida das categorias pequenas (Trançados, Instrumentos, Cordões e Tecidos), ≥15 povos distintos, e cobertura das 7 categorias de borda.

### E3 — casos.jsonl (interativa) 🔶
**Preparação concluída (24/08/2026):**
- Coleta complementar via taxquery (`tainacan.py --completar`): pool 500 → **555 itens**, todas as 10 categorias com ≥15 (incluindo **Armas**, que a coleta original tinha perdido por completo). Taxonomia `tnc_tax_543` e term ids registrados em `config.py`.
- Schema do caso + validador: `avaliacao/rodar.py --so-validar` (checa campos, quotas da E2, cobertura das 7 bordas, 40+10).
- Seleção estratificada determinística (`selecionar_candidatos.py`, seed 42): **70 candidatos**, 33 povos, quota + 2 extras por categoria; 5 âncoras do smoke test garantidas com bordas conhecidas.
- Página de revisão: `avaliacao/candidatos.html` (gerada por `gerar_pagina_revisao.py`).

**Concluída (24/08/2026):** Eduardo revisou os 70 cards, um a um. Decisões codificadas em `finalizar_casos.py` (REVISAO) → `casos.jsonl` (40) + `holdout.jsonl` (10), validados por `rodar.py --so-validar` (8/8 bordas, 30 povos, 10 categorias, quota Cerâmica 7/10). **Holdout não se abre até E12.**

Achados da revisão humana:
- **Nova borda descoberta:** `enquadramento_distante` (objeto ocupa área mínima do quadro — não é foto parcial) — 3 casos.
- **Padrão sistemático:** etiquetas/numerações de inventário fotografadas junto ao objeto em Utensílios, Plumária e Cordões (15 casos com `artefato_estudio`).
- **Todas as fotos de Armas são closes/detalhes** (5/5 candidatos `foto_parcial`).
- **11 divergências foto×catálogo** anotadas com o elemento específico ausente (cores, tonalidades, penas azuis, formatos, cordas) — o campo `notas` de cada caso guarda o que o Eduardo viu.
- 5 candidatos descartados por resolução de imagem inutilizável.

### E4 — Notebook 01 no Colab
`notebooks/01_primeiro_item.ipynb`: instala dependências, busca o Pote Karajá (9196) direto da API, carrega o **Qwen3-VL-8B quantizado em 4-bit** (cabe na GPU T4 gratuita) e roda a observação visual com o prompt anti-alucinação. Notebook didático: cada código precedido de explicação em linguagem simples, com nota de metodologia (vibe coding transparente) na abertura.
**Divisão:** Claude escreve o notebook · Eduardo roda no Colab (GPU T4 → "Executar tudo") e cola o resultado no chat.
**Verificação:** observação visual do Pote impressa, sem invenções óbvias (grafismos vermelho/preto descritos, nada inventado).

**Concluída (24/08/2026, notebook v3):** duas iterações de correção de ambiente (v2: não atualizar Pillow/requests; v3: pin da Pillow na versão do Colab — issue conhecida da Pillow 12 —, célula de checagem fail-fast e classe oficial `Qwen3VLForConditionalGeneration`). Resultado em `resultados/01_observacao_item_9196.json` (e no Drive). **Análise da observação:** zero alucinação — cores, forma, material e fundo corretos; incerteza expressa direito ("provavelmente uma jarra ou copo"); ausência de artefatos confirmada. Lacunas de cobertura p/ ajustar no prompt v2 (E5): não citou a inclinação do enquadramento nem a boca/interior visíveis e a faixa escura da borda.

### E5 — Pipeline nível 1 (Notebook 02) 🔶
`notebooks/02_nivel1_smoke_test.ipynb`: observação visual (**prompt v2** — pede orientação/partes internas/cores de bordas, corrigindo as lacunas da E4) → redação do alt-text com regras (≤30 palavras, objeto primeiro, avisa close, JSON estruturado) → comparação lado a lado com o gabarito humano da proposta + checagens automáticas (JSON válido, limite de palavras). Mesmo modelo nas duas etapas (memória da T4); a separação está no que ele recebe em cada uma.
**Verificação:** 5/5 JSONs válidos; caso crítico: o alt do Abano avisa que é close.

**Concluída (24/08/2026):** 5/5 JSONs válidos, 5/5 ≤30 palavras, **Abano avisou o close ✓**. Resultado em `resultados/02_nivel1_smoke_test.json`.
- **Observação v2 funcionou:** as 3 lacunas da E4 sumiram (Pote: inclinação, boca/interior e borda escura descritos); artefatos detectados ativamente (cartela da Faixa ✓; numeração da Flauta lida — "8285", real 8283, OCR quase exato).
- **Achados para o prompt de redação v2 (corrigir na E6/E7):** (1) *"close" usado errado* — 4/5 alts disseram "close" mesmo com objeto inteiro (a observação usa o termo de forma ambígua; exigir "inteiro"/"detalhe" como termos exclusivos); (2) *vazamento de artefatos* — cartela e numeração entraram no alt (regra: artefatos NUNCA no alt; viram flag); (3) *cores vagas* — "tons terrosos", "penas coloridas" (regra: nomear as cores da observação); (4) *hedge perdido* — "vime" afirmado quando a observação dizia "provavelmente".
- **Verificação humana resolvida (24/08):** a Faixa tem mesmo **duas penas azuis** (uma parcialmente encoberta) — **o modelo corrigiu o gabarito humano**, que registrava só a pena óbvia. Gabaritos atualizados (demo, proposta, notebook 02). Episódio de mão dupla máquina↔humano registrado para o texto descritivo.

### E6 — RAG (Notebook 03) 🔶
**Base de conhecimento autorada e versionada** em `dados/rubrica/rubrica.json` (v1.0): 8 regras gerais (codificam as 4 correções da E5), 11 diretrizes por categoria de objeto e 10 termos de glossário — glossário construído do vocabulário do próprio catálogo (acordelado, sarjado, gregas...), em vez do Tesauro (indisponível como dataset; decisão honesta registrada).
`notebooks/03_rag_redacao.ipynb`: embeddings **Qwen3-Embedding-0.6B** + busca por similaridade direta (30 trechos — ChromaDB fica para o site/E11, decisão explicada no notebook); teste de recuperação (tanga → miçangaria, não cerâmica); **redação v3** (regras fixas + diretrizes recuperadas) comparada com a v2 nos 5 objetos, com checagens automáticas das 4 falhas. Reaproveita as observações do Notebook 02.
**Verificação:** recuperação correta nos 2 testes + as 4 falhas da E5 zeradas na v3.

**Concluída (24/08/2026):** recuperação verificada ✓ (tanga→miçangaria, pote→cerâmica). Scorecard das 4 falhas na v3: "close" indevido **4/5→0/5 ✓**; cores vagas ~zeradas; hedge preservado ✓ (Abano: "provavelmente vime"→"fibra vegetal"); artefato no alt 2/5→**1/5** (Flauta ainda citou "marcação numérica" — endurecer regra 4 na E7 com exemplo negativo). Destaque do RAG em ação: o alt do Abano usou "espinha-de-peixe" vindo do glossário recuperado (`glossario-02`); campo `diretrizes_usadas` torna a recuperação rastreável por item.
**Bug de integração encontrado (Eduardo detectou):** a redação saiu **sem os povos** ("[nome do povo]" literal no Pote) — o resultado salvo do nb02 não carregava metadados e o nb03 passou Povo vazio. Erro de passagem de dados entre etapas, não do modelo. Correções na E7: pipeline completo direto da API + **regra nova: todo resultado salvo carrega os metadados-chave**. Resultado em `resultados/03_rag_redacao.json`.

### E7 — Nível 2 + flags (Notebook 04) ✅
`notebooks/04_pipeline_completo.ipynb`: pipeline fechado — observação (prompt v2) → **redação v4 estruturada** (alt-text + descrição do objeto + flags num único JSON; regra do artefato endurecida com exemplo errado×certo). Correções incorporadas: **bug do povo** (registro completo da API viaja no prompt e no resultado — regra nova), **salvaguardas de imagem** (EXIF transpose + RGB). Lote: 5 smoke + **15 novos** (seed 42, estratificado, fora dos 50 casos — ids no notebook e no commit). Verificação automática embutida: povo no alt, artefato, ≤30 palavras, atribuição no nível 2, caso-referência Abano.

**Concluída (24/08/2026):** 20/20 JSONs válidos, **20/20 sem problemas** na verificação automática (povo no alt ✓, "close" indevido 0 ✓, artefato no alt 0 ✓ — a Flauta parou de citar a numeração, remanescente da E6 resolvido), caso-referência Abano ✓✓. Bônus: a observação releu a numeração da Flauta como "8283" (corrigindo o "8285" da E5 — o número real do item é 51023, a inscrição física é o nº de inventário). Nível 2 já cita as aves das penas quando o registro traz (Faixa: arara/jaburu/jacu com mapa de cores; Braçadeiras: arara) e **não inventa** ave quando o registro cala (Flauta de osso). Resultado em `resultados/04_pipeline_completo.json`; página de revisão editorial em `resultados/tabela_lote_04.html` (gerada por `avaliacao/gerar_tabela_lote.py`).
**Revisão editorial (24/08/2026):** Eduardo revisou os cards #1–#4 da página e a revisão parou ali por decisão conjunta — os achados repetiam. Saíram **12 regras** (documentadas em `avaliacao/revisao_editorial_04.md`), aplicadas em **rubrica v1.1** (`dados/rubrica/rubrica.json` + Drive `dados/rubrica_v1_1.json`) e **prompt de redação v5** no **Notebook 04 v2** (Drive: colab.research.google.com/drive/1asI5gBepXxQuTYiqL5GwQtMp8g8wYPcq), com verificação automática ampliada (frases-etiqueta, afirmações de ausência, foto no nível 2) e resultado salvo como `04_pipeline_completo_v2.json`.
**Achados para prompt v5 / rubrica v1.1 (na origem da v2):** (1) **flags com recall baixo** — 1 gerada (cartela ✓), mas a numeração vista na Flauta não virou flag; (2) **alt deve nomear o objeto pelo título do registro** — Faixa virou "chapéu plumário" e Estojo peniano virou "bastão de madeira" (divergência visual×título sem flag); (3) defeitos de texto pontuais: "cinza-escur" truncado (item 210680, alt e nível 2) e "azul-escuríssimo" (500322); (4) hedge violado 1×: "corda de cânhamo" afirmada onde o registro diz fibra não identificada (210680). Revisão editorial do Eduardo sobre a tabela alimenta a rubrica v1.1 (hipóteses dele: material antes de cor; ave de origem das penas).

**Análise da v2 (24/08/2026, achada por checagem de código — não usou revisão visual do Eduardo):** vitórias claras 20/20 — fotografia (posição/inclinação/enquadramento) sumiu do nível 2; ficha técnica de medidas virou escala natural; "foi aquisição em" corrigido; abertura em rótulo sumiu; aves das penas citadas onde o registro traz; regra "todo artefato vira flag" funcionou (8 flags vs. 1 no lote anterior). **2 bugs reais achados**: (a) a regra "artefato nunca aparece" só estava escrita para o alt-text no prompt v5 — a Flauta descreveu a numeração no nível 2 mesmo com a flag correta gerada; (b) a atribuição ao registro sumiu em 15/20 textos — o prompt só garantia isso via um exemplo específico (o Pote), sem generalizar. **2 falsos positivos na própria checagem automática, também corrigidos**: "o objeto é" e "sobre fundo X" (vocabulário legítimo de padronagem, não fotografia) estavam sendo pegos em qualquer posição do texto, não só na abertura. **Prompt v6 + checagem corrigida no Notebook 04 v3** (Drive: colab.research.google.com/drive/1nhk-dsCCsWyG3dbko57ZXCeG4zmnxJaX), resultado esperado em `04_pipeline_completo_v3.json`.
**Segunda revisão editorial (25/08/2026, sem GPU — sobre o lote v2):** Eduardo revisou os **20 cards** com foco em fidelidade visual → **12 regras novas (14–25)** em `avaliacao/revisao_editorial_04.md`: fundo fotográfico contaminando cores do objeto; só afirmações verificáveis (sem "sugere/parecendo", inferências de uso, juízos, padrões abstratos virando "corações"); frases vazias cortadas; pares cor↔ave (cor primeiro); contagem de partes; relações de ponto de vista só no alt; enquadramento refinado (sangrar margens ≈ completo; nunca "inteiro/horizontal"); não explicar o óbvio; sem redundância lexical; conteúdo antes do recipiente; vocabulário fisicamente correto (zarabatana tem tubo; "tortual" não existe); escala = maior dimensão, miniatura declarada. **Achados factuais**: Pote 9196 = miniatura genuína (3 dimensões coerentes, não erro); Braçadeira 1376 = 76 cm deve incluir as "alças soltas" do registro (flag) e o registro tem os pares cor↔ave que o modelo não usou; Zarabatana 883523 = contradição interna do registro (Descrição "brinquedo em miniatura" × Função "utilizado para caça") — caso real de metadado_suspeito; "cabo" veio do próprio registro. **Prompt v7** (v6 + regras 14–25) e verificação ampliada (especulação, frases vazias, "fundo" no alt) no **Notebook 04 v4** (Drive: colab.research.google.com/drive/1N_iIlMK4xK05k7V8-n4iBynWde-sueOL), resultado esperado em `04_pipeline_completo_v4.json`. A v3 fica pulada (nunca rodou — GPU bloqueada; suas correções estão contidas na v4).
**Lote v4 rodado (25/08/2026) — o teto do controle por prompt.** Resultado misto: **4/20 sem problemas**, análise completa em `avaliacao/revisao_editorial_04.md`. Ganhou: **atribuição 5/20 → 20/20** (correção da v6 funcionou integralmente), contagem de partes ("seis tubos"), "sobre a argila bege" nas cerâmicas, fim das invenções "corações/flores" e da palavra "tortual". **Mas duas regras produziram efeito colateral**: (1) a regra dos pares cor↔ave **causou alucinação nova** — a Flauta de osso 210680 ganhou "penas de arara" sem nenhuma fonte (registro sem matéria-prima, observação sem menção; na v2 o modelo acertava justamente por não inventar); (2) a regra "uma atribuição por texto" quebrou a auditabilidade — a "roseta azul e verde" do Abano **está no registro** (verificado), mas aparece sem marca de atribuição e lê como se fosse visível. Regressões: "foi aquisição em" voltou (4 itens), povo sumiu do alt (200648), e 12 das 18 flags são só "existe um fundo" (várias afirmando ausência dentro da flag). Não pegaram: miniatura declarada, "tubo" na zarabatana, e `metadado_suspeito` zero vezes apesar de 2 casos claros (Abano de 290 cm reproduzido como "3 metros"; contradição brinquedo×caça do 883523, que o modelo harmonizou em vez de sinalizar).
**Conclusão metodológica (resultado defensável para a banca):** o Qwen3-VL-8B atingiu o teto de obediência a prompt — com 25 regras concorrendo, cada regra nova passou a custar uma antiga. **Decisão: parar de extrair regras**, aplicar só 2 correções pontuais (fonte obrigatória para nomear ave; atribuição por fato, não por texto) e seguir para E8–E10. Defeitos residuais são o que as flags + interface de revisão (E11) existem para capturar.
**Notebook 04 v5 pronto (25/08/2026):** prompt v8 = v7 + as 2 correções + 3 apertos de regressão ("adquirido em", povo sempre no alt, fundo de estúdio não é flag) + verificação com qualidade de flags (Drive: colab.research.google.com/drive/1sawQgxdQW3X16ZsY7mrs3JGA84nwy-Vg → salva `04_pipeline_completo_v5.json`). Após esta rodada o prompt CONGELA.
**Notebook 05 — bake-off de redator (25/08/2026, pedido do Eduardo):** Gemma 3 12B (`unsloth/gemma-3-12b-it-unsloth-bnb-4bit`, pré-quantizado, sem cadastro HF) redige os mesmos 20 objetos reaproveitando as observações salvas pela v5 — mesmo registro, mesma rubrica, mesmo prompt v8 (lido de dentro do resultado da v5), mesma verificação (Drive: colab.research.google.com/drive/1vNXhY6LedsIL52_oF9VpRy8Tw_I9LA3b → salva `05_bakeoff_gemma.json`). Critério de decisão: o Gemma só assume a redação se vencer nas checagens E no julgamento editorial do Eduardo; empate mantém o Qwen.
**Lote v5 rodado (25/08/2026) — prompt CONGELADO no v8.** As correções cirúrgicas **funcionaram no que dependia de instrução recuperável**: atribuição manteve 20/20 e a roseta do Abano agora diz "segundo o registro" ✓; "foi aquisição" 4→1; povo 20/20 ✓; **flags limparam** (18→5, sendo 4 REAIS — cartela da Faixa, marcação da Flauta finalmente flagada, 2 etiquetas — e só 1 ruído). **Mas os resíduos teimosos confirmaram o teto pela segunda vez**: (1) a "arara" voltou no 210680 mesmo com a regra "pior erro possível" — verificado: a observação diz só "penas vibrantes de cor vermelha"; o prior "pena vermelha→arara" do 8B é imune a prompt; (2) "sobre fundo X" persiste em 15/20 alts; (3) "close-up"/"plano médio" apareceram como vocabulário novo de enquadramento; (4) miniatura não declarada; (5) etiqueta vazou para o alt do 1376 (regressão pontual da regra mais antiga); (6) metadado_suspeito segue 0× (290 cm reproduzido de novo). Sem problemas: 3/20 — número enganoso: a qualidade real subiu (atribuição, flags), os defeitos restantes são padrões mecânicos repetitivos.
**Encaminhamento:** resíduos mecânicos ("sobre fundo X", contagem de palavras) são candidatos a **pós-processamento determinístico** na E8 (código remove, não prompt); a alucinação da arara vira caso de estudo do bake-off (o Gemma resiste ao prior sob o mesmo prompt?) e, em produção, é o que a revisão humana com flags captura.
**Bake-off rodado (26/08/2026, Notebook 05 v2 — Gemma via Unsloth):** placar objetivo nas mesmas checagens: **Gemma 13/20 sem problemas × Qwen 3/20**. "Fundo" no alt: 15/20 → **1/20**. Atribuição: 20/20 nos dois. Flags do Gemma com qualidade nova: **7 divergências reais** (incluindo as penas azuis da Faixa ausentes do registro — o achado original do smoke test, redescoberto pelo modelo — e a marcação "8283" da Flauta virando metadado_suspeito). Fraquezas do Gemma: "Detalhe de" usado em excesso (13/20 alts, vs 5/20 do Qwen — objetos inteiros marcados como detalhe), 1 figura subjetiva ("forma de flor"), 2 medidas no alt. Pontos cegos compartilhados pelos dois: miniatura não declarada, "cabo" na zarabatana, 290 cm sem flag. Resultado em `resultados/05_bakeoff_gemma.json`; **página de comparação CEGA** em `resultados/tabela_bakeoff.html` (A/B sorteado por item, gabarito em `avaliacao/bakeoff_gabarito.json` — não abrir antes de julgar). Pendente: julgamento editorial cego do Eduardo → decisão do redator.
**ERRATA (26/08/2026):** a "alucinação da arara" da v4/v5 **não era alucinação** — o campo Descrição do registro do 210680 diz "tufos de penas de arara de cor vermelhas" (a análise da época leu a Descrição truncada em 200 caracteres). A conclusão de saturação permanece pelas regressões verificadas; detalhes em `avaliacao/revisao_editorial_04.md` (seção Errata).

**Redesenho do sistema de instruções (26/08/2026) — a hipótese do Eduardo.** Antes de julgar o
bake-off, o autor levantou que parte dos erros vinha de instruções mal desenhadas, não do modelo.
A análise confirmou três mecanismos (`avaliacao/analise_prompt_rubrica.md`): frase de exemplo do
prompt copiada literalmente ("sobre a argila bege" numa bolsa de fio de tucum); pergunta que induz
resposta na observação; palavra-gatilho lida sem a negação ("não há close-up" → alt vira detalhe).
Achado estrutural junto: os 11 trechos "geral" da rubrica **nunca eram recuperados** — a função
`recuperar()` os pulava por desenho, e eles pareciam regra ativa. Resultado: **observação v3** em
seções nomeadas, **redação v9** com Contrato de Fontes, **rubrica v1.2** enxuta e o **Notebook 04
v6** (`avaliacao/prompt_v9_proposta.md`, revisado pelo Eduardo antes de virar código).

**Revisão técnica e endurecimento do v6 (26/08/2026).** Revisão do notebook, dos três documentos e
da rubrica antes de rodar, com correções em três frentes:

- **Bugs achados e corrigidos:** o parse das seções não lia cabeçalho em negrito ou em título
  markdown (a seção era removida do texto mas não lida — o enquadramento caía no padrão em
  silêncio); o pós-processamento do alt amputava a frase depois de "fundo" ("sobre fundo bege **e
  boca larga**"); a verificação repetia a doença que o próprio projeto diagnosticou, casando
  "aparece" com "parece" e "profundo" com "fundo"; o embedder ocupava a GPU antes do modelo 4-bit;
  o alt bruto não era salvo, o que impedia separar o efeito do prompt do efeito do pós-processamento.
- **Decisões que saíram do prompt para o código:** `FUNDO E ESTÚDIO` deixou de viajar para a
  redação (o que o texto não pode usar, não viaja); a diretriz de categoria passou a vir do campo
  `Categoria` do registro em vez de sorteio semântico (RAG híbrido, rubrica **v1.3**); a **escala**
  virou aritmética sobre `Dimensões`; a **plausibilidade da dimensão** virou detecção de outlier
  com teto por categoria (Q3 + 3×IQR do próprio acervo, piso de 150 cm — 0,4% de alarme em 547
  itens); a **contradição entre campos** virou pergunta isolada, fora da tarefa de escrita.
- **Régua única (`avaliacao/checar_lote.py`):** as checagens de hoje aplicadas aos cinco lotes
  anteriores, tabela em `avaliacao/revisao_editorial_04.md`. A régua reproduz achados que vieram de
  leitura humana (atribuição sumindo em 15/20 na v2, "fundo" subindo 5→15 na linha do Qwen) e
  revela dois defeitos que nenhuma versão da verificação enxergava: **escala pela medida errada nos
  cinco lotes** e **miniatura não declarada nos cinco**. Com a régua única o bake-off fica Gemma
  11/20 × Qwen v5 3/20 (era 13 × 3 com as réguas antigas).

**Lote v6 rodado (26/08/2026) — a hipótese se confirma.** Mesmo modelo, mesmos 20 objetos, mesma
régua: **3/20 (v5) → 11/20 (v6) sem problemas**, empatando com o Gemma. O fundo do estúdio no alt,
resíduo que sobreviveu a três prompts que o proibiam, foi a **15 → 0** quando a seção `FUNDO E
ESTÚDIO` parou de viajar para a redação — regra negativa planta a palavra proibida no contexto.
Jargão de foto, artefato no alt e foto no nível 2 também zeraram, e o Qwen produziu sua primeira
flag de divergência legítima (sete tubos × seis do registro, o mesmo achado do Gemma).
**Dois custos:** a frase-etiqueta voltou (0 → 4) porque a lista explícita de proibições saiu do
prompt ao virar checklist positivo; e a observação v3 **perdeu artefatos** (5 → 2 flags) — não é
bug de parse, é a observação em seções deixando de ver a marcação da Flauta e a etiqueta do 200648.
A vantagem do Gemma em flags de divergência (7 × 1) não foi tocada: é diferença de modelo.
Análise em `avaliacao/revisao_editorial_04.md`; resultado em `resultados/04_pipeline_completo_v6.json`.
*A rodada usou o notebook como estava no Drive pela manhã — as garantias da revisão técnica da
tarde (escala injetada, teto de plausibilidade, contradição isolada, alt bruto) ainda não rodaram.*

**Pendências da E7:** (1) rodar o notebook v6 **de novo**, com as garantias da revisão técnica (escala,
plausibilidade, contradição isolada) + a lista de proibições de abertura de volta no prompt; (2) **julgamento editorial cego do bake-off** (`resultados/tabela_bakeoff.html`,
gabarito lacrado em `avaliacao/bakeoff_gabarito.json`) → decide o redator.

### E8 — Métricas automáticas
`avaliacao/rodar.py` completo: schema válido, ancoragem, comprimento do alt, checklist por categoria. Primeira rodada oficial nos 40 casos → `avaliacao/resultados/`.
**Verificação:** uma tabela de métricas impressa em um comando.

### E9 — Lote no Colab
Notebook `notebooks/01_lote_descricoes.ipynb` (com células markdown explicativas, padrão combinado) para gerar descrições dos 40 casos + amostra ampliada com GPU. Eduardo roda ("Executar tudo"), baixa resultados, Claude analisa.
**Verificação:** resultados idênticos em formato aos do pipeline local.

### E10 — Avaliação cega e por critérios (redesenhada 25/08/2026)
**Mudança de metodologia (decisão do Eduardo):** o projeto NÃO terá acesso a usuários cegos nem a curadores do museu. A avaliação foi redesenhada para refletir a realidade, com a limitação registrada honestamente no README (e a validação com usuários reais documentada como trabalho futuro). Três frentes:
1. **A/B cego com avaliadores leigos** (3–5 pessoas — colegas do estúdio, amigos): descrição curatorial × gerada, ordem aleatorizada, sem saber qual é qual; formulário simples (qual descreve melhor? qual você confiaria num site público? notas por critério).
2. **LLM-juiz** com a rubrica de 25 regras + os critérios de cada caso — avaliação automatizada e rastreável dos 40 casos (metodologia LLM-as-judge, tema do próprio curso; juiz ≠ redator para reduzir viés).
3. **Teste de leitor de tela pelo próprio Eduardo**: NVDA (gratuito, Windows) lendo os alt-texts em contexto de página — a experiência auditiva real, na primeira pessoa que o projeto consegue alcançar.
A pergunta-guia do projeto ajusta junto: "as descrições geradas superam a descrição curatorial usada como alt-text, **segundo critérios objetivos de acessibilidade e avaliação cega**?" (atualizar proposta/README na E12; **avisar a Manoela da mudança**).
**Verificação:** resultados por caso registrados em `avaliacao/painel/`.

### E11 — Site
`site/app.py` (Gradio): navegação pelos objetos, dois níveis, comparativo com baseline, flags — servindo o lote pré-computado. Interface de revisão (aprovar/editar). Deploy no HF Spaces gratuito.
**Verificação:** URL pública funcionando.

### E12 — Fechamento
Rodar holdout (primeira e única vez). Preencher `docs/modelo-readme-banca.md` → `README.md` final (Resumo, Introdução, Modelagem, Resultados, Conclusões — remover comentários HTML). Texto descritivo. Ensaio da demo: problema em 30s, 2 casos, 1 falha explicada.
**Verificação:** checklist §8.8 do curso completo.

### EP — GitHub remoto (paralela) ✅
**Concluída (25/08/2026):** o `gh` já estava instalado e autenticado (conta eduardotosto, keyring). Repo criado com `gh repo create --source . --push`: **github.com/eduardotosto/acervo-que-fala** — os 28 commits subiram com o histórico completo, branch main com tracking. **Tornado PÚBLICO em 25/08/2026** (decisão do Eduardo) — o link pode ir na nota para a orientadora e na página de andamento.
