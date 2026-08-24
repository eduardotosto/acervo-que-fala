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
| E7 | Nível 2 + flags + saída estruturada; lote de 20 (5 smoke + 15 novos) — Notebook 04 | 🔶 notebook v1 no Drive — aguardando Eduardo rodar (~40 min) |
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
**Revisão editorial (24/08/2026):** Eduardo revisou os cards #1–#4 da página e a revisão parou ali por decisão conjunta — os achados repetiam. Saíram **12 regras** (documentadas em `avaliacao/revisao_editorial_04.md`), aplicadas em **rubrica v1.1** (`dados/rubrica/rubrica.json` + Drive `dados/rubrica_v1_1.json`) e **prompt de redação v5** no **Notebook 04 v2** (Drive: colab.research.google.com/drive/1asI5gBepXxQuTYiqL5GwQtMp8g8wYPcq), com verificação automática ampliada (frases-etiqueta, afirmações de ausência, foto no nível 2) e resultado salvo como `04_pipeline_completo_v2.json`. Pendente: Eduardo rodar a v2 (~40 min); segunda revisão foca só fidelidade visual.
**Achados para prompt v5 / rubrica v1.1 (entram na E8):** (1) **flags com recall baixo** — 1 gerada (cartela ✓), mas a numeração vista na Flauta não virou flag; (2) **alt deve nomear o objeto pelo título do registro** — Faixa virou "chapéu plumário" e Estojo peniano virou "bastão de madeira" (divergência visual×título sem flag); (3) defeitos de texto pontuais: "cinza-escur" truncado (item 210680, alt e nível 2) e "azul-escuríssimo" (500322); (4) hedge violado 1×: "corda de cânhamo" afirmada onde o registro diz fibra não identificada (210680). Revisão editorial do Eduardo sobre a tabela alimenta a rubrica v1.1 (hipóteses dele: material antes de cor; ave de origem das penas).

### E8 — Métricas automáticas
`avaliacao/rodar.py` completo: schema válido, ancoragem, comprimento do alt, checklist por categoria. Primeira rodada oficial nos 40 casos → `avaliacao/resultados/`.
**Verificação:** uma tabela de métricas impressa em um comando.

### E9 — Lote no Colab
Notebook `notebooks/01_lote_descricoes.ipynb` (com células markdown explicativas, padrão combinado) para gerar descrições dos 40 casos + amostra ampliada com GPU. Eduardo roda ("Executar tudo"), baixa resultados, Claude analisa.
**Verificação:** resultados idênticos em formato aos do pipeline local.

### E10 — Painel humano
Claude prepara: planilha/formulário A/B cego (descrição curatorial × gerada, ordem aleatorizada), roteiro de sessão, termo de consentimento simples. Eduardo conduz com 1 curador/museólogo + 2 usuários de leitor de tela. Claude consolida os resultados.
**Verificação:** resultados por caso registrados em `avaliacao/painel/`.

### E11 — Site
`site/app.py` (Gradio): navegação pelos objetos, dois níveis, comparativo com baseline, flags — servindo o lote pré-computado. Interface de revisão (aprovar/editar). Deploy no HF Spaces gratuito.
**Verificação:** URL pública funcionando.

### E12 — Fechamento
Rodar holdout (primeira e única vez). Preencher `docs/modelo-readme-banca.md` → `README.md` final (Resumo, Introdução, Modelagem, Resultados, Conclusões — remover comentários HTML). Texto descritivo. Ensaio da demo: problema em 30s, 2 casos, 1 falha explicada.
**Verificação:** checklist §8.8 do curso completo.

### EP — GitHub remoto (paralela)
Instalar `gh` (`winget install GitHub.cli`), autenticar, criar repo privado `eduardotosto/acervo-que-fala`, push. Os commits locais garantem o histórico até lá — o push pode acontecer a qualquer momento sem pressa.
