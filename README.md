# Acervo que Fala

Descrições acessíveis em dois níveis (alt-text da fotografia + descrição do objeto) para os 20.965 itens do acervo digital do Museu do Índio, geradas por modelos abertos de visão e linguagem, ancoradas nos metadados curatoriais — com baseline, avaliação por painel humano e revisão humana obrigatória.

> **Trabalho em andamento.** Projeto final do curso *Inteligência Artificial Generativa & Large Language Models* (ICA/PUC-Rio). O README final seguirá o modelo da banca ([docs/modelo-readme-banca.md](docs/modelo-readme-banca.md)); o plano de execução por etapas está em [docs/ETAPAS.md](docs/ETAPAS.md).

## Rodar a coleta

```
pip install -r requirements.txt
python app/tainacan.py --n 60
```

Saída em `dados/itens.json` (metadados) e `dados/estatisticas.json`. A API do Tainacan é pública, sem autenticação — não há segredos neste repositório.
