# Market Regimes — Baseadas em Papers Acadêmicos

Seções adicionais para integrar ao documento principal. Extraídas e sintetizadas a partir de quatro papers recentes sobre regime-switching, machine learning aplicado a regimes, reinforcement learning em trading e detecção de regimes via mixture models. Todas as seções mantêm foco operacional e incluem perspectivas para Bitcoin/crypto.

---

## Modelos de Detecção de Regime — Aprofundamento

A seção original de "Considerações de Implementação" lista HMMs, Random Forests, GMMs e Hamilton como opções. Esta seção expande significativamente essa discussão com fundamentação teórica e detalhes práticos de implementação, incorporando insights da literatura recente.

### Markov-Switching Models (MS) — Fundamentação Formal

Os modelos Markov-Switching, formalizados por Hamilton (1989), são a espinha dorsal da literatura de detecção de regimes. A ideia central é que uma variável latente (não observável) segue uma cadeia de Markov de primeira ordem e governa os parâmetros do processo gerador de dados observado — tipicamente retornos ou volatilidade de um ativo.

**Estrutura formal:** o modelo assume K regimes discretos. Em cada regime k, os retornos seguem uma distribuição com parâmetros específicos (μ_k, σ_k). A transição entre regimes é governada por uma matriz de probabilidades de transição P, onde p_ij = P(S_t = j | S_{t-1} = i). A estimação é feita via máxima verossimilhança usando o filtro de Hamilton, que calcula a probabilidade filtrada P(S_t = k | Y_1, ..., Y_t) a cada período.

**Saída do modelo:** para cada período t, o modelo fornece um vetor de probabilidades sobre os K regimes. Isso é diretamente utilizável como input para sizing — em vez de um label binário "estamos em regime X", você obtém "probabilidade de 72% de Trending Up, 20% de Distribution, 8% de Choppy", o que permite sizing proporcional à convicção.

**Vantagens para o framework:**

- Captura transições entre regimes de forma probabilística, alinhado com a filosofia de que regimes não mudam abruptamente (zona de NoLabel como transição).
- A matriz de transição estimada pode ser comparada diretamente com a Matriz de Transição qualitativa do documento principal, servindo como validação empírica.
- A duração média de cada regime é derivável da matriz P: duração esperada do regime k = 1 / (1 - p_kk). Isso fornece estimativas quantitativas para a coluna "Duração 1H / Duração 1D" da tabela de Referência Rápida.

**Limitação principal:** o número de regimes K precisa ser especificado a priori. O documento principal define 14 regimes, o que é excessivo para um MS padrão (problemas de convergência e overfitting). A solução é usar MS para um nível macro (2-4 estados: expansão, contração, crise, transição) e classificadores supervisionados para o nível fino (trending up vs down, distribution vs accumulation, etc.).

**Especificidade para Bitcoin:** Bitcoin opera 24/7 sem gaps de overnight, o que é uma vantagem para MS — não há descontinuidades de sessão que complicam a estimação em equities. Por outro lado, a distribuição de retornos do Bitcoin tem caudas significativamente mais pesadas que equities, o que exige o uso de distribuições t (não Gaussianas) nas emissões de cada regime.

### T-Distributed Mixture Models + GARCH

Uma abordagem recente da State Street (Ung, 2025) propõe um framework alternativo aos HMMs tradicionais: mixture models com distribuição t integrados com GARCH para capturar volatility clustering. Esse modelo foi aplicado a 23 séries de retorno e incerteza para identificar regimes no mercado americano de 1995 a 2024.

**Por que distribuição t em vez de Gaussiana:** dados financeiros, especialmente crypto, apresentam caudas pesadas e eventos extremos que são mal capturados pela distribuição normal. A distribuição t tem um parâmetro de graus de liberdade (ν) que controla a espessura das caudas. Quando ν é baixo (3-5), a distribuição acomoda retornos extremos sem tratá-los como outliers. Para Bitcoin, onde retornos diários de ±10% não são incomuns, a distribuição t é significativamente mais adequada.

**Integração com GARCH:** mercados financeiros exibem volatility clustering — períodos de alta volatilidade tendem a ser seguidos por mais alta volatilidade. GARCH modela esse fenômeno, ajustando dinamicamente a variância condicional. A combinação t-mixture + GARCH permite que o modelo capture tanto as diferenças estruturais entre regimes (via mixture) quanto a evolução temporal da volatilidade dentro de cada regime (via GARCH). Isso é particularmente relevante para os regimes de Low Vol → Breakout, onde a volatilidade muda de forma abrupta.

**Resultados de validação:** o modelo identificou 4 regimes — Emerging Expansion (42% do tempo), Robust Expansion (25%), Cautious Decline (19%) e Market Turmoil (13%). A validação contra os piores drawdowns do S&P 500 produziu F1 score de ~73% para os 10 piores drawdowns e ~78% para os 5 piores. Esses números servem como benchmark realista para validação do nosso classificador.

**Mapeamento para nossa taxonomia:**

| Regime State Street         | Regimes equivalentes na taxonomia | Prevalência |
| --------------------------- | --------------------------------- | ----------- |
| Emerging Expansion          | Recovery → Trending Up (início)   | 42%         |
| Robust Expansion            | Trending Up (maduro), Blow-off    | 25%         |
| Cautious Decline            | Distribution, Trending Down leve  | 19%         |
| Market Turmoil              | Crisis / Risk-Off                 | 13%         |

**Implementação prática:**

```python
# Pseudocódigo conceitual
from sklearn.mixture import BayesianGaussianMixture
from arch import arch_model

# 1. Pré-processar: remover efeitos de vol time-varying via GARCH
garch = arch_model(returns, vol='Garch', p=1, q=1, dist='t')
garch_fit = garch.fit()
standardized_returns = returns / garch_fit.conditional_volatility

# 2. Aplicar mixture model nos retornos padronizados
# (Na prática, usar implementação com distribuição t,
#  não Gaussiana — ex: pomegranate, hmmlearn com customização)
mixture = BayesianGaussianMixture(n_components=4,
                                    covariance_type='full',
                                    max_iter=500)
regime_labels = mixture.fit_predict(feature_matrix)
regime_probs = mixture.predict_proba(feature_matrix)
```

**Nota:** a implementação real requer cuidado com a escolha de features (retornos + medidas de incerteza), pré-processamento (residualização para isolar fatores comuns, scaling robusto para evitar que uma feature domine), e seleção do número de componentes via critérios como AIC/BIC.

### Threshold Models e Smooth Transition (TAR / STAR)

Uma classe alternativa de modelos de regime-switching onde a transição não é governada por uma variável latente (como nos MS), mas por uma variável observável que cruza um limiar (threshold).

**Self-Exciting Threshold Autoregressive (TAR):** o regime muda quando o valor defasado da própria série cruza um threshold estimado. Exemplo concreto para nossa taxonomia: se o retorno acumulado de 20 dias cruza zero de cima para baixo, o regime transita de Trending Up para Ranging ou Trending Down. A vantagem é a interpretabilidade total — o gatilho de transição é observável e verificável.

**Smooth Transition Autoregressive (STAR):** generalização do TAR que permite transições graduais entre regimes, usando uma função logística (LSTAR) ou exponencial (ESTAR) como peso de transição. Em vez de saltar de regime A para regime B quando a variável cruza o threshold, o modelo calcula um peso w(t) ∈ [0, 1] que indica "quanto" do regime A vs regime B está ativo.

**Relevância para o framework:** o modelo STAR é filosoficamente alinhado com o conceito de NoLabel como zona de transição. Em vez de classificar cada período como pertencendo a um regime discreto, o STAR produz uma mistura contínua. Isso resolve o problema de transições ruidosas: quando o ADX está em 23 (abaixo de 25 = Ranging, acima = Trending), o STAR não força uma escolha binária — calcula uma probabilidade suave de cada regime.

**Implementação para detecção de regime:**

O modelo STAR usa uma variável de transição z_t (por exemplo, ADX, retorno acumulado, Hurst exponent) e uma função de transição:

```
G(z_t; γ, c) = 1 / (1 + exp(-γ(z_t - c)))
```

Onde γ controla a velocidade da transição (γ alto ≈ threshold abrupto, γ baixo ≈ transição suave) e c é o threshold. Os parâmetros do modelo em cada período são uma combinação ponderada dos parâmetros dos dois regimes:

```
y_t = (1 - G(z_t)) × [modelo_regime_A] + G(z_t) × [modelo_regime_B]
```

**Aplicação concreta:** usar ADX como variável de transição entre Ranging (ADX < 20) e Trending (ADX > 30), com transição suave na zona 20-30. Isso elimina o problema de sinais instáveis quando o ADX oscila em torno de 25 — em vez de trocar de regime a cada candle, o modelo gradualmente transfere peso.

**Para Bitcoin:** a alta volatilidade do Bitcoin torna os thresholds mais difíceis de calibrar. Recomendo estimar thresholds de forma adaptativa (rolling, com janela de 100-200 períodos) em vez de fixos, porque a estrutura de volatilidade do Bitcoin muda significativamente entre ciclos (halving cycles, adoption waves).

### Reinforcement Learning como Detecção Implícita de Regime

Uma abordagem radicalmente diferente emerge da literatura de RL em trading: em vez de classificar regimes explicitamente e depois escolher estratégias, treinar um agente que aprende a adaptar seu comportamento a diferentes condições de mercado sem labels de regime.

**Conceito:** o agente de RL observa um state vector que inclui features de mercado (retornos, volatilidade, momentum, volume) e features de portfólio (posição atual, P&L, exposição) e aprende uma política que mapeia estados em ações (comprar, vender, manter, sizing). O regime está implícito no state vector — o agente aprende que "quando a volatilidade é alta e os retornos são negativos" (≈ Crisis), a melhor ação é reduzir exposição, sem que alguém lhe diga que esse estado se chama "Crisis".

**State space relevante:**

O state vector deve incluir três componentes:
1. **Market observations:** features de preço (retornos em múltiplas janelas, volatilidade, ATR, z-score do preço vs MA), momentum (RSI, MACD), e volume (ratio volume atual/média).
2. **Portfolio status:** posição atual, P&L não-realizado, cash disponível, exposure ratio.
3. **Action history:** últimas N ações tomadas (para evitar churning e capturar dependência temporal).

**Reward function design:** o ponto mais crítico. Uma reward function que apenas maximiza retorno produz agentes que tomam risco excessivo. A literatura recente propõe reward functions compostas:

```
R_t = retorno_liquido - λ_dd × penalidade_drawdown - λ_tc × custo_transação
```

Onde:
- retorno_liquido = variação do valor do portfólio após custos.
- penalidade_drawdown = penaliza drawdowns proporcionalmente à sua magnitude (ex: 0 se drawdown < 5%, penalidade crescente acima disso).
- custo_transação = spread + slippage + comissão para cada trade executado.
- λ_dd e λ_tc são hiperparâmetros que controlam o trade-off entre retorno e risco.

**Resultados benchmarked:** um sistema RL testado em múltiplos regimes (bull, bear, sideways) obteve Sharpe de 1.52 em bull markets (vs 1.31 do buy-and-hold), 0.91 em bear markets com retorno positivo de ~5% (vs -27.6% do buy-and-hold), e 1.02 em sideways (vs 0.21 do buy-and-hold). O resultado mais impressionante é o bear market — o agente aprendeu estratégias defensivas (manter cash, reduzir posição, explorar bounces) sem programação explícita.

**Integração com o framework de regimes explícitos:**

O RL não substitui a taxonomia de regimes — complementa. A proposta é um sistema em dois níveis:

1. **Nível 1 — Classificador explícito:** detecta o regime usando a taxonomia de 14 estados e define o universo de ações permitidas (ex: em Crisis, proibir long agressivo; em Trending Up, permitir pyramiding).
2. **Nível 2 — Agente RL:** opera dentro das restrições definidas pelo nível 1, otimizando timing, sizing e execução dentro do regime corrente.

Essa arquitetura combina a interpretabilidade e controle de risco do classificador explícito com a adaptabilidade do RL. O classificador garante que o agente não faça coisas estruturalmente erradas (shortar em bull market forte), enquanto o RL otimiza dentro do espaço permitido.

**Riscos do RL puro:** overfitting a condições históricas específicas, instabilidade de treinamento em ambientes não-estacionários, e opacidade (não saber por que o agente tomou uma decisão). Para Bitcoin, o histórico limitado (dados diários desde ~2013) e a natureza extremamente não-estacionária (ciclos de 4 anos com características distintas) tornam o RL puro particularmente arriscado. O framework de dois níveis mitiga esses riscos.

**⏱ Perspectiva 1H:**
RL é mais viável no 1H do que no 1D por ter muito mais dados de treinamento (24 barras por dia × 365 dias = ~8.760 observações por ano vs 365 no diário). O tradeoff é que o 1H é mais ruidoso e os custos de transação pesam mais. O agente RL no 1H deve ter custos de transação realistas na reward function — caso contrário, aprende a fazer overtrading que é lucrativo em backtesting mas deficitário em live.

**⏱ Perspectiva 1D:**
RL no diário sofre com dados limitados (Bitcoin tem ~4.000 barras diárias desde 2013). A solução é data augmentation: treinar com bootstrap das séries históricas, ou com dados sintéticos gerados a partir dos parâmetros estimados dos regimes (simulação Monte Carlo condicionada ao regime). Outra abordagem é transfer learning: pré-treinar o agente em múltiplos ativos (equities, commodities, FX) e fine-tunar em Bitcoin.

### Abordagens Híbridas: ML para Seleção + Econometria para Estrutura

A direção mais promissora identificada na literatura é a combinação de ML com modelos tradicionais, aproveitando os pontos fortes de cada abordagem.

**Workflow proposto:**

1. **Seleção de features via ML:** usar Random Forest ou XGBoost com as features candidatas listadas na seção de implementação. Treinar o modelo para classificar regimes históricos (labels gerados por um MS ou por classificação manual). Extrair feature importance para identificar quais variáveis são mais discriminativas.

2. **Redução de dimensionalidade informada:** das 8+ features sugeridas no documento original, selecionar as 4-5 com maior importância. Isso reduz o risco de overfitting e melhora a estabilidade do classificador.

3. **Alimentar modelo estruturado:** usar as features selecionadas como variáveis observáveis em um MS com probabilidades de transição time-varying (TVTP-MS), onde P(transição) depende das features de alta importância.

4. **Validação cruzada:** comparar os regimes identificados pelo híbrido com benchmarks conhecidos (drawdowns do mercado, ciclos de halving do Bitcoin, eventos de capitulação documentados).

**Vantagem da abordagem híbrida:** o ML identifica o que observar (features importantes) e o modelo econométrico fornece a estrutura formal de como interpretar. Isso evita tanto o problema de "black box" do ML puro quanto o de "assumir que sabemos o que importa" dos modelos tradicionais.

---

## Matriz de Transição com Duration Dependence

A Matriz de Transição do documento principal assume probabilidades de transição estáticas — "Trending Up → Distribution: Média-Alta" independente de há quanto tempo estamos em Trending Up. A literatura sobre duration dependence mostra que isso é uma simplificação significativa.

### Conceito de Duration Dependence

A observação empírica é que regimes de mercado não seguem memoryless property (propriedade sem memória). Especificamente:

- **Bull markets envelhecem:** quanto mais longo um regime de Trending Up ou Robust Expansion, maior a probabilidade de transição para Distribution ou Choppy. Evidência empírica (Maheu & McCurdy, 2000) mostra que a probabilidade de um bull market terminar aumenta com sua duração.
- **Bear markets são diferentes:** a probabilidade de um bear market terminar é relativamente constante (ou até diminui) nos primeiros meses, e depois aumenta abruptamente — sugerindo que bear markets têm uma "vida média" mais definida.
- **Crises são curtas mas auto-reforçantes:** regimes de Market Turmoil raramente duram mais que 3-6 meses, mas nos primeiros dias/semanas, a probabilidade de permanecer em crise é alta (feedback loops de margin calls e contágio ainda ativos).

### Formalização

No modelo MS padrão, a probabilidade de permanecer no regime k é constante: p_kk. A duração no regime segue distribuição geométrica com esperança 1/(1 - p_kk).

Com duration dependence, p_kk(d) depende de d = tempo já gasto no regime atual:

```
p_kk(d) = Λ(α_k + β_k × d)
```

Onde Λ é a função logística e β_k captura o efeito de duração. Se β_k < 0, a probabilidade de permanecer cai com a duração (o regime "envelhece" — típico de Trending Up e Blow-off). Se β_k > 0, a probabilidade de permanecer aumenta com a duração (o regime se auto-reforça — típico dos estágios iniciais de Crisis).

### Matriz de Transição Expandida com Duration

A tabela abaixo substitui a seção "Transições de alta probabilidade" do documento original, adicionando o efeito de duração e condicionamento a indicadores observáveis.

| De → Para                          | Prob. Base  | Efeito de Duração                                                                 | Indicador Condicionante                                      |
| ---------------------------------- | ----------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| Trending Up → Distribution         | Média       | **Aumenta com duração.** Após 30d+, probabilidade sobe significativamente         | RSI divergence + breadth deteriorating                       |
| Trending Up → Blow-off             | Baixa       | **Aumenta em fases tardias.** Mais provável após 60d+ de trending up              | Aceleração de retornos (2ª derivada > 0) + volume spike      |
| Low Vol → Breakout                 | Alta        | **Aumenta com duração.** Compressão > 10d tem probabilidade >70% de breakout      | Bollinger Bandwidth < P10 + volume contraindo                |
| Breakout → Trending                | Alta        | **Máxima nos primeiros 3-5 períodos.** Se não resolve em trending rápido, vira Choppy | Follow-through volume + ADX subindo                          |
| Breakout → Choppy                  | Média       | **Aumenta após 3-5 períodos sem resolução**                                       | Volume caindo após breakout + preço oscilando                |
| Trending Down → Crisis             | Baixa       | **Relativamente constante**, mas correlação cross-asset é trigger                  | Correlação cross-asset > 0.85 + spread HY alargando          |
| Trending Down → Accumulation       | Média       | **Aumenta com duração.** Após 20-40d, vendedores se esgotam                       | Volume em testes de suporte decrescente + RSI divergence     |
| Crisis → Recovery                  | Alta        | **Aumenta rapidamente após 2-4 semanas.** Pânico é insustentável                  | VIX começando a cair + intervenção de autoridades            |
| Distribution → Trending Down       | Média-Alta  | **Aumenta com duração de distribution.** Após 3-4 semanas, risco de colapso alto  | Breadth continuando a deteriorar + volume nos sell-offs      |
| Accumulation → Trending Up         | Média-Alta  | **Aumenta com duração.** Após 3-6 semanas, spring mais provável                   | Testes de suporte com vol decrescente + Wyckoff spring       |
| Blow-off → Crisis/Trending Down    | Alta        | **Aumenta exponencialmente.** Cada dia adicional de blow-off aumenta risco de crash| Divergência volume-preço + alavancagem em máxima             |
| Recovery → Trending Up             | Alta        | **Aumenta após 2ª confirmação (2º higher low)**                                   | VIX em contango + breadth melhorando + higher lows           |
| Ranging → Low Vol                  | Média       | **Aumenta com duração.** Range > 15d tende a comprimir                            | ATR contraindo + volume decrescente                          |
| Choppy → Ranging                   | Média       | **Aumenta com duração.** Vol eventualmente arrefece                               | ATR começando a cair + reversões menos violentas             |
| Mean-Reverting → Trending          | Média       | **Não linear.** Half-life crescente sinaliza mudança                              | Hurst exponent cruzando 0.5 + half-life O-U crescendo       |

### Implementação de Duration Dependence

**Para o classificador:** adicionar `duration_in_current_regime` como feature do modelo. Calcular como o número de períodos consecutivos em que o regime atual foi o label dominante. Essa feature interage com as features de mercado para modular as probabilidades de transição.

**Para sizing:** usar a duration como multiplicador de cautela. Quanto mais longo o regime de Trending Up, mais agressivo deve ser o trailing stop e mais conservador o pyramiding (o regime está "envelhecendo" e a probabilidade de transição está aumentando).

**Tabela de ajuste de sizing por duração:**

| Regime         | Duração < P25 | Duração P25-P75 | Duração > P75 | Duração > P90        |
| -------------- | ------------- | --------------- | ------------- | -------------------- |
| Trending Up    | 100% sizing   | 100% sizing     | 75% sizing    | 50% sizing + trailing agressivo |
| Trending Down  | 75% sizing    | 100% sizing     | 75% sizing    | 50% + monitorar accumulation    |
| Ranging        | 25% sizing    | 0% sizing       | Preparar breakout entries       | Alta convicção em breakout iminente |
| Low Vol        | 25% sizing    | 50% vol buying  | 75% vol buying| Máxima convicção em explosão de vol |
| Crisis         | 0% (hedge)    | 0% (hedge)      | 25% (início de recovery?)       | Recovery provável — preparar long |
| Mean-Reverting | 50% sizing    | 75% sizing      | 50% sizing    | Monitorar Hurst — regime pode estar mudando |

**Onde P25, P75, P90 referem-se aos percentis da distribuição histórica de duração de cada regime.** Exemplo: se o Trending Up no Bitcoin diário dura tipicamente entre 15 e 60 dias (P25-P75), uma tendência de alta com 70+ dias (>P90) deve ser tratada com cautela crescente.

### Time-Varying Transition Probabilities (TVTP)

Além de depender da duração, as probabilidades de transição podem depender de variáveis observáveis. Isso formaliza o que o documento principal descreve qualitativamente ("Trending Down → Crisis se correlação cross-asset > 0.85").

**Variáveis condicionantes sugeridas para TVTP:**

Para transições de regimes bullish para bearish:
- VIX term structure (contango → backwardation sinaliza stress).
- Spread de crédito HY-IG (alargamento antecede problemas).
- Breadth do mercado (deterioração antecede reversão do índice).

Para transições de regimes bearish para bullish:
- VIX absoluto e direção (caindo de níveis extremos).
- Fluxo de put/call (extremos contrarianos).
- Ações de autoridades (corte de juros, QE, estímulo fiscal).

Para transições envolvendo volatilidade:
- IV percentile vs HV percentile (IV muito abaixo de HV sugere complacência → breakout).
- GEX (mudança de sinal sinaliza mudança no mecanismo de amplificação/supressão de vol).

**Implementação:** estimar um modelo MS-TVTP onde:

```
P(S_t = j | S_{t-1} = i, Z_t) = Λ(α_ij + β_ij' × Z_t)
```

Onde Z_t é o vetor de variáveis condicionantes. Isso produz uma matriz de transição que muda a cada período, condicionada ao estado observável do mercado.

---

## Sentimento como Feature de Regime

### Motivação

O documento principal menciona social sentiment apenas no contexto de Blow-off (Google Trends e menções em social media como indicadores contrarianos). Porém, a literatura recente demonstra que sentimento financeiro — processado via NLP — é uma feature valiosa para detecção e confirmação de regime em múltiplos contextos, não apenas em topos especulativos. Para Bitcoin, onde o ciclo de notícias e o sentimento de social media têm impacto demonstrável no preço, essa dimensão é particularmente importante.

### FinBERT e Sentiment Scoring

FinBERT é um modelo transformer (baseado em BERT) fine-tuned especificamente em texto financeiro. Diferentemente de análise de sentimento genérica (VADER, TextBlob), FinBERT compreende nuances financeiras como negação ("not expected to miss earnings"), hedging ("may underperform"), e jargão setorial.

**Score de sentimento agregado:** para cada ativo e cada período, agregar as probabilidades de sentimento (positivo, neutro, negativo) de todas as notícias relevantes:

```
S_t = (1/N) × Σ (P_positive(i) - P_negative(i))
```

Onde S_t ∈ [-1, 1]. Valores próximos de +1 indicam sentimento unanimemente positivo; próximos de -1, unanimemente negativo. Valores próximos de 0 indicam neutralidade ou divisão.

**Uso como filtro (gate), não como sinal:** a aplicação mais robusta documentada na literatura é usar sentimento como gate — um filtro que bloqueia ou permite trades gerados por outros sinais, não como gerador de sinais primário. Concretamente:

- Se S_t < -0.70 (sentimento fortemente negativo): suspender novas entradas long, independente do regime detectado. Apertar stops em posições existentes.
- Se S_t > 0.70 (sentimento fortemente positivo): pode ser contrarian em regimes tardios (Distribution, Blow-off) — euforia extrema como sinal de alerta.
- Se -0.70 < S_t < 0.70: sem override de sentimento; seguir regime detectado normalmente.

**Justificativa para gate em vez de sinal:** sentimento é ruidoso, atrasado em relação ao preço na maioria dos regimes, e sujeito a vieses de seleção (mídias reportam mais notícias negativas). Usá-lo como sinal primário produz overtrading e falsos positivos. Como gate, adiciona uma camada de proteção contra "regime correto mas contexto de notícias adverso" (ex: Trending Up legítimo mas notícia de regulação cripto iminente que pode invalidar a tendência).

### Adaptação para Bitcoin e Crypto

Para crypto, o universo de fontes de sentimento é diferente de equities:

**Fontes de alta relevância:**
- Crypto Twitter (CT) / X: a fonte mais rápida de sentimento no ecossistema crypto. Influenciadores, fundadores de projetos, e traders publicam em tempo quase-real.
- Reddit (r/Bitcoin, r/CryptoCurrency): indicador de sentimento retail. Extremos (bullish ou bearish) são contrarianos.
- Fear & Greed Index (Alternative.me): índice composto que agrega volatilidade, momentum, social media, dominância do Bitcoin e Google Trends. Escala 0-100 (0 = medo extremo, 100 = ganância extrema).
- Funding rates em perpétuos: não é "sentimento" textual mas reflete o sentimento posicional do mercado. Funding positivo alto = muitos longs alavancados (bullish extremo → contrarian); funding negativo = muitos shorts (bearish extremo → contrarian).
- Deribit options flow: para Bitcoin, Deribit concentra >80% do volume de opções. O skew e o put/call ratio fornecem sentimento do mercado sofisticado.

**Processamento para Bitcoin:** FinBERT foi treinado em texto financeiro tradicional e pode não capturar nuances de crypto (jargon como "HODL", "to the moon", "rekt", "rug pull"). Para crypto, considerar fine-tuning adicional em corpus de crypto news, ou usar modelos alternativos como CryptoBERT (se disponível e validado).

### Sentimento por Regime — Tabela de Interação

| Regime         | Sentimento    | Interpretação                                          | Ação                                                    |
| -------------- | ------------- | ------------------------------------------------------ | ------------------------------------------------------- |
| Trending Up    | Positivo      | Confirmação — sentimento alinhado com preço             | Manter posição, sizing normal                           |
| Trending Up    | Negativo      | Divergência — possível notícia adversa iminente         | Apertar stops, reduzir sizing em 25%                    |
| Trending Down  | Negativo      | Confirmação — sentimento alinhado com preço             | Manter short/hedge                                      |
| Trending Down  | Positivo      | Possível bounce ou narrativa de recovery prematura      | Não comprar; se muito positivo, pode ser bull trap       |
| Distribution   | Positivo      | **Perigo** — euforia mascarando distribuição            | Acelerar redução de posição                             |
| Accumulation   | Negativo      | **Oportunidade** — pessimismo extremo em base           | Confirma acumulação; considerar aumentar sizing gradual  |
| Blow-off       | Muito Positivo| **Red flag** — unanimidade bullish é contrarian         | Trailing stop ultra-agressivo; preparar saída            |
| Crisis         | Muito Negativo| Possível capitulação próxima                           | Monitorar para sinais de recovery; não agir imediatamente|
| Recovery       | Negativo      | **Normal** — disbelief rally; maioria ainda com medo    | Confirmação de recovery genuína; manter/adicionar       |
| Choppy         | Misto         | Sentimento dividido confirma indecisão                  | Confirma Choppy; ficar flat                             |

### Fear & Greed Index como Proxy Simplificada para Bitcoin

Para traders que não querem implementar NLP completo, o Fear & Greed Index é uma proxy prática:

- **0-25 (Extreme Fear):** potencial contrarian bullish. Se o regime é Accumulation, é confirmação forte. Se o regime é Crisis/Trending Down, esperar mais antes de comprar.
- **25-45 (Fear):** cautela mas não pânico. Consistente com regimes de Distribution ou Trending Down leve.
- **45-55 (Neutral):** sem informação adicional. Seguir regime detectado.
- **55-75 (Greed):** consistente com Trending Up. Não é extremo o suficiente para ser contrarian.
- **75-100 (Extreme Greed):** red flag contrarian. Se o regime é Trending Up há >P75 da duração histórica, probabilidade alta de transição para Distribution ou Blow-off.

**⏱ Perspectiva 1H:**
Sentimento textual muda mais rápido que o preço no 1H, especialmente em crypto. Uma notícia de regulação pode inverter o sentimento em minutos, antes do preço reagir completamente. No 1H, implementar um "sentiment alert" que monitora headlines em tempo real e gera um override temporário (similar a Event-Driven Override Tier 2) quando o sentimento muda abruptamente (|ΔS_t| > 0.5 em menos de 1 hora). Isso funciona como early warning para movimentos de preço iminentes.

**⏱ Perspectiva 1D:**
No diário, o sentimento agregado do dia é mais estável e informativo. Recomendo calcular S_t ao final de cada sessão (média ponderada das notícias do dia, com peso maior para notícias pré-abertura e durante horário de mercado) e incluir como feature no classificador de regime diário. O sentimento diário é particularmente útil para confirmar ou questionar regimes de transição (Distribution, Accumulation, Recovery) onde os sinais de preço são ambíguos.

---

## QCD e Framework de Validação do Classificador

### Quantile-Conditional Density (QCD) como Métrica de Confiabilidade

A seção de Sizing por Regime do documento principal define sizing como percentual fixo por regime. Porém, nem todos os períodos dentro de um mesmo regime são igualmente confiáveis. O QCD (Quantile-Conditional Density), proposto pela State Street, mede a dispersão dos retornos condicionados ao regime — ou seja, quão previsíveis são os retornos quando sabemos que estamos em determinado regime.

**Conceito:** para cada regime k, examinar a distribuição empírica dos retornos. Se os retornos são consistentemente positivos e pouco dispersos (ex: Trending Up produz retornos de +0.5% a +2% por dia com poucos outliers), o QCD é baixo e a confiança no sizing agressivo é alta. Se os retornos são dispersos (ex: Choppy produz retornos de -3% a +3% sem padrão), o QCD é alto e o sizing deve ser mínimo.

**Cálculo simplificado:**

```
QCD_k = IQR_k / |média_k|
```

Onde IQR_k é o intervalo interquartil dos retornos no regime k e |média_k| é o valor absoluto do retorno médio. Quanto menor o QCD, mais "confiável" é o regime — os retornos são concentrados em torno da média e na direção esperada.

**Resultado empírico de referência:** na análise de 30 anos de dados americanos, os regimes de expansão robusta (≈ Trending Up maduro) apresentaram QCD de ~0.4 para equities, enquanto Market Turmoil apresentou QCD de ~0.6 para equities. Ou seja, mesmo em crise — onde sabemos que o mercado cai — a dispersão dos retornos é alta, tornando o sizing preciso mais difícil.

**Integração com sizing:** o QCD pode funcionar como multiplicador de sizing:

```
Sizing_efetivo = Sizing_base_do_regime × (1 - QCD_normalizado)
```

Onde QCD_normalizado ∈ [0, 1] é o QCD do regime atual, normalizado pelo range histórico. Se o QCD é baixo (retornos confiáveis), o sizing é mantido próximo do base. Se o QCD é alto (retornos dispersos), o sizing é automaticamente reduzido.

### Tabela de QCD Esperado por Regime (Bitcoin — estimativa)

| Regime         | QCD Estimado | Confiabilidade | Ajuste de Sizing Sugerido |
| -------------- | ------------ | -------------- | ------------------------- |
| Trending Up    | 0.35-0.50    | Alta           | 100% do base              |
| Trending Down  | 0.40-0.60    | Média-Alta     | 85-100% do base           |
| Mean-Reverting | 0.45-0.55    | Média          | 80-90% do base            |
| Recovery       | 0.50-0.65    | Média          | 75-85% do base            |
| Breakout       | 0.55-0.70    | Média-Baixa    | 70-80% do base            |
| Distribution   | 0.60-0.75    | Baixa          | 60-70% do base            |
| Blow-off       | 0.65-0.80    | Baixa          | 55-65% do base            |
| Choppy         | 0.80-1.00    | Muito Baixa    | 0-25% do base             |
| Crisis         | 0.70-0.90    | Baixa          | 0-25% do base (hedge)     |
| Ranging        | 0.85-1.00    | Muito Baixa    | 0-25% do base             |

**Nota:** estes valores são estimativas baseadas na analogia com dados de equities, ajustados para a maior volatilidade do Bitcoin. Devem ser calibrados empiricamente com dados históricos reais do Bitcoin em cada regime.

### Framework de Validação do Classificador

Validar um classificador de regime é fundamentalmente diferente de validar um modelo de previsão de retornos. Não existe um "ground truth" objetivo — regimes são construções teóricas. A abordagem é validar contra múltiplos benchmarks independentes.

**Nível 1 — Validação contra eventos conhecidos:**

Compilar uma lista de eventos históricos do Bitcoin com regime "óbvio" e verificar se o classificador os identifica corretamente:

| Período              | Evento                        | Regime Esperado        |
| -------------------- | ----------------------------- | ---------------------- |
| Dez 2017             | Rally parabólico para ~$20K   | Blow-off               |
| Jan-Fev 2018         | Crash pós-blow-off            | Crisis → Trending Down |
| Mar-Nov 2018         | Bear market prolongado        | Trending Down          |
| Dez 2018 - Mar 2019  | Bottoming                     | Accumulation           |
| Mar 2020             | COVID crash                   | Crisis                 |
| Abr-Out 2020         | Recuperação pós-COVID         | Recovery → Trending Up |
| Nov 2020 - Abr 2021  | Bull run para ~$64K           | Trending Up → Blow-off |
| Mai-Jul 2021         | Crash (-50%) e consolidação   | Crisis → Ranging       |
| Ago-Nov 2021         | Rally para ~$69K              | Trending Up → Blow-off |
| Nov 2021 - Jun 2022  | Bear market                   | Trending Down          |
| Jun-Nov 2022         | FTX period / consolidação     | Ranging → Crisis       |
| Jan-Mar 2023         | Início de recovery            | Accumulation → Recovery|
| Out 2023 - Mar 2024  | ETF rally                     | Trending Up            |

Calcular precision, recall e F1 score para cada regime contra esta classificação manual. O benchmark da State Street (F1 ~73-78% para Market Turmoil contra drawdowns conhecidos) sugere que F1 > 70% para regimes primários é um resultado forte.

**Nível 2 — Validação estatística:**

Para cada regime identificado, verificar que as distribuições de retorno condicionais são estatisticamente diferentes entre si:
- Teste de Kolmogorov-Smirnov entre pares de regimes: H0 = "a distribuição de retornos é a mesma nos dois regimes".
- Se H0 não é rejeitada para um par de regimes, considerar fundir esses regimes (são estatisticamente indistinguíveis).

**Nível 3 — Validação operacional (out-of-sample):**

Walk-forward validation com os seguintes passos:
1. Treinar o classificador nos primeiros 70% dos dados.
2. Nos 30% restantes, gerar labels de regime e simular a estratégia de sizing do documento principal.
3. Comparar retorno ajustado ao risco (Sharpe, Sortino, max drawdown) da estratégia regime-conditioned vs buy-and-hold e vs estratégia com sizing uniforme.
4. A estratégia regime-conditioned deve superar as alternativas de forma consistente. Se não supera, o classificador não está adicionando valor operacional.

**Nível 4 — Estabilidade temporal:**

Verificar se os labels são estáveis — o regime não deve trocar a cada período (flickering). Métricas:
- **Duração média do regime:** deve ser consistente com as estimativas na tabela de Referência Rápida. Se o modelo troca de regime a cada 2-3 períodos, está overfitting ao ruído.
- **Frequência de transição:** número de transições por unidade de tempo. Deve ser significativamente menor que uma transição por período.
- **Filtering lag:** quantos períodos o modelo leva para detectar uma mudança real de regime. Lag < 5 períodos para regimes no 1D é aceitável; lag > 10 períodos é problemático (o regime pode ter acabado antes de ser detectado).

**Nível 5 — Rentabilidade incremental:**

O teste definitivo: a detecção de regime melhora o P&L líquido (após custos de transação das mudanças de sizing)? Calcular:

```
Alpha_regime = Retorno_com_sizing_regime - Retorno_buy_and_hold
Custo_transicoes = Σ(custos de rebalanceamento por mudança de regime)
Alpha_liquido = Alpha_regime - Custo_transicoes
```

Se Alpha_liquido < 0, o sistema está destruindo valor — o custo de rebalancear entre regimes excede o benefício do sizing condicional. Nesse caso, reduzir a granularidade (menos regimes), aumentar os filtros de estabilidade (exigir mais confirmação antes de trocar), ou aceitar que para o ativo/timeframe específico, regime detection não tem edge operacional.

---

## Feature Importance via ML para Seleção de Variáveis de Regime

### Motivação

A seção de implementação do documento principal lista 8 features mínimas para detecção de regime. Essa lista foi construída com base em teoria e experiência — ADX para direcionalidade, Hurst para persistência, volatilidade para classificar regimes de vol, etc. Porém, a literatura recente mostra que a seleção teórica de features pode ser subótima: variáveis que parecem importantes na teoria podem ser redundantes na prática, e variáveis ignoradas podem ser altamente informativas.

### Metodologia

**Passo 1 — Gerar labels de regime (supervisão):**

Usar um método semi-automático para classificar historicamente cada período do Bitcoin:
- MS-GARCH com 4 estados (macro regimes) como ponto de partida.
- Ajustar manualmente os períodos mais óbvios (blow-offs, crises, ranges longas) baseado em conhecimento de domínio.
- Para regimes de transição (Distribution, Accumulation), usar critérios Wyckoff documentados na seção de Sub-estados.

**Passo 2 — Criar feature matrix expandida:**

Incluir todas as features candidatas, não apenas as 8 do mínimo viável:

Features de retorno e tendência:
- Retorno acumulado: 5, 10, 20, 50 períodos.
- Inclinação da regressão linear: 10, 20, 50 períodos.
- R² da regressão linear: 10, 20, 50 períodos.
- Posição relativa às EMAs: z-score do preço vs EMA(20), EMA(50), EMA(200).
- Ordenamento de EMAs: EMA(20) > EMA(50) > EMA(200) codificado como categórico.

Features de volatilidade:
- Volatilidade realizada: 5, 10, 20, 50 períodos.
- ATR: 14 períodos, percentile rank vs 100 períodos.
- Bollinger Bandwidth: 20 períodos.
- Razão vol curta / vol longa: σ(5) / σ(50).
- Parkinson estimator (high-low range based vol).

Features de momentum e mean-reversion:
- ADX: 14 períodos.
- RSI: 14 períodos.
- MACD histogram.
- Hurst exponent: rolling 50-100 períodos.
- Autocorrelação lag 1: rolling 20 períodos.
- Half-life de Ornstein-Uhlenbeck: rolling 50 períodos.
- ADF test statistic: rolling 50 períodos.

Features de volume:
- Razão volume / volume MA(20).
- OBV (On-Balance Volume): direção e magnitude.
- Volume em dias de alta vs volume em dias de baixa (ratio).

Features de sentimento e mercado (para Bitcoin):
- Fear & Greed Index.
- Funding rate (perpétuos).
- Open interest em futuros (mudança percentual).
- Dominância do Bitcoin (% do market cap total de crypto).

Features de liquidez:
- Bid-ask spread médio (se disponível).
- Slippage estimado (via orderbook depth ou proxy).

**Passo 3 — Treinar ensemble e extrair importâncias:**

```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.inspection import permutation_importance

# Treinar Random Forest
rf = RandomForestClassifier(n_estimators=500, max_depth=10, random_state=42)
rf.fit(X_train, y_train_regime_labels)

# Feature importance nativa (Mean Decrease in Impurity)
mdi_importance = rf.feature_importances_

# Permutation importance (mais confiável — mede quanto a performance
# cai quando uma feature é embaralhada)
perm_importance = permutation_importance(rf, X_test, y_test,
                                          n_repeats=30, random_state=42)
```

**Passo 4 — Selecionar features e validar:**

Ordenar features por importância (usar permutation importance, que é menos enviesada que MDI para features correlacionadas). Selecionar as top-K features que coletivamente explicam >90% da importância total.

Validar removendo cada feature do top-K individualmente e verificando a queda de performance do classificador. Se remover uma feature não piora significativamente o F1 score, ela é redundante e pode ser descartada.

### Resultados Esperados e Interpretação

Com base na literatura e na estrutura dos regimes, as features com maior importância esperada são:

**Tier 1 — Provavelmente as mais importantes:**
- Volatilidade realizada (discrimina regimes de vol: Low Vol, Crisis, Choppy, Breakout).
- Retorno acumulado de 20 períodos (discrimina direção: Trending Up vs Down vs Ranging).
- ADX (discrimina direcionalidade: Trending vs Ranging vs Choppy).
- Razão vol curta / vol longa (captura transições: Low Vol → Breakout, estabilidade → instabilidade).

**Tier 2 — Provavelmente importantes:**
- Hurst exponent (discrimina Mean-Reverting vs Trending).
- RSI (captura extremos: Blow-off, Accumulation com divergências).
- Autocorrelação lag 1 (confirma persistência vs anti-persistência).
- Volume ratio (confirma convicção: Breakout legítimo vs falso, Distribution vs pausa saudável).

**Tier 3 — Potencialmente importantes, depende do ativo:**
- Fear & Greed Index (pode ser muito informativo para Bitcoin, menos para equities).
- Funding rate (específico de crypto, alta informação sobre posicionamento).
- Bollinger Bandwidth (proxy de vol comprimida, pode ser redundante com ATR percentile).

**Features provavelmente redundantes:**
- Inclinação da regressão linear vs retorno acumulado (altamente correlacionados).
- MACD histogram vs ADX (ambos medem momentum/direcionalidade).
- Múltiplas janelas da mesma feature (vol de 5 e 10 períodos são muito correlacionados; manter uma janela curta e uma longa).

### Importância Variável por Regime

Um insight sofisticado: features diferentes são importantes para classificar regimes diferentes. Random Forest fornece importância global, mas é possível calcular importância por classe.

**Expectativa:**
- Para classificar **Crisis vs Trending Down**: volatilidade absoluta e correlação cross-asset são decisivas.
- Para classificar **Trending Up vs Distribution**: breadth e volume ratio são decisivos (ambos têm retornos positivos, mas distribution tem breadth deteriorando e volume nos rallies caindo).
- Para classificar **Ranging vs Mean-Reverting**: Hurst exponent e autocorrelação são decisivos (únicos discriminadores entre lateralidade explorável e não-explorável).
- Para classificar **Low Vol vs Ranging**: ATR percentile e Bollinger Bandwidth são decisivos (ambos têm baixa direcionalidade, mas Low Vol tem compressão extrema).
- Para classificar **Breakout vs Choppy**: volume no movimento e follow-through são decisivos (ambos têm vol alta, mas Breakout tem direcionalidade e volume confirmando).

### Partial Dependence e Thresholds Empíricos

Após identificar as features mais importantes, usar partial dependence plots (PDP) para entender a relação funcional entre cada feature e cada regime. Isso pode revelar thresholds empíricos que refinam os thresholds teóricos do documento principal.

**Exemplo hipotético:** o documento define ADX > 25 como threshold para Trending. O PDP do Random Forest pode revelar que, para Bitcoin, o threshold efetivo é ADX > 28 no diário e ADX > 22 no 1H (porque a dinâmica de Bitcoin é diferente de equities). Isso permite calibração empírica dos thresholds que atualmente são definidos por convenção.

**Ferramentas de interpretabilidade adicionais:**
- **SHAP values:** explicam a contribuição de cada feature para cada classificação individual, não apenas na média. Útil para entender por que o modelo classificou um período específico como Regime X quando parecia ser Regime Y.
- **ICE plots (Individual Conditional Expectation):** mostram como a probabilidade de cada regime muda conforme uma feature varia, para observações individuais. Revelam heterogeneidade que o PDP (que mostra a média) pode mascarar.

---

## Regime Detector Mínimo Viável — Baseline para Comparação

### Motivação

Antes de implementar classificadores sofisticados (HMM, mixture models, ML), é essencial ter um baseline simples contra o qual comparar. Se o classificador sofisticado não superar consistentemente o baseline, a complexidade adicional não se justifica.

### Detector Simples via Retornos Rolantes

A abordagem mais simples documentada na literatura: classificar o regime com base na média móvel dos retornos.

```
R_t = SMA_20(retornos_diários)
```

- Se R_t > 0 e vol < P50: **Trending Up** (alta com vol normal).
- Se R_t > 0 e vol > P75: **Blow-off** ou **Recovery** (alta com vol elevada).
- Se R_t < 0 e vol < P50: **Trending Down leve** (queda com vol normal).
- Se R_t < 0 e vol > P75: **Crisis** ou **Trending Down forte** (queda com vol elevada).
- Se |R_t| < threshold e vol < P25: **Low Vol / Ranging** (sem direção, vol baixa).
- Se |R_t| < threshold e vol > P50: **Choppy** (sem direção, vol alta).

**Onde threshold ≈ 0.001-0.003 (retorno diário), calibrado empiricamente.**

Esse detector de 6 estados com 2 features (retorno acumulado + volatilidade) é surpreendentemente eficaz como baseline. A literatura mostra que sistemas de trading usando esse detector simples para ajustar sizing já superam buy-and-hold em termos de risco ajustado, mesmo sem a sofisticação dos 14 regimes do documento principal.

### Uso como Benchmark

Qualquer classificador mais sofisticado deve superar este baseline em:

1. **F1 score** para classificação de regimes contra labels manuais.
2. **Sharpe ratio** da estratégia de sizing condicionado ao regime.
3. **Max drawdown** reduzido em comparação com sizing baseado no detector simples.

Se o classificador de 14 regimes não supera o baseline de 6 regimes nessas três métricas simultaneamente, a taxonomia está over-engineered para o ativo/timeframe em questão — simplificar para menos regimes ou agregar regimes similares.

### Detector Intermediário — XGBoost com Features Técnicas

Um passo intermediário entre o baseline mínimo e os modelos sofisticados: XGBoost treinado com features interpretáveis.

**Configuração de referência documentada na literatura:**
- 10 features de input (EMAs, MACD, RSI, Bollinger Bands, ATR, volatilidade, interaction terms como EMA50/EMA200).
- 200 estimators, max depth 6, learning rate 0.05.
- Split 70/30 temporal (sem shuffling — preservar ordem cronológica).
- Acurácia out-of-sample reportada: ~63% para previsão direcional binária (próximo dia up/down).

**Para classificação de regime (multi-class):** a acurácia esperada é menor que para binário (mais classes = mais difícil), mas com features bem construídas, 50-55% de acurácia em 6 classes já é operacionalmente útil (vs ~17% de um classificador aleatório).

---

## Leituras Adicionais e Referências dos Papers

### Papers analisados neste documento

1. **Ung, D. (2025).** "Decoding Market Regimes: Machine-learning insights into US asset performance over the last 30 years." State Street Investment Management Insights. — Metodologia de t-distributed mixture model + GARCH; QCD; análise de asset performance por regime com dados de 1995-2024.

2. **Qureshi, W. et al. (2026).** "Autonomous Trading Across Bull, Bear, and Sideways Markets with Reinforcement Learning Algorithm." IJEDR, Vol. 14, Issue 1. — Framework de RL para trading multi-regime; design de reward function; resultados por regime.

3. **Mullapudi, P. (2025).** "Regime Switching Models in Finance and Economics: Traditional Approaches and Machine Learning Enhancements." IJFMR, Vol. 7, Issue 2. — Survey de modelos MS, threshold, HMM; duration dependence; feature importance para regime detection; abordagens híbridas ML + econometria.

4. **Pillai, V.N.K. et al. (2026).** "Generating Alpha: A Hybrid AI-Driven Trading System Integrating Technical Analysis, Machine Learning and Financial Sentiment for Regime-Adaptive Equity Strategies." arXiv:2601.19504. — Sistema híbrido com XGBoost + FinBERT + regime filter; ATR-based sizing; backtesting em 100 ações do S&P 500.

### Referências fundamentais citadas nos papers (para aprofundamento)

- **Hamilton, J.D. (1989).** "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." Econometrica, 57(2). — O paper fundacional de Markov-switching models. Leitura obrigatória.
- **Maheu, J.M. & McCurdy, T.H. (2000).** "Identifying Bull and Bear Markets in Stock Returns." JBES, 18(1). — Duration dependence em bull/bear markets. Evidência empírica de que regimes envelhecem.
- **Ang, A. & Bekaert, G. (2002).** "Regime Switches in Interest Rates." JBES, 20(2). — Aplicação de regime-switching a taxas de juros; referência para TVTP.
- **Guidolin, M. & Timmermann, A. (2007).** "Asset Allocation under Multivariate Regime Switching." JEDC, 31(11). — Como regimes afetam alocação ótima de portfólio; evidência de que ignorar regimes leva a decisões subótimas.
- **Breiman, L. (2001).** "Random Forests." Machine Learning, 45(1). — Referência técnica para feature importance e ensemble methods.
- **Araci, D. (2019).** "FinBERT: Financial Sentiment Analysis with Pre-Trained Language Models." — Paper original do FinBERT; metodologia de fine-tuning para texto financeiro.
