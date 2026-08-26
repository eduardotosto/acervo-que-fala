# Acervo que Fala

Descrições acessíveis em dois níveis (alt-text da fotografia + descrição do objeto) para os 20.965 itens do acervo digital do Museu do Índio, geradas por modelos abertos de visão e linguagem, ancoradas nos metadados curatoriais — com baseline (a descrição curatorial usada como alt-text), avaliação por métricas objetivas + comparativo cego entre modelos, e revisão humana obrigatória.

> **Trabalho em andamento.** Projeto final do curso *Inteligência Artificial Generativa & Large Language Models* (ICA/PUC-Rio). Este README será preenchido ao final, seguindo o modelo da banca ([docs/modelo-readme-banca.md](docs/modelo-readme-banca.md)). Até lá: o plano por etapas com o status atual está em [docs/ETAPAS.md](docs/ETAPAS.md), as regras editoriais extraídas das revisões em [avaliacao/revisao_editorial_04.md](avaliacao/revisao_editorial_04.md), e os notebooks executados no Colab em [notebooks/](notebooks/).

## Rodar a coleta

```
pip install -r requirements.txt
python app/tainacan.py --n 60
```

Saída em `dados/itens.json` (metadados) e `dados/estatisticas.json`. A API do Tainacan é pública, sem autenticação — não há segredos neste repositório.
