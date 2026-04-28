A grande sacada é que você não está pedindo um sinal de trade, está pedindo *features* — que é uma tarefa diferente e mais técnica. Isso muda o tipo de detalhe que o prompt precisa exigir.

Antes do template, três decisões de design que vale entender:

**Por que descrever o pipeline inteiro, não só "me dê indicadores":** se a IA não souber que isso vai virar feature de um classificador supervisionado, ela vai te entregar indicadores estilo TradingView (cruzamento, sinal de compra/venda) em vez de variáveis estatisticamente bem-comportadas. Você precisa que ela pense em estacionariedade, escala e distribuição.

**Por que exigir justificativa econômica/estatística:** sem isso, ela junta MACD + RSI + Bollinger e te entrega um Frankenstein. Forçar fundamentação corta 80% da preguiça.

**Por que pedir explicitamente "modos de falha" e "o que invalidaria":** é o equivalente, no seu domínio, dos itens 4 e 5 do prompt do Lo (riscos / incertezas). É onde aparece a parte honesta da resposta.

## O prompt

```
Atue como um quant researcher sênior com experiência em microestrutura
de criptoativos e em feature engineering para modelos de classificação
de regime de mercado.

CONTEXTO DO PROJETO
- Mercado: cripto (24/7, sem gap de abertura, liquidez variável por
  horário e dia da semana, presença de funding rate em perpétuos)
- Ativos: [BTC/USDT, ETH/USDT — perpétuos, exchange X]
- Timeframe das barras: [ex.: 5m e 1h]
- Dados disponíveis: OHLCV + [trades tick-a-tick / order book L2 /
  funding rate / open interest — listar o que você realmente tem]
- Tamanho do histórico: [ex.: 3 anos]
- Objetivo: classificar cada barra como TRENDING ou RANGING usando
  um modelo supervisionado (gradient boosting). Os indicadores que
  você propor serão FEATURES, não sinais de execução.

O QUE EU PRECISO
Proponha N indicadores quantitativos. Para CADA indicador, entregue:

1. Justificativa econômica/estatística de por que ele discrimina
   trend de range (cite literatura quando aplicável: Hurst,
   variance ratio de Lo & MacKinlay, Kyle's lambda, Amihud, etc).
2. Definição matemática completa (fórmulas, não pseudocódigo vago).
3. Hiperparâmetros e faixas razoáveis, com a lógica da escolha.
4. Propriedades estatísticas: é estacionário? Tem escala fixa?
   Qual distribuição empírica esperada?
5. Estratégia de normalização para uso como feature de ML
   (z-score rolling, rank percentil, winsorização, log-transform).
6. Comportamento esperado em cada regime (sinal e magnitude).
7. Custo computacional e se é calculável em streaming (online).
8. Modos de falha — quando o indicador "mente" e por quê.

ESTRUTURA OBRIGATÓRIA POR INDICADOR (igual a um briefing fiduciário):
- Definição e intuição
- Premissas (o que precisa ser verdade no mercado para funcionar)
- Riscos (lookahead, sensibilidade a outliers, vieses estatísticos)
- O que invalidaria (regimes em que perde poder discriminativo)
- Lacunas e incerteza (que dados adicionais melhorariam, e onde
  você tem menos confiança na robustez)

RESTRIÇÕES
- Nada de indicadores clássicos sem variação não-trivial. Se propor
  ADX ou largura de Bollinger, justifique a adaptação para cripto.
- Considere sazonalidade intradiária e efeitos de fim de semana.
- Sem filtros não-causais (nada centralizado, nada que use t+k).
- Pelo menos um indicador deve ser de microestrutura, se eu
  declarei ter dados de trades/order book.
- Pelo menos um indicador deve testar formalmente a hipótese de
  random walk vs trending (variance ratio, Hurst, etc).
- Diversifique famílias: não me dê 5 indicadores de volatilidade.

FORMATO
Comece com uma tabela: nome | família | custo | poder
discriminativo esperado. Depois o detalhamento por indicador
no padrão acima.

ANTES DE COMEÇAR
Liste suas principais incertezas sobre o meu setup e me pergunte
o que faltou. Não invente premissas sobre dados que eu não declarei.
```

## Como tirar o máximo

Esse último parágrafo ("antes de começar, me pergunte o que faltou") força a IA a expor lacunas antes de inventar. Use sempre.

Depois da primeira resposta, a parte de conversa entra. Algumas perguntas-faca que rendem muito numa segunda rodada:

- *"Para cada indicador, me mostre a correlação esperada com os outros. Quero diversificação informacional, não redundância."*
- *"Quais desses indicadores têm risco de leakage se eu calcular features e labels com a mesma janela? Como evitar?"*
- *"Quero a versão multi-timeframe: como combinar o mesmo indicador em 5m, 1h e 4h sem explodir o número de features?"*
- *"Para o label de regime (trend vs range), que esquemas de rotulagem você recomenda? Triple barrier, regime switching via HMM, threshold em Hurst? Discuta trade-offs."*

E uma família de indicadores que vale citar pelo nome no prompt para escapar do óbvio, caso ela não puxe sozinha: 
- variance ratio test (Lo & MacKinlay), 
- Hurst exponent (R/S e DFA), 
- Kaufman Efficiency Ratio, 
- fractal dimension, 
- Kyle's lambda, 
- Amihud illiquidity, 
- order flow imbalance, 
- realized-vs-Parkinson volatility ratio, 
- autocorrelação serial de retornos em múltiplas defasagens. 

Se você mencionar 3 ou 4 desses como "considere também", a qualidade da resposta sobe bastante.

Última dica específica do seu caso: peça num prompt separado, depois, *"agora critique os indicadores que você acabou de propor como se fosse um reviewer hostil de um paper de finanças quantitativas."* É o passo que mais melhora o conjunto final, a IA é muito melhor criticando do que gerando.