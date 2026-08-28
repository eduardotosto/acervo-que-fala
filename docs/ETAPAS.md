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
| E7 | Nível 2 + flags + saída estruturada; lote de 20 — Notebook 04 | ✅ 24/08 · **v10 rodado: 1,7 problemas/item (melhor lote)** · decisão: congelar × lapidar × trocar redator |
| E8 | `rodar.py` completo: métricas automáticas nos 40 casos | ⬜ |
| E9 | Lote completo no Colab (notebook com markdown explicativo) | ⬜ |
| E10 | Painel humano: material A/B + condução (trabalho de Eduardo; Claude prepara) | ⬜ |
| E11 | Site Gradio + deploy no HF Spaces + interface de revisão | ⬜ |
| E12 | Holdout (roda 1x) + README da banca + texto descritivo + ensaio da demo | ⬜ |
| EP | *(paralela, qualquer momento)* GitHub remoto: instalar `gh`, criar repo, push | ⬜ |

Mapeamento com o plano de 10 semanas: E1–E3 = Fases 0–1 · E4–E7 = Fase 2 · E8–E10 = Fase 3 · E11 = Fase 4 · E12 = Fase 5.

**Mapa único de versionamentos** (notebook × observação × redação × rubrica × lote):
`docs/VERSOES.md` (27/08/2026) — reconstruído dos JSONs de `resultados/`, que embutem os prompts
e a rubrica de cada rodada; onde a narrativa diverge do artefato, prevalece o artefato (o lote v7
rodou com a redação **v11**, não v10 — a 3ª revisão editorial elevou o prompt antes da rodada).
Insumo do README final (E12).

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
resíduo que sobreviveu a três prompts que o proibiam, foi a **15 → 0** — e a análise seguinte
mostrou que o crédito é do prompt v9, não da remoção da seção `FUNDO E ESTÚDIO`, que não chegou
a acontecer (errata abaixo).
Jargão de foto, artefato no alt e foto no nível 2 também zeraram, e o Qwen produziu sua primeira
flag de divergência legítima (sete tubos × seis do registro, o mesmo achado do Gemma).
**Dois custos:** a frase-etiqueta voltou (0 → 4) porque a lista explícita de proibições saiu do
prompt ao virar checklist positivo; e as flags de artefato caíram (5 → 2).
A vantagem do Gemma em flags de divergência (7 × 1) não foi tocada: é diferença de modelo.
Análise em `avaliacao/revisao_editorial_04.md`; resultado em `resultados/04_pipeline_completo_v6.json`.
*A rodada usou o notebook como estava no Drive pela manhã — as garantias da revisão técnica da
tarde (escala injetada, teto de plausibilidade, contradição isolada, alt bruto) ainda não rodaram.*

**Errata do lote v6 e Notebook 04 v7 (26/08/2026).** A análise do lote encontrou uma falha
silenciosa no próprio código: o modelo escreveu `FONDO E ESTÚDIO` em 19 das 20 observações e
`FUNDOS E ESTÚDIO` numa — nenhuma acertou a grafia exigida, então a seção **não foi lida nem
removida** em nenhum item. O fundo viajou inteiro para o prompt de redação e o alt ficou 0/20 com
"fundo" mesmo assim: o crédito é do prompt v9 e do pós-processamento, não da remoção da seção — e
quanto coube a cada um só a v7 dirá, porque ela salva o alt bruto. Pelo mesmo motivo, a perda de
artefatos tem outra causa: a observação **viu** os dois artefatos e os descreveu em outras seções
(`PARTES E QUANTIDADES`, `LEGIBILIDADE`, `FUNDO E ESTÚDIO`), respondendo "nenhum" em `ARTEFATOS` —
o modelo não repete o que já disse. É o terceiro caso em que a análise erra antes do modelo, sempre
por conclusão tirada sem conferir o dado bruto.

**O que a v7 corrige:** parse tolerante à grafia do cabeçalho, com aviso quando uma seção esperada
não aparece; flag de artefato por **varredura de todas as seções**, descartando menções sob negação
(validada contra o lote v6: 4/4 itens certos, 0 falso positivo, contra 2/4 da seção sozinha, e a
régua ganhou a checagem `artefato_visto_sem_flag`); e a regra contra frase-etiqueta de volta,
escrita como afirmação ("a primeira palavra do texto é o nome do objeto") — prompt de redação
**v10**. Entram também as garantias que ficaram prontas depois que o v6 já estava no Drive: escala
calculada, teto de plausibilidade, contradição isolada e alt bruto salvo.

**No Drive (convenção do projeto — arquivo novo leva sufixo, os antigos ficam):** o notebook está
em `notebooks/04_pipeline_completo_v7.ipynb`
(colab.research.google.com/drive/1ep0iZVKXPWWrr8kncWcVHpfH-PMiJceG) e a rubrica em
`dados/rubrica_v1_3.json`. Os dois foram conferidos depois do upload: o notebook bate célula a
célula com o do repositório (16/16) e a rubrica bate byte a byte (só a quebra de linha muda,
CRLF local × LF no Drive). O notebook lê a rubrica do Drive e, se não a encontrar, do
repositório público — a comparação vale para os dois caminhos.

**Lote v7 rodado (27/08/2026).** A régua atual (com as checagens dos 8 achados da terceira revisão)
pune todos os lotes retroativamente — a comparação honesta é por checagem e pela média:
**2,7 (v5) → 2,5 (v6) → 2,2 (v7) problemas/item** (Gemma 2,0, ainda no prompt antigo). O número
central da rodada: **o pós-processamento do fundo agiu em 0/20 alts** — o prompt v10 resolveu
sozinho o que era 15/20 na v5; o código ficou de rede de segurança ociosa, e o alt bruto salvo é a
prova. Zeraram: fundo, escala, miniatura, frase-etiqueta, especulação, jargão de foto, repetição de
atribuição, artefato sem flag. As **flags de cor estrearam** redescobrindo as penas azuis da Faixa
(o achado do smoke test, agora pelo Qwen), e o abano de 290 cm virou `metadado_suspeito` pela
primeira vez. A contradição brinquedo×caça seguiu não detectada mesmo como pergunta isolada — o
modelo harmoniza; resíduo assumido para a revisão humana. **Duas regressões nascidas das próprias
correções** (análise em `revisao_editorial_04.md`): a marca de atribuição migrou para o campo JSON
e sumiu do texto audível em 13/20 (correção candidata: o código sorteia a formulação e a injeta
como variável, como enquadramento e escala); e o teto de 30 palavras quebrou em 10/20 alts (31–53).
Persistem afirmações de ausência (9) e função óbvia (4).

**Quarta revisão editorial (27/08/2026) — a métrica que faltava.** Eduardo revisou os cards #1–#3
do v7 e parou: defeitos já apontados estavam voltando (escuríssimo, jargão "globular/extrovertida",
cor de material natural, analogias, sete tubos pela 4ª rodada) e apareceram alucinações novas
("decoração em relevo" onde o registro diz "pintados"; "alça lateral" inexistente; "bordadas" onde
o registro diz "costuradas em couro de onça"). Pedido dele: **consolidar todas as revisões como
métrica de avaliação** → `avaliacao/gabarito_editorial.json` (29 padrões verificáveis das 4
revisões) + `avaliacao/checar_gabarito.py` (matriz de reincidência, os 7 lotes). **A leitura
corrige o veredito do v7**: na métrica de reincidência, v7 = v6 = 14/29 defeitos presentes, PIOR
que v4/v5 (8/29) — o redesenho ganhou nos padrões estruturais que a régua mede e devolveu o que o
prompt de 25 regras segurava por extenso (o teto de saturação, medido pelo outro lado). Decisões
novas do Eduardo codificadas: **a contagem do catálogo prevalece sempre** (régua nova
`contagem_diverge_do_registro`, dispara na Flauta em 4 lotes) e **dimensão atipicamente pequena
vira flag de conferência** (piso implementado ao lado do teto). Defeitos presentes em 7/7 lotes:
"cabo" na zarabatana, contradição brinquedo×caça sem flag, dimensão pequena sem flag (este último
agora resolvido em código). Vocabulário aprovado registrado: "dispostos paralelamente" (do próprio
registro da Flauta).

**Revisão do juiz sobre o v7 completa (27/08/2026) — o fluxo invertido em operação.** Depois de o
Eduardo adjudicar "concordo" nos 3 cards-piloto, Claude revisou os 14 restantes com foto em
resolução máxima + registro completo: **~45 achados numerados** em `avaliacao/revisao_juiz_v7.md`,
aguardando adjudicação. Padrões sistemáticos: a observação perde artefatos visíveis (2 cards — só
revisão com imagem pega); o vocabulário do glossário é sistematicamente ignorado pelo redator
(gregas dispara nos 7 lotes; espinha-de-peixe em 2 cards); a regra 15 super-aplicada suprime
figuras reais (a onça do estojo Bororo virou "desenhos estilizados"; o "X" que o registro da
panela nomeia sumiu); molduras de variáveis vazam ("em escala de", "Escala:"); a ficha técnica
volta pelo nível 2. **Código novo saído da revisão:** filtro de cordel corrigido (a escala da
Flauta 210680 era 41 cm com cordel; o certo é 12,7), flag de alças soltas, e cinco checagens novas
na régua (`ausencia_no_alt`, `medida_no_alt`, `molde_de_escala_no_texto`, `colagem_do_registro`,
`estado_sem_fonte`) — a última corrigiu o próprio juiz, que ia reportar 5 estados alucinados
quando só 2 trocas Amazonas→Amazônia são reais (o dump do protocolo omitia o campo; caso-método:
a camada que audita também precisa ser auditável). Régua e gabarito rodados de novo nos 7 lotes.

**5ª adjudicação (27/08/2026) — o juiz calibrado e as 8 políticas novas.** Eduardo adjudicou os
48 achados do juiz: **concordância ~95%** (2 discordâncias + 1 parcial) e **recall ~89%** (6
achados que só ele viu, todos convertidos em checagem ou glossário) — números que validam o
LLM-as-judge da E10 com dados próprios. As discordâncias recalibraram a régua e o gabarito: a
regra 24 foi **revertida** no caso "cabo" (o termo está no catálogo e não é jargão — catálogo
manda; a linha 7/7 do gabarito era uma regra errada fabricando defeito universal), e duas medidas
coerentes deixaram de ser ficha técnica (3+ continua). **Oito políticas novas** registradas no
gabarito (`politicas.5a_adjudicacao_27_08`): foto sem resolução → flag e NENHUM texto; informação
flagada é omitida da redação (flag = quarentena); catálogo manda no vocabulário não-técnico;
espécie/figura só com fonte (zoomorfos → "animais", nunca "onça" sem catálogo); número literal do
catálogo (41,5 não vira 42 — código corrigido); alças/cordas fora da medida e do foco; função só
com especificidade cultural; jargão de título (gameliforme) explicado pelo glossário — **rubrica
v1.4** ganhou o verbete. Régua ganhou `povo_em_minuscula` e `funcao_obvia` ampliada (remo,
panela). Auditoria do dataset assumida como função do projeto (flags de dataset: nylon×algodão da
pulseira, miniatura×102 cm da zarabatana).

**Notebook v8 construído e no Drive (27/08/2026).** As oito políticas da 5ª adjudicação viraram
sistema: porteiro de resolução (foto < 100 mil px → flag `falta_de_resolucao`, nenhum texto),
seção EM QUARENTENA no prompt (o código lista o que as flags tiraram da redação), cláusula
"O CATÁLOGO MANDA NAS PALAVRAS" no contrato, CONTAGENS DO REGISTRO injetadas, escala com número
literal, funções óbvias vetadas com exemplos, e **validação com um retry** (marca de atribuição,
teto de 30, ausências, quarentena — diagnóstico devolvido ao modelo uma vez; campo `retry` salvo).
Observação v3.1 pede todas as cores, inclusive minoritárias. Contradição miniatura×função virou
heurística de código. Prompt de redação **v12**; rubrica **v1.4** no Drive (`dados/rubrica_v1_4.json`,
byte-conferida) e no repo. Notebook no Drive em `notebooks/04_pipeline_completo_v8.ipynb`
(colab.research.google.com/drive/1l96mAdKvMLK1Lvru8bVOKoQ8tzB1h4VD), conferido célula a célula
contra o repositório (16/16 idênticas). Dry-run com modelo simulado passou de ponta a ponta.
**Critério de saída registrado (decisão do Eduardo): a etapa só fecha com resultado satisfatório —
zero reincidência dos defeitos adjudicados no gabarito e régua limpa nas checagens mecânicas.**

**Lote v8 rodado (27/08/2026) — as políticas funcionaram.** Régua mecânica: **3,1 → 0,5
problemas/item** (11/20 sem problema); gabarito de reincidência: **25 → 2 defeitos distintos**.
Antes do veredito, 4 falsos positivos da própria régua foram achados e corrigidos (a fórmula
"ficha do museu" do nosso rodízio não era reconhecida; "gregos"×"grega"; o "X" que vem do
registro da Panela — exceção catálogo-manda agora codificada; item sem resolução punido por
checagens de texto que a política mandou não gerar). Vitrines: Flauta com **seis tubos** (defeito
de 4 lotes, resolvido pela contagem injetada), "costuradas" na Faixa, espinha-de-peixe no Abano,
azul/laranja em flag e fora do texto (quarentena), 4 medidas suspeitas fora do texto, Pião barrado
pelo porteiro de resolução. Retry usado em 5/20. **Resíduo = uma família**: jargão não traduzido
(globular/extrovertida/zoomorfos, 4 itens), função óbvia (5 — o modelo escreveu até os exemplos
proibidos do prompt), povo fora do alt (2) — nada disso estava no validador do retry. **Notebook
v9 pronto** (muda SÓ a função `validar_rascunho`: jargão, povo e função óbvia entram na cobrança
do retry; prompt intocado), no Drive em `notebooks/04_pipeline_completo_v9.ipynb`, conferido
célula a célula. Análise completa em `avaliacao/revisao_editorial_04.md`; tabela comparativa
atualizada com colunas v5 × v7 × v8.

**6ª adjudicação (27/08/2026) — revisão do Eduardo sobre o v8 vira o notebook v10.** Decisões
novas: material natural NUNCA tem nome de cor ("não existe base bege" — no máximo clara/escura,
procedência só do catálogo); alt restrito ao visível (a roseta do catálogo sai do alt); miçangas
"confeccionadas com linha" e penas "compostas por" (nunca "sobre"); cor presa à parte; povo, ano e
origem sempre na descrição; contenedor de amostra só no alt (dekai e Igarapé Ucuqui entram);
`funcao_obvia` recalibrada (função com fonte no campo Função é legítima — catálogo manda);
capitalização de frases corrigida em código. Dois achados de conferência: os textos truncados do
1376/200648 (régua nova `nivel2_truncado`) e o #14 que TINHA fonte (campo Função — a tabela é que
só mostrava a Descrição; corrigida). O v9 fica superado sem rodar; **v10 no Drive**. Régua ganhou
7 checagens; gabarito, 5 entradas e as 8 políticas da 6ª.

**Bake-off v2 preparado (27/08/2026) — decisão do Eduardo: caminho 3.** Dos três caminhos do
v10, o escolhido foi refazer o bake-off com o Gemma sob o sistema atual. O julgamento cego do
bake-off v1 fica **dispensado** — aquele material compara redatores sob o prompt v8, quatro
revisões atrás; a página e o gabarito lacrado permanecem como registro. O **Notebook 05 v3**
está no repositório: o Gemma 3 12B redige os mesmos 20 objetos reaproveitando do resultado do
04 v10 todos os insumos (observações v3.1, escala, quarentena, contagens, marca de atribuição
sorteada por item e as diretrizes pelos **ids salvos** — única variável: o redator), com o mesmo
prompt v13 lido de dentro do resultado e o mesmo validador com um retry. Duas decisões de
construção: o lado da redação foi **extraído byte a byte** do Notebook 04 v10 por script (não
redigitado), e a régua é **baixada do repositório** (`avaliacao/checar_lote.py`) em tempo de
execução — a cópia embarcada no 04 ficou defasada quando a régua foi recalibrada depois da
rodada, e o placar interno recalcula os problemas do Qwen com a mesma régua (régua única).
`max_seq_length` sobe para 8192 (o prompt v13 + retry não cabem nos 4096 do bake-off v1).
Dry-run com modelo simulado passou de ponta a ponta: retry forçado em 19/20, porteiro de
resolução ativo, campos do JSON idênticos aos do v10 — e a média recalculada do Qwen bateu com
o 1,7 registrado. Resultado esperado: `resultados/05_bakeoff_gemma_v2.json`.

**No Drive (27/08/2026):** `notebooks/05_bakeoff_redator_v3.ipynb`
(colab.research.google.com/drive/1Hd-W2JkSde9tzCVFNiqIcX0qD4cNgYyD), conferido depois do upload
por download e comparação: **byte a byte idêntico ao do repositório (12/12 células)**.

**Rodada perdida do bake-off v2 (28/08/2026) — e a lição de observabilidade.** A primeira
rodada do Notebook 05 v3 terminou "com sucesso" mas **19/20 itens saíram sem texto**: toda
extração de JSON falhou (`json_valido: false`, retry 0), e o `except` do notebook engolia a
exceção sem gravar nem o erro nem a resposta do modelo — o resultado
(`resultados/05_bakeoff_gemma_v2.json`, mantido como registro do incidente) não permite
diagnóstico. Pesquisa feita (pedido do autor): issues conhecidas do Unsloth com Gemma-3 no
caminho `apply_chat_template`/`token_type_ids`, e o Colab instala sempre o Unsloth mais novo —
o ambiente que rodou o bake-off v1 em 26/08 não é o mesmo de 28/08, e nenhuma rodada registrava
versões. **Notebook 05 v4** construído: resposta bruta + erro gravados por item, **teste de
fumaça** (geração mínima sem try/except — quebra alto antes do lote), `entradas` filtradas para
`input_ids`/`attention_mask`, `max_tokens` 1024, e versões de unsloth/transformers/torch salvas
no resultado. Dry-run com modelo simulado passou de ponta a ponta. No Drive:
`notebooks/05_bakeoff_redator_v4.ipynb`
(colab.research.google.com/drive/1Z_yhDS65BuRPiXPRMEiv0J5we3Y8bU0P), conferido por tamanho
exato e marcos do base64 (o caminho de upload foi validado byte a byte na véspera).

**Pendências da E7:** (1) rodar o bake-off v2 de novo no Colab (Notebook 05 v4, GPU T4,
Executar tudo → salva `resultados/05_bakeoff_gemma_v3.json`; se o teste de fumaça quebrar,
colar o traceback no chat); (2) análise do lote + página de comparação cega v2 (A/B sorteado
por item, gabarito lacrado) → **julgamento editorial cego do Eduardo decide o redator**.

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
