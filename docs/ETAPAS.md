# Acervo que Fala — Execução em etapas

> Regras de ouro (pensadas para os créditos do Claude):
> 1. **1 etapa = 1 sessão = 1 commit.** Nenhuma etapa começa sem estimativa de terminar na mesma sessão.
> 2. **Fim de etapa:** commit + atualizar o status aqui. Se a sessão for interrompida, nada além do commit anterior se perde.
> 3. **Retomada:** toda sessão nova começa lendo este arquivo ("onde paramos").
> 4. **GPU vai para o Colab** (não gasta crédito de Claude): lotes de inferência e processamento pesado rodam em notebook, Claude só escreve o notebook e analisa o resultado.
> 5. **Modelo por etapa:** Sonnet 5 para execução mecânica · Opus 5 para pipeline/RAG/código novo · Fable 5 para travamentos e decisões de arquitetura.

## Status

| Etapa | Descrição | Status |
|---|---|---|
| E1 | Fundação: repo + coleta reprodutível + amostra smoke | ✅ 24/08/2026 |
| E2 | Dataset completo (500 itens) + relatório de inspeção | ✅ 24/08/2026 |
| E3 | `casos.jsonl`: 40 casos fixos + 10 holdout (sessão interativa com Eduardo) | ⬜ |
| E4 | Ambiente de inferência: Ollama + qwen3-vl:8b local, 1 item ponta a ponta | ⬜ |
| E5 | Pipeline nível 1 (alt-text) nos 5 objetos do smoke test | ⬜ |
| E6 | RAG: rubrica indexada + recuperação por tipo de objeto | ⬜ |
| E7 | Nível 2 + flags de divergência + saída estruturada; lote de 20 itens | ⬜ |
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

### E3 — casos.jsonl (interativa)
Esquema do caso definido; Eduardo escolhe os 50 itens (estratificados pelas 6 categorias de borda já mapeadas: `jargao_catalogo`, `divergencia_imagem_catalogo`, `artefato_estudio`, `foto_parcial`, `metadado_suspeito`, `texto_sem_hierarquia` + `caso_simples`) e define critérios por caso. 10 vão para `holdout.jsonl` — **não abrir até E12**.
**Verificação:** `python avaliacao/rodar.py --so-validar` valida o schema dos 50.
**Atenção:** é a sessão de julgamento do Eduardo — Claude guia, ele decide.

### E4 — Ambiente de inferência
Instalar Ollama, `ollama pull qwen3-vl:8b` (~6 GB), `app/vlm.py` com a função `observar()`, rodar 1 item de ponta a ponta (Pote 9196). Se a máquina não aguentar o modelo local: fallback imediato para notebook Colab 01 (mesma função, mesma interface).
**Verificação:** observação visual do Pote impressa, sem invenções óbvias.

### E5 — Pipeline nível 1
`app/redator.py` v1: observação + metadados → alt-text com ancoragem (JSON estruturado). Rodar nos 5 objetos do smoke test e comparar com os alt-texts manuais da proposta (que viram referência de qualidade).
**Verificação:** 5/5 saídas com schema válido; comparação lado a lado gerada.

### E6 — RAG
Indexar rubrica de descrição (adaptada em `dados/rubrica/`) + trechos do Tesauro com ChromaDB + Qwen3-Embedding. `app/rag.py`: recuperação por tipo de objeto. Integrar ao redator.
**Verificação:** para "tanga de miçangas", a recuperação traz trecho de têxtil/adorno, não de cerâmica.

### E7 — Nível 2 + flags
Descrição do objeto (nível 2) + flags de divergência + ancoragem afirmação-a-afirmação. Rodar lote de 20 itens novos (fora dos casos).
**Verificação:** o caso Abano reproduz o comportamento esperado (alt avisa que é close; nível 2 usa o registro com atribuição).

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
