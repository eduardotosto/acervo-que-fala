# Acervo que Fala — instruções do projeto

Projeto final da pós **Inteligência Artificial Generativa & Large Language Models** (ICA/PUC-Rio).
Autor: Eduardo Tosto · matrícula 252.100.045 · orientadora: Profa. Manoela Kohler.
Repositório público: github.com/eduardotosto/acervo-que-fala

## O que o sistema faz

Descrições de acessibilidade em dois níveis para o acervo digital do Museu do Índio
(20.965 itens, API Tainacan pública, publicados hoje com `alt=""`):

- **nível 1 — alt-text**: descreve a FOTOGRAFIA, ≤30 palavras, começa pelo objeto e pelo povo;
- **nível 2 — descrição do objeto**: descreve o OBJETO, independente da foto (serve de audioguia);
  fato de catálogo só entra com marca de atribuição ("segundo o registro do museu");
- **flags**: o que precisa de revisão humana (artefato de estúdio, divergência foto×catálogo,
  metadado suspeito).

Pipeline: observação (o modelo vê SÓ a foto) → redação (só texto: observação + registro + diretrizes
do RAG) → verificação automática → revisão humana. A separação existe para auditar cada erro:
nasceu no olho ou na escrita?

**Baseline da avaliação:** a descrição curatorial usada como alt-text.

## Comece toda sessão por aqui

1. `docs/ETAPAS.md` — o status de cada etapa (E1–E12 + EP) e o histórico de achados. É a fonte
   da verdade do andamento.
2. `avaliacao/revisao_editorial_04.md` — as 25 regras editoriais extraídas das revisões humanas,
   cada uma rastreável ao caso que a originou. Inclui a errata da "arara".
3. `avaliacao/analise_prompt_rubrica.md` — por que erros nasciam do próprio prompt (papagaio de
   exemplo, pergunta que induz resposta, sobrecarga de regra negativa).

**Regra de trabalho:** 1 etapa = 1 sessão = 1 commit. Ao fechar uma etapa: atualizar `ETAPAS.md`,
commitar e reportar.

## Regras de procedimento com o autor (28/08/2026)

- **Consulta prévia obrigatória:** nenhum notebook/Colab novo (nem versão nova) e nenhuma
  decisão de impacto, arquitetura ou alto nível sem apresentar antes ao autor o quê, o porquê
  e as alternativas — em 2-3 frases. Ele decide.
- **Aprendizado > conclusão da tarefa.** Explicar os pontos cruciais de forma sucinta, sem
  detalhamento técnico: o autor não é dev; o que interessa é a lógica por trás de cada decisão.
- **Erro ou imprevisto:** primeiro explicar o que aconteceu, por quê, e expor o raciocínio do
  diagnóstico; a proposta de correção vem depois, para aprovação.
- **Conceito novo se explica na hora** (dry-run, smoke test, LLM-as-judge...), com analogia
  simples.

## Divisão de responsabilidades do sistema

| Camada | O que carrega |
|---|---|
| Prompt de observação (v3) | O olhar, em seções nomeadas; `ENQUADRAMENTO:` e `ARTEFATOS:` são consumidos pelo código |
| Prompt de redação (v9) | Contrato de Fontes + regras universais, hierarquizadas |
| `dados/rubrica/rubrica.json` (v1.2) | Só o que o RAG entrega: diretrizes por categoria + glossário |
| Código do notebook | Garantias mecânicas: flags automáticas, enquadramento injetado, pós-processamento |
| `docs/` e `avaliacao/` | Documentação para a banca — não é insumo de runtime |

Regra que gerou essa divisão: **o que precisa de 100% de garantia não se pede a um modelo, se
resolve em código.** E regra universal não pode depender de sorteio do RAG (a função `recuperar()`
não entrega trechos "gerais").

## Convenções de escrita

- **Português** no texto, **jargão técnico em inglês** sem tradução (smoke test, prompt, baseline,
  bake-off, flag, RAG, fine-tuning).
- **Não usar o rótulo "designer"** para se referir ao autor em nenhum material do projeto.
- **Não citar fine-tuning** em nenhum material — nem como extensão futura (fora do escopo).
- **Nada de julgamentos que o autor não fez**: relatar fato e consequência, nunca "foi a decisão
  certa", "ficou excelente". O julgamento é dele.
- As descrições são **ouvidas** por pessoas cegas via leitor de tela — nunca "lidas".

## Execução: sempre no Colab

Toda inferência roda no **Google Colab** (T4 gratuita), nunca local. Os notebooks são didáticos,
voltados à banca: célula markdown explicando cada etapa antes do código. O autor só abre, ativa a
GPU e clica em "Executar tudo"; o Claude escreve o notebook, busca o resultado no Drive e analisa.

**Drive:** `MyDrive/00_IA/GenAI & LLMs - PUC/Projeto_LLM/` → `notebooks/`, `resultados/`, `dados/`.
Arquivo novo no Drive leva sufixo numérico (`_v6`); as versões antigas ficam. No repo, o nome é
estável — o git é o versionamento.

### Armadilhas de ambiente já pagas (não repetir)

- **Pillow**: NUNCA atualizar no Colab. Pin obrigatório: `pillow=={PIL.__version__}` na instalação
  (Pillow 12 quebra o torchvision do Colab com `ImportError: _Ink`).
- Erro que persiste depois de "Reiniciar sessão" = disco sujo → **"Desconectar e excluir ambiente
  de execução"**.
- **Gemma 3 não funciona em float16** (ativações estouram o teto de 65504) e a T4 não tem bfloat16
  → carregar via **Unsloth**, único framework que corrige isso na T4.
- **4-bit + `device_map="auto"` com a GPU ocupada** = camadas vão para a CPU, o estado de
  quantização se perde e a geração quebra com `AssertionError`. Liberar a GPU antes de carregar
  o modelo grande.
- Classe oficial do Qwen: `Qwen3VLForConditionalGeneration`.
- Imagens: `ImageOps.exif_transpose(...).convert("RGB")` sempre.
- **Pesquisar antes de corrigir** erro de Colab — pedido explícito do autor.

## Windows / PowerShell

- Evitar aspas duplas em mensagens de `git commit` (quebram o parsing do here-string).
- `gh` está em `C:\Program Files\GitHub CLI\gh.exe`, autenticado, mas **fora do PATH** — chamar
  pelo caminho completo. `git push` normal funciona.
- Pasta dentro do Dropbox: um `update_ref failed` ocasional é lock do Dropbox, não erro real —
  conferir com `git fetch` antes de reagir.

## Achados que definem o projeto (não redescobrir)

- **O modelo corrigiu o gabarito humano**: a Faixa Kalapalo tem duas penas azuis, não uma.
- **Saturação de prompt**: acima de ~25 regras, o cumprimento fica instável — regras antigas
  regridem quando novas entram. Levou ao congelamento do prompt e ao redesenho do sistema.
- **Erros induzidos pelo próprio prompt**: exemplos literais viram papagaio ("sobre a argila bege"
  numa bolsa de tucum); palavra-gatilho é lida sem a negação ("não há close-up" → alt vira detalhe).
- **O catálogo também erra** — abano de 290 cm, "brinquedo em miniatura" com função "caça".
  As flags viraram, de quebra, uma auditoria do acervo.
- **A análise também erra**: a "alucinação da arara" não era alucinação — a evidência tinha sido
  lida truncada. Cada camada da avaliação precisa ser auditável.
