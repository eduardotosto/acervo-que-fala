# Revisão do juiz — lote v7, 17 cards (27/08/2026)

**Protocolo:** Claude (Opus) revisou cada card com a foto em resolução máxima, o registro completo,
a observação do Qwen e os textos gerados, contra as 25 regras + gabarito editorial. O papel do
Eduardo muda de anotador para **adjudicador**: cada achado numerado abaixo recebe *concordo /
discordo / parcial*. Achado adjudicado entra no gabarito; discordância calibra o juiz. Os cards
#4–#6 já foram adjudicados (concordo nos três); #1–#3 são a revisão do próprio Eduardo.

**Correção de protocolo no meio da revisão:** o juiz quase repetiu o erro-classe da arara — ia
reportar "estado alucinado" em 5 cards, mas o dump que ele lia omitia o campo `Estado de origem`;
a checagem `estado_sem_fonte` (que compara com o registro COMPLETO) mostrou que só a troca
"Amazonas"→"Amazônia" é real (2 cards). **Regra nova do protocolo: o juiz sempre vê todos os
campos do registro.** Fica como caso de método: até a camada que audita precisa ser auditável.

## Achados por card (#7–#20, pendentes de adjudicação)

### #7 — Pulseira de miçangas Kaxinawá (84811)
- **7.1** Preto e azul ausentes dos textos: o registro nomeia preta e azul ("laterais com contas
  azuis"), a foto mostra fileiras pretas de contorno e azul nas laterais dobradas; a observação só
  viu verde/branco/vermelho — reincidência da 2ª revisão ("faltou o preto"). Camada: observação
  (por isso a flag de cor não disparou — ela compara o registro com o que a observação viu).
- **7.2** Gregas de novo: o motivo é grego (labirintos nítidos na foto; glossário-04 define); a
  observação disse "meandros" (aceitável) e a redação piorou para "quadrados interligados".
- **7.3** *(conferir)* Contradição interna do registro: Matéria-prima "fio de algodão
  industrializado" × Descrição "fios de nylon" — candidata a metadado_suspeito.
- ✓ Consolidado: o fecho com botões, perdido na 2ª revisão, agora é citado com atribuição.

### #8 — Brinquedo zarabatana Baniwa (883523)
- **8.1** "arma de caça usada pelo povo Baniwa" — o texto harmoniza a contradição
  brinquedo×caça pela quarta vez (defeito 7/7 no gabarito).
- **8.2** "O objeto é inteiro" no nível 2 — moldura + palavra vetada ("inteiro") + enquadramento
  dentro do texto do objeto.
- **8.3** O registro afirma "em miniatura" TEXTUALMENTE e o texto cala — a heurística de
  miniatura é dimensional (102 cm não dispara); miniatura declarada no registro deveria entrar
  com atribuição.
- **8.4** "cabo" (7/7 no gabarito; regra 24: zarabatana tem tubo).

### #9 — Pote Karajá (2081)
- **9.1** "sem alças ou tampas" no alt — ausência + meta-linguagem da observação no texto público.
- **9.2** "cerâmica bege claro" (cor de material natural) e "borda extrovertida" (jargão) — ambos
  reincidentes, ambos já rastreados pelo gabarito.
- **9.3** "boca parcialmente visível" no alt e no nível 2 — condição da FOTO dentro da descrição
  do objeto.
- **9.4** *(conferir)* Registro diz pintura "na cor preto"; texto diz "marrom escuro" — divergência
  tonal (a foto sugere marrom-escuro envelhecido).

### #10 — Fuso Xavante (5011)
- **10.1** O ALGODÃO sumiu: o registro diz "algodão bruto enrolado à vareta"; o texto diz só
  "fibra branca-cremosa" — o nome que o ouvinte entenderia ficou de fora (a 2ª revisão já dizia:
  o felpudo é próprio do algodão cru).
- **10.2** Divergência de material sem flag: a observação viu "extremidade circular de madeira", o
  registro diz tortual de cerâmica; a redação usou cerâmica (correto), mas o conflito
  observação×registro não virou flag (contrato de fontes, cláusula 3).
- ✓ "tortual" não voltou.

### #11 — Argila Baniwa (200648)
- **11.1** "sem padrão" e "altura de 14,7 cm" no alt — ausência + medida no alt (as duas checagens
  novas da régua nasceram deste card e do #5).
- **11.2** Frase incoerente no nível 2: "Fragmentos de argila clara e escura, sem padrão, em tampa
  metálica dourada com inscrição legível" — os fragmentos não estão NA tampa; e a inscrição
  (artefato) segue citada no texto público.
- **11.3** RETRATAÇÃO do juiz: "Amazonas" tem fonte (campo Estado de origem) — ver protocolo.
- ✓ Conteúdo antes do recipiente (regra 23) consolidado.

### #12 — Flauta reta de osso Hixkaryána (210680)
- **12.1** A foto mostra um pequeno rótulo com caracteres junto às penas — a observação v7 NÃO o
  viu ("nada é legível"; ARTEFATOS: nenhum). v5 e v6 viam a marcação ("8283"/"8285"). Artefato
  perdido pela observação: nem a varredura salva o que a observação não escreve.
- **12.2** Escala 41 cm = osso + cordel — **bug nosso**: o filtro de cordel não cobria
  "(osso + cordel)"; o certo é 12,7 cm (osso). Corrigido no código; o texto que repetiu 41 passa a
  acusar `escala_errada`.
- **12.3** *(conferir, menor)* Penas acinzentadas/penugem visíveis não citadas.

### #13 — Pião noz de tucum Canela (5146)
- **13.1** A FOTO DISPONÍVEL TEM 100×66 PIXELS — o notebook recebeu a mesma imagem; a observação
  descreveu "textura em espiral" e "furo central" de uma imagem onde isso é ilegível: detalhes
  provavelmente confabulados. Proposta de código: flag automática de resolução mínima (a E3
  descartou 5 candidatos por isso; este escapou).
- **13.2** Cabaça omitida no alt ("objeto cilíndrico de madeira clara"; registro: recipiente de
  cabaça + haste de madeira); "é um objeto" como moldura no meio do alt.
- **13.3** Relação invertida no nível 2: "haste atravessada por recipiente de cabaça" (o registro
  diz o recipiente contendo a haste atravessada).

### #14 — Abano de talo de tucum Baniwa (500179)
- **14.1** A forma geral continua ausente (reincidência da 2ª revisão): a foto mostra forma nítida
  de leque/coração; o texto só fala do centro.
- **14.2** Espinha-de-peixe ignorada de novo: o centro é espinha-de-peixe clara; o texto diz
  "padrão em forma de 'X'" (letra). Mesmo padrão dos cards #4, #5, #7: o vocabulário que o RAG
  entrega não é usado.
- **14.3** "bordas suaves" — frase vetada na 2ª revisão (#20) aparecendo em outro item: candidata
  a proibição global.
- **14.4** "A cor é bege a marrom claro, sem tingimento" — cor de material natural + ausência.
- **14.5** *(menor)* Empunhadura visível (base amarrada) omitida — a diretriz de trançados pede.

### #15 — Remo espatular Karajá (3411)
- **15.1** "lâmina" (4×) em vez de "pá" — o registro usa pá; família da regra 24 (vocabulário
  fisicamente correto).
- **15.2** "sem furos ou alças" no alt — ausência/meta no alt.
- **15.3** "Escala: 124,2 cm" no nível 2 — a moldura da variável colada no texto (como o
  "em escala de 50 cm" do card #5); a régua agora pega nos dois campos.
- **15.4** *(menor)* Punho em forma de muleta (do registro, visível na foto) omitido.
- ✓ "inteiro e horizontal" não voltou.

### #16 — Braçadeira emplumada Kalapalo (1366)
- **16.1** "penas de arara em tons de vermelho, laranja e amarelo" no nível 2 — laranja preso à
  espécie; o registro dá à arara só amarelo e vermelho (a flag de cor, correta, registrou o
  laranja como divergência).
- **16.2** "Mede 76,0cm de comprimento e 9,0cm de largura" — duas medidas, formato colado do
  registro (sem espaço antes de "cm").
- **16.3** Alças soltas sem flag (2ª revisão) — o código agora gera para lotes futuros.
- **16.4** *(conferir)* A "peça branca inserida entre as penas" pode ser etiqueta de inventário
  (como a do 1376); se for, é artefato citado no alt e no nível 2.

### #17 — Estojo peniano Bororo (4156)
- **17.1** OS ANIMAIS SUMIRAM: a foto mostra com clareza uma onça pintada (quadrúpede com manchas)
  e um segundo quadrúpede (anta?); o registro autoriza "motivos zoomorfos"; o texto diz apenas
  "desenhos estilizados em preto". Perda informativa grande — e provável efeito colateral da regra
  15, calibrada para impedir figuras EM padrões abstratos e agora suprimindo figuras REAIS.
- **17.2** "dobrada em afunil" — palavra inventada (família "tortual"): o registro diz "dobradura
  afunilada".
- **17.3** *(conferir)* A ponta é bifurcada (rabo de andorinha, nítido na foto); o texto diz
  "pontiaguda".
- **17.4** *(menor)* "folhagem de palmeira" no alt — o registro diz folíolo do broto.

### #18 — Arco plano-côncavo Waimiri-Atroari (205095)
- **18.1** *(conferir)* A característica dominante da foto — corda grossa enrolada em muitas
  voltas na extremidade — virou "uma tira de fibra formando um nó": subdescrição.
- **18.2** Duas medidas no nível 2 (237,2 cm + 3 cm) — ficha técnica.
- **18.3** *(menor)* "torção em S" (técnica distintiva do registro) omitida.
- ✓ Card relativamente limpo; "sinais de uso" da 2ª revisão não voltou.

### #19 — Panela gameliforme Karajá (905)
- **19.1** As figuras em "X" — que o REGISTRO nomeia e a foto mostra — viraram "linhas diagonais
  cruzadas em ângulos retos". Par com 17.1: aqui a "letra" é legítima (vem do catálogo) e foi
  suprimida; a regra anti-letra super-aplicada.
- **19.2** "cerâmica bege clara" (cor de material), "borda extrovertida" (jargão), "interior
  visível" (foto no nível 2), "sem alças ou furos" (ausência no alt).
- **19.3** Duas medidas no nível 2 — ficha técnica.

### #20 — Bolsa tecida Baniwa (500322)
- **20.1** Etiqueta visível na alça (pequeno rótulo branco, lado direito) que a observação não viu
  — segundo artefato perdido pela observação no lote (com 12.1).
- **20.2** "23,5 cm de altura QUANDO DOBRADA" — invenção interpretativa: o registro não diz
  dobrada; 23,5 cm é a altura da bolsa.
- **20.3** Três medidas no nível 2 — ficha técnica.
- **20.4** *(menor)* O "fecho escuro" visível é a semente de açaí da Matéria-prima — a conexão,
  audível e interessante, não foi feita.
- ✓ "bordas suaves" e "peça pequena" não voltaram.

## Padrões sistemáticos (o que os 17 cards dizem juntos)

1. **A observação perde artefatos que estão na foto** (12.1, 20.1) — a varredura de texto não
   salva o que a observação nem escreve. Só revisão com imagem pega; é o argumento empírico para
   o papel do juiz (e da revisão humana da E11).
2. **Vocabulário do glossário sistematicamente ignorado** — espinha-de-peixe (#4, #14), gregas
   (#5, #7; `gregas_ignoradas` dispara nos 7 lotes do gabarito). O RAG recupera; o redator não
   usa. Candidato a instrução: "quando a diretriz nomear o padrão que você vê, use o termo dela".
3. **Regra 15 produzindo o erro oposto** (17.1, 19.1) — calibrada contra inventar figuras em
   padrões abstratos, passou a suprimir figuras reais e a letra que o próprio registro usa.
4. **Molduras de variáveis vazando** ("em escala de", "Escala:") — papagaio de injeção: toda
   variável que entra no prompt é um exemplo copiável em potencial.
5. **Ficha técnica voltando pelo nível 2** (16.2, 18.2, 19.3, 20.3) — duas ou três medidas coladas
   do registro; a régua ganhou `colagem_do_registro` e o gabarito já media `ficha_tecnica`.
6. **Foto de 100×66 px no 5146** — checagem de resolução mínima precisa existir em código no
   próximo notebook.
