# Relatório de inspeção do dataset — E2 (2026-08-24)

**500 itens** com imagem e metadados, coletados da coleção pública do Museu do Índio (Tainacan). Gerado por `python app/relatorio.py`.

## Presença dos campos-chave

| Campo | Presente | % |
|---|---:|---:|
| Descrição | 500/500 | 100% |
| Povo | 500/500 | 100% |
| Categoria | 500/500 | 100% |
| Estado de origem | 500/500 | 100% |
| Ano de aquisição do objeto | 500/500 | 100% |
| Dimensões | 499/500 | 100% |
| Autoidentificação | 498/500 | 100% |
| Função | 495/500 | 99% |
| Matéria-prima | 459/500 | 92% |
| Técnica de confecção | 414/500 | 83% |
| Nome étnico do item | 96/500 | 19% |

Descrição curatorial (a baseline): mediana de **164 caracteres**; menor 19, maior 957.

## Distribuição por categoria

| Valor | Itens | % |
|---|---:|---:|
| Cerâmica | 254 | 51% |
| Adornos de Materiais Ecléticos, Indumentária e Toucador | 102 | 20% |
| Objetos rituais, mágicos e lúdicos | 57 | 11% |
| Adornos Plumários | 51 | 10% |
| Utensílios e implementos de materiais ecléticos | 16 | 3% |
| Trançados | 8 | 2% |
| Cordões e Tecidos | 8 | 2% |
| Instrumentos musicais e de sinalização | 3 | 1% |
| Etnobotânica | 1 | 0% |

**Verificação da E2** (nenhuma categoria >50%): maior categoria = 51% → ⚠️ categoria dominante acima de 50% — estratificar a amostra dos casos

## Distribuição por povo

| Valor | Itens | % |
|---|---:|---:|
| Karajá | 92 | 18% |
| Kadiweu | 91 | 18% |
| Tiriyó | 27 | 5% |
| Canela | 26 | 5% |
| Xavante | 26 | 5% |
| Kamayurá | 25 | 5% |
| Pankararu | 22 | 4% |
| Suruí | 16 | 3% |
| Tikuna | 15 | 3% |
| Kalapalo | 15 | 3% |
| Kaxinawá | 13 | 3% |
| Kaingang | 13 | 3% |
| Apurinã | 12 | 2% |
| Krahô | 9 | 2% |
| Tukano | 6 | 1% |
| *(outros 34 valores)* | 92 | 18% |

Povos distintos: **49** · Estados: **14**

## Campos raros (presentes em <10% dos itens)

Participação em exposição (17), História administrativa (26), Descritor comum (36), Autoria (46)
