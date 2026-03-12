# Market Regimes — Taxonomia Operacional

Classificação de regimes de mercado orientada à tomada de decisão em trading sistemático. Cada regime implica um conjunto distinto de estratégias viáveis, parâmetros de risco e comportamento esperado dos indicadores.

Este documento inclui análise específica para dois timeframes operacionais: **1H (intraday/swing)** e **1D (swing/position)**. A escolha do timeframe altera fundamentalmente como cada regime se manifesta, qual a latência aceitável na detecção, e quais parâmetros devem ser ajustados.

---

## Nota sobre Timeframes: 1H vs 1D

Antes de entrar nos regimes, é importante entender as diferenças estruturais entre operar no gráfico de 1H e 1D, pois isso afeta a interpretação de todos os regimes.

**1H (Hourly):**

- Captura microestrutura intraday: abertura europeia, abertura americana, sobreposição de sessões, fechamento.
- Muito mais ruído. A relação sinal/ruído é significativamente pior do que no diário.
- Regimes mudam mais rápido — um regime que dura semanas no diário pode durar apenas 1-3 dias no horário.
- Gaps entre sessões (overnight, fim de semana) criam descontinuidades que afetam stops e detecção.
- Volume intraday tem padrão U-shape previsível (alto na abertura e fechamento, baixo no meio do dia). Isso precisa ser normalizado antes de usar volume como feature de detecção.
- Custos de transação (spread, slippage, comissões) pesam mais porque a frequência de operação é maior e o lucro por trade é menor.
- Dados de order flow e microestrutura (tape reading, DOM, footprint) são mais relevantes.
- A detecção de regime precisa ser mais responsiva — lookback windows menores, decaimento exponencial mais agressivo.

**1D (Daily):**

- Filtra boa parte do ruído intraday. Cada candle agrega uma sessão inteira.
- Regimes são mais estáveis e duradouros — menos transições falsas.
- Volume diário é mais informativo (não precisa de normalização por hora do dia).
- Gaps de abertura são features importantes (gap up/down com volume indica convicção).
- Permite usar indicadores de médio/longo prazo (MA50, MA200) de forma confiável.
- Custos de transação são menos relevantes porque o holding period é maior.
- Dados fundamentais, macro e de fluxo institucional se integram melhor.
- A detecção de regime pode usar lookback windows maiores (20-100 períodos = 20-100 dias úteis).

**Recomendação geral:** usar o 1D como timeframe primário para detecção de regime e o 1H como timeframe de execução/timing. Ou seja, o regime é definido pelo diário e as entradas/saídas são refinadas pelo horário. Essa abordagem top-down reduz falsos sinais e melhora o timing.

---

## Regimes Primários

---

### 0 — NoLabel

Nenhum regime identificado com confiança suficiente. O classificador não atingiu o threshold mínimo para atribuir um label. Tratamento operacional: manter posição neutra ou aplicar a estratégia default do portfólio com sizing reduzido. A presença frequente deste estado pode indicar necessidade de recalibração do modelo.

**Causas comuns:**

- Transição entre dois regimes onde as features estão ambíguas.
- Dados insuficientes após eventos disruptivos (mudança de horário de negociação, feriado prolongado).
- Ativo com baixa liquidez ou poucos dados históricos para o modelo calibrar.
- Conflito entre features — por exemplo, vol subindo (sugere breakout) mas ADX caindo (sugere ranging).

**Métricas de monitoramento:**

- Frequência de NoLabel: se está acima de 15-20% do tempo, o modelo precisa de ajuste.
- Duração média de NoLabel: períodos longos (>5 candles consecutivos) sugerem que o regime real pode ser Ranging ou Low Vol.
- Entropia da distribuição de probabilidades do classificador: alta entropia = incerteza genuína; baixa entropia com probabilidade máxima logo abaixo do threshold = ajustar threshold.

**⏱ Perspectiva 1H:**
NoLabel aparece com mais frequência no horário, especialmente durante sessões de baixa liquidez (almoço nos EUA, sessão asiática em ativos europeus). Não é necessariamente um problema — pode ser tratado como "hora de não operar". Sugiro mapear quais horários do dia concentram NoLabel e excluí-los do universo operacional. Tipicamente, 30-40% das horas do dia não valem a pena operar.

**⏱ Perspectiva 1D:**
NoLabel no diário é mais significativo e geralmente indica transição real entre regimes. Quando aparece após um trending forte, pode antecipar reversão ou consolidação. Recomendo usar o NoLabel diário como sinal para reduzir exposição em 50% e apertar stops em posições abertas. Não é sinal para zerar tudo, mas para ficar defensivo.

---

### 1 — Trending

Tendência direcional sustentada, seja de alta ou de baixa, sem distinção de sentido. Útil como label genérico quando o modelo detecta persistência serial nos retornos (autocorrelação positiva) mas não há necessidade ou capacidade de distinguir a direção.

**Características observáveis:**

- ADX elevado (tipicamente acima de 25).
- Médias móveis ordenadas e divergindo.
- Retornos apresentam autocorrelação positiva em múltiplos lags.
- Pullbacks são rasos e de curta duração.
- Hurst exponent > 0.5 (série persistente).
- Inclinação da regressão linear dos retornos significativamente diferente de zero.

**Métricas quantitativas para detecção:**

- ADX > 25 (confirmação), > 40 (tendência forte).
- Autocorrelação dos retornos em lag 1-5 > 0 com significância estatística.
- Hurst exponent estimado > 0.55.
- R² da regressão linear do preço nos últimos N períodos > 0.65.
- Preço consistentemente de um lado das Bollinger Bands (acima da média ou abaixo).

**Transições típicas:**

- Trending → Ranging (tendência perde força, ADX cai).
- Trending → Choppy (vol se mantém mas direcionalidade desaparece).
- Trending → Volatile/Breakout (aceleração após consolidação dentro da tendência).
- Trending → Distribution/Accumulation (sinais de exaustão aparecem).

**Estratégias favorecidas:** trend-following, momentum, breakout continuation.

**Estratégias penalizadas:** mean-reversion, fade de extremos.

**⏱ Perspectiva 1H:**
No 1H, uma tendência "sustentada" pode significar 8-20 horas (1-3 sessões). O desafio é distinguir uma tendência real de um movimento intraday estendido. Recomendo exigir que a tendência persista por pelo menos 2 sessões completas antes de classificar como Trending no 1H. Usar EMA(20) e EMA(50) no 1H como referência — quando ambas estão inclinadas na mesma direção e o preço respeita a EMA(20) como suporte/resistência dinâmico, a tendência é válida. Pullbacks até a EMA(20) no 1H são bons pontos de entrada com stop abaixo da EMA(50).

**⏱ Perspectiva 1D:**
O diário é o timeframe natural para detectar tendências. ADX > 25 no diário é um filtro robusto e confiável. Recomendo combinar ADX com a inclinação da MA(50) — ADX alto com MA(50) flat pode ser um falso positivo (choppy com ADX elevado por causa de movimentos bruscos em ambas as direções). A tendência no diário pode durar semanas a meses. Uma vez confirmada, o viés direcional deve ser mantido até que ADX comece a cair E o preço viole a estrutura de topos/fundos.

---

### 2 — Trending Up

Tendência de alta sustentada. Preço formando sequência de topos e fundos ascendentes com momentum confirmado.

**Características observáveis:**

- Retornos acumulados positivos em janelas de 20, 50 e 100 períodos.
- Preço acima das médias móveis principais (20, 50, 200), com médias ordenadas de cima para baixo (20 > 50 > 200).
- Breadth positiva (em índices): maioria dos componentes acima das próprias médias.
- Volume tendendo a ser maior nos dias de alta (on-balance volume crescente).
- RSI operando na faixa 40-80 sem divergências de topo.
- MACD acima da linha de sinal e acima de zero.
- Estrutura de higher highs e higher lows intacta.

**Métricas quantitativas para detecção:**

- Retorno acumulado de 20 períodos > 0.
- Preço > EMA(20) > EMA(50) > EMA(200).
- ADX > 25 com +DI > -DI.
- OBV (On-Balance Volume) fazendo novos máximos junto com o preço.
- Percentual de períodos positivos nos últimos 20 > 55%.

**Fases dentro do Trending Up:**

1. **Início:** breakout de zona de acumulação, volume alto, ADX subindo de nível baixo.
2. **Desenvolvimento:** pullbacks regulares até a EMA(20), cada rally faz novo topo.
3. **Maturação:** rallies menores, divergências começando a aparecer, transição para Distribution.

**Estratégias favorecidas:** buy the dip, trend-following long, carry positivo, pyramiding em pullbacks.

**Gestão de risco:** trailing stops dinâmicos baseados em ATR; sizing pode ser mais agressivo enquanto a estrutura de topos/fundos ascendentes se mantiver.

**⏱ Perspectiva 1H:**
No 1H, trending up se manifesta como sequência de candles predominantemente verdes com pullbacks que encontram suporte na EMA(20) horária. A melhor estratégia é esperar pullbacks até a EMA(20) ou até zonas de suporte intraday (como a VWAP ou POC do perfil de volume do dia) e entrar long com stop abaixo do último swing low horário. O target pode ser projetado via extensão de Fibonacci ou via ATR (1.5x-2x ATR como target). No 1H, trending up raramente dura mais de 3-5 dias consecutivos sem uma pausa significativa (consolidação intraday). Atenção especial ao horário: tendências intraday frequentemente se formam após a abertura da sessão de NY (14:30-15:30 UTC) e perdem força a partir das 19:00-20:00 UTC.

**⏱ Perspectiva 1D:**
Este é o regime mais limpo e lucrativo no diário. Uma vez que o preço se estabelece acima da EMA(50) diária com ADX subindo, a posição long pode ser mantida por semanas. O stop natural é abaixo do último higher low significativo no diário. Recomendo usar a EMA(21) diária como trailing stop dinâmico — enquanto o preço fechar acima dela, manter. Se fechar abaixo por 2 dias consecutivos, reduzir sizing em 50%. A grande vantagem do diário é que você pode ignorar o ruído intraday e dormir tranquilo com a posição. Pyramiding funciona bem aqui: adicionar em cada pullback até a EMA(21) com sizing decrescente (50% do tamanho original, depois 25%).

---

### 3 — Trending Down

Tendência de baixa sustentada. Preço formando sequência de topos e fundos descendentes com momentum negativo confirmado.

**Características observáveis:**

- Retornos acumulados negativos em múltiplas janelas temporais.
- Preço abaixo das médias móveis principais, com médias ordenadas de cima para baixo (200 > 50 > 20).
- Bounces são vendidos com agressividade — rallies de alívio com volume decrescente.
- Correlação entre ativos de risco tende a aumentar (contágio).
- VIX ou volatilidade implícita elevada e com estrutura a termo em backwardation.
- RSI operando na faixa 20-55, com bounces falhando na zona 50-55.
- OBV fazendo novos mínimos.

**Métricas quantitativas para detecção:**

- Retorno acumulado de 20 períodos < 0.
- Preço < EMA(20) < EMA(50) < EMA(200).
- ADX > 25 com -DI > +DI.
- Bounces falham consistentemente na EMA(20) ou EMA(50).

**Assimetria importante:** tendências de baixa são tipicamente mais rápidas e voláteis que tendências de alta. O medo é um motivador mais forte que a ganância, o que faz com que sell-offs tenham velocidade maior. Isso implica que stops precisam ser mais largos (em termos de ATR) em posições short para evitar ser stopado em bounces de alívio.

**Características distintivas em relação a Crisis/Risk-Off:** a velocidade do declínio é menor e mais ordenada. Não há pânico generalizado, mas sim pressão vendedora persistente. O VIX está elevado mas relativamente estável, não em spike agudo.

**Transições típicas:**

- Trending Down → Crisis (aceleração do sell-off com feedback loops).
- Trending Down → Accumulation (vendedores se esgotam, absorção começa).
- Trending Down → Choppy (volatilidade se mantém mas pressão vendedora perde consistência).
- Trending Down → Ranging (queda desacelera, preço estabiliza em nova faixa).

**Estratégias favorecidas:** trend-following short, hedging com puts, redução de exposição, rotação para defensivos.

**Gestão de risco:** stops mais apertados em posições long; atenção a gaps de abertura contra. Posições short devem ter stops acima do último lower high.

**⏱ Perspectiva 1H:**
No 1H, tendências de baixa produzem os movimentos mais rápidos e assimétricos. Um trending down horário pode gerar 2-3% de movimento em poucas horas, especialmente durante sell-offs institucionais. A melhor abordagem é short em bounces até a EMA(20) horária ou até a VWAP do dia. O padrão clássico é: abertura fraca (abaixo do close anterior), bounce até a VWAP nos primeiros 30-60 minutos, rejeição, e continuação da queda. Stops devem ser colocados acima do high do bounce. Atenção: bounces intraday em trending down podem ser violentos (short squeezes de curta duração) — sizing mais conservador do que em trending up.

**⏱ Perspectiva 1D:**
No diário, o trending down é identificável pela sequência de lower highs e lower lows com fechamentos predominantemente abaixo da abertura. A EMA(21) diária funciona como resistência dinâmica — rallies que alcançam a EMA(21) e são rejeitados confirmam a continuação. Recomendo não tentar "pegar a faca caindo" (bottom fishing) enquanto o preço estiver abaixo da EMA(50) com ADX subindo. O signal para considerar reversão é: preço fazer um higher low claro no diário + fechar acima da EMA(21) + ADX começando a cair. Sem esses três elementos juntos, manter viés short ou neutro.

---

### 4 — Ranging

Lateralização ou consolidação. O preço oscila dentro de uma faixa horizontal sem estrutura interna previsível. Não há tendência nem padrão explorável de reversão à média.

**Características observáveis:**

- ADX baixo (tipicamente abaixo de 20).
- Médias móveis flat e entrelaçadas, gerando sinais falsos de cruzamento.
- Retornos com autocorrelação próxima de zero.
- Suporte e resistência horizontais claros, mas os toques são irregulares.
- Volume tipicamente decrescente ao longo do tempo (desinteresse).
- Candles alternando entre alta e baixa sem padrão.
- Bollinger Bands horizontais com largura estável.

**Métricas quantitativas para detecção:**

- ADX < 20.
- R² da regressão linear dos últimos 20 períodos < 0.3.
- Range (high-low) dos últimos 20 períodos estável ou contraindo.
- Autocorrelação dos retornos estatisticamente insignificante.
- Desvio padrão dos retornos relativamente baixo.

**Distinção chave de MeanReverting:** no ranging, as oscilações dentro da faixa são erráticas e não oferecem edge explorável. A distribuição dos retornos é aproximadamente aleatória dentro dos limites. No mean-reverting, existe um eixo identificável e as reversões são estatisticamente exploráveis. A diferença prática: no mean-reverting, o teste de Dickey-Fuller rejeita a hipótese de random walk; no ranging, não rejeita (ou rejeita com p-value marginal).

**Transições típicas:**

- Ranging → Volatile/Breakout (preço rompe suporte/resistência com volume).
- Ranging → Low Vol/Compression (range continua se estreitando).
- Ranging → Trending (rompimento seguido de follow-through sustentado).

**Estratégias favorecidas:** nenhuma com alta convicção. Range trading com sizing mínimo ou ficar flat.

**Estratégias penalizadas:** trend-following (whipsawed por falsos breakouts), momentum.

**⏱ Perspectiva 1H:**
No 1H, ranging é extremamente comum e pode representar 40-60% de todas as horas de mercado. Muitos ativos ficam ranging durante grande parte do dia e só apresentam movimentos direcionais em janelas específicas (abertura, fechamento, eventos macro). Recomendo fortemente não tentar operar ranging no 1H — o custo de transação combinado com a falta de edge torna qualquer estratégia deficitária. O valor de detectar ranging no 1H é saber quando NÃO operar. Usar esse tempo para preparar ordens condicionais para quando o breakout acontecer.

**⏱ Perspectiva 1D:**
Ranging no diário dura tipicamente 5-15 sessões e geralmente antecede um movimento significativo. A informação mais valiosa é a própria faixa (suporte e resistência). Recomendo marcar esses níveis e preparar estratégias de breakout com entrada condicional (ordem stop acima da resistência com filtro de volume, ou abaixo do suporte). Enquanto estiver ranging, a melhor posição é flat ou com sizing mínimo (<25% do normal). Se você tem posição de um regime anterior (ex: estava long em trending up que virou ranging), considere realizar lucro parcial nos toques na resistência da range.

---

### 5 — Mean-Reverting

Oscilação previsível em torno de um valor justo identificável. O preço exibe autocorrelação negativa — desvios do eixo central tendem a ser corrigidos de forma estatisticamente significativa.

**Características observáveis:**

- Z-score do preço relativo a uma média móvel oscilando de forma regular entre ±1.5 a ±2.0 desvios.
- Bandas de Bollinger funcionam bem como sinalizadores de entrada/saída.
- Half-life de reversão estimável via regressão de Ornstein-Uhlenbeck (tipicamente entre 3 e 20 períodos).
- Hurst exponent < 0.5 (série anti-persistente).
- Volatilidade realizada relativamente estável.
- Teste ADF (Augmented Dickey-Fuller) rejeita a hipótese nula de unit root.

**Métricas quantitativas para detecção:**

- Hurst exponent < 0.45.
- Half-life de O-U entre 3 e 20 períodos.
- Autocorrelação em lag 1 negativa e significativa.
- ADF p-value < 0.05.
- Variância dos retornos relativamente constante (homocedasticidade).

**Parâmetros operacionais:**

- Entrada: z-score atinge ±1.5 a ±2.0 (ajustar conforme backtesting).
- Saída: z-score retorna a 0 (ou a ±0.25 para capturar a maior parte do movimento).
- Stop: z-score atinge ±3.0 (regime pode estar mudando para trending).
- Sizing: proporcional à convicção estatística (p-value mais baixo → sizing maior).

**Estratégias favorecidas:** mean-reversion (comprar abaixo do eixo, vender acima), pairs trading, statistical arbitrage, grid trading.

**Estratégias penalizadas:** trend-following, breakout trading.

**Gestão de risco:** stops baseados em múltiplos do desvio padrão. O risco principal é a transição para trending — monitorar o Hurst exponent e a half-life para detectar mudança de regime. Se a half-life começa a crescer, o regime pode estar se tornando trending.

**⏱ Perspectiva 1H:**
Mean-reversion no 1H é o pão com manteiga de muitas mesas de prop trading. O padrão mais comum é: ativo se afasta da VWAP por 1.5-2 desvios padrão e reverte. A VWAP funciona como o "valor justo" natural para o intraday. Recomendo calibrar a half-life no 1H separadamente para cada sessão (asiática, europeia, americana) porque a dinâmica de liquidez muda. A half-life típica no 1H é 3-8 barras (3-8 horas). Atenção: mean-reversion no 1H falha perto de horários de evento macro (FOMC, payroll, CPI) — nesses momentos, o ativo pode transitar abruptamente para breakout.

**⏱ Perspectiva 1D:**
Mean-reversion no diário é menos frequente mas mais confiável. Geralmente aparece em ativos com fundamentos estáveis que estão sendo negociados em torno de um valor justo bem definido (pares de moedas em regimes de política monetária estável, commodities com produção/demanda equilibradas). A half-life típica no diário é 5-15 dias. Recomendo usar a MA(20) diária como eixo e exigir z-score de ±2.0 para entrada (mais conservador que no 1H porque os movimentos são maiores). Pairs trading funciona especialmente bem no diário — dois ativos cointegrados com half-life de 5-10 dias oferecem oportunidades limpas com Sharpe ratio atrativo.

---

### 6 — Low Volatility / Compression

Volatilidade historicamente baixa com bandas de preço apertadas. Regime que tipicamente antecede uma expansão significativa de volatilidade (breakout), embora a direção do movimento subsequente seja indeterminada.

**Características observáveis:**

- Volatilidade realizada no percentil inferior da sua distribuição histórica (abaixo do percentil 20).
- Bollinger Bands estreitas — Bandwidth no mínimo de N períodos.
- ATR comprimido.
- Candles com range reduzido (inside bars frequentes).
- Volatilidade implícita pode estar em desconto relativo à realizada (opcionalidades baratas).
- Volume tipicamente baixo e decrescente.
- Keltner Channels dentro das Bollinger Bands (TTM Squeeze ativo).

**Métricas quantitativas para detecção:**

- ATR percentile rank nos últimos 100 períodos < 20.
- Bollinger Bandwidth percentile rank < 20.
- Contagem de inside bars nos últimos 10 períodos > 3.
- Desvio padrão dos retornos nos últimos 10 períodos significativamente menor que nos últimos 50.
- Volume médio dos últimos 5 períodos < 70% do volume médio dos últimos 50.

**Dinâmica probabilística:** a volatilidade é mean-reverting no longo prazo (vol baixa tende a ser seguida por vol alta). Quanto mais tempo dura a compressão, maior a probabilidade de uma explosão de vol. Porém, a compressão pode durar mais do que o esperado — time decay em opções compradas é o maior risco.

**Indicadores de detecção:** Bollinger Bandwidth, ATR percentile rank, IV percentile, squeeze indicators (TTM Squeeze), Historical Vol vs Implied Vol ratio.

**Estratégias favorecidas:** compra de volatilidade (long straddles/strangles), preparação de breakout entries com ordens condicionais acima e abaixo da faixa, iron condors de curto prazo (risco definido).

**Gestão de risco:** posições direcionais devem ter sizing reduzido até a resolução. O custo principal é o time decay se usando opções.

**⏱ Perspectiva 1H:**
Low vol no 1H é particularmente útil para day traders. A compressão horária frequentemente se resolve na mesma sessão ou na abertura da sessão seguinte. O setup clássico: 3-5 inside bars consecutivas no 1H (tipicamente durante sessão asiática ou almoço americano) seguidas de breakout na abertura da próxima sessão de alta liquidez. Recomendo colocar ordens bracket (buy stop acima do range + sell stop abaixo) com target de 1.5x o range da consolidação. Stop: centro da consolidação. O timing é previsível porque a resolução tende a coincidir com inícios de sessão.

**⏱ Perspectiva 1D:**
Low vol no diário é um dos sinais mais valiosos do mercado. Compressão diária de 5-10 dias antecede os maiores movimentos do ano. Histórico: períodos com Bollinger Bandwidth diário no percentil inferior tipicamente são seguidos por movimentos de 2-3x o ATR normal nos 5 dias seguintes. Recomendo monitorar a compressão diária como alarme e preparar posições de breakout com sizing relevante (este é o regime onde o risco/retorno é mais favorável para comprar vol). Long straddles com vencimento em 30-45 dias funcionam bem aqui se IV também estiver baixo.

---

### 7 — Volatile / Breakout

Alta incerteza com movimentos bruscos e expansão de volatilidade. O preço rompeu uma faixa de consolidação ou está em transição rápida entre regimes.

**Características observáveis:**

- Expansão súbita do ATR e da volatilidade realizada.
- Candles de range largo, frequentemente com fechamento próximo ao extremo.
- Volume significativamente acima da média (confirmação de breakout legítimo).
- ADX subindo rapidamente (indicando formação de tendência).
- Possível gap de abertura.
- Preço rompendo Bollinger Bands com corpo cheio (não apenas sombra).

**Métricas quantitativas para detecção:**

- ATR atual > 1.5x ATR(20).
- Volume > 2x volume médio de 20 períodos.
- Preço fechando acima/abaixo das Bollinger Bands (2 desvios).
- Range do candle atual > percentil 90 dos últimos 50 candles.
- ADX subindo com DI+ ou DI- divergindo.

**Validação de breakout (filtros para reduzir falsos positivos):**

- Volume acima da média confirma convicção institucional.
- Fechamento no terço superior (breakout de alta) ou inferior (breakout de baixa) do candle.
- Follow-through no próximo período (continuação na direção do rompimento).
- Ausência de sombra longa na direção oposta ao rompimento (rejeição = falso breakout).
- Retest da zona rompida com volume baixo e defesa do nível (agora suporte/resistência invertido).

**Distinção chave de Choppy/Whipsaw:** no breakout, a expansão de vol tem direcionalidade — o preço se afasta da zona de consolidação e não retorna rapidamente. No choppy, a vol expande mas o preço fica preso, alternando direção.

**Transições típicas:**

- Breakout → Trending (follow-through sustentado, regime mais comum pós-breakout).
- Breakout → Choppy (falso breakout, preço retorna à faixa e começa a oscilar).
- Breakout → Trending + Blow-off (breakout com aceleração parabólica).

**Estratégias favorecidas:** breakout trading (com filtro de volume), momentum inicial, pyramiding na direção do rompimento.

**Gestão de risco:** stops atrás da zona de consolidação rompida. Risco principal: falso breakout com reversão violenta.

**⏱ Perspectiva 1H:**
Breakouts no 1H têm taxa de falso positivo significativamente maior que no diário (estimo 50-60% vs 30-40%). Isso acontece porque o volume intraday tem padrões previsíveis e muitos "breakouts" horários são apenas ruído amplificado perto de abertura/fechamento de sessão. Filtros essenciais para breakout horário: (1) volume normalizado pelo horário do dia (um breakout às 15:00 UTC precisa de muito mais volume que um às 19:00 UTC para ser significativo); (2) confluência com nível de suporte/resistência do diário; (3) ausência de evento macro iminente (breakouts antes de FOMC são frequentemente falsos). Stop para breakout no 1H: atrás do centro da consolidação horária, tipicamente 0.5-0.7x ATR(14) horário.

**⏱ Perspectiva 1D:**
Breakouts diários são os movimentos que definem trimestres e às vezes anos. Um breakout legítimo no diário — com volume 2x+ acima da média e fechamento no extremo do candle — inicia tendências que duram semanas. A confirmação ideal é: breakout no dia 1, retest do nível rompido no dia 2-3 com volume baixo, e follow-through no dia 4-5. Recomendo entrar no retest em vez de no breakout inicial (melhor risco/retorno, evita falsos breakouts). Stop: abaixo do nível rompido (que agora deve funcionar como suporte). Se o preço fechar de volta abaixo/acima do nível rompido, sair imediatamente — o breakout falhou.

---

### 8 — Choppy / Whipsaw

Alta volatilidade sem direcionalidade. O preço faz movimentos amplos em ambas as direções sem resolução. É o regime mais destrutivo para estratégias sistemáticas porque invalida tanto trend-following quanto mean-reversion.

**Características observáveis:**

- Volatilidade realizada elevada, mas retornos acumulados próximos de zero.
- ADX baixo apesar de candles de range grande.
- Múltiplos cruzamentos de médias móveis em sequência rápida (sinais falsos).
- Volume pode ser alto mas desorganizado (sem convicção institucional).
- Stops são atingidos com frequência acima do normal em ambas as direções.
- Candles com sombras longas em ambas as direções (doji, spinning tops).
- ATR alto com retorno acumulado baixo (vol alta / retorno baixo = choppy).

**Métricas quantitativas para detecção:**

- ATR percentile rank > 60 (vol elevada).
- |Retorno acumulado de 10 períodos| < 0.5x ATR(10) (sem direcionalidade).
- Contagem de reversões de sinal (positivo → negativo e vice-versa) nos últimos 10 períodos > 6.
- ADX < 20 apesar de ATR alto.
- Sharpe ratio rolling de 10-20 períodos próximo de zero.

**Distinção chave de Ranging:** vol é significativamente mais alta. No ranging o preço oscila pouco; no choppy, oscila muito, mas sem ir a lugar nenhum.

**Distinção chave de Mean-Reverting:** no mean-reverting, as oscilações são previsíveis e exploráveis; no choppy, a amplitude e frequência das oscilações são erráticas, destruindo qualquer edge de reversão.

**Causas comuns:**

- Incerteza genuína do mercado (pré-decisão de política monetária, eleição).
- Conflito entre compradores e vendedores de tamanho similar.
- Liquidez fragmentada (market makers recuando, bid-ask alargando).
- Algoritmos de HFT explorando e amplificando a volatilidade sem direcionalidade.

**Estratégias favorecidas:** venda de volatilidade (se IV estiver em prêmio em relação a RV direcional), ou simplesmente não operar.

**Estratégias penalizadas:** trend-following (destroçado por reversões), mean-reversion (stops estourados por amplitude), breakout (falsos rompimentos constantes).

**Tratamento operacional:** reduzir sizing drasticamente ou ficar flat. Este regime é para preservar capital, não para gerar alpha.

**⏱ Perspectiva 1H:**
Choppy no 1H é o pior cenário para day traders e onde a maioria perde dinheiro. O preço pode mover 1-2% em uma hora e reverter completamente na hora seguinte. O maior erro é aumentar sizing para "recuperar" perdas de stops estourados — isso transforma perdas pequenas em perdas catastróficas. Recomendo um circuit breaker pessoal: se 2 stops consecutivos forem atingidos no 1H, parar de operar por no mínimo 4 horas (até a próxima sessão). Se o modelo detectar choppy no 1H, a ação correta é zerar tudo e ir estudar/descansar. Nenhuma estratégia horária tem edge positivo neste regime.

**⏱ Perspectiva 1D:**
Choppy no diário geralmente dura 5-15 sessões e frequentemente aparece em torno de eventos macro importantes (FOMC, earnings season, decisões geopolíticas). O diário dá uma perspectiva melhor para identificar se o choppy está resolvendo — observar se as sombras estão diminuindo e os closes estão se concentrando em um lado do range. Quando isso acontece, o próximo regime provavelmente será breakout seguido de trending. Recomendo manter sizing em 25% do normal (ou flat) durante choppy diário. Se obrigado a manter posição, usar opções para definir risco máximo (compra de put para proteção de long, por exemplo).

---

### 9 — Crisis / Risk-Off

Colapso direcional acompanhado de pânico sistêmico. Não é apenas uma tendência de baixa — é uma mudança qualitativa no comportamento do mercado inteiro.

**Características observáveis:**

- Drawdown acelerado e não-linear (quedas de 3-5+ desvios padrão em dias consecutivos).
- Correlações entre ativos de risco explodem para 1.0 (diversificação colapsa).
- VIX spike acima de 30-40+, estrutura a termo em backwardation severa.
- Spreads de crédito alargando violentamente (HY-IG, TED spread).
- Flight to quality: treasuries, ouro, USD, JPY, CHF se valorizam.
- Liquidez evapora — bid-ask spreads alargam, slippage aumenta drasticamente.
- Circuit breakers podem ser acionados (limit down).
- Funding stress: taxas overnight sobem, repos ficam caros.

**Métricas quantitativas para detecção:**

- Retornos diários < -2 desvios padrão por 2+ dias consecutivos.
- VIX > 30 (alerta), > 40 (pânico), > 50 (crise severa).
- Correlação rolling de 20 dias entre SPX e HYG > 0.85.
- Spread HY-IG alargando > 2 desvios padrão acima da média de 1 ano.
- TED spread > 50 bps (stress de funding).
- Drawdown acelerando (a taxa de queda está aumentando, não diminuindo).

**Anatomia de uma crise (fases típicas):**

1. **Choque inicial:** evento gatilho (Lehman, COVID, flash crash). Queda súbita, VIX spike, liquidez desaparece.
2. **Contágio:** sell-off se espalha para ativos não relacionados. Correlações explodem. Margin calls forçam vendas adicionais.
3. **Capitulação:** volume extremo, VIX atinge máxima, o último holdout vende. Frequentemente marca o fundo (ou próximo).
4. **Estabilização:** autoridades intervêm (Fed, fiscal), volatilidade começa a cair de níveis extremos. Transição para Risk-On/Recovery.

**Distinção chave de Trending Down:** velocidade, correlação e pânico. Trending Down é gradual e ordenado; Crisis é não-linear, com feedback loops (margin calls gerando mais vendas, gerando mais margin calls).

**Estratégias favorecidas:** hedging ativo (puts, VIX calls), cash, posições defensivas, tail-risk strategies que pagam neste cenário.

**Gestão de risco:** preservação de capital é prioridade absoluta. Liquidez deve ser considerada — pode ser impossível sair de posições ao preço desejado.

**⏱ Perspectiva 1H:**
No 1H, crises se manifestam como cascatas de selling pressure que atravessam sessões inteiras. O gráfico horário durante uma crise mostra candles vermelhos gigantes com sombras inferiores longas (tentativas de bounce que falham) seguidos por mais selling. O 1H é perigoso durante crises porque os movimentos são não-lineares — o preço pode cair 3% em uma hora e mais 5% na hora seguinte. Recomendo fortemente NÃO tentar operar crises no 1H (nem para shortar), a menos que você tenha infraestrutura de risco institucional. A liquidez intraday durante crises é tão ruim que seu stop pode ser executado 2-3% pior do que o preço definido. Se você tem posições abertas quando a crise começa, saia na primeira oportunidade de liquidez razoável (tipicamente nos primeiros 30 minutos da sessão americana).

**⏱ Perspectiva 1D:**
O diário é mais útil durante crises para perspectiva, não para trading. O valor do diário é identificar os sinais de capitulação que indicam que o fundo está próximo: volume record, VIX em máxima com reversão intraday (candle diário com sombra inferior longa), e divergência positiva em indicadores de breadth. Recomendo não tentar comprar durante a crise ativa — esperar pelo regime de Recovery (Risk-On). A exceção é se você opera tail-risk strategies com sizing predefinido e ordens já colocadas antes da crise (puts deep OTM compradas durante Low Vol, por exemplo). Historicamente, comprar na capitulação gera os melhores retornos de longo prazo, mas exige convicção e tolerância a drawdown adicional que poucos traders têm.

---

### 10 — Risk-On / Recovery

Rally coordenado com compressão de prêmios de risco. É o espelho assimétrico do Crisis/Risk-Off: enquanto o pânico é súbito e violento, a recuperação é tipicamente gradual e escalonada.

**Características observáveis:**

- Correlações entre ativos de risco elevadas, mas na direção positiva.
- VIX caindo de níveis elevados, estrutura a termo normalizando para contango.
- Spreads de crédito comprimindo (HY-IG estreitando).
- Rotação para beta alto: small caps, emergentes, high yield outperformam.
- Short covering amplificando o rally inicial.
- Fluxo saindo de safe havens (treasuries, USD caindo).
- TINA effect ("There Is No Alternative") — yield baixo empurra capital para equities.

**Métricas quantitativas para detecção:**

- VIX caindo de >30 para <25 (transição de medo para complacência).
- VIX em contango (meses futuros > spot).
- Spread HY-IG estreitando por 5+ dias consecutivos.
- Breadth melhorando: advance-decline line subindo.
- Small caps e high beta outperformando large caps.
- Put/Call ratio caindo de níveis elevados.

**Dinâmica assimétrica:** risk-off acontece em dias; risk-on se desenrola em semanas ou meses. Isso importa para sizing e timing — entradas não precisam ser perfeitas porque o movimento é prolongado.

**Fases da recuperação:**

1. **Bear market rally / short squeeze:** a primeira onda é liderada por short covering. Pode ser violenta mas é frágil.
2. **Normalização:** spreads de crédito normalizam, vol cai, fundamentais estabilizam. A maioria ainda não acredita na recuperação.
3. **Expansão:** novo capital entra, rotação para risco, breadth melhora. A recuperação se torna auto-sustentável.

**Estratégias favorecidas:** long beta, long ativos de risco, sell puts (coleta de prêmio em vol ainda elevada), carry trades.

**Gestão de risco:** o risco é a falsa recuperação (dead cat bounce dentro de um bear market). Filtrar verificando se os indicadores de stress (VIX, spreads) estão realmente normalizando, não apenas pausando.

**⏱ Perspectiva 1H:**
O 1H durante recovery mostra um padrão interessante: os dips intraday ficam progressivamente mais rasos. No início, o preço cai 1-2% intraday e recupera; depois as quedas são de 0.5% e a recuperação é mais rápida. Esse padrão de "dips rasos + recovery rápido" é a fingerprint de demanda institucional absorvendo a oferta. No 1H, a melhor estratégia é comprar dips até a VWAP do dia com stop curto. O timing ideal é: esperar queda na abertura europeia ou americana (profit-taking), entrar quando o preço encontrar suporte, target no high do dia anterior.

**⏱ Perspectiva 1D:**
Recovery no diário é onde a maioria do dinheiro é feito em ciclos de mercado. O signal principal é: preço fazendo higher lows consecutivos no diário + VIX em downtrend + breadth melhorando. Recomendo entrar na segunda confirmação (segundo higher low), não no primeiro. O primeiro pode ser dead cat bounce; o segundo indica que compradores estão dispostos a defender preços progressivamente mais altos. Sizing: começar com 50% e adicionar nos dips até chegar a 100%. O erro mais comum é entrar tarde demais (quando já virou Trending Up pleno) — a melhor relação risco/retorno está no início da recovery, quando a maioria ainda está com medo.

---

## Sub-estados de Transição

Regimes de transição que representam inflexões entre estados primários. São mais difíceis de detectar em tempo real e podem ser tratados como moduladores dos regimes primários.

---

### 11 — Distribution / Topping

Momentum decaindo em topo com sinais de exaustão. O regime de Trending Up ainda está tecnicamente vigente, mas perdendo força. Representa a transição entre trending up e ranging, trending down ou crash.

**Características observáveis:**

- Divergência negativa em RSI, MACD e outros osciladores (preço faz novo topo, indicador não confirma).
- Volume decrescente nos rallies e crescente nas correções.
- Amplitude dos rallies diminuindo (topos cada vez mais próximos entre si).
- Breadth deteriorando: poucos nomes carregando o índice (concentração).
- Smart money indicators sugerindo distribuição (Wyckoff).
- Aumento de hedging institucional visível no skew de opções.
- Setores defensivos começando a outperformar cíclicos.
- Insider selling acelerando.

**Métricas quantitativas para detecção:**

- RSI(14) fazendo lower highs enquanto preço faz higher highs (divergência).
- Volume médio nos últimos 5 dias de alta < volume médio nos últimos 5 dias de baixa.
- Advance-decline line fazendo lower highs enquanto o índice faz higher highs.
- Percentual de ações acima da MA(50) caindo enquanto o índice sobe.
- Número de novos máximos de 52 semanas diminuindo.

**Contexto Wyckoff:** distribution é uma das fases do ciclo de Wyckoff. A sequência clássica é: Preliminary Supply (PSY), Buying Climax (BC), Automatic Reaction (AR), Secondary Test (ST), Upthrust (UT), e finalmente Sign of Weakness (SOW) com breakdown.

**Estratégias favorecidas:** redução gradual de exposição long, compra de proteção (puts ficando mais baratas antes do colapso de vol), rotação para defensivos.

**Sinal de invalidação:** novo topo com volume forte e breadth ampla invalida a tese de distribution.

**⏱ Perspectiva 1H:**
Distribution no 1H é difícil de detectar de forma isolada. O que você verá são sessions onde o preço abre forte (gap up ou rally na abertura), faz novo intraday high, e depois vende durante o resto do dia, fechando perto do low. Esse padrão repetido por 3-5 sessões consecutivas é distribution intraday. O perfil de volume intraday mostra concentração de volume nos preços mais altos (indicando venda institucional em força). Recomendo usar o 1H não para detectar distribution, mas para executar saídas: vender rallies intraday que falham em sustentar novos highs, especialmente se o volume cai na subida.

**⏱ Perspectiva 1D:**
O diário é o timeframe ideal para detectar distribution. A divergência entre preço e RSI diário é o sinal mais clássico e confiável. Processo recomendado: (1) identificar divergência no diário; (2) confirmar com deterioração de breadth; (3) começar a reduzir posição em 1/3; (4) se o preço falhar em fazer novo topo, reduzir mais 1/3; (5) se romper o último higher low, sair completamente. Distribution no diário pode durar 2-6 semanas, então não há pressa — a vantagem é que você está vendendo em força, não em pânico.

---

### 12 — Accumulation / Bottoming

Absorção de pressão vendedora em base com volatilidade decrescente. Regime de transição que tipicamente antecede uma reversão para trending up. Representa o inverso da distribution.

**Características observáveis:**

- Volume alto em dias de queda que não produzem novos mínimos (absorção).
- Divergência positiva em osciladores (preço faz novo fundo, indicador não confirma).
- Volatilidade começando a comprimir após um período de stress.
- Testes de suporte com volume decrescente a cada tentativa.
- Breadth parando de deteriorar e começando a melhorar.
- Insiders e smart money acumulando (visível em fluxos, 13F filings).
- Setores cíclicos parando de underperformar.
- Put/Call ratio atingindo extremos (pessimismo máximo).

**Métricas quantitativas para detecção:**

- RSI(14) fazendo higher lows enquanto preço faz equal lows ou lower lows (divergência positiva).
- Volume em dias de queda diminuindo a cada teste do suporte.
- Volatilidade realizada começando a cair de níveis elevados.
- Advance-decline line começando a subir enquanto índice ainda lateral ou em queda.
- Percentual de ações abaixo da MA(200) atingindo extremos e começando a reverter.

**Contexto Wyckoff:** accumulation no framework de Wyckoff segue: Preliminary Support (PS), Selling Climax (SC), Automatic Rally (AR), Secondary Test (ST), Spring (teste abaixo do suporte com volume baixo que reverte), Sign of Strength (SOS), e Last Point of Support (LPS) antes do markup.

**Estratégias favorecidas:** construção gradual de posição long, scaling in com sizing pequeno, venda de puts (coleta de prêmio com disposição para receber o ativo).

**Risco principal:** confundir pausa temporária em tendência de baixa com acumulação genuína. Confirmar com múltiplos sinais antes de aumentar exposição.

**⏱ Perspectiva 1H:**
No 1H, acumulação aparece como sessions onde o preço cai na abertura, testa o low (de ontem ou da semana), e fecha perto do high do dia. O perfil de volume mostra absorção — volume alto nos lows que são defendidos. O spring de Wyckoff é particularmente visível no 1H: queda rápida abaixo do suporte intraday com volume, seguida de reversão imediata com volume ainda maior. Esse é um dos melhores setups de entrada no 1H. Stop: abaixo do low do spring. Target: topo do range de acumulação. Recomendo esperar o spring (ou pelo menos um secondary test com volume decrescente) antes de entrar — entrar cedo demais em acumulação é catching a falling knife.

**⏱ Perspectiva 1D:**
Acumulação no diário é um dos setups mais confiáveis para swing trading. O padrão clássico: preço faz fundo, bounce, retesta o fundo com volume menor, e depois começa a subir. Divergência positiva no RSI diário + volume decrescente nos testes de suporte = alta probabilidade de reversão. Recomendo construir posição em 3 tranches: (1) 1/3 no secondary test; (2) 1/3 no spring ou LPS; (3) 1/3 quando o preço romper acima do range com volume. Stop: abaixo do low da acumulação. Holding period típico: 3-8 semanas (do breakout até o trending up maduro). Acumulação no diário dura tipicamente 2-6 semanas.

---

### 13 — Blow-off / Euphoria

Aceleração parabólica em tendência de alta com volatilidade crescente. O regime de Trending Up se transforma em algo qualitativamente diferente: o preço sobe exponencialmente, atraindo FOMO e alavancagem especulativa.

**Características observáveis:**

- Retornos diários muito acima da média, com aceleração (cada semana mais forte que a anterior).
- Desvio extremo das médias móveis (preço 3+ desvios padrão acima da MA20).
- Volume explosivo — muitas vezes o maior volume do ciclo inteiro.
- Volatilidade subindo junto com o preço (incomum — normalmente vol e preço são inversamente correlacionados).
- Narrativa dominante de "desta vez é diferente" na mídia e nas redes sociais.
- Alavancagem do mercado em máximas (margin debt, open interest em futuros).
- Google Trends e menções em social media em máximas históricas.
- Participantes novatos entrando (indicador contrarian clássico).

**Métricas quantitativas para detecção:**

- Preço > 3 desvios padrão acima da MA(20).
- Retorno semanal > percentil 95 da distribuição histórica por 2+ semanas consecutivas.
- RSI(14) > 80 por 5+ períodos.
- Volume > 3x a média de 50 períodos.
- Taxa de variação do preço (ROC) acelerando (2ª derivada positiva).
- Distância entre preço e MA(50) crescendo exponencialmente.

**Distinção chave de Trending Up:** a taxa de variação está acelerando em vez de se manter estável. O gráfico é convexo (curvando para cima), não linear.

**Psicologia do blow-off:** este regime é alimentado por feedback positivo: preço sobe → mais compradores entram (FOMO) → preço sobe mais → mais alavancagem → preço sobe ainda mais. O loop se mantém até que o último comprador marginal entrou e não há mais demanda incremental. O colapso que se segue é tipicamente proporcional à extensão do blow-off.

**Exemplos históricos:** tulipas holandesas (1637), dot-com final (dez 1999 – mar 2000), Bitcoin em dezembro de 2017, GameStop em janeiro de 2021, meme coins em ciclos cripto.

**Estratégias favorecidas:** trailing stops extremamente agressivos (baseados em ATR com multiplicador reduzido), redução de sizing para proteger ganhos acumulados, compra de puts como seguro (caras, mas o risco de reversão justifica).

**Gestão de risco:** este regime termina quase sempre de forma violenta. A prioridade é capturar o máximo possível do movimento mantendo um plano de saída rígido. Nunca aumentar posição neste regime — apenas administrar e proteger o que já tem.

**⏱ Perspectiva 1H:**
No 1H, blow-offs produzem candles de range extremo quase sem pullback — o preço sobe 1-2% por hora sem pausa. O gráfico horário mostra uma sequência de candles verdes com pouca ou nenhuma sombra inferior (sem sellers). Quando a primeira sombra superior significativa aparece no 1H (candle de alta com rejeição forte no topo), é o primeiro sinal de exaustão. Recomendo usar trailing stop no 1H baseado em 1x ATR(14) horário (mais apertado que o normal de 2-3x). Se o preço fechar abaixo da EMA(8) horária (sim, EMA(8), não EMA(20) — precisa ser agressivo), considere sair de 50% da posição. O problema com blow-offs é que o topo parece óbvio em hindsight mas no momento parece que "pode subir mais" — a disciplina do trailing stop horário resolve isso mecanicamente.

**⏱ Perspectiva 1D:**
No diário, blow-off é identificável pela sequência de candles de corpo grande com gap ups entre eles. O preço se afasta cada vez mais da MA(20) diária — quando a distância excede 3 desvios padrão E o volume começa a cair (divergência volume-preço), o fim está próximo. Recomendo colocar stop na MA(10) diária durante blow-offs (não na MA(20), que fica muito longe). Se o preço fechar abaixo da MA(10) no diário, sair de 75% e mover stop do restante para breakeven. Historicamente, blow-offs no diário duram 5-15 sessões. A reversão subsequente tipicamente retraça 50-80% do movimento em metade do tempo que levou para subir.

---

## Matriz de Transição entre Regimes

Compreender as transições mais prováveis entre regimes ajuda a antecipar mudanças e posicionar-se antes que o novo regime esteja plenamente estabelecido.

**Transições de alta probabilidade:**

| De → Para                          | Probabilidade          | Comentário                             |
| ---------------------------------- | ---------------------- | -------------------------------------- |
| Low Vol → Breakout                 | Alta                   | Vol comprimida resolve em expansão     |
| Breakout → Trending                | Alta                   | Breakout legítimo vira tendência       |
| Breakout → Choppy                  | Média                  | Falso breakout gera confusão           |
| Trending Up → Distribution         | Média                  | Exaustão natural da tendência          |
| Trending Down → Accumulation       | Média                  | Vendedores se esgotam                  |
| Distribution → Trending Down       | Média-Alta             | Distribuição resolve em queda          |
| Accumulation → Trending Up         | Média-Alta             | Acumulação resolve em alta             |
| Trending Down → Crisis             | Baixa (mas impactante) | Aceleração com feedback loops          |
| Crisis → Risk-On/Recovery          | Alta                   | Pânico é insustentável no longo prazo  |
| Trending Up → Blow-off             | Baixa                  | Aceleração parabólica rara             |
| Blow-off → Crisis ou Trending Down | Alta                   | Blow-offs terminam violentamente       |
| Ranging → Low Vol                  | Média                  | Consolidação se estreita               |
| Choppy → Ranging                   | Média                  | Vol arrefece mantendo falta de direção |
| Mean-Reverting → Trending          | Média                  | Hurst exponent cruza 0.5 para cima     |
| Recovery → Trending Up             | Alta                   | Normalização vira tendência            |

**Transições raras/improváveis:**

| De → Para            | Comentário                                       |
| -------------------- | ------------------------------------------------ |
| Crisis → Blow-off    | Quase impossível sem fase intermediária          |
| Low Vol → Crisis     | Requer choque exógeno extremo                    |
| Choppy → Low Vol     | Muito raro — vol alta não comprime diretamente   |
| Trending Up → Crisis | Possível mas raro sem Distribution intermediária |

---

## Conflitos entre Timeframes

Um aspecto crítico e pouco discutido: o regime no 1H pode ser diferente do regime no 1D. Isso cria conflitos que precisam ser resolvidos com regras claras.

**Princípio geral:** o timeframe maior domina. Se o diário diz Trending Up e o horário diz Ranging, você está em pullback dentro de uma tendência de alta — a ação é buy the dip, não ficar flat.

**Tabela de resolução de conflitos comuns:**

| 1D            | 1H                  | Interpretação                                  | Ação                                              |
| ------------- | ------------------- | ---------------------------------------------- | ------------------------------------------------- |
| Trending Up   | Ranging             | Pullback / consolidação dentro de uptrend      | Buy dips no 1H, manter viés long                  |
| Trending Up   | Choppy              | Distribuição intraday ou shakeout              | Reduzir exposição, apertar stops                  |
| Trending Down | Mean-Reverting      | Bounce técnico dentro de downtrend             | Não comprar, ou short em rallies                  |
| Ranging       | Trending Up         | Falso breakout intraday dentro de range diária | Não confiar, esperar confirmação no diário        |
| Low Vol       | Breakout            | Início de resolução da compressão              | Alta convicção — entrar na direção do breakout 1H |
| Crisis        | Mean-Reverting      | Dead cat bounce                                | Não comprar, manter hedge                         |
| Recovery      | Choppy              | Recuperação ainda frágil                       | Sizing reduzido, paciência                        |
| Distribution  | Trending Up no 1H   | Últimos suspiros da tendência                  | Vender rallies, não comprar dips                  |
| Accumulation  | Trending Down no 1H | Teste de suporte dentro de acumulação          | Preparar compra, esperar spring                   |
| Blow-off      | Choppy no 1H        | Possível topo sendo formado                    | Sair de 50%, trailing stop agressivo              |

**Recomendação:** criar uma lookup table no modelo que mapeia (regime_1D, regime_1H) → (ação, sizing_modifier, estratégia). Isso sistematiza a resolução de conflitos e remove decisões emocionais.

---

## Sizing por Regime

O sizing é tão importante quanto a direção. Cada regime implica um nível diferente de confiança e de risco, o que deve ser refletido no tamanho da posição.

**Tabela de sizing recomendado (como % do sizing máximo permitido):**

| #   | Regime         | Sizing 1H            | Sizing 1D            | Justificativa                               |
| --- | -------------- | -------------------- | -------------------- | ------------------------------------------- |
| 0   | NoLabel        | 0-25%                | 25-50%               | Incerteza alta                              |
| 1   | Trending       | 75-100%              | 75-100%              | Edge alto, direcionalidade clara            |
| 2   | Trending Up    | 75-100%              | 100%                 | Melhor regime para long                     |
| 3   | Trending Down  | 50-75%               | 75-100%              | Assimetria desfavorável (bounces violentos) |
| 4   | Ranging        | 0-25%                | 0-25%                | Sem edge                                    |
| 5   | Mean-Reverting | 50-75%               | 50-75%               | Edge existe mas limitado                    |
| 6   | Low Vol        | 25-50%               | 25-50%               | Aguardando resolução                        |
| 7   | Breakout       | 75-100%              | 75-100%              | Alto edge se validado                       |
| 8   | Choppy         | 0%                   | 0-25%                | Preservar capital                           |
| 9   | Crisis         | 0%                   | 0-25% (hedge only)   | Preservar capital                           |
| 10  | Recovery       | 50-75%               | 75-100%              | Bom edge mas incerteza residual             |
| 11  | Distribution   | 25-50% (reduzindo)   | 50-75% (reduzindo)   | Transição, reduzir gradualmente             |
| 12  | Accumulation   | 25-50% (construindo) | 50-75% (construindo) | Transição, construir gradualmente           |
| 13  | Blow-off       | 50% (reduzindo)      | 50% (reduzindo)      | Alto risco de reversão                      |

**Nota sobre sizing no 1H vs 1D:** o sizing no 1H é consistentemente menor porque o ruído é maior, os custos de transação pesam mais, e a taxa de falsos sinais é mais alta. O 1H serve primariamente para timing, não para sizing. O sizing deve ser definido pelo regime no 1D e ajustado (para baixo, nunca para cima) pelo regime no 1H.

---

## Indicadores Recomendados por Regime

**Indicadores que funcionam melhor em cada regime:**

| Regime         | Indicadores Primários                | Indicadores Secundários                    |
| -------------- | ------------------------------------ | ------------------------------------------ |
| Trending       | ADX, EMAs, Hurst                     | MACD, ROC                                  |
| Trending Up    | EMAs, OBV, RSI                       | Breadth, A/D line                          |
| Trending Down  | EMAs, OBV, VIX                       | Credit spreads, Put/Call                   |
| Ranging        | Bollinger Bands, ATR                 | ADX (para confirmar baixa direcionalidade) |
| Mean-Reverting | Z-score, Bollinger, ADF              | Hurst, Half-life O-U                       |
| Low Vol        | BB Bandwidth, ATR rank, TTM Squeeze  | IV percentile, Volume                      |
| Breakout       | Volume, ATR expansion, ADX           | Gap analysis, Range breakout               |
| Choppy         | ATR vs Retorno acumulado             | ADX, Contagem de reversões                 |
| Crisis         | VIX, Credit spreads, Correlação      | TED spread, Breadth, Circuit breakers      |
| Recovery       | VIX term structure, Spreads, Breadth | Small cap vs Large cap, Put/Call           |
| Distribution   | RSI divergence, OBV, Breadth         | Skew opções, Insider selling               |
| Accumulation   | RSI divergence, Volume em testes     | Wyckoff phases, Breadth                    |
| Blow-off       | Distância da MA, ROC aceleração      | Volume divergence, Social sentiment        |

**Ajustes por timeframe:**

No 1H, adicionar: VWAP, perfil de volume intraday, delta de volume (buying vs selling pressure), tempo e sessão (hora do dia como feature).

No 1D, adicionar: MA(200), breadth indicators, dados macro (VIX, spreads de crédito, curva de juros), dados de fluxo (COT report, fund flows, 13F).

---

## Considerações de Implementação

**Para detecção de regime via modelo:**

1. **Features sugeridas (mínimo viável):**
   - Retorno acumulado (5, 10, 20 períodos).
   - Volatilidade realizada (5, 10, 20 períodos).
   - ADX (14 períodos).
   - Hurst exponent (rolling, 50-100 períodos).
   - Autocorrelação lag 1 dos retornos (rolling, 20 períodos).
   - Z-score do preço relativo à MA(20).
   - Razão volume atual / volume MA(20).
   - ATR percentile rank (100 períodos).

2. **Modelos sugeridos:**
   - Hidden Markov Model (HMM): natural para regimes, captura transições.
   - Random Forest / XGBoost: boa performance com features bem construídas.
   - Gaussian Mixture Model (GMM): identifica clusters naturais nos dados.
   - Regime switching models (Hamilton): fundamentação econométrica sólida.

3. **Validação:**
   - Testar estabilidade dos labels (mesmo regime persistindo por N períodos).
   - Medir latência de detecção (quantos períodos para detectar mudança real).
   - Calcular a confusion matrix entre regimes previstos e realizados.
   - Walk-forward validation para evitar overfitting.

4. **Calibração por timeframe:**
   - 1H: lookback windows menores (10-50 períodos), decay mais agressivo, features de microestrutura.
   - 1D: lookback windows maiores (20-100 períodos), mais estabilidade, features macro.
   - Considerar calibrar modelos separados para cada timeframe em vez de usar o mesmo modelo com parâmetros diferentes.

---

## Referência Rápida

| #   | Regime                | Ação Default           | Vol            | Direcionalidade    | Duração 1H   | Duração 1D    |
| --- | --------------------- | ---------------------- | -------------- | ------------------ | ------------ | ------------- |
| 0   | NoLabel               | Neutro / sizing mínimo | —              | —                  | —            | —             |
| 1   | Trending              | Seguir tendência       | Média          | Alta               | 8-40h        | Semanas–Meses |
| 2   | Trending Up           | Long / buy dips        | Média-Baixa    | Alta (positiva)    | 8-40h        | Semanas–Meses |
| 3   | Trending Down         | Short / reduce long    | Média-Alta     | Alta (negativa)    | 8-30h        | Semanas–Meses |
| 4   | Ranging               | Flat / sizing mínimo   | Baixa          | Nenhuma            | 4-20h        | Dias–Semanas  |
| 5   | Mean-Reverting        | Fade extremos          | Média          | Oscilante          | 3-15h        | Dias–Semanas  |
| 6   | Low Vol / Compression | Comprar vol / aguardar | Muito Baixa    | Nenhuma            | 4-12h        | Dias–Semanas  |
| 7   | Volatile / Breakout   | Seguir rompimento      | Alta           | Emergente          | 1-8h         | Horas–Dias    |
| 8   | Choppy / Whipsaw      | Não operar             | Alta           | Nenhuma            | 4-20h        | Dias–Semanas  |
| 9   | Crisis / Risk-Off     | Hedge / cash           | Muito Alta     | Alta (negativa)    | 8-40h        | Dias–Semanas  |
| 10  | Risk-On / Recovery    | Long beta              | Alta→Média     | Alta (positiva)    | 8-40h        | Semanas–Meses |
| 11  | Distribution          | Reduzir long           | Média          | Decaindo           | 12-40h       | Semanas       |
| 12  | Accumulation          | Construir long         | Alta→Baixa     | Formando           | 12-40h       | Semanas       |
| 13  | Blow-off / Euphoria   | Proteger ganhos        | Alta e subindo | Extrema (positiva) | Dias–Semanas | Dias–Semanas  |

---

## Stop Loss Rules por Regime

O tipo de stop, sua largura e lógica de ajuste devem mudar conforme o regime. Usar o mesmo stop em todos os regimes é um dos erros mais comuns em trading sistemático — equivale a usar o mesmo remédio para todas as doenças.

**Princípios gerais:**

- Stops mais largos em regimes de alta volatilidade (para evitar ser stopado por ruído).
- Stops mais apertados em regimes de transição e exaustão (para proteger capital).
- Stops estruturais (baseados em price action) em regimes de tendência.
- Stops estatísticos (baseados em desvio padrão/z-score) em regimes de mean-reversion.
- Stops temporais (sair após N períodos) em regimes sem direcionalidade.

### Tabela de Stop Loss por Regime

| #   | Regime         | Tipo de Stop                  | Fórmula / Regra (1H)                                                                            | Fórmula / Regra (1D)                                                                                           | Notas                                                                             |
| --- | -------------- | ----------------------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| 0   | NoLabel        | Temporal + Vol                | Sair após 4-8 barras se sem lucro; stop em 1.5x ATR(14)                                         | Sair após 3-5 dias se sem lucro; stop em 2x ATR(14)                                                            | Não ficar exposto sem convicção                                                   |
| 1   | Trending       | Estrutural trailing           | Abaixo/acima do último swing low/high no 1H; mínimo 1x ATR(14)                                  | Abaixo/acima do último swing low/high diário; mínimo 1.5x ATR(14)                                              | Nunca mover stop contra a tendência                                               |
| 2   | Trending Up    | Trailing EMA                  | Fechar abaixo da EMA(20) 1H por 2 barras → sair 50%; abaixo da EMA(50) → sair tudo              | Fechar abaixo da EMA(21) diária por 2 dias → sair 50%; abaixo do último HL → sair tudo                         | Stop nunca sobe menos que o anterior                                              |
| 3   | Trending Down  | Trailing EMA (short)          | Fechar acima da EMA(20) 1H por 2 barras → cobrir 50%; acima da EMA(50) → cobrir tudo            | Fechar acima da EMA(21) diária por 2 dias → cobrir 50%; acima do último LH → cobrir tudo                       | Bounces são mais violentos que pullbacks — stop 20% mais largo que em Trending Up |
| 4   | Ranging        | Fixo + Temporal               | 0.7x ATR(14) do preço de entrada; sair após 6-10 barras se sem resolução                        | 1x ATR(14); sair após 5 dias se dentro da range                                                                | Sizing mínimo torna o stop menos relevante                                        |
| 5   | Mean-Reverting | Z-score                       | Stop em z-score ±3.0 (ou ±2.5 para conservador); sair se z-score não reverteu em 1.5x half-life | Stop em z-score ±3.0; sair se não reverteu em 2x half-life estimada                                            | Se half-life > 20 períodos, considerar que regime mudou                           |
| 6   | Low Vol        | Breakout-triggered            | Se entrou em breakout: stop no centro da consolidação (0.5x range)                              | Stop no centro da consolidação; se usando opções, stop é o prêmio pago                                         | O stop mais "caro" é o time decay em opções                                       |
| 7   | Breakout       | Estrutural                    | Atrás da zona de consolidação rompida; 0.5-0.7x ATR(14) abaixo/acima do nível                   | Atrás do nível rompido; se preço fechar de volta dentro da range, sair imediatamente                           | Stop apertado — breakout funciona ou não funciona                                 |
| 8   | Choppy         | Não deveria estar posicionado | Se pego posicionado: 1x ATR(14), sem questionar; circuit breaker após 2 stops                   | Se pego posicionado: 1.5x ATR(14); não reentrar até regime mudar                                               | Prioridade é sair, não otimizar                                                   |
| 9   | Crisis         | Emergencial                   | Sair na primeira oportunidade de liquidez; aceitar slippage                                     | Sair ou hedge imediato; puts se disponíveis; aceitar execução ruim                                             | Não é hora de otimizar stop — é hora de sobreviver                                |
| 10  | Recovery       | Estrutural progressivo        | Stop abaixo do último swing low 1H; apertar a cada novo HL                                      | Stop abaixo do último HL diário; começar largo (2x ATR) e apertar para 1.5x após confirmação                   | Aceitar stops mais largos no início (incerteza alta)                              |
| 11  | Distribution   | Trailing agressivo (longs)    | Fechar abaixo da EMA(10) 1H → sair 50%; abaixo da EMA(20) → sair tudo                           | Fechar abaixo da EMA(10) diária → sair 1/3; abaixo da EMA(21) → sair mais 1/3; abaixo do último HL → sair tudo | Stops progressivamente mais apertados à medida que distribution avança            |
| 12  | Accumulation   | Abaixo do range               | Stop abaixo do low do spring (se ocorreu); ou abaixo do low da range de acumulação              | Stop abaixo do low da acumulação; aceitar ser stopado 1x — é o custo de tentar pegar a reversão                | Posição pequena, stop largo                                                       |
| 13  | Blow-off       | Trailing ultra-agressivo      | 1x ATR(14) trailing; fechar abaixo da EMA(8) → sair 50%                                         | Fechar abaixo da MA(10) diária → sair 75%; mover restante para breakeven                                       | Nunca usar stop mental — deve ser automático                                      |

### Regras Adicionais de Stop

**Stop de correlação (cross-asset):** se o ativo está em Trending Up mas um ativo altamente correlacionado (ex: índice do setor) rompe suporte importante, apertar stop em 50% independente do regime local.

**Stop de volatilidade (regime-override):** se a volatilidade realizada de 5 períodos exceder 2x a volatilidade de 50 períodos, reduzir a largura do stop em 30% (o mercado ficou mais perigoso, independente do regime).

**Stop de drawdown do portfólio:** se o drawdown do portfólio total atinge -5% no dia (1H) ou -10% na semana (1D), reduzir todas as posições em 50% e apertar todos os stops, independente dos regimes individuais. Isso é o circuit breaker do portfólio.

**Stop de tempo (universal):** posição que não está gerando P&L positivo após 2x a duração típica do regime deve ser fechada. Se o regime é Mean-Reverting com half-life de 8 períodos e a posição não está no lucro após 16 períodos, a tese falhou.

---

## Event-Driven Regime Overrides

Eventos macro agendados criam janelas temporárias onde o regime "real" do mercado é sobrescrito por um regime de incerteza. O modelo pode dizer Trending Up, mas 30 minutos antes do FOMC o mercado efetivamente está em modo de espera — e imediatamente após pode entrar em Breakout ou Choppy.

### Classificação de Eventos por Impacto

**Tier 1 — Alto impacto (override obrigatório):**

- FOMC (decisão de taxa + press conference).
- Non-Farm Payrolls (NFP).
- CPI / Inflação.
- Earnings de mega caps (AAPL, NVDA, MSFT, AMZN, GOOG, META, TSLA).
- Decisões de bancos centrais (ECB, BoJ, BoE).
- Eleições nacionais em economias do G7.
- Eventos geopolíticos de alto impacto (escalada militar, sanções).

**Tier 2 — Impacto médio (cautela recomendada):**

- PPI, Retail Sales, GDP (revisão).
- Earnings de large caps relevantes para o setor.
- Minutes do FOMC (3 semanas após a decisão).
- Dados de emprego (Jobless Claims, ADP).
- PMI (Manufacturing e Services).
- Decisões de bancos centrais de emergentes relevantes (China, Brasil).

**Tier 3 — Baixo impacto (monitorar):**

- Dados de housing (Housing Starts, Existing Home Sales).
- Consumer Confidence, University of Michigan Sentiment.
- Earnings de mid caps.
- Speeches de membros individuais do Fed (não o Chair).
- Dados de trade balance.

### Protocolo de Override por Tier

**Tier 1 — Pré-evento:**

| Janela          | Ação no 1H                                                                | Ação no 1D                                                         |
| --------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| 24h antes       | Reduzir sizing para 50%; não abrir novas posições                         | Apertar stops em 30%; revisar hedge                                |
| 2h antes        | Reduzir sizing para 25%; considerar flat                                  | Nenhuma ação adicional (diário não é afetado por janelas de horas) |
| 30min antes     | Flat ou sizing mínimo com hedge; qualquer regime → NoLabel                | —                                                                  |
| Evento          | Não operar; observar                                                      | —                                                                  |
| 0-30min depois  | Regime = Volatile/Breakout temporário; não reagir a movimentos iniciais   | —                                                                  |
| 30min-2h depois | Regime começa a se estabilizar; permitir sinais do modelo se consistentes | Avaliar candle diário no fechamento                                |
| 2h+ depois      | Retornar ao regime do modelo se o novo estado for coerente com pré-evento | Regime diário pode mudar; atualizar no fechamento                  |

**Tier 2 — Pré-evento:**

| Janela         | Ação no 1H                             | Ação no 1D              |
| -------------- | -------------------------------------- | ----------------------- |
| 2h antes       | Reduzir sizing para 75%; apertar stops | Nenhuma ação específica |
| 30min antes    | Não abrir novas posições               | —                       |
| 0-15min depois | Observar; não reagir a spike inicial   | —                       |
| 15min+ depois  | Retornar ao regime do modelo           | Avaliar no fechamento   |

**Tier 3 — Monitorar:** não requer override formal, mas estar ciente. Se o dado surpreender significativamente (> 2 desvios do consenso), tratar como Tier 2.

### Regras Específicas para Earnings

Earnings são eventos únicos porque afetam ativos individuais, não o mercado inteiro.

**Pré-earnings (24h antes):**

- Reduzir posição no ativo para 25-50%.
- Se a posição é core (convicção alta de longo prazo), considerar hedge com opções em vez de reduzir.
- Regime do ativo → NoLabel até o resultado.
- Não abrir novas posições no ativo.

**Pós-earnings (imediato):**

- Gap up/down > 5% com volume → tratar como Breakout.
- Movimento < 3% → retornar ao regime anterior se coerente.
- Esperar 30min após a abertura para avaliar o regime real (a reação inicial é frequentemente revertida).

**Pós-earnings (1-5 dias):**

- O novo regime pós-earnings é geralmente Trending (na direção da reação) se o gap foi > 5%.
- Earnings negativos podem acelerar Distribution → Trending Down.
- Earnings positivos podem resolver Accumulation → Trending Up.

### Calendário de Eventos como Feature

Recomendo incluir a proximidade de eventos como feature no modelo de detecção:

- `hours_to_tier1_event`: distância em horas até o próximo evento Tier 1.
- `hours_since_tier1_event`: distância em horas desde o último evento Tier 1.
- `event_surprise`: desvio do dado realizado vs consenso (em Z-score), disponível após o evento.

Quando `hours_to_tier1_event < 4`, o modelo deve automaticamente aumentar o threshold de confiança necessário para manter o regime atual (equivalente a puxar o regime na direção de NoLabel).

---

## Regime Decay / Confidence Score

A confiança no regime atual não é estática. Ela decai com o tempo e com mudanças nas features subjacentes. Este sistema permite ajustar sizing e stops dinamicamente com base na "saúde" do regime.

### Modelo de Confidence Score

O confidence score C(t) de um regime é função de três componentes:

**C(t) = w₁ × C_model(t) + w₂ × C_duration(t) + w₃ × C_consistency(t)**

Onde:

- **C_model(t)**: probabilidade do regime atual na saída do classificador (0 a 1).
- **C_duration(t)**: fator de decaimento baseado em quanto tempo o regime já dura.
- **C_consistency(t)**: medida de consistência das features com o regime atribuído.
- **Pesos sugeridos:** w₁ = 0.4, w₂ = 0.3, w₃ = 0.3.

### C_duration — Decaimento Temporal

A probabilidade de transição de regime aumenta com o tempo. Cada regime tem uma duração esperada, e quanto mais tempo o regime excede essa expectativa, mais a confiança decai.

**Fórmula:**

```
C_duration(t) = exp(-λ × max(0, t - T_median))
```

Onde:

- `t` = duração atual do regime (em períodos).
- `T_median` = duração mediana esperada do regime.
- `λ` = taxa de decaimento (calibrar por regime e timeframe).

**Durações medianas estimadas (para calibração inicial):**

| Regime         | T_median (1H)     | T_median (1D) | λ (1H) | λ (1D) |
| -------------- | ----------------- | ------------- | ------ | ------ |
| Trending Up    | 24 barras (1 dia) | 30 dias       | 0.03   | 0.02   |
| Trending Down  | 20 barras         | 25 dias       | 0.04   | 0.025  |
| Ranging        | 12 barras         | 10 dias       | 0.05   | 0.04   |
| Mean-Reverting | 10 barras         | 12 dias       | 0.05   | 0.04   |
| Low Vol        | 8 barras          | 8 dias        | 0.06   | 0.05   |
| Breakout       | 4 barras          | 3 dias        | 0.10   | 0.10   |
| Choppy         | 10 barras         | 8 dias        | 0.05   | 0.05   |
| Crisis         | 12 barras         | 8 dias        | 0.04   | 0.05   |
| Recovery       | 20 barras         | 20 dias       | 0.03   | 0.03   |
| Distribution   | 16 barras         | 15 dias       | 0.04   | 0.03   |
| Accumulation   | 16 barras         | 15 dias       | 0.04   | 0.03   |
| Blow-off       | 6 barras          | 8 dias        | 0.08   | 0.06   |

**Nota:** estes valores são pontos de partida. Devem ser calibrados com dados reais do ativo/mercado específico.

### C_consistency — Consistência das Features

Mede se as features atuais ainda são consistentes com o regime atribuído.

**Para cada regime, definir um conjunto de "feature checks":**

Exemplo para Trending Up:

- Preço > EMA(20)? (sim = +0.2, não = -0.3)
- ADX > 25? (sim = +0.2, não = -0.2)
- Retorno 10 períodos > 0? (sim = +0.2, não = -0.3)
- OBV fazendo novos máximos? (sim = +0.1, não = -0.1)
- RSI sem divergência? (sim = +0.1, não = -0.2)

C_consistency = max(0, min(1, 0.5 + soma_dos_checks))

### Aplicação Prática do Confidence Score

**Sizing ajustado:** `sizing_efetivo = sizing_base_do_regime × C(t)`

Se o regime é Trending Up (sizing base = 100%) mas C(t) = 0.6, o sizing efetivo é 60%.

**Thresholds de ação:**

- C(t) > 0.8: alta confiança. Sizing pleno, stops normais.
- C(t) 0.6-0.8: confiança moderada. Sizing 75%, stops 20% mais apertados.
- C(t) 0.4-0.6: confiança baixa. Sizing 50%, considerar realizar lucro parcial.
- C(t) < 0.4: confiança muito baixa. Tratar como NoLabel. Sizing 25% ou flat.

**Alerta de transição:** quando C(t) cai abaixo de 0.5, ativar monitoramento de transição — calcular probabilidades dos regimes alternativos e preparar plano de ação para os 2 regimes mais prováveis.

---

## Asset-Class Specific Notes

Cada classe de ativo tem características estruturais que fazem certos regimes mais ou menos frequentes, e que alteram como os regimes se manifestam.

### Equities (Ações / Índices)

**Regimes mais frequentes:** Trending Up (viés estrutural de alta no longo prazo), Ranging, Distribution, Recovery.

**Regimes menos frequentes:** Mean-Reverting (ações individuais raramente mean-revert; índices um pouco mais), Crisis (raro mas devastador).

**Particularidades:**

- O viés de alta de longo prazo (equity risk premium) significa que Trending Up é o "estado natural" para índices. Estratégias devem ter viés long no default.
- Earnings season (4x por ano) cria janelas previsíveis de aumento de volatilidade individual.
- Correlação intra-setor é alta — se NVDA está em Trending Down, AMD provavelmente também.
- After-hours e pre-market podem mudar o regime antes da sessão regular abrir (especialmente pós-earnings).
- Dividendos e buybacks criam fluxo comprador previsível em certas datas.
- Options expiration (OpEx) mensal e trimestral pode amplificar movimentos via gamma exposure.

**Ajustes para 1H:** atenção a padrões intraday específicos de equities: abertura volátil (primeiros 30min), almoço calmo, power hour (última hora). Esses padrões afetam qual regime é detectado em cada parte do dia.

**Ajustes para 1D:** MA(200) diária é o nível mais respeitado em equities. Cruzamento de preço pela MA(200) frequentemente sinaliza mudança de regime secular (bull → bear e vice-versa). Breadth indicators são fundamentais no diário de índices.

### FX (Câmbio)

**Regimes mais frequentes:** Mean-Reverting (câmbio é fortemente mean-reverting em muitos pares), Ranging, Trending (tendências de prazo mais longo alinhadas a ciclos de política monetária).

**Regimes menos frequentes:** Blow-off (raro em majors, possível em emergentes), Crisis (manifesta-se como currency crisis em emergentes).

**Particularidades:**

- FX opera 24h — não há gaps diários em dias úteis (exceto fim de semana). Isso torna o 1H mais limpo que em equities.
- Carry trade é um driver fundamental: moedas de alto yield vs baixo yield. Isso cria um viés direcional de longo prazo que não é puramente técnico.
- Intervenções de bancos centrais podem mudar o regime instantaneamente (ex: BoJ intervindo no USD/JPY). Esses eventos são impossíveis de prever mas identificáveis em real-time.
- Sessões (Tóquio, Londres, NY) têm personalidades diferentes: Tóquio = ranging, Londres = breakout/trending, NY = continuação ou reversão.
- Correlações entre pares são estruturais e previsíveis (EUR/USD e GBP/USD altamente correlacionados; USD/JPY e risco inversamente correlacionados).
- Volatilidade em FX é tipicamente menor que em equities — ATR como percentual do preço é muito menor. Ajustar sizing e stops proporcionalmente.

**Ajustes para 1H:** as 3 sessões são quase como 3 mercados diferentes. Recomendo detectar regime separadamente por sessão ou pelo menos usar a sessão como feature. Mean-reversion em torno da VWAP funciona excepcionalmente bem no 1H para FX.

**Ajustes para 1D:** tendências em FX no diário são frequentemente alinhadas a diferenciais de taxa de juros. Quando o regime é Trending em FX, verificar se é suportado por fundamentos macro (diferencial de juros, balança de pagamentos). Tendências fundamentais-alinhadas duram muito mais.

### Commodities

**Regimes mais frequentes:** Trending (tendências longas de superciclo), Ranging (quando oferta/demanda estão equilibradas), Volatile/Breakout (supply shocks).

**Regimes menos frequentes:** Mean-Reverting (exceto em spreads calendar), Blow-off (possível em energia e agro).

**Particularidades:**

- Supply shocks criam regimes únicos: Trending Up pode ser extremamente violento quando há escassez física (ex: petróleo em 2022, gás natural em picos de inverno).
- Sazonalidade é forte em muitas commodities (gás natural no inverno, grãos na época de plantio/colheita). A sazonalidade pode ser incorporada como feature moduladora do regime.
- Contango/Backwardation na curva de futuros é uma feature poderosa: backwardation forte sugere escassez (Trending Up ou Blow-off); contango forte sugere excesso (Trending Down ou Ranging).
- Estoque (inventories) é um fundamental key: queda de estoques + preço subindo = Trending Up com alta convicção.
- OPEC e decisões de produtores criam eventos similares a FOMC para energia.
- Limit up/limit down é mais comum em commodities que em equities.

**Ajustes para 1H:** commodities no 1H são fortemente influenciadas pela sessão. Energy (WTI, Brent) é mais ativo durante a sessão americana. Metais (ouro, prata) são mais ativos na sobreposição Londres-NY. Agro tem horários específicos de negociação.

**Ajustes para 1D:** dados de estoque semanais (EIA para petróleo, USDA para grãos) são os eventos mais impactantes no diário. Relatório COT (Commitment of Traders) semanal mostra posicionamento institucional e é muito útil para validar regimes.

### Crypto

**Regimes mais frequentes:** Choppy (muito do tempo), Blow-off (ciclos de bull run), Crisis/Risk-Off (crypto winters), Trending (em ambas as direções com alta volatilidade).

**Regimes menos frequentes:** Mean-Reverting (possível em stablecoins depegged ou pares de ratio), Low Vol (raro historicamente, mais comum conforme o mercado amadurece).

**Particularidades:**

- Opera 24/7/365 — sem fechamento, sem gaps (exceto em futuros de crypto na CME). Isso muda fundamentalmente como regimes são detectados no "diário" (qual timezone define o candle diário?).
- Volatilidade significativamente maior que qualquer outro asset class. ATR como percentual do preço pode ser 5-10x maior que em equities. Todos os thresholds de detecção precisam ser recalibrados.
- Blow-off / Euphoria é mais comum e mais extremo em crypto. Ciclos de 300-1000% de alta seguidos por 80-90% de queda são normais em ciclos de 4 anos (alinhados ao halving do Bitcoin).
- Correlação intra-crypto é altíssima (BTC domina). Quando BTC está em Crisis, 95% dos altcoins estão em Crisis mais severa.
- On-chain metrics são features únicas de crypto: hash rate, active addresses, exchange inflows/outflows, MVRV ratio, SOPR. Esses dados podem melhorar significativamente a detecção de regimes.
- Liquidez é fragmentada entre exchanges. Slippage e execução variam drasticamente entre plataformas.
- Funding rates em perpetual futures são indicadores de sentiment poderosos: funding positivo alto = muito long → risco de liquidação cascade (Crisis); funding negativo = muito short → risco de short squeeze (Breakout Up).

**Ajustes para 1H:** a ausência de fechamento torna o 1H uniforme ao longo do dia/noite. Porém, a liquidez varia por sessão (mais alta durante sobreposição EUA-Europa). Liquidation cascades são visíveis no 1H como candles de 10-20% de range — estes são o equivalente de Crisis no micro.

**Ajustes para 1D:** como não há fechamento oficial, recomendo usar UTC 00:00 como referência (padrão da maioria das exchanges). O "diário" em crypto é menos limpo que em equities porque não agrega uma sessão definida. Ciclos de crypto são mais longos (meses em trending, semanas em blow-off) mas as crises são mais rápidas (horas para crash de 30-50%).

### Tabela Comparativa entre Asset Classes

| Característica           | Equities                     | FX                  | Commodities        | Crypto                 |
| ------------------------ | ---------------------------- | ------------------- | ------------------ | ---------------------- |
| Regime mais frequente    | Trending Up                  | Mean-Reverting      | Trending           | Choppy                 |
| Viés estrutural          | Long (ERP)                   | Neutro              | Neutro             | Long (bull cycles)     |
| Volatilidade típica      | Média                        | Baixa               | Média-Alta         | Muito Alta             |
| Mean-reversion           | Fraca (em ações individuais) | Forte               | Média (em spreads) | Fraca                  |
| Crisis speed             | Dias-Semanas                 | Horas-Dias          | Dias               | Horas                  |
| Blow-off frequency       | Raro (setores/temas)         | Muito raro (majors) | Ocasional (energy) | Frequente (cada ciclo) |
| Sazonalidade             | Fraca (sell in May)          | Fraca               | Forte              | Fraca (halving cycles) |
| Dados fundamentais úteis | Earnings, breadth            | Taxas de juros, BoP | Estoques, produção | On-chain metrics       |
| Horário de operação      | 6.5h/dia                     | 24h/5 dias          | 6-23h/dia          | 24/7                   |

---

## Correlação entre Regimes de Múltiplos Ativos

Quando múltiplos ativos são monitorados simultaneamente, a combinação de regimes entre eles gera informação adicional que não está disponível olhando cada ativo isoladamente.

### Princípio: Coerência vs Divergência

**Regimes coerentes** entre ativos correlacionados reforçam a convicção. **Regimes divergentes** sinalizam stress ou oportunidade.

### Pares de Monitoramento Essenciais

**Equity + VIX:**

| SPX Regime    | VIX Regime          | Interpretação                                     | Convicção         |
| ------------- | ------------------- | ------------------------------------------------- | ----------------- |
| Trending Up   | Trending Down       | Coerente — rally saudável                         | Alta              |
| Trending Up   | Ranging/Low Vol     | Coerente — complacência (cuidado se excessiva)    | Média-Alta        |
| Trending Up   | Trending Up         | DIVERGENTE — risco oculto subindo apesar do rally | Baixa (reduzir)   |
| Trending Down | Trending Up         | Coerente — sell-off com medo                      | Alta (para short) |
| Ranging       | Low Vol             | Coerente — mercado dormindo                       | Média             |
| Recovery      | Trending Down (VIX) | Coerente — medo dissipando                        | Alta              |
| Distribution  | Low Vol (VIX)       | Perigoso — complacência no topo                   | Muito Baixa       |

**Equity + Credit (HYG/JNK):**

| SPX Regime  | HYG Regime    | Interpretação                                            |
| ----------- | ------------- | -------------------------------------------------------- |
| Trending Up | Trending Up   | Coerente — risk-on amplo                                 |
| Trending Up | Trending Down | DIVERGENTE — crédito não confirma; risco de reversão     |
| Trending Up | Distribution  | ALERTA — smart money saindo de crédito antes de equities |
| Crisis      | Crisis        | Coerente — contágio pleno                                |
| Recovery    | Trending Up   | Coerente — crédito liderando a recuperação (bullish)     |
| Recovery    | Ranging       | Crédito ainda cético — recovery frágil                   |

**USD + Emerging Markets:**

| DXY Regime         | EEM Regime    | Interpretação                                                             |
| ------------------ | ------------- | ------------------------------------------------------------------------- |
| Trending Up        | Trending Down | Coerente — USD forte pressiona emergentes                                 |
| Trending Down      | Trending Up   | Coerente — USD fraco beneficia emergentes                                 |
| Trending Up        | Trending Up   | DIVERGENTE — emergentes subindo apesar do USD forte; momentum muito forte |
| Crisis (DXY spike) | Crisis        | Coerente — flight to quality                                              |

**Treasuries + Equities:**

| TLT Regime    | SPX Regime    | Interpretação                                                        |
| ------------- | ------------- | -------------------------------------------------------------------- |
| Trending Up   | Trending Down | Coerente — flight to quality clássico                                |
| Trending Up   | Trending Up   | Risk-on com queda de yields — cenário Goldilocks                     |
| Trending Down | Trending Down | PERIGOSO — stocks e bonds caindo juntos (stagflation, taper tantrum) |
| Trending Down | Trending Up   | Reflação — yields subindo por crescimento forte                      |

### Índice de Coerência do Portfólio

Proposta de métrica: **Regime Coherence Index (RCI)**

Para um conjunto de N ativos monitorados:

1. Para cada par de ativos, verificar se a combinação de regimes é "coerente" (score 1), "neutra" (score 0), ou "divergente" (score -1).
2. RCI = média dos scores de todos os pares.

**Interpretação:**

- RCI > 0.5: alta coerência. Regimes se confirmam mutuamente. Convicção alta em posições.
- RCI 0 a 0.5: coerência moderada. Alguns sinais conflitantes. Sizing normal.
- RCI < 0: divergência dominante. Algo está "errado" no mercado. Reduzir exposição geral, aumentar hedge.

### Cross-Asset Regime Signals

Alguns padrões cross-asset são sinais de regime poderosos:

**Tudo sobe junto (equities, commodities, credit, EM):** regime global = Risk-On/Recovery. Alta convicção em long beta.

**Tudo cai junto (exceto USD e Treasuries):** regime global = Crisis/Risk-Off. Alta convicção em hedge/cash.

**Equities sobem mas credit cai:** Distribution avançada. Smart money saindo. Reduzir long equities.

**Commodities em Blow-off com equities em Distribution:** risco de estagflação. Regime mais perigoso para portfólios long-only.

**VIX em Low Vol com equities em Trending Up:** complacência. Comprar puts baratas como seguro (vol implícita está baixa = proteção barata).

**Gold em Trending Up com Treasuries em Trending Up com equities em Trending Up:** sinal confuso — alguém está errado. Tipicamente indica incerteza sobre o caminho futuro (inflação vs deflação). Sizing reduzido até resolução.

---

## Backtest Framework Template

Estrutura para avaliar se a detecção de regime está adicionando valor e para otimizar parâmetros por regime.

### Métricas a Calcular por Regime

**Performance metrics:**

| Métrica                               | O que mede                                | Target                                                                   |
| ------------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------ |
| Sharpe Ratio por regime               | Retorno ajustado ao risco em cada regime  | > 0.5 em regimes "operáveis"                                             |
| Win Rate por regime                   | % de trades lucrativos por regime         | > 55% em trending, > 50% em mean-reversion                               |
| Profit Factor por regime              | Lucro bruto / Perda bruta                 | > 1.5                                                                    |
| Average Win / Average Loss por regime | Payoff ratio                              | > 1.0 em trending, pode ser < 1.0 em mean-reversion se win rate compensa |
| Max Drawdown por regime               | Pior sequência de perdas dentro do regime | Menor que o lucro esperado do regime                                     |
| Max Consecutive Losses por regime     | Pior sequência de losses                  | Calibrar stops e sizing para sobreviver a 2x este valor                  |
| Holding Period médio por regime       | Duração média de cada trade               | Deve ser coerente com a duração esperada do regime                       |
| % do tempo em cada regime             | Distribuição de tempo entre regimes       | Verificar se é coerente com o esperado                                   |

**Regime detection metrics:**

| Métrica              | O que mede                                           | Target                           |
| -------------------- | ---------------------------------------------------- | -------------------------------- |
| Latência de detecção | Quantos períodos para detectar mudança de regime     | < 5 períodos no 1H, < 3 no 1D    |
| False positive rate  | % de detecções que estavam erradas                   | < 20%                            |
| Regime stability     | Duração média de cada regime atribuído               | > 5 períodos (evitar flickering) |
| Transition accuracy  | % de transições previstas que ocorreram corretamente | > 60%                            |

### Estrutura do Backtest

**Step 1: Baseline (sem regime detection)**

- Executar a estratégia com parâmetros fixos (mesmo sizing, mesmo stop, mesma lógica) para todo o período.
- Esta é a linha base contra a qual o regime-conditioned vai ser comparado.

**Step 2: Regime-conditioned**

- Mesmo período, mas com sizing, stops e lógica ajustados por regime.
- Comparar: Sharpe, Max DD, Calmar ratio, % no mercado (tempo investido).

**Step 3: Análise por regime**

- Quebrar o P&L por regime: quanto cada regime contribuiu para o resultado total?
- Identificar regimes onde a estratégia perde dinheiro consistentemente (provavelmente deveria ficar flat nesses).
- Identificar regimes onde a estratégia tem melhor performance (talvez aumentar sizing).

**Step 4: Análise de transição**

- Quanto P&L é perdido nas transições de regime? (tipicamente o maior custo).
- Qual é a latência de detecção e quanto isso custa?
- Se reduzir a latência em 1 período, quanto melhora o P&L?

**Step 5: Walk-forward validation**

- NUNCA otimizar parâmetros no mesmo período do teste.
- Usar rolling window: treinar em 2 anos, testar em 6 meses, rolar.
- Verificar estabilidade dos parâmetros ótimos entre janelas.

### Template de Relatório de Backtest

```
=== REGIME-CONDITIONED BACKTEST REPORT ===
Período: [data_inicio] a [data_fim]
Ativo(s): [lista]
Timeframe: [1H / 1D]
Modelo de regime: [HMM / XGBoost / etc]

--- PERFORMANCE GERAL ---
Sharpe (baseline):          [X.XX]
Sharpe (regime-conditioned): [X.XX]
Melhoria:                   [+XX%]
Max DD (baseline):          [-XX%]
Max DD (regime-conditioned): [-XX%]
Calmar (baseline):          [X.XX]
Calmar (regime-conditioned): [X.XX]
% tempo investido (baseline): [XX%]
% tempo investido (regime):   [XX%]

--- PERFORMANCE POR REGIME ---
Regime        | % Tempo | Sharpe | Win% | PF   | Avg Win/Loss | Max DD
Trending Up   | XX%     | X.XX   | XX%  | X.XX | X.XX         | -XX%
Trending Down | XX%     | X.XX   | XX%  | X.XX | X.XX         | -XX%
[...]

--- CONTRIBUIÇÃO POR REGIME (% do P&L total) ---
Trending Up:    +XX%
Mean-Reverting: +XX%
Choppy:         -XX% (deveria ficar flat?)
[...]

--- TRANSIÇÕES ---
Latência média de detecção: [X.X] períodos
Custo estimado de latência:  [XX bps por transição]
Transições totais:          [N]
Transições corretas:        [N] (XX%)

--- RECOMENDAÇÕES ---
[Baseadas nos dados acima]
```

### Pitfalls Comuns em Backtesting de Regimes

**Lookahead bias:** o regime é detectado com informação futura? Verificar que o modelo usa apenas dados disponíveis no momento da decisão. Isso é especialmente insidioso em HMM onde o smoothing usa dados futuros — usar apenas o filtered estimate, não o smoothed.

**Overfitting de regimes:** com 14 regimes e múltiplos parâmetros por regime, o espaço de otimização é enorme. Risco alto de overfitting. Mitigar: usar poucos parâmetros por regime (máximo 3-4), validação walk-forward, e verificar que os resultados fazem sentido econômico.

**Survivorship bias:** se o regime detection evitou uma crise histórica específica (ex: COVID), o backtest vai parecer incrível. Verificar: a detecção funcionou em múltiplas crises, não apenas em uma? Remove a crise específica do backtest e veja se o sistema ainda funciona.

**Transaction cost sensitivity:** regime-conditioned trading tem mais transições (mudanças de sizing, stops, etc). Verificar que os custos de transação não consomem o alpha gerado pela detecção de regime. Particularmente importante no 1H.

---

## Regime Duration Distributions

Entender a distribuição de duração de cada regime (não apenas a média) permite estimar a probabilidade de transição dado que o regime já dura X períodos.

### Distribuição Teórica

A maioria dos regimes de mercado segue aproximadamente uma **distribuição geométrica** ou **log-normal** de duração:

- Muitas ocorrências curtas e poucas ocorrências longas.
- A moda (valor mais comum) é menor que a média.
- A cauda direita (durações longas) é gorda — regimes podem durar muito mais que o esperado.

### Estimativas de Duração por Regime e Timeframe

**1H (em barras horárias):**

| Regime         | P10 | P25 | Mediana | P75 | P90 | Notas                                               |
| -------------- | --- | --- | ------- | --- | --- | --------------------------------------------------- |
| Trending Up    | 6   | 12  | 24      | 48  | 80  | Pode durar dias se alinhado com diário              |
| Trending Down  | 5   | 10  | 20      | 40  | 65  | Mais curto que Trending Up (assimetria)             |
| Ranging        | 4   | 8   | 12      | 24  | 40  | Muito comum; frequentemente interrompido por sessão |
| Mean-Reverting | 3   | 6   | 10      | 18  | 30  | Duração ligada à half-life                          |
| Low Vol        | 3   | 5   | 8       | 15  | 25  | Resolve tipicamente na troca de sessão              |
| Breakout       | 1   | 2   | 4       | 8   | 14  | Curto — ou vira trending ou falha                   |
| Choppy         | 4   | 8   | 12      | 20  | 35  | Tende a durar mais que o trader aguenta             |
| Crisis         | 6   | 10  | 16      | 30  | 50  | Pode parecer eterno no momento                      |
| Recovery       | 8   | 16  | 24      | 48  | 80  | Gradual, pode durar semanas                         |
| Distribution   | 8   | 12  | 20      | 35  | 55  | Processo lento                                      |
| Accumulation   | 8   | 14  | 20      | 35  | 55  | Processo lento                                      |
| Blow-off       | 2   | 4   | 8       | 14  | 22  | Curto e violento                                    |

**1D (em dias úteis):**

| Regime         | P10 | P25 | Mediana | P75 | P90 | Notas                                         |
| -------------- | --- | --- | ------- | --- | --- | --------------------------------------------- |
| Trending Up    | 8   | 15  | 30      | 60  | 120 | Pode durar trimestres                         |
| Trending Down  | 6   | 12  | 25      | 50  | 90  | Mais rápido que Trending Up                   |
| Ranging        | 3   | 5   | 10      | 18  | 30  | Frequente entre earnings                      |
| Mean-Reverting | 4   | 7   | 12      | 20  | 35  | Alinhado à half-life                          |
| Low Vol        | 3   | 5   | 8       | 14  | 22  | Pode comprimir por semanas                    |
| Breakout       | 1   | 2   | 3       | 5   | 8   | Transição rápida para trending                |
| Choppy         | 3   | 5   | 8       | 14  | 22  | Frequentemente em torno de FOMC               |
| Crisis         | 3   | 5   | 8       | 15  | 25  | Crises agudas: 5-10 dias; sistêmicas: semanas |
| Recovery       | 8   | 15  | 25      | 45  | 80  | Meses                                         |
| Distribution   | 5   | 10  | 18      | 30  | 50  | Semanas a meses no topo                       |
| Accumulation   | 5   | 10  | 18      | 30  | 50  | Semanas a meses no fundo                      |
| Blow-off       | 2   | 4   | 7       | 12  | 18  | Dias a semanas                                |

**Nota importante:** estes valores são estimativas baseadas em comportamento típico de índices de equities (S&P 500 e similares). Para FX, commodities e crypto, ajustar conforme as notas da seção de Asset-Class.

### Hazard Rate (Taxa de Risco de Transição)

A hazard rate h(t) responde à pergunta: "dado que o regime já dura t períodos, qual a probabilidade de transição no próximo período?"

**Para distribuição geométrica (memoryless):** h(t) = constante. A probabilidade de transição é a mesma independente de quanto tempo o regime já dura.

**Para distribuição com aging (mais realista):** h(t) aumenta com t. Quanto mais tempo o regime dura, mais provável é a transição.

**Aplicação prática:**

```
h(t) = h_base × (1 + α × max(0, t - T_median) / T_median)
```

Onde:

- h_base = probabilidade base de transição por período (ex: 0.05 = 5% por barra).
- α = fator de aging (0 = sem aging / geométrica; 1 = aging moderado; 2 = aging forte).
- T_median = duração mediana do regime.

Quando h(t) ultrapassa um threshold (ex: 0.3), ativar alerta de transição iminente e começar a reduzir exposição.

### Uso Prático

**Sizing dinâmico baseado em duração:** `sizing(t) = sizing_base × (1 - h(t))`. Conforme a probabilidade de transição aumenta, o sizing diminui naturalmente.

**Alerta de overstay:** se o regime já dura mais que o P90 da distribuição histórica, a probabilidade de transição é muito alta. Considerar tratar como NoLabel independente do que o modelo diz.

---

## Journal / Logging Template

Registrar sistematicamente as decisões regime-condicionadas é essencial para calibrar tanto o modelo quanto o trader.

### Template de Log por Trade

```
=== TRADE LOG ===
ID: [auto-incremento]
Data/Hora Entrada: [YYYY-MM-DD HH:MM]
Data/Hora Saída:   [YYYY-MM-DD HH:MM]
Ativo:             [ticker]
Timeframe:         [1H / 1D]
Direção:           [Long / Short / Hedge]

--- CONTEXTO DE REGIME ---
Regime 1D (entrada):     [nome + confidence score]
Regime 1H (entrada):     [nome + confidence score]
Regime 1D (saída):       [nome + confidence score]
Regime 1H (saída):       [nome + confidence score]
Conflito entre TFs?      [Sim/Não — qual?]
Regime Coherence Index:  [X.XX]
Evento macro próximo?    [Sim/Não — qual? Tier?]

--- DECISÃO ---
Sizing aplicado:         [XX% do máximo]
Tipo de stop usado:      [estrutural / z-score / trailing / temporal]
Stop price:              [preço]
Target price:            [preço]
Razão de entrada:        [texto livre — por que entrou?]
Setup/pattern:           [pullback to EMA / breakout / spring / etc]
Convicção (1-5):         [subjetivo]

--- RESULTADO ---
P&L bruto:               [$XX.XX]
P&L líquido:             [$XX.XX] (depois de custos)
P&L em R (múltiplo do risco inicial): [X.XX R]
Duração do trade:        [X barras / X dias]
Stop ajustado durante?   [Sim/Não — como?]
Saída por:               [stop / target / trailing / mudança de regime / evento / discricionária]

--- AVALIAÇÃO PÓS-TRADE ---
O regime estava correto?       [Sim / Não / Parcialmente]
A transição foi prevista?      [Sim / Não / Não houve transição]
O sizing foi adequado?         [Sim / Subdimensionado / Superdimensionado]
O stop foi adequado?           [Sim / Muito apertado / Muito largo]
O que faria diferente?         [texto livre]
Regime detection accuracy:     [Correto / Atrasado por X barras / Errado]
Lição aprendida:               [texto livre]
```

### Template de Log Diário

```
=== DAILY REGIME LOG ===
Data: [YYYY-MM-DD]

--- ESTADO DO PORTFÓLIO ---
Exposição total:         [XX% long / XX% short / XX% cash]
Número de posições:      [N]
P&L do dia:              [$XX.XX] (XX%)
Drawdown corrente:       [-XX%] do pico

--- REGIMES ATIVOS (1D) ---
[Ativo 1]: [Regime] (confidence: X.XX, duração: X dias)
[Ativo 2]: [Regime] (confidence: X.XX, duração: X dias)
[...]
Regime Coherence Index:  [X.XX]

--- TRANSIÇÕES HOJE ---
[Ativo X]: [Regime A] → [Regime B] (às HH:MM)
Ação tomada: [o que fez em resposta]

--- EVENTOS MACRO ---
Eventos de hoje:         [lista]
Impacto observado:       [descrição]
Override aplicado?       [Sim/Não]

--- NOTAS ---
[observações gerais, anomalias, insights]
```

### Template de Review Semanal

```
=== WEEKLY REGIME REVIEW ===
Semana: [YYYY-WNN]

--- PERFORMANCE ---
P&L semanal:             [$XX.XX] (XX%)
Trades realizados:       [N]
Win rate semanal:        [XX%]
Melhor trade:            [Ativo, regime, P&L]
Pior trade:              [Ativo, regime, P&L]

--- REGIME DETECTION ACCURACY ---
Regimes atribuídos esta semana:     [N]
Regimes que pareciam corretos:      [N] (XX%)
Transições detectadas:              [N]
Transições corretas:                [N] (XX%)
Latência média de detecção:         [X barras]

--- PADRÕES OBSERVADOS ---
[Quais regimes dominaram esta semana?]
[Algum ativo mudou de regime de forma inesperada?]
[Cross-asset coherence: coerente ou divergente?]

--- AJUSTES PARA PRÓXIMA SEMANA ---
[Threshold de confiança precisa de ajuste?]
[Sizing estava adequado por regime?]
[Stops estavam calibrados corretamente?]
[Eventos macro da próxima semana e plano de override]
```

### Automação do Logging

Recomendo automatizar o máximo possível:

- Regime atual e confidence score → gerado automaticamente pelo modelo.
- Entrada/saída de trades → capturado do execution system.
- P&L e métricas → calculados automaticamente.
- O que NÃO deve ser automatizado: avaliação pós-trade, lições aprendidas, notas. Esses campos forçam o trader a refletir e são onde acontece o aprendizado real.

---

## False Signal Catalog

Lista dos falsos positivos e erros de classificação mais comuns, organizados por regime, com filtros para evitá-los.

### Falsos Positivos por Regime

#### Falso Trending (classificado como Trending mas não é)

**Cenário 1: ADX alto em Choppy.**
O ADX pode subir quando há movimentos bruscos em ambas as direções, não apenas em tendência. Um sell-off seguido de rally gera ADX alto sem direcionalidade sustentada.
**Filtro:** exigir que +DI e -DI estejam divergindo (um subindo e outro descendo). Se ambos estão altos, é choppy, não trending. Verificar também R² da regressão — trending real tem R² > 0.6.

**Cenário 2: Momentum pós-earnings confundido com tendência.**
Um gap de 10% pós-earnings pode parecer "trending" para o modelo, mas é um evento discreto, não uma tendência sustentada.
**Filtro:** se o movimento está concentrado em 1-2 candles com gap, classificar como Breakout, não Trending. Exigir follow-through de pelo menos 3-5 candles para confirmar Trending.

**Cenário 3: Tendência em timeframe curto dentro de range longo.**
No 1H, o preço pode "trendar" por 8-12 horas (toda uma sessão) mas no contexto do diário estar simplesmente oscilando dentro de uma range.
**Filtro:** cross-check com regime do 1D. Se 1D = Ranging, trending no 1H é suspeito.

#### Falso Mean-Reverting (classificado como Mean-Reverting mas não é)

**Cenário 1: Início de trending confundido com mean-reversion.**
Nos primeiros períodos de uma nova tendência, o preço se afasta da média e pode parecer "mean-reverting" (o modelo espera que volte). Se o trader entra contra a tendência, perde.
**Filtro:** verificar Hurst exponent — se está cruzando 0.5 de baixo para cima, a série está passando de anti-persistente para persistente. Não entrar contra o movimento até que o Hurst volte abaixo de 0.45.

**Cenário 2: Mean-reversion em ativo com shift fundamental.**
Uma ação que perdeu 30% por mudança fundamental (perda de contrato, fraude, etc) não vai mean-revertar para o preço antigo. O "valor justo" mudou.
**Filtro:** verificar se houve evento fundamental (earnings miss, notícia). Se o gap > 5% com volume > 3x a média, desativar mean-reversion para aquele ativo por pelo menos 20 períodos.

**Cenário 3: ADF falso positivo em série com quebra estrutural.**
O teste ADF pode rejeitar a hipótese de unit root falsamente se há uma quebra estrutural (mudança de nível) na série.
**Filtro:** usar ADF com rolling window (não na série inteira). Verificar com teste KPSS (que testa a hipótese inversa). Se ADF rejeita mas KPSS também rejeita, o resultado é inconclusivo.

#### Falso Breakout (classificado como Breakout mas não é)

**Cenário 1: Breakout em horário de baixa liquidez.**
"Breakouts" durante a sessão asiática em ativos europeus ou americanos frequentemente são falsos — não há volume para sustentar o movimento.
**Filtro:** normalizar volume pelo horário do dia. Um breakout só é válido se o volume normalizado > 1.5x.

**Cenário 2: Breakout por stop hunting.**
Market makers ou grandes players podem forçar o preço acima de um nível de resistência para acionar stops de short sellers, e depois o preço reverte.
**Filtro:** observar o comportamento pós-breakout. Se o preço rompe com sombra longa (wick) e o corpo do candle está de volta dentro da range, é provável stop hunt. Esperar fechamento acima do nível para confirmar.

**Cenário 3: Breakout pré-evento macro.**
Breakout 1-2 horas antes de FOMC ou CPI é quase sempre ruído (traders se posicionando especulativamente).
**Filtro:** se hours_to_tier1_event < 4, desabilitar sinais de breakout.

#### Falsa Crisis (classificado como Crisis mas não é)

**Cenário 1: Flash crash de liquidez.**
Queda súbita de 3-5% em minutos causada por erro de ordem ou liquidez extremamente baixa (ex: flash crash de 2010, ETF flash crashes). O preço se recupera em minutos/horas.
**Filtro:** se o drawdown > 3% em < 30 minutos E o volume não é sustentadamente alto, pode ser flash crash e não crise real. Esperar 1-2 horas para confirmar. Crises reais não se recuperam imediatamente.

**Cenário 2: Sell-off setorial confundido com crise sistêmica.**
Um setor pode cair 5-10% por razões específicas (regulação, earnings miss coletivo) enquanto o mercado amplo está estável.
**Filtro:** verificar correlação cross-sector. Se apenas 1-2 setores estão caindo e VIX não está em spike, é sell-off setorial, não crise. Breadth é o melhor indicador.

**Cenário 3: Ajuste de posicionamento em fim de trimestre.**
Rebalanceamentos institucionais no fim de trimestre podem gerar sell-offs técnicos que parecem sistêmicos.
**Filtro:** contexto de calendário. Se a queda coincide com fim de trimestre e os indicadores de stress (VIX, spreads de crédito) não estão confirmando, provavelmente é rebalanceamento.

#### Falsa Recovery (classificado como Recovery mas é Dead Cat Bounce)

**Cenário 1: Bounce técnico em oversold extremo.**
Após queda de 20%, um bounce de 5% é normal (short covering + bottom fishing). Não é recovery.
**Filtro:** recovery genuína tem VIX caindo e spreads de crédito melhorando junto. Se VIX está flat ou subindo durante o bounce, é dead cat bounce.

**Cenário 2: Rally de alívio por notícia temporária.**
"Fed considerando corte de emergência" pode gerar rally de 3% que reverte em dias quando a ação real não materializa.
**Filtro:** verificar se o catalisador é estrutural (ação concreta tomada) ou especulativo (declaração, rumor). Rally por ação concreta é mais sustentável.

**Cenário 3: Short squeeze sem demanda real.**
Short interest alto + notícia positiva = short squeeze violento. Pode parecer recovery mas é puramente mecânico.
**Filtro:** verificar short interest e dias para cobrir. Se o rally coincide com queda abrupta no short interest, é squeeze, não recovery orgânica. A recovery deve ser acompanhada por melhora em fundamentos (spreads, earnings expectations, guidance).

#### Falsa Distribution (classificado como Distribution mas é Pausa Saudável)

**Cenário 1: Consolidação normal dentro de uptrend.**
Todo trending up tem períodos de consolidação. Divergência de RSI por 3-5 dias pode ser apenas uma pausa antes da próxima perna de alta.
**Filtro:** verificar breadth. Se a breadth se mantém forte durante a "distribuição", provavelmente é pausa saudável. Distribution genuína tem breadth deteriorando. Exigir pelo menos 2-3 semanas de divergência no diário para confirmar.

**Cenário 2: Rotação setorial confundida com distribution.**
O índice pode ficar flat enquanto há rotação de tech para industrials. Isso não é distribution — é reciclagem.
**Filtro:** verificar se a advance-decline line está saudável. Se o número de ações subindo se mantém estável apesar do índice flat, é rotação, não distribution.

#### Falsa Accumulation (classificado como Accumulation mas é Pausa antes de mais Queda)

**Cenário 1: Bear flag / consolidação bearish.**
O preço pode consolidar por 1-2 semanas em downtrend antes de outra perna de queda. Parece accumulation mas é apenas pausa.
**Filtro:** volume no "bounce" deve ser menor que volume na queda anterior. Se o bounce tem volume alto, pode ser acumulação genuína. Se o volume é baixo, é provavelmente bear flag.

**Cenário 2: Suporte técnico temporário antes de quebra.**
Um nível de suporte importante (ex: MA(200) diária) pode segurar o preço temporariamente, criando aparência de acumulação. Se o suporte eventualmente cede, a queda acelera.
**Filtro:** observar a reação a cada teste. Se cada teste tem volume decrescente e o bounce pós-teste é menor, o suporte está enfraquecendo. Acumulação genuína mostra bounces progressivamente maiores.

### Checklist Anti-False Signal

Antes de agir sobre qualquer regime detectado, verificar:

1. **O regime é coerente entre timeframes?** (1H e 1D concordam?)
2. **O regime é coerente entre ativos correlacionados?** (cross-asset check)
3. **Há evento macro próximo que pode invalidar o sinal?** (event override check)
4. **O regime já dura além do P90 da distribuição histórica?** (duration check)
5. **O confidence score está acima de 0.6?** (model confidence check)
6. **O volume confirma?** (quase todo falso sinal tem volume inconsistente)
7. **O horário do dia é favorável?** (sessão de alta liquidez vs baixa liquidez, especialmente no 1H)

Se mais de 2 respostas forem "não" ou "incerto", tratar o regime como NoLabel até obter confirmação adicional.
