# Relatório do juiz — lote de avaliação (29/09/2026)

Gerado por `avaliacao/gerar_relatorio_juiz.py` a partir de `juiz_criterios.json` e `juiz_ab.json`. Protocolo em [protocolo_juiz.md](protocolo_juiz.md).

**Como usar:** cada item numerado pede uma decisão — *concordo*, *discordo* ou *parcial*. Achado adjudicado vira dado do projeto; discordância calibra o juiz.

**Adjudicado por Eduardo Tosto em 2026-09-29:** 57 concordo, de 57 itens. Origem do registro: decisão declarada pelo autor no chat, depois de percorrer a página de adjudicação: "concordei com todos os itens na adjudicação". O arquivo foi montado a partir dessa declaração; não é a exportação item a item da página.

## O julgamento em números

| | Total |
|---|---|
| Casos julgados | 50 |
| Achados | 358 |
| Achados de gravidade alta | 37, em 22 casos |
| Vereditos `conferir` | 20 |
| Pares do A/B | 49 |
| Pares em que a baseline descreve melhor | 18 |

Camada dos achados de gravidade alta: redação 20, observação 17.

## 1. Achados de gravidade alta

Informação falsa ou inventada, segundo o juiz. A camada diz onde o erro nasceu.

### Pote Karajá (9196, casos)

**1.** Base descrita como arredondada; o registro diz base plana e a foto não mostra a base.
   - Onde: alt-text · camada: observação
   - Evidência: Observação: 'base arredondada'; alt: 'base arredondada'; registro, Descrição: 'base plana'. Na foto o pote está inclinado e a base não é visível.
   - Adjudicação: concordo

**2.** Contradição interna: a descrição afirma base arredondada e depois base plana.
   - Onde: descrição · camada: redação
   - Evidência: 'Apresenta corpo arredondado, gargalo estreito, boca que se abre para fora e base arredondada' ... 'com base plana e borda extrovertida'.
   - Adjudicação: concordo

**3.** Afirmação sem fonte no registro nem na foto.
   - Onde: descrição · camada: redação
   - Evidência: 'o padrão decorativo é identidade visual do povo'.
   - Adjudicação: concordo

### Tigela Kadiweu (1260, casos)

**4.** Objeto e material errados na observação: disco de madeira em vez de tigela de cerâmica vista pela base.
   - Onde: observação · camada: observação
   - Evidência: Observação: 'um disco circular', 'madeira de tom marrom avermelhado'; registro: Tigela, Matéria-prima 'Mineral > Argila'.
   - Adjudicação: concordo

**5.** Padrão nomeado 'gregas' sem apoio na foto, no registro nem na observação.
   - Onde: alt-text · camada: redação
   - Evidência: Alt: 'padrão geométrico em gregas'; observação: 'padrão central em forma de cruz com elementos triangulares e curvas', 'curvas em espiral'; foto mostra volutas entrelaçadas.
   - Adjudicação: concordo

**6.** Mesmo padrão 'gregas' repetido na descrição.
   - Onde: descrição · camada: redação
   - Evidência: 'decoração externa em padrão de gregas'.
   - Adjudicação: concordo

### Tigela Kadiweu (1826, casos)

**7.** Rosto alucinado na observação passou para a descrição.
   - Onde: descrição · camada: observação
   - Evidência: Observação: 'com formato de rosto', 'destacam os contornos faciais'; descrição: 'detalhes em relevo que destacam os contornos faciais'. A foto mostra tigela oval com volutas, sem rosto.
   - Adjudicação: concordo

**8.** Material errado.
   - Onde: observação · camada: observação
   - Evidência: Observação: 'Madeira escura'; registro: 'Mineral > Argila'.
   - Adjudicação: concordo

**9.** Forma inventada: 'gamela, baixa e larga' não tem fonte; o registro diz fitomorfa, com lábio ondulado.
   - Onde: descrição · camada: redação
   - Evidência: Descrição: 'Tigela de cerâmica, em forma de gamela, baixa e larga'.
   - Adjudicação: concordo

### Tigela Kadiweu (1996, casos)

**10.** Decoração lida como manchas irregulares; a foto mostra motivos curvos pintados (volutas) e o registro fala em motivos geometrizantes.
   - Onde: alt-text · camada: observação
   - Evidência: Observação: 'Nenhum padrão repetido ou geométrico', 'manchas irregulares'; alt: 'interior com manchas irregulares'; descrição: 'com manchas irregulares no interior'.
   - Adjudicação: concordo

**11.** Material errado na observação.
   - Onde: observação · camada: observação
   - Evidência: Observação: 'Madeira clara'; registro: 'Mineral > Argila'.
   - Adjudicação: concordo

**12.** Forma inventada: 'gamela' sem fonte.
   - Onde: descrição · camada: redação
   - Evidência: 'Tigela em forma de gamela, baixa e larga'.
   - Adjudicação: concordo

### Brinco cavilha Xavante (4246, casos)

**13.** Lado da mancha escura invertido: o texto diz extremidade direita, e na foto é a esquerda.
   - Onde: alt-text · camada: observação
   - Evidência: Observação: 'extremidade mais escura na direção inferior direita' / 'pequena área mais escura na extremidade direita'. Foto: disco escuro na ponta inferior esquerda.
   - Adjudicação: concordo

### Pulseira de miçangas Tiriyó (77963, casos)

**14.** Material inventado: 'fibra natural' para uma linha industrializada. A observação classificou os cordéis como fibra natural.
   - Onde: alt-text · camada: observação
   - Evidência: Observação: 'fios de fibra natural de cor marrom claro'. Registro: 'Fio de algodão industrializado'.
   - Adjudicação: concordo

**15.** Contradição interna: 'fios de fibra natural marrom claro' e, logo depois, 'cordel branco para amarração'.
   - Onde: descrição · camada: redação
   - Evidência: Descrição: '... sobre fios de fibra natural marrom claro. Confeccionada com técnica de entretecido, com cordel branco para amarração.'
   - Adjudicação: concordo

### Máscara antropomorfa Tikuna Tikuna (2601, casos)

**16.** Pintura no nariz inventada: a observação atribui a pintura às 'feições', 'pálpebras e lábios', e a redação estendeu ao nariz.
   - Onde: alt-text · camada: redação
   - Evidência: Foto: nariz entalhado, sem tinta. Observação: 'detalhes em marrom-avermelhado nas pálpebras e lábios'.
   - Adjudicação: concordo

**17.** 'olhos ... salientes' é falso: os olhos são pintados, e o registro diz exatamente isso.
   - Onde: descrição · camada: redação
   - Evidência: Registro: 'olhos pintados, nariz e boca salientes'. Descrição: 'A peça exibe olhos, nariz e boca salientes'.
   - Adjudicação: concordo

### Peteca Menkrangnotí (4056, casos)

**18.** Função inventada: 'atividades rituais', quando o registro diz lúdicas.
   - Onde: descrição · camada: redação
   - Evidência: Função: 'Objeto utilizado em atividades lúdicas'. Descrição: 'objeto lúdico usado em atividades rituais'.
   - Adjudicação: concordo

### Escultura zoomorfa ritual Timbira Krahô (2826, casos)

**19.** Forma inventada: 'globular' para uma peça longa e cilíndrica, e além disso um termo de jargão do glossário (regra 3). A observação dizia 'longo, cilíndrico'.
   - Onde: descrição · camada: redação
   - Evidência: Foto: corpo alongado de ~67 cm. Descrição: 'com forma globular'.
   - Adjudicação: concordo

**20.** As duas pontas são descritas como 'fios desfeitos', o que sugere dano. Na peça, a ponta esquerda é o rabo em feixe e a direita é uma abertura com borda.
   - Onde: alt-text · camada: observação
   - Evidência: Observação: 'terminando em nós ou fios desfeitos em ambas as extremidades'. Foto: extremidade direita aberta, com aro trançado.
   - Adjudicação: concordo

### Braçadeira emplumada Waurá (2316, casos)

**21.** Padrão inventado: 'base de fibra entrelaçada em padrão de espinha-de-peixe'.
   - Onde: alt-text · camada: redação
   - Evidência: Observação: 'entrelaçamento contínuo, com curvas suaves... Não há padrões geométricos'. Foto: cordel de algodão enrolado, penas amarradas em franja.
   - Adjudicação: concordo

**22.** Local de aquisição falso: 'adquirido em 1996 no estado de Mato Grosso'.
   - Onde: descrição · camada: redação
   - Evidência: Registro, Observação sobre o item: os Waurá vieram ao Museu do Índio em abril e as peças foram compradas pelo Museu após as comemorações. Mato Grosso é o Estado de origem.
   - Adjudicação: concordo

### Recipiente de cabaça Guarani-Kaiowá (5371, casos)

**23.** Material errado: 'feito de madeira escura' (repetido na descrição: 'O material é madeira escura'). O objeto é cabaça.
   - Onde: alt-text · camada: observação
   - Evidência: Observação: 'Madeira de tom marrom avermelhado'; registro, Matéria-prima: 'Vegetal > Cabaça'; o próprio título diz cabaça.
   - Adjudicação: concordo

**24.** Padrão inventado: 'padrões gregas pirogravados' (e 'motivos gregas' na descrição); erro de concordância 'padrões gregas'.
   - Onde: alt-text · camada: redação
   - Evidência: Observação: 'Linhas retas e cruzes escuras'; registro: 'motivos geometrizantes pirogravados'; foto: linhas, cruzes e pontos, sem meandro.
   - Adjudicação: concordo

### Recipiente de cabaça Guarani-Kaiowá (1321, casos)

**25.** Padrão inventado: 'cordões de fibra natural em padrão de espinha-de-peixe' (repetido na descrição).
   - Onde: alt-text · camada: redação
   - Evidência: Observação: 'rede de linhas diagonais e verticais ... padrão irregular'; foto: malha poligonal com nós.
   - Adjudicação: concordo

### Recipiente de cabaça Guarani-Kaiowá (5366, casos)

**26.** Padrão inventado: 'padrão em gregas' (repetido na descrição).
   - Onde: alt-text · camada: redação
   - Evidência: Observação: 'Linhas escuras desenhadas em forma de riscos ou traços irregulares'; registro: 'motivos geometrizantes pirogravados'.
   - Adjudicação: concordo

### Recipiente de cabaça Guarani Nhandeva (1316, casos)

**27.** Material errado: 'em cerâmica marrom avermelhada', contradizendo o próprio 'Recipiente de cabaça' do início da frase.
   - Onde: alt-text · camada: observação
   - Evidência: Observação: 'Um recipiente de cerâmica'; Matéria-prima: 'Vegetal > Cabaça'.
   - Adjudicação: concordo

**28.** Padrão inventado: 'corda trançada em padrão de espinha-de-peixe' (repetido na descrição).
   - Onde: alt-text · camada: redação
   - Evidência: Observação: 'padrão de nós e laços ... linhas diagonais e verticais'; foto: cordões cruzados e anel com nós.
   - Adjudicação: concordo

### Bolsa tecida Pankararu (777254, casos)

**29.** Técnica descrita com nós, contra o registro 'enlace sem enodação'; o texto fica autocontraditório.
   - Onde: descrição · camada: observação
   - Evidência: Observação: 'formado por nós entrelaçados'; descrição: 'formada por nós entrelaçados' ... 'técnica de contratorcido e enlace sem enodação'.
   - Adjudicação: concordo

### Alforge Kadiweu (4896, casos)

**30.** Padrão inventado: 'gregas' não aparece na foto nem na observação; repetido na descrição.
   - Onde: alt-text · camada: redação
   - Evidência: Alt e descrição: 'com padrão de gregas'. Observação: 'fios entrelaçados em padrões irregulares'. Foto: malha aberta com faixas lisas de cor.
   - Adjudicação: concordo

**31.** Descrição truncada: termina na marca de atribuição, sem fato de catálogo.
   - Onde: descrição · camada: redação
   - Evidência: '... três faixas. De acordo com a ficha do museu'
   - Adjudicação: concordo

### Cachimbo de cerâmica Canela (4391, holdout)

**32.** Material trocado: a observação vê metal onde há cerâmica (não propagou para os textos).
   - Onde: observação · camada: observação
   - Evidência: 'metal escuro com aspecto oxidado'; registro: Mineral > Argila; a foto mostra fornilho de barro escuro.
   - Adjudicação: concordo

### Máscara antropomorfa Tikuna Tikuna (2746, holdout)

**33.** Olhos e boca descritos como aberturas; são entalhes e relevos.
   - Onde: alt-text · camada: observação
   - Evidência: Observação: 'duas aberturas circulares para os olhos e uma abertura retangular para a boca'; foto: olhos ovais entalhados na superfície e boca em degraus salientes; registro: 'testa, nariz e boca salientes'.
   - Adjudicação: concordo

### Flauta reta de osso Hixkaryána (210599, holdout)

**34.** Material trocado: osso visto como madeira (não propagou para os textos).
   - Onde: observação · camada: observação
   - Evidência: 'Um artefato de madeira'; registro: 'fêmur de mamífero'.
   - Adjudicação: concordo

### Cesto-cargueiro Baniwa (508608, holdout)

**35.** Padrão do trançado lido errado e propagado para os dois textos; a descrição fica contraditória.
   - Onde: alt-text · camada: observação
   - Evidência: Observação: 'padrão de cruzeta (ou xadrez) formado por fios entrelaçados em ângulos retos'; foto: malha vazada hexagonal; descrição: 'trançado hexagonal' e, na frase seguinte, 'padrão de cruzeta'.
   - Adjudicação: concordo

### Bilhas comunicantes Palikur (630, holdout)

**36.** Informação inventada: a peça seria parte de um conjunto.
   - Onde: descrição · camada: redação
   - Evidência: 'sendo parte de um conjunto de cerâmica acordelada'; registro: Número de peças '1'.
   - Adjudicação: concordo

### Tipiti dente de cutia Baniwa (499969, holdout)

**37.** Alças descritas como nós; a observação ainda nega que haja alças.
   - Onde: alt-text · camada: observação
   - Evidência: Observação: 'laço ou nó complexo' e 'Não há furos, alças'; alt: 'fechado em dois nós'; descrição: 'acabamento em nós'; registro: 'duas alças'.
   - Adjudicação: concordo

## 2. Vereditos que pedem olho humano

O juiz não decidiu: depende de tonalidade, leitura de padrão ou nitidez da foto.

**38.** Tigela Kadiweu (1826, casos) — critério: *alt-text descreve a fotografia (enquadramento incluído)*
   - O que o juiz viu: Alt descreve cor e padrão visíveis ('linhas curvas e espirais', 'marrom e branco sobre base escura'), mas não diz que a peça aparece emborcada, vista pela face externa oval; o vermelho da foto é chamado de 'marrom' (tonalidade a conferir).
   - Adjudicação: concordo

**39.** Tigela Kadiweu (1996, casos) — critério: *elemento visível ausente do catálogo é descrito*
   - O que o juiz viu: As cores (registro não nomeia nenhuma) entram no texto, mas com leitura errada: a borda vermelha não é nomeada e aparece 'azul-claro'; tonalidade a conferir por olho humano.
   - Adjudicação: concordo

**40.** Pote Karajá (2151, casos) — critério: *nenhum elemento inventado*
   - O que o juiz viu: 'marrom-avermelhado': o preenchimento dos meandros parece ocre/amarelado (registro: 'amarelo'); tonalidade a conferir.
   - Adjudicação: concordo

**41.** Brinco cavilha Xavante (4286, casos) — critério: *nenhum elemento inventado*
   - O que o juiz viu: 'acabamento arredondado' (alt): a esta distância as pontas não se leem bem; a observação já hesitava ('ligeiramente mais esférico ou arredondado').
   - Adjudicação: concordo

**42.** Brinco cavilha Xavante (4286, casos) — critério: *descrição não inventa detalhes ilegíveis pela distância do enquadramento*
   - O que o juiz viu: Os textos ficam no nível de forma e cor; só 'acabamento arredondado' e 'textura alongada' dependem de detalhe pouco legível.
   - Adjudicação: concordo

**43.** Colar de miçangas Waiwái (4116, casos) — critério: *nenhum elemento inventado*
   - O que o juiz viu: 'contas ... branco' e 'pequena peça branca no final': a peça branca na foto parece um nó/linha no cordão, não contas e não no final; conferir.
   - Adjudicação: concordo

**44.** Brinco cavilha Xavante (4246, casos) — critério: *descrição não inventa detalhes ilegíveis pela distância do enquadramento*
   - O que o juiz viu: Os 'veias naturais' (veios) são pouco legíveis a essa distância na foto de 640 px: a superfície parece lisa, com leve variação de tom. Depende de olho humano.
   - Adjudicação: concordo

**45.** Máscara antropomorfa Tikuna Tikuna (2601, casos) — critério: *divergência sinalizada em flag para revisão, não omitida*
   - O que o juiz viu: flags: []. O registro não nomeia cor nenhuma, então o código não tinha como comparar cores. A pintura da boca é uma omissão do catálogo, não uma contradição. Falta decidir se omissão de catálogo exige flag.
   - Adjudicação: concordo

**46.** Estojo para guardar umbigo Canela (4606, casos) — critério: *nenhum elemento inventado*
   - O que o juiz viu: 'padrão espiralado': a foto mostra camadas enroladas em torno da abertura; se isso é espiral ou camadas concêntricas depende de olho humano. O resto tem fonte.
   - Adjudicação: concordo

**47.** Braçadeira emplumada Kamayurá (2236, casos) — critério: *elemento visível ausente do catálogo é descrito*
   - O que o juiz viu: As pontas azuis (anotação E3) aparecem na descrição, mas, pela quarentena, cor vista que o registro não nomeia deveria ir para flag e ficar fora do texto. O critério é cumprido ao pé da letra, contra a regra posterior.
   - Adjudicação: concordo

**48.** Braçadeira emplumada Kalapalo (1521, casos) — critério: *nenhum elemento inventado*
   - O que o juiz viu: Penas 'em tons amarelo e marrom': a foto mostra penas laranja-amareladas com algumas pontas mais escuras e poucas penas azuis sob a franja; 'marrom' vem da observação e não do registro. Tonalidade depende de olho humano.
   - Adjudicação: concordo

**49.** Braçadeira emplumada Kalapalo (1436, casos) — critério: *nenhum elemento inventado*
   - O que o juiz viu: Nada claramente inventado; tonalidades 'marrom-avermelhado' (base) e 'verde-oliva' (fio) dependem de olho humano. Foto: base de cordão bege-acastanhado, fios verde-acinzentados.
   - Adjudicação: concordo

**50.** Abano trançado Tembé (3176, casos) — critério: *alt-text descreve a fotografia (enquadramento incluído)*
   - O que o juiz viu: Alt diz 'Detalhe' (correto), mas omite a empunhadura amarrada com cordão, que ocupa o terço superior da foto; o trançado da pá é sarjado em degraus diagonais, e chamá-lo de 'espinha-de-peixe' depende de conferência humana.
   - Adjudicação: concordo

**51.** Abano trançado Tembé (3176, casos) — critério: *nenhum elemento inventado*
   - O que o juiz viu: 'padrão de espinha-de-peixe' não vem da observação ('linhas retas e diagonais'); na foto o sarjado forma degraus diagonais, sem inversão clara em ziguezague.
   - Adjudicação: concordo

**52.** Bolsa tecida Pankararu (777254, casos) — critério: *divergência sinalizada em flag para revisão, não omitida*
   - O que o juiz viu: Flags vazias. A única divergência candidata é 'nós' (observação) contra 'enlace sem enodação' (registro), cuja leitura depende de olho humano sobre a técnica.
   - Adjudicação: concordo

**53.** Tecido bordado Tembé (775243, casos) — critério: *nenhum elemento inventado*
   - O que o juiz viu: 'franjas douradas': na foto as franjas parecem do mesmo tom bege do tecido (registro: 'franjas do mesmo tecido'); a leitura de tom depende de olho humano.
   - Adjudicação: concordo

**54.** Óleo vegetal de coco de babaçu Tabajara (206999, casos) — critério: *artefatos de estúdio/inventário (etiqueta, numeração, cartela, borda, suporte) excluídos da descrição*
   - O que o juiz viu: A etiqueta citada no alt é o rótulo manuscrito da produtora ('AZEITE DE COCO BABAÇU'), parte da peça doada, não etiqueta de inventário; o código a marcou como artefato_estudio. Decisão de classificação para o revisor.
   - Adjudicação: concordo

**55.** Cachimbo de cerâmica Canela (4391, holdout) — critério: *nenhum elemento inventado*
   - O que o juiz viu: 'boca que se abre para fora' (alt e descrição) descreve borda extrovertida; na foto a boca do fornilho é cilíndrica, de borda reta. Não há outro elemento visual inventado.
   - Adjudicação: concordo

**56.** Pulseira de miçangas Kaxinawá (84836, holdout) — critério: *nenhum elemento inventado*
   - O que o juiz viu: 'linhas retas e curvas interligadas': na foto os motivos são meandros retilíneos em ângulo reto, sem curvas visíveis.
   - Adjudicação: concordo

**57.** Flauta reta de osso Hixkaryána (210599, holdout) — critério: *nenhum elemento inventado*
   - O que o juiz viu: 'penas amarelas e brancas': na foto há penas amarelas e penas claras de tom creme/esverdeado; o registro fala só em penas amarelas.
   - Adjudicação: concordo

## 3. A/B cego: pares em que a descrição curatorial descreve melhor

No motivo, A e B são os lados do sorteio; a coluna ao lado diz qual era o texto gerado.

| Caso | Lado do gerado | Critério decisivo | Motivo do juiz |
|---|---|---|---|
| Recipiente de cabaça Guarani Nhandeva (1316, casos) | B | fidelidade | A foto mostra uma cabaça envolta por cordões torcidos soltos e tampa de sabugo; B erra ao dizer cerâmica e padrão espinha-de-peixe. |
| Recipiente de cabaça Guarani-Kaiowá (1321, casos) | A | fidelidade | A rede de cordões na cabaça forma malhas hexagonais, não espinha-de-peixe como diz A; B cita alça, revestimento e tampa de sabugo, todos visíveis. |
| Braçadeira emplumada Waurá (2316, casos) | B | fidelidade | A foto mostra penas vermelhas, amarelas, pretas (e algumas azuis) presas a um cordel de algodão com longas pontas soltas; B inventa base em espinha-de-peixe e A é longo e técnico demais para o ouvido. |
| Cesto-cargueiro Baniwa (508608, holdout) | B | fidelidade | O cesto tem trançado aberto hexagonal de fibra clara e uniforme; B fala em padrão de cruzeta e fibras claras e escuras, que a foto não confirma. |
| Recipiente de cabaça Guarani-Kaiowá (1331, casos) | B | fidelidade | A foto mostra cabaça com cordões, alça e tampa de sabugo, como diz A; B descreve cruzetas pouco evidentes e gasta palavras com etiqueta de museu. |
| Brinco cavilha Xavante (4246, casos) | A | fidelidade | O bastão de madeira clara tem a ponta escura do lado esquerdo, não do direito como afirma A; B é genérico mas não erra. |
| Recipiente de cabaça Guarani-Kaiowá (5366, casos) | B | fidelidade | A foto mostra cabaça redonda com abertura na borda e traços riscados em volta dela, como diz A; B fala em gregas, que não aparecem, e se ocupa da etiqueta. |
| Flauta reta sem aeroduto Salumã (199679, holdout) | A | clareza_ao_ouvido | A flauta de taquara com quatro furos, duas penas pintadas e franjas vermelhas é detalhada em B, mas com jargão e frase longa; A resume o essencial e se ouve de uma vez. |
| Colar de miçangas Tiriyó (90371, holdout) | B | clareza_ao_ouvido | O colar de franjas coloridas tem pingente triangular com figura de animal; A diz isso com mais detalhe, mas B se ouve de uma vez e serve melhor como alt-text. |
| Alforge Kadiweu (4896, casos) | B | fidelidade | A peça de malha com três faixas verde-escuras é bem descrita em A; B cita padrão de gregas, que não existe na foto. |
| Tipiti dente de cutia Baniwa (499969, holdout) | B | clareza_ao_ouvido | O tubo trançado em espinha-de-peixe termina em argolas, não em nós como diz B; A acerta mas explica um uso que não se vê e fica longo demais para ouvir. |
| Recipiente de cabaça Guarani-Kaiowá (5371, casos) | A | fidelidade | A foto mostra uma cabaça ovoide marrom com linhas e pontos pirogravados; A diz que é de madeira e fala em gregas, o que a foto desmente. |
| Bilhas comunicantes Palikur (630, holdout) | A | fidelidade | Dois potes de cerâmica ligados por um tubo sobre uma base única, um de boca larga e outro com pequeno orifício; B descreve essa estrutura, A só cores e linhas. |
| Bilha Marubo (1050, holdout) | A | fidelidade | Bilha escura de corpo lobulado, gargalo curto e alça de cordel; B cita forma, alça e gargalo, A é vago e de redação truncada. |
| Pote Karajá (2151, casos) | A | fidelidade | Pote claro com gregas contornadas em preto e preenchidas em ocre no gargalo; A omite o corpo claro e diz marrom-avermelhado. |
| Escultura zoomorfa ritual Timbira Krahô (2826, casos) | A | fidelidade | Peça alongada de palha trançada em espinha com franjas laterais e cauda desfiada, com forma de peixe; B identifica o peixe, nadadeiras e rabo, A não diz o que a figura representa. |
| Estojo para guardar umbigo Canela (4606, casos) | B | fidelidade | Estojo de folha dobrada em dois cones com abertura no meio; A cita o orifício central visível, B fala em padrão espiralado menos claro. |
| Tigela Kadiweu (1260, casos) | B | fidelidade | Peça escura avermelhada com linhas brancas em curvas e cruz central; B diz gregas em tons claros, o que a foto desmente, A cita motivos por corda plausíveis. |
