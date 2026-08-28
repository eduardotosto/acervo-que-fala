# Versionamento — tabela única

Cada camada do sistema versiona no seu próprio ritmo: o notebook é o contêiner, e dentro dele
viajam o prompt de observação, o prompt de redação e a rubrica — por isso o Notebook 04 **v8**
carrega a redação **v12**, a observação **v3.1** e a rubrica **v1.4**. Esta tabela é o mapa
único dessas quatro linhagens mais os lotes gerados, e é insumo direto do README final (E12).

**Fonte da verdade:** cada JSON em `resultados/` embute os prompts e a versão da rubrica usados
na rodada (artefato autodescritivo). A tabela foi reconstruída desses JSONs, dos notebooks no
git e do `ETAPAS.md`; onde a narrativa diverge do artefato, prevalece o artefato (caso
redação v10→v11, nota 2).

## A tabela

| Notebook (repo · versão no Drive) | Observação | Redação | Rubrica | Lote em `resultados/` | Data | Marco |
|---|---|---|---|---|---|---|
| 01_primeiro_item · v3 | v1 | — | — | `01_observacao_item_9196.json` (1 item) | 24/08 | E4: primeiro item ponta a ponta; zero alucinação |
| 02_nivel1_smoke_test · v1 | v2 | v2 ¹ | — | `02_nivel1_smoke_test.json` (5 itens) | 24/08 | E5: nível 1 no smoke test; Abano avisou o close |
| 03_rag_redacao · v1 | reusa as do 02 (v2) | v3 | v1.0 | `03_rag_redacao.json` (5 itens) | 24/08 | E6: RAG entra; 4 falhas da E5 → 1; bug do povo |
| 04_pipeline_completo · v1 | v2 | v4 | v1.0 | `04_pipeline_completo.json` (20 itens) | 24/08 | E7: pipeline fechado (nível 2 + flags) |
| 04 · v2 | v2 | v5 | v1.1 | `04_pipeline_completo_v2.json` (20) | 24/08 | 1ª revisão editorial (12 regras) |
| 04 · v3 | v2 | v6 | v1.1 | — nunca rodou | — | GPU bloqueada; correções herdadas pela v4 |
| 04 · v4 | v2 | v7 | v1.1 | `04_pipeline_completo_v4.json` (20) | 25/08 | 2ª revisão (regras 14–25); teto do prompt |
| 04 · v5 | v2 | v8 | v1.1 | `04_pipeline_completo_v5.json` (20) | 25/08 | prompt congelado no v8 |
| 05_bakeoff_redator · v1 | — | v8 | v1.1 | — nunca rodou | 25/08 | Gemma 3 em float16 quebra na T4 |
| 05 · v2 | reusa as do lote v5 (v2) | v8 (lida do resultado v5) | v1.1 | `05_bakeoff_gemma.json` (20) | 26/08 | bake-off: Gemma 3 12B via Unsloth |
| 04 · v6 | v3 | v9 | v1.2 | `04_pipeline_completo_v6.json` (20) | 26/08 | redesenho: seções nomeadas + Contrato de Fontes |
| 04 · v7 | v3 | v10 → v11 ² | v1.3 | `04_pipeline_completo_v7.json` (20) | 27/08 | garantias em código (escala, teto, alt bruto) |
| 04 · v8 | v3.1 | v12 | v1.4 | `04_pipeline_completo_v8.json` (20) | 27/08 | 8 políticas da 5ª adjudicação; retry (5/20) |
| 04 · v9 | v3.1 | v12 | v1.4 | — nunca rodou | 27/08 | só amplia `validar_rascunho`; superado pelo v10 |
| 04 · v10 | v3.1 | v13 | v1.4 | `04_pipeline_completo_v10.json` (20) | 27/08 | 6ª adjudicação; validador de 14 exigências; retry 19/20 |
| 05 · v3 | reusa as do lote v10 (v3.1) | v13 (lida do resultado v10) | v1.4 | `05_bakeoff_gemma_v2.json` (20; **sem textos**) | 28/08 | bake-off v2, rodada perdida: 19/20 sem JSON, erro não gravado |
| 05 · v4 | reusa as do lote v10 (v3.1) | v13 (lida do resultado v10) | v1.4 | `05_bakeoff_gemma_v3.json` (20; **sem textos**) | 28/08 | bake-off v2, 2ª rodada: OOM na T4 em 19/19 — causa gravada (o 12B não cabe sob o sistema atual) |
| 05 · v5 | reusa as do lote v10 (v3.1) | v13 (lida do resultado v10) | v1.4 | `05_bakeoff_gemma_v4.json` (20; **sem textos**) | 28/08 | bake-off v2, 3ª rodada: OOM idêntico (ajustes sem efeito) → **regra de parada: bake-off encerrado, Qwen v10 titular** |

¹ O prompt de redação do Notebook 02 nasceu sem rótulo; "v2" é o nome retroativo que o
Notebook 03 usa ao comparar as duas redações. Não existe redação v1.

² O Notebook 04 v7 foi criado com a redação v10, mas a 3ª revisão editorial (8 achados do
Eduardo) elevou o prompt a v11 **antes** da rodada. O `ETAPAS.md` e as análises da época dizem
"prompt v10"; o JSON do lote registra `prompt_redacao_v11` — e é o que rodou.

**Modelos:** observação sempre com Qwen3-VL-8B-Instruct em 4-bit; redação com o mesmo modelo,
exceto o Notebook 05 (Gemma 3 12B, `unsloth/gemma-3-12b-it-unsloth-bnb-4bit`). Embeddings do
RAG: Qwen3-Embedding-0.6B. Todos os lotes do Notebook 04 usam os mesmos 20 objetos (5 do smoke
test + 15 estratificados, seed 42); o bake-off redige esses mesmos 20 reaproveitando as
observações do lote v5.

## As quatro linhagens, com a causa de cada salto

**Observação:** v1 (Notebook 01, prompt anti-alucinação) → v2 (lacunas da E4: orientação,
partes internas, bordas) → v3 (redesenho de 26/08: seções nomeadas parseáveis, fim da pergunta
que induz resposta) → v3.1 (pede todas as cores, inclusive minoritárias).

**Redação:** v2 (Notebook 02) → v3 (diretrizes do RAG) → v4 (saída estruturada: alt + nível 2 +
flags) → v5 (1ª revisão editorial) → v6 (2 bugs da análise da v2; nunca rodou) → v7 (2ª revisão,
regras 14–25) → v8 (2 correções cirúrgicas; congelado) → v9 (Contrato de Fontes) → v10 (errata
do v6 + frase-etiqueta como afirmação; nunca rodou) → v11 (3ª revisão editorial) → v12 (8
políticas da 5ª adjudicação: quarentena, catálogo manda, contagens injetadas) → v13 (6ª
adjudicação: cor-material, alt restrito ao visível, povo/ano/origem na descrição).

**Rubrica:** v1.0 (E6: 8 regras + 11 diretrizes + 10 termos) → v1.1 (12 regras da 1ª revisão) →
v1.2 (enxuta: os trechos "geral" que o RAG nunca recuperava saem) → v1.3 (RAG híbrido: diretriz
pelo campo Categoria, não por sorteio semântico) → v1.4 (verbete de jargão de título, ex.
gameliforme).

**Lotes:** a numeração dos arquivos segue o notebook que os gerou — por isso não existem
`_v3.json` nem `_v9.json` (notebooks que nunca rodaram) e o lote do v1 não tem sufixo.

## Como ler as métricas entre lotes

A régua (`avaliacao/checar_lote.py`) e o gabarito de reincidência
(`avaliacao/gabarito_editorial.json` + `checar_gabarito.py`) evoluíram junto com os prompts —
cada revisão adicionou checagens que punem os lotes anteriores retroativamente. Número de
"problemas/item" só é comparável **dentro da mesma versão da régua**, nunca entre relatórios de
épocas diferentes; a comparação honesta é rodar a régua atual sobre todos os lotes (é o que a
tabela comparativa de `avaliacao/revisao_editorial_04.md` faz). Exemplo: o lote v8 marcou 0,5
problemas/item na régua da época e 4,0 na régua endurecida pela 6ª adjudicação — o lote não
piorou; a régua enxergou mais.

## Onde mora cada artefato

No repositório o nome é estável e o git é o versionamento (`notebooks/04_pipeline_completo.ipynb`
sempre contém a última versão; as anteriores estão nos commits). No Drive, arquivo novo leva
sufixo numérico e os antigos ficam (`04_pipeline_completo_v8.ipynb`...). Os links do Colab de
cada versão estão registrados no `docs/ETAPAS.md`.
