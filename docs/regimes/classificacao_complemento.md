# Market Regimes — Complemento à Taxonomia Operacional

Seções adicionais para integrar ao documento principal de classificação de regimes de mercado. Cada seção foi desenvolvida para complementar e aprofundar a taxonomia existente, com foco em impacto operacional.

---

## Gamma Exposure (GEX) e Fluxos de Dealers como Feature de Regime

A atividade de hedging de market makers de opções é um dos drivers mais poderosos — e menos documentados em frameworks de regime — do comportamento de preço no curto e médio prazo. O Gamma Exposure (GEX) agregado mede a sensibilidade do delta dos dealers a variações de preço, e seu sinal (positivo ou negativo) determina se o mercado tem um "estabilizador automático" ou um "amplificador automático" de movimentos.

### Mecanismo Fundamental

Quando dealers vendem opções (o caso mais comum, já que investidores compram proteção e especulação), eles ficam short gamma. Para manter-se delta-neutral, precisam hedgear dinamicamente:

**GEX Positivo (dealers long gamma):** os dealers compram quando o preço cai e vendem quando o preço sobe. Esse comportamento contracíclico suprime a volatilidade realizada e empurra o mercado para regimes de Ranging, Low Vol ou Mean-Reverting. O preço tende a ser "puxado" de volta a níveis com alta concentração de open interest (efeito "pin" ou "magnet"). Esse efeito é particularmente forte próximo de vencimentos de opções.

**GEX Negativo (dealers short gamma):** os dealers são forçados a vender quando o preço cai (para reduzir delta) e comprar quando o preço sobe. Esse comportamento pró-cíclico amplifica movimentos e favorece regimes de Breakout, Trending, Choppy e Crisis. Quando o GEX é significativamente negativo, os movimentos de preço são auto-reforçantes — exatamente o oposto de quando o GEX é positivo.

**Zona de transição (GEX próximo de zero):** a influência dos dealers é neutra. O preço responde a forças fundamentais e de fluxo sem amplificação nem supressão significativa. Regimes variados são possíveis.

### Cálculo e Fontes de Dados

O GEX agregado é calculado como:

```
GEX = Σ (OI × Gamma × Contrato × 100 × S²) × Sinal_Dealer
```

Onde:

- OI = open interest por strike e vencimento.
- Gamma = gamma da opção naquele strike.
- S = preço do subjacente.
- Sinal_Dealer = +1 se dealers estão long (calls vendidas = dealers long gamma no call; puts vendidas = dealers long gamma no put), -1 se short.

**Simplificação prática:** assumir que dealers estão short calls e long puts até o put open interest exceder um threshold (indicando venda de puts especulativa). Fontes: dados de open interest e volume por strike da exchange (CBOE, CME, Deribit para crypto).

Para quem não tem acesso a dados granulares de OI por strike, proxies úteis incluem:

- **Ratio put/call de volume:** put/call alto → dealers provavelmente long gamma em puts (comprados de hedgers).
- **IV skew 25-delta:** skew muito íngreme → muita demanda por puts → mais gamma nos dealers.
- **Open interest concentrado em poucos strikes:** efeito de "pin" amplificado.

### Greeks de Segunda Ordem como Sinais de Regime

Além do GEX, dois Greeks de segunda ordem são particularmente úteis para antecipar transições de regime:

**Vanna (∂Delta/∂IV ou equivalentemente ∂Vega/∂Spot):** mede a sensibilidade do delta a mudanças na volatilidade implícita. Quando a IV cai (ex: mercado subindo), Vanna positivo faz com que dealers precisem comprar mais delta (comprar o subjacente), amplificando a alta. O fluxo de Vanna é mais forte em ambientes de queda de IV e explica por que mercados em Trending Up com IV caindo têm "momentum gravitacional" — o hedging de Vanna adiciona fluxo comprador estrutural. Quando a IV sobe abruptamente (ex: sell-off), o efeito se inverte, adicionando pressão vendedora.

**Charm (∂Delta/∂Tempo ou Theta do Delta):** mede a mudança de delta com a passagem do tempo. À medida que opções se aproximam do vencimento, o delta de opções ITM se aproxima de 1 (ou -1) e o de OTM se aproxima de 0. Isso gera fluxos de hedge previsíveis, especialmente nas últimas 24-48 horas antes do vencimento. Em dias de OpEx (Options Expiration), o Charm pode ser o driver dominante de preço intraday, criando movimentos que parecem aleatórios mas são mecanicamente explicáveis.

**Vomma (∂Vega/∂IV ou convexidade da volatilidade):** mede a sensibilidade do vega a mudanças na IV. Vomma alto indica que uma mudança na IV terá efeito cascata sobre o hedging. Spikes em Vomma, mesmo em mercados aparentemente calmos, podem sinalizar que o mercado está precificando uma transição de regime iminente — traders de opções estão comprando proteção contra explosão de vol.

### Tabela: GEX como Modulador de Regime

| GEX      | Regime Detectado | Efeito                                                      | Ajuste Operacional                                                                    |
| -------- | ---------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Positivo | Trending Up      | Suprime pullbacks, trend mais suave e ordenado              | Stops mais apertados (pullbacks serão rasos); sizing normal                           |
| Positivo | Ranging          | Reforça a faixa, preço "preso" entre strikes com alto OI    | Mean-reversion mais confiável; pode aumentar sizing de range trades                   |
| Positivo | Breakout         | Falso breakout mais provável (dealers suprimem o movimento) | Exigir filtro de volume mais agressivo; esperar confirmação de D+1                    |
| Negativo | Trending Up      | Rally amplificado, moves mais verticais                     | Trailing stop mais largo (volatilidade intraday maior); cuidado com reversão violenta |
| Negativo | Trending Down    | Sell-off amplificado, cascata de liquidações                | Stops mais largos para shorts (bounces violentos de short covering)                   |
| Negativo | Choppy           | Amplificação de whipsaws — o pior cenário                   | 0% sizing, não operar de forma alguma                                                 |
| Negativo | Low Vol          | Complacência perigosa; breakout iminente será amplificado   | Comprar vol com convicção; straddles mais agressivos                                  |
| Neutro   | Qualquer         | Sem amplificação nem supressão                              | Seguir regime detectado sem ajuste                                                    |

### Datas de Vencimento de Opções (OpEx) como Evento de Regime

Vencimentos mensais (terceira sexta-feira) e trimestrais (março, junho, setembro, dezembro) são eventos de regime temporários que merecem tratamento similar a eventos Tier 2 ou mesmo Tier 1 (para vencimentos trimestrais com volume excepcional).

**Pré-OpEx (2-3 dias antes):** o efeito de "pin" se intensifica. O preço é atraído para strikes com maior open interest. Gamma nos dealers aumenta conforme as opções ATM se aproximam do vencimento. Regime efetivo: Ranging com baixa vol em torno do strike de maior OI.

**Dia de OpEx:** fluxos de Charm dominam. À medida que opções expiram, o gamma desaparece abruptamente. Isso é chamado de "gamma unpin" ou "vol release". O preço, antes preso pelo GEX positivo, fica livre para se mover.

**Pós-OpEx (primeira sessão após):** com o gamma expirado, o mercado fica temporariamente em estado de GEX reduzido. Movimentos que estavam suprimidos podem se materializar. Historicamente, os maiores movimentos semanais em equities frequentemente ocorrem na semana seguinte ao OpEx mensal.

**Recomendação:** incluir `days_to_opex` (distância em dias até o próximo vencimento de opções relevante) e `gex_sign` (+1, 0, -1) como features no modelo de detecção de regime. Tratar dias de OpEx como regime override temporário (similar a Tier 2 na seção de Event-Driven Overrides).

### Perspectiva 1H

No 1H, o GEX é o driver dominante de regime em grande parte das sessões, especialmente em índices líquidos (SPX, QQQ). Um regime de Ranging no 1H em dia com GEX fortemente positivo tem probabilidade muito alta de persistir até o fim da sessão. Inversamente, GEX negativo no 1H antecede os maiores movimentos intraday. Recomendo calcular o GEX antes da abertura (com dados de OI do dia anterior) e usá-lo como filtro de regime para toda a sessão.

### Perspectiva 1D

No diário, o GEX agregado muda mais lentamente (o OI não muda drasticamente dia a dia, exceto perto de vencimentos). O efeito mais útil no diário é a transição de GEX pós-vencimento: o "regime release" após OpEx frequentemente coincide com o início de novas tendências ou breakouts que estavam sendo suprimidos. Monitorar a mudança de GEX de positivo para negativo (ou vice-versa) como sinal antecipado de transição de regime.

---

## Regime de Liquidez como Dimensão Independente

### Conceito

O documento principal trata liquidez como atributo dentro de cada regime (ex: "liquidez evapora em Crisis"). Porém, a liquidez merece ser modelada como dimensão separada porque um mesmo regime direcional se comporta de forma fundamentalmente diferente dependendo do estado de liquidez. Um Trending Up em alta liquidez é um regime limpo e operável; o mesmo Trending Up em baixa liquidez é errático, com slippage alto e gaps inesperados.

Proposta: criar um classificador de liquidez paralelo com 3-4 estados, e usar a combinação (regime_direcional × regime_liquidez) como input para sizing e execução.

### Estados de Liquidez

**Liquid (Normal):** bid-ask spreads apertados, profundidade do book estável, ordens grandes executam sem impacto significativo, reposição rápida de ordens após trades. Este é o estado default — a maioria dos dias de mercado em ativos líquidos.

**Thinning (Deteriorando):** bid-ask spreads alargando gradualmente, profundidade do book diminuindo, impacto de preço por unidade de volume aumentando, reposição de ordens desacelerando. Este estado frequentemente antecede transições de regime (especialmente para Breakout ou Crisis) e é um early warning poderoso.

**Illiquid (Stress):** bid-ask spreads muito acima da média, profundidade do book mínima, ordens de mercado executam com slippage severo (2-5x normal), gaps intraday sem catalisador aparente, market makers recuando ou reduzindo tamanho. Comum durante crises, flash crashes, e em horários de baixa liquidez.

**Vacuum (Colapso):** liquidez efetivamente desaparece em um ou ambos os lados do book. Preço pode "pular" níveis inteiros sem transações intermediárias. Circuit breakers podem ser acionados. Exclusivo de crises severas e flash crashes.

### Métricas para Detecção de Regime de Liquidez

**Bid-Ask Spread Normalizado:**

```
Spread_norm(t) = Spread(t) / Spread_MA(50)
```

- Liquid: < 1.2
- Thinning: 1.2 - 2.0
- Illiquid: 2.0 - 5.0
- Vacuum: > 5.0

**Profundidade do Book (Market Depth):**
Soma do volume disponível nos N melhores níveis de bid e ask. Normalizar pela média histórica.

```
Depth_ratio(t) = Depth(t) / Depth_MA(50)
```

- Liquid: > 0.7
- Thinning: 0.4 - 0.7
- Illiquid: 0.15 - 0.4
- Vacuum: < 0.15

**Kyle's Lambda (Impacto de Preço):**
Mede quanto o preço se move por unidade de volume negociado. Estimado via regressão de variação de preço em volume assinado (signed volume).

```
ΔP = λ × Volume_assinado + ε
```

Lambda alto → baixa liquidez (cada trade move mais o preço).

**Amihud Illiquidity Ratio:**

```
ILLIQ(t) = |R(t)| / Volume(t)
```

Onde R(t) é o retorno do período. Medida simples que funciona bem no diário. Normalizar por percentil histórico.

**Velocidade de Reposição (Quote-to-Trade Ratio):**
Número de atualizações de cotação por trade executado. Ratio caindo → market makers estão se retirando.

**Roll Measure (para dados de baixa frequência):**
Quando não há dados de microestrutura (caso de crypto em exchanges menores, ou ativos de baixa liquidez):

```
Roll = 2 × sqrt(-Cov(ΔP_t, ΔP_{t-1}))
```

A covariância negativa dos retornos consecutivos é um proxy do bid-ask bounce (spread implícito).

### Tabela de Interação: Regime Direcional × Regime de Liquidez

| Regime Direcional | Liquid                         | Thinning                                             | Illiquid                                                | Vacuum                                |
| ----------------- | ------------------------------ | ---------------------------------------------------- | ------------------------------------------------------- | ------------------------------------- |
| Trending Up       | Sizing 100%; stops normais     | Sizing 75%; stops 20% mais largos                    | Sizing 50%; stops 40% mais largos; ordens limit only    | Sair na primeira oportunidade         |
| Trending Down     | Sizing 100%; stops normais     | Sizing 75%; cuidado com bounces amplificados         | Sizing 50%; não shortar com market orders               | Sair; não operar                      |
| Ranging           | Sizing normal do regime        | Reduzir para 50%; possível transição para breakout   | Não operar; possível flash crash dentro do range        | Sair completamente                    |
| Mean-Reverting    | Sizing normal do regime        | Reduzir sizing; alargar stops para acomodar slippage | Mean-reversion pode não funcionar (gaps destroem edge)  | Não operar                            |
| Breakout          | Sizing 100%; entrada no retest | Sizing 75%; breakout pode ser amplificado            | Alta probabilidade de false breakout por baixa liquidez | Não operar                            |
| Choppy            | Sizing mínimo                  | 0% — thinning + choppy = destruição garantida        | 0%                                                      | 0%                                    |
| Crisis            | Hedge ativo; execução viável   | Execução já comprometida; aceitar slippage moderado  | Execução muito comprometida; usar opções se possível    | Aceitar qualquer saída; sobrevivência |

### Perspectiva 1H

A liquidez intraday tem padrões previsíveis (o U-shape mencionado no documento principal), mas o regime de liquidez pode se desviar drasticamente desse padrão em dias de stress. Recomendo calcular o Depth_ratio e Spread_norm em tempo real a cada 15 minutos e compará-los com o esperado para aquele horário. Um desvio de 2x do esperado para aquela hora é sinal de mudança de regime de liquidez. Exemplo: se o spread no almoço (tipicamente largo) está 3x o spread normal do almoço, a liquidez está deteriorando além do padrão sazonal — treat como Thinning ou Illiquid.

### Perspectiva 1D

No diário, o Amihud Illiquidity Ratio e o volume normalizado são suficientes como features de liquidez. Períodos de liquidez diária em deterioração (Amihud subindo por 5+ dias) frequentemente antecedem sell-offs significativos em 1-2 semanas — a liquidez seca antes que o preço reaja. Isso é um early warning que complementa os indicadores de regime direcional.

---

## Order Flow e Microestrutura como Features de Detecção

### Contexto

O documento principal menciona order flow brevemente na seção de timeframe 1H, mas sem detalhar quais features usar e como integrá-las ao classificador de regime. Para operações intraday (1H e menores), features de order flow detectam transições de regime significativamente antes que indicadores tradicionais baseados em preço (ADX, EMAs) reajam — a vantagem pode ser de 2-8 barras horárias.

### Features de Order Flow para Detecção de Regime

**1. Cumulative Volume Delta (CVD):**
Diferença acumulada entre volume comprador (agressivo, executando no ask) e volume vendedor (agressivo, executando no bid).

```
CVD(t) = Σ (Volume_at_ask - Volume_at_bid)
```

- CVD subindo com preço subindo → Trending Up com convicção (compradores agressivos dominam).
- CVD caindo com preço subindo → Distribution (preço sobe por falta de vendedores, não por compradores agressivos). Alerta precoce de que o trend está frágil.
- CVD subindo com preço caindo → Accumulation (compradores absorvendo oferta sem mover preço).
- CVD caindo com preço caindo → Trending Down com convicção.
- CVD flat com preço volátil → Choppy (nenhum lado domina).

**Integração ao modelo:** divergência entre direção do CVD e direção do preço por 3+ barras no 1H é um sinal antecipado de transição de regime com alta confiabilidade.

**2. Delta por Nível de Preço (Volume Profile Delta):**
Dentro do perfil de volume, calcular o delta (buy vs sell) em cada nível de preço. Isso revela onde os compradores e vendedores agressivos estão concentrados.

- Forte delta comprador no POC (Point of Control) → suporte real, não apenas histórico.
- Forte delta vendedor em levels de resistência → resistência com convicção institucional.
- Delta neutro em zona de alto volume → equilíbrio real = Ranging ou Mean-Reverting.

**3. Imbalance do Book de Ofertas (Bid-Ask Imbalance):**

```
Imbalance(t) = (Volume_Bid - Volume_Ask) / (Volume_Bid + Volume_Ask)
```

Calculado nos N melhores níveis de preço do order book.

- Imbalance persistentemente positivo (mais bids que asks) → demanda latente, favorece upside.
- Imbalance persistentemente negativo → oferta latente, favorece downside.
- Imbalance oscilando rapidamente → Choppy ou Ranging.

**Nota:** essa feature é mais útil em mercados com order book transparente (futuros, crypto spot). Em equities com dark pools, grande parte do fluxo é invisível.

**4. Absorção e Exaustão:**

**Absorção:** volume alto em um nível de preço que não se move (ou move pouco). Indica que um lado do mercado está absorvendo a agressividade do outro. Absorção no suporte → Accumulation. Absorção na resistência → Distribution.

Detecção:

```
Absorção = (Volume no nível > 2x média) AND (Movimento de preço < 0.3x ATR no período)
```

**Exaustão:** volume alto com desaceleração de momentum. O preço move, mas a taxa de variação está diminuindo apesar do volume crescente. Indica que o último impulso do trend está se esgotando.

Detecção:

```
Exaustão = (Volume > 2x média) AND (|ΔPreço atual| < 0.5 × |ΔPreço anterior|)
```

**5. Taxa de Cancelamento de Ordens (Cancel-to-Fill Ratio):**
Proporção de ordens colocadas que são canceladas antes de serem executadas.

- Ratio subindo → market makers ficando nervosos, liquidez se retirando. Early warning de transição para Thinning e possível Breakout ou Crisis.
- Ratio estável → market normal, regime provavelmente estável.

**6. Sweeps (Varredura de Liquidez):**
Ordens agressivas que consomem múltiplos níveis de preço de uma vez. Indicam urgência institucional.

- Sweep de compra → breakout bullish iminente ou short covering forçado.
- Sweep de venda → breakout bearish ou liquidação.
- Sweeps bidirecionais em sequência → Choppy, stop hunting, ou pré-evento.

### Tabela: Features de Order Flow como Sinais Antecipados de Transição

| Sinal de Order Flow                                          | Transição Antecipada               | Latência (1H) | Confiabilidade |
| ------------------------------------------------------------ | ---------------------------------- | ------------- | -------------- |
| CVD divergindo do preço por 3+ barras                        | Regime atual → regime oposto       | 2-5 barras    | Alta           |
| Absorção repetida no suporte com CVD subindo                 | Trending Down → Accumulation       | 3-8 barras    | Alta           |
| Absorção repetida na resistência com CVD caindo              | Trending Up → Distribution         | 3-8 barras    | Alta           |
| Exaustão de volume em rally (volume alto + preço desacelera) | Trending Up → Distribution/Ranging | 1-3 barras    | Média-Alta     |
| Sweep agressivo rompendo nível key com follow-through        | Ranging/Low Vol → Breakout         | 0-1 barras    | Média          |
| Cancel-to-fill ratio spike + depth caindo                    | Qualquer → Thinning/Illiquid       | 2-4 barras    | Alta           |
| Bid-ask imbalance invertendo de forma sustentada             | Trending → reversão                | 3-6 barras    | Média          |

### Integração ao Modelo de Detecção

As features de order flow podem ser incorporadas ao classificador de duas formas:

**1. Como features adicionais no modelo existente:** adicionar CVD_direction, Absorption_score, Imbalance_rolling, e Sweep_count ao vetor de features do HMM ou XGBoost. Isso é direto mas requer dados de nível 2 (order book) ou nível 3 (individual orders).

**2. Como filtro confirmatório (mais prático):** usar o modelo de regime baseado em preço como classificador primário e as features de order flow como validação. Se o modelo diz Trending Up mas o order flow mostra absorção na resistência + CVD divergindo, a confiança do regime cai (reduzir C_consistency no Confidence Score).

**Recomendação:** para quem está começando, a abordagem 2 é muito mais prática. O CVD sozinho já é extremamente informativo e está disponível na maioria das plataformas (TradingView, Sierra Chart, Bookmap).

### Disponibilidade por Asset Class

| Asset Class   | Nível 1 (Trades) | Nível 2 (Book) | Nível 3 (Orders) | CVD Disponível | Notas                                         |
| ------------- | ---------------- | -------------- | ---------------- | -------------- | --------------------------------------------- |
| Equities      | Sim (tape)       | Parcial (NBBO) | Limitado         | Sim (estimado) | Dark pools escondem ~40% do fluxo             |
| Futuros       | Sim              | Sim (DOM)      | Sim (CME MBO)    | Sim (preciso)  | Melhor fonte de order flow                    |
| FX (spot)     | Sim              | Parcial        | Não              | Estimado       | ECNs fragmentadas; EBS e Reuters para majors  |
| Crypto (spot) | Sim              | Sim            | Parcial          | Sim            | Exchanges centralizadas têm book transparente |
| Crypto (perp) | Sim              | Sim            | Parcial          | Sim            | Funding rate adiciona dimensão extra          |

---

## Estratégias de Opções Mapeadas por Regime

### Princípio

Cada regime de mercado implica um perfil específico de volatilidade, direcionalidade e velocidade de movimento. Opções permitem expressar visões sobre todas essas dimensões simultaneamente. O mapeamento regime → estrutura de opções elimina a "paralisia de escolha" que muitos traders enfrentam ao selecionar estratégias de opções.

### Conceitos-Chave para Seleção de Estratégia

**IV Percentile (IVP):** onde a volatilidade implícita atual está em relação ao seu histórico de 1 ano. IVP alta (>60) → opções caras → favorece venda de vol. IVP baixa (<30) → opções baratas → favorece compra de vol.

**IV vs RV (Implied vs Realized Volatility):** se IV > RV consistentemente, vendedores de vol têm edge (variance risk premium positivo). Se IV < RV, o mercado está subestimando o risco.

**Skew:** a inclinação do smile de volatilidade. Skew íngreme (puts muito mais caras que calls) → mercado precificando risco de queda → estruturas que se beneficiam de skew são mais eficientes.

**Prazo de Vencimento:** regimes de curta duração (Breakout, Choppy) pedem vencimentos curtos (7-21 DTE). Regimes de longa duração (Trending, Recovery) permitem vencimentos mais longos (30-60 DTE). Regimes incertos (NoLabel, Low Vol aguardando resolução) pedem 30-45 DTE para ter tempo sem pagar theta excessivo.

### Tabela de Mapeamento: Regime → Estratégia de Opções

| #   | Regime         | Estratégia Primária                           | Estratégia Secundária                      | Greek Dominante   | DTE Ideal | IVP Condition         | Risco Principal                            |
| --- | -------------- | --------------------------------------------- | ------------------------------------------ | ----------------- | --------- | --------------------- | ------------------------------------------ |
| 0   | NoLabel        | Nenhuma; ou iron condor curto com sizing mín. | Cash; ou collar em posição existente       | Theta (se vender) | 14-21     | Qualquer              | Transição inesperada                       |
| 1   | Trending       | Vertical spread na direção da tendência       | Calendar spread (longo venc. na direção)   | Delta + Theta     | 30-45     | Qualquer              | Reversão súbita                            |
| 2   | Trending Up    | Bull call spread ou bull put spread (credit)  | LEAPS calls; protective puts como seguro   | Delta             | 30-45     | Melhor se IVP<50      | Correção violenta; theta em débito spreads |
| 3   | Trending Down  | Bear put spread ou bear call spread (credit)  | Long puts; put backspread                  | Delta (negativo)  | 21-45     | IVP alta = crédito    | Short squeeze; bounce violento             |
| 4   | Ranging        | Iron condor; short strangle (se exp.)         | Nenhuma com alta convicção                 | Theta + Vega(neg) | 21-30     | IVP > 40              | Breakout inesperado                        |
| 5   | Mean-Reverting | Short strangle nos extremos do z-score        | Iron butterfly centrado no eixo            | Theta + Vega(neg) | 14-30     | IVP > 40              | Transição para trending                    |
| 6   | Low Vol        | Long straddle; long strangle                  | Calendar spread (comprar vol curta barata) | Vega + Gamma      | 30-45     | IVP < 30 (ideal)      | Time decay se vol não expandir             |
| 7   | Breakout       | Vertical spread na direção do breakout        | Long call/put direcional                   | Delta + Gamma     | 14-30     | Qualquer              | Falso breakout; reversão violenta          |
| 8   | Choppy         | Iron condor largo; ou nenhuma                 | Short-term iron butterfly                  | Theta             | 7-14      | IVP > 50 (vender)     | Whipsaw que ultrapassa strikes             |
| 9   | Crisis         | Long puts; put backspread; VIX calls          | Reverse risk (long put + short call)       | Delta(neg) + Vega | 30-60     | IVP alta mas justif.  | Dead cat bounce stopando puts              |
| 10  | Recovery       | Bull call spread; short puts                  | Risk reversal (long call + short put)      | Delta + Theta     | 30-60     | IVP > 40 (coleta)     | Falsa recovery (dead cat bounce)           |
| 11  | Distribution   | Protective puts; collars                      | Bear put spread; put calendar              | Delta(neg) + Vega | 30-60     | IVP<40 = puts baratas | Invalidação (novo topo com breadth forte)  |
| 12  | Accumulation   | Short puts OTM (disposição de comprar)        | Bull put spread largo; long calls LEAPS    | Theta + Delta     | 30-60     | IVP > 40 (coleta)     | Continuação da queda                       |
| 13  | Blow-off       | Put spreads como seguro; collars agressivos   | Long puts OTM (tail hedge)                 | Vega + Delta(neg) | 14-30     | IVP subindo (caro)    | Timing errado do topo                      |

### Detalhamento de Estruturas-Chave por Regime

**Trending Up — Bull Call Spread:**
Comprar call ATM (ou ligeiramente ITM), vender call OTM. Captura direcionalidade com custo limitado. O spread financia parte do theta da call comprada. Escolher strikes de modo que o delta líquido do spread seja ~0.30-0.40. Rolar a posição a cada 15-20 dias para manter exposição sem acumular theta decay excessivo.

**Low Vol — Long Straddle:**
Comprar call + put ATM com vencimento 30-45 dias. Theta é o inimigo, mas se a compressão de vol se resolver (como esperado), o ganho em gamma e vega compensa. Timing: entrar quando o Bollinger Bandwidth diário estiver no percentil <10 E o IV percentile estiver <25 (vol implícita tão baixa quanto a realizada — opções precificando incorretamente a complacência).

**Crisis — Put Backspread (Ratio Put Spread):**
Vender 1 put ATM, comprar 2 puts OTM. Custo zero ou pequeno crédito. Se o mercado colapsa, as 2 puts OTM ganham mais do que a 1 put vendida perde. Payoff convexo: perda máxima limitada (entre os strikes), ganho ilimitado na queda. Ideal quando o skew está íngreme (puts OTM relativamente baratas em termos de vol per dollar of protection).

**Distribution — Collar:**
Possuir o ativo + comprar put OTM + vender call OTM. Custo zero se os strikes forem simétricos. Protege contra a queda que a distribution antecipa enquanto mantém exposição parcial à alta (caso a distribution seja falsa). A call vendida financia a put comprada. Ideal quando a convicção de distribution é média-alta mas não absoluta.

**Recovery — Short Puts:**
Vender puts OTM (delta 0.15-0.25) em ativos que você quer possuir. Se o ativo continuar subindo (recovery funciona), coleta o prêmio. Se o ativo cair e a put for exercida, compra o ativo a um preço com desconto (strike - prêmio). IVP alta durante recovery (vol ainda elevada de crise recente) significa prêmios suculentos. Essa estratégia se alinha com a recomendação do regime Recovery de "construir posição long gradualmente".

### Greeks Dominantes por Regime — Resumo Visual

| Regime         | Delta         | Gamma    | Theta     | Vega     |
| -------------- | ------------- | -------- | --------- | -------- |
| Trending Up    | ++ Long       | Neutro   | Neutro    | Neutro   |
| Trending Down  | -- Short      | Neutro   | Neutro    | Neutro   |
| Ranging        | Neutro        | Neutro   | ++ Coleta | -- Short |
| Mean-Reverting | Neutro        | Neutro   | ++ Coleta | -- Short |
| Low Vol        | Neutro        | ++ Long  | -- Paga   | ++ Long  |
| Breakout       | ± Direcional  | + Long   | - Paga    | + Long   |
| Choppy         | Neutro        | -- Short | + Coleta  | -- Short |
| Crisis         | -- Short      | + Long   | - Paga    | ++ Long  |
| Recovery       | + Long        | Neutro   | + Coleta  | - Short  |
| Distribution   | - Hedged      | + Long   | - Paga    | + Long   |
| Accumulation   | + Construindo | Neutro   | + Coleta  | - Short  |
| Blow-off       | Hedged        | + Long   | - Paga    | + Long   |

---

## Regime de Correlação como Dimensão Independente

### Conceito

Correlações entre ativos não são constantes — elas próprias operam em regimes. A seção existente sobre Correlação entre Regimes de Múltiplos Ativos cobre pares de monitoramento e sinais cross-asset, mas não modela o estado de correlação como variável de regime.

Proposta: classificar o "regime de correlação" do portfólio em estados discretos, similar aos regimes direcionais, e usar isso como modulador de sizing e diversificação.

### Estados de Correlação

**Correlação Normal:** correlações entre ativos de risco estão próximas de suas médias históricas. Diversificação funciona como esperado. Este é o estado em que a maioria dos modelos de portfólio é calibrada.

**Correlação Elevada (Convergência):** correlações entre ativos de risco sobem significativamente. Diversificação enfraquece. Comum em sell-offs e crises (todos os ativos de risco caem juntos) e também em rallies eufóricos de risk-on (tudo sobe junto). O risco de portfólio real é maior do que o modelo baseline sugere.

**Descorrelação Anômala (Divergência):** correlações históricas se invertem ou quebram de forma inesperada. Exemplo: ações e bonds caindo juntos (como em 2022 — taper tantrum / stagflation), ou USD caindo enquanto equities também caem. Esse estado é o mais perigoso para portfólios que dependem de hedging via correlação negativa (ex: 60/40 stocks/bonds).

**Rotação Setorial (Dispersão Alta):** o índice fica relativamente flat mas componentes individuais divergem significativamente. Correlação intra-índice cai. Setores rodam — dinheiro sai de tech e entra em industrials, etc. Diversificação entre setores é alta mas o alpha está na seleção setorial, não na direcionalidade do índice.

### Métricas de Detecção

**Correlação Rolling Percentile:**

```
Corr_pct(t) = Percentile(Corr_rolling_20d(t), Corr_history_1year)
```

- Normal: percentil 20-80
- Elevada: > percentil 80
- Anômalamente Baixa: < percentil 20 (rotação ou dislocation)

**Implied Correlation (IC):**
Derivada de preços de opções de índice vs. opções de componentes individuais.

```
IC = (σ²_index - Σw²ᵢσ²ᵢ) / (Σᵢ≠ⱼ wᵢwⱼσᵢσⱼ)
```

IC alta → mercado precifica que componentes vão se mover juntos → convergência.
IC baixa → mercado precifica dispersão → rotação setorial.

A vantagem da IC é que é forward-looking (baseada em IV, não em realized correlation).

**Dispersion Index:**

```
Dispersion(t) = σ(retornos dos N componentes) no período t
```

Dispersão alta = componentes divergindo = correlação baixa.
Dispersão baixa = componentes convergindo = correlação alta.

**Cross-Sector Correlation Matrix:**
Calcular correlação rolling entre os 11 setores do S&P 500 e monitorar o eigenvalue máximo da matriz de correlação. Eigenvalue dominante subindo → mais variância explicada por 1 fator (mercado) → convergência. Eigenvalue dominante caindo → dispersão.

### Tabela de Ajuste por Regime de Correlação

| Regime Correlação       | Efeito na Diversificação                         | Ajuste de Sizing                                              | Ajuste de Hedge                                                    |
| ----------------------- | ------------------------------------------------ | ------------------------------------------------------------- | ------------------------------------------------------------------ |
| Normal                  | Funciona como modelado                           | Sizing normal; confiar no modelo de risco                     | Hedges standard (VIX, treasuries)                                  |
| Convergência (Risk-On)  | Diversificação fraca; tudo sobe junto            | Reduzir exposição total em 20-30% (risco real > modelado)     | Comprar proteção barata (vol baixa em risk-on = puts baratas)      |
| Convergência (Risk-Off) | Diversificação colapsa; tudo cai junto           | Reduzir exposição em 40-50%; aumentar cash                    | Hedges tradicionais podem falhar; cash é o melhor hedge            |
| Descorrelação Anômala   | Relações históricas quebram                      | Sizing mínimo até normalizar; modelo de risco não é confiável | Reavaliar todos os hedges; correlação negativa pode estar quebrada |
| Rotação Setorial        | Diversificação intra-índice alta; alpha setorial | Sizing total pode ser normal; concentrar em setores fortes    | Hedge de índice menos necessário; long-short setorial              |

### Regime Coherence Index (RCI) — Expansão

O documento principal propõe o RCI como média dos scores de coerência entre pares. Sugiro expandir o RCI com a dimensão temporal:

**RCI_trend(t) = (RCI(t) - RCI(t-5)) / 5**

- RCI_trend positivo → coerência aumentando → convicção crescendo → sizing pode aumentar.
- RCI_trend negativo → coerência deteriorando → reduzir sizing proativamente → algo está mudando.
- RCI_trend perto de zero → coerência estável → manter posição atual.

---

## Técnicas de Detecção Mais Recentes

### Ensemble HMM + Tree-Based Models (Framework de Votação Multi-Modelo)

Pesquisa publicada em 2025 propõe combinar HMM com modelos de ensemble (bagging e boosting) via hybrid voting classifiers. A ideia é que HMM captura bem a dinâmica temporal (transições entre estados) mas é fraco em features estáticas, enquanto Random Forests e XGBoost são bons classificadores de features mas não modelam transições explicitamente.

**Implementação prática:**

1. Treinar HMM nos retornos e volatilidade → produz probabilidades de estado.
2. Treinar XGBoost no vetor completo de features (incluindo indicadores técnicos e macro) → produz probabilidades de regime.
3. Combinar via votação ponderada: se ambos concordam, confiança alta; se divergem, confiança baixa (→ NoLabel ou sizing reduzido).
4. Validar via walk-forward: treinar em janela de 2-5 anos, testar em 6-12 meses, rolar.

**Vantagem sobre HMM puro:** o ensemble reduz a taxa de falsos positivos em ~20-30% (estimativa baseada nos resultados publicados) porque o XGBoost pode capturar padrões não-lineares que o HMM com distribuições Gaussianas perde.

### Bayesian Online Change-Point Detection (BOCPD)

Abordagem que detecta mudanças de regime em tempo real sem definir estados a priori. Em vez de classificar "o mercado está em Trending Up", o BOCPD responde à pergunta "o processo gerador dos dados mudou?".

**Como funciona:**

1. Manter uma distribuição posterior sobre o "run length" (quantos períodos desde a última mudança).
2. A cada novo dado, calcular a probabilidade de change-point vs. continuação.
3. Se a probabilidade de change-point exceder um threshold, sinalizar transição.

**Score-Driven BOCPD** (variante recente): incorpora correlação temporal e parâmetros time-varying dentro de cada regime, melhorando a performance em dados financeiros que não são i.i.d. mesmo dentro de regimes.

**Integração ao framework existente:** usar BOCPD como "alarme de transição" que antecede o classificador de regime. Quando o BOCPD sinaliza change-point, ativar monitoramento intensivo e reduzir confiança no regime atual (equivalente a puxar C_duration para baixo imediatamente). O classificador de regime (HMM/XGBoost) continua sendo o que atribui o label — o BOCPD apenas diz "algo mudou" sem dizer o quê.

**Aplicação prática testada:** aplicado a dados de order flow no NASDAQ, BOCPD detectou regimes de flow (onde buy orders seguem buy orders persistentemente) que coincidiram com movimentos direcionais relevantes. A latência de detecção foi significativamente menor que HMM padrão.

### Path Signatures para Dados de Alta Dimensão

Método baseado em rough path theory que usa "signatures" — representações algébricas de paths — como feature map para detecção de regime. Particularmente útil para:

- Dados multidimensionais (múltiplos ativos simultaneamente).
- Dados path-dependent (onde a trajetória importa, não apenas o ponto atual).
- Dados com autocorrelação (que violam premissas de i.i.d.).

**Como funciona simplificado:**

1. Representar os dados recentes como um caminho multidimensional (ex: retornos de 10 ativos nos últimos 20 dias = um path em R^10).
2. Calcular a signature truncada desse path (um vetor de features que resume toda a informação da trajetória).
3. Usar a signature como input para um classificador de regime ou como métrica de similaridade entre períodos.

**Two-sample test para detecção online:** comparar a signature do período recente com a signature do regime atual. Se a distância exceder um threshold, sinalizar mudança de regime. Vantagem: não requer definir estados a priori (como BOCPD), mas é mais robusto a dados de alta dimensão.

**Aplicação demonstrada:** aplicado a baskets de equities e crypto, detectou com precisão períodos de turbulência histórica com latência baixa.

### Abordagem de "Momentos Análogos" (Mulliner, Harvey et al., 2025)

Método que identifica regimes não por classification em categorias predefinidas, mas por similaridade com períodos históricos. A ideia central: o regime atual é definido como "o conjunto de períodos históricos com condições macro mais similares às atuais".

**Implementação:**

1. Definir um vetor de condições macro/técnicas atuais (taxas de juros, inflação, growth, vol, credit spreads, etc.).
2. Calcular a distância entre o vetor atual e todos os vetores históricos.
3. Os períodos mais similares definem o "regime análogo".
4. A performance subsequente desses períodos análogos gera uma distribuição forward-looking de retornos.

**Resultado empírico:** testado em 6 fatores de equities de 1985-2024, a estratégia baseada em momentos análogos gerou alpha estatisticamente significativo (3 desvios padrão de zero). Houve correlação positiva entre similaridade dos momentos e performance — os períodos mais similares tinham melhor poder preditivo.

**Integração ao framework:** pode ser usado como layer complementar ao classificador de regime. Em vez de apenas atribuir um label, verificar "historicamente, períodos com condições similares ao estado atual tiveram performance X nos próximos 20 dias". Isso adiciona uma dimensão probabilística forward-looking ao regime detection.

### HMM + Reinforcement Learning para Portfolio Management

Fronteira ativa de pesquisa que combina detecção de regime via HMM com otimização de portfólio via RL.

**Conceito:**

1. HMM detecta o regime atual (estado oculto).
2. O agente de RL recebe o regime como parte do estado de observação.
3. O agente aprende a política ótima de alocação condicionada ao regime.

**Vantagem sobre regras fixas por regime:** as regras de sizing e alocação por regime (como a tabela de sizing no documento principal) são heurísticas estáticas. O RL pode descobrir políticas mais nuanceadas — por exemplo, "em Trending Up com recovery recente de Crisis, alocar mais agressivamente do que em Trending Up contínuo" — sem que o trader precise especificar essas regras manualmente.

**Limitação prática:** requer significativamente mais dados e infraestrutura computacional. Mais apropriado para operações sistemáticas de médio porte para cima. Para traders individuais, as tabelas heurísticas do documento principal são suficientes.

---

## Regime-Aware Execution (Algoritmos de Execução por Regime)

### Princípio

O documento principal cobre sizing (quanto) e stops (onde sair) por regime, mas não aborda a execução (como entrar e sair). A forma de executar uma ordem deve mudar conforme o regime, porque as condições de liquidez, volatilidade e microestrutura variam dramaticamente entre regimes.

### Tabela de Execução por Regime

| #   | Regime         | Tipo de Ordem Preferido              | Algoritmo de Execução                                | Urgência    | Slippage Esperado | Notas                                                                |
| --- | -------------- | ------------------------------------ | ---------------------------------------------------- | ----------- | ----------------- | -------------------------------------------------------------------- |
| 0   | NoLabel        | Limit                                | Passivo; não perseguir                               | Baixa       | Mínimo            | Sem urgência — se não executar, ok                                   |
| 1   | Trending       | Limit agressivo (próximo ao ask/bid) | Entrar em pullbacks; limit no bid/ask                | Média       | 0.5-1x spread     | Balancear urgência com qualidade de preço                            |
| 2   | Trending Up    | Limit no bid + paciência             | Esperar pullback; buy limit escalonado               | Média       | 0.5x spread       | Pullbacks acontecem; não perseguir rally                             |
| 3   | Trending Down  | Limit no ask + paciência             | Short em bounces; sell limit escalonado              | Média       | 0.5x spread       | Bounces são oportunidades; não shortar na queda                      |
| 4   | Ranging        | Limit nos extremos do range          | Ordens limit no suporte/resistência                  | Baixa       | Mínimo            | Tempo é aliado; colocar e esperar                                    |
| 5   | Mean-Reverting | Limit nos extremos de z-score        | Escalonado: 1/3 em z=1.5, 1/3 em z=2.0, 1/3 em z=2.5 | Baixa-Média | Mínimo            | Não usar market; reversão pode demorar                               |
| 6   | Low Vol        | Stop orders condicionais             | Bracket: buy stop acima + sell stop abaixo da range  | Baixa       | Mínimo            | Entrada automática no breakout; sem pressa                           |
| 7   | Breakout       | Market ou Limit agressivo            | Entrada imediata na confirmação de breakout          | Alta        | 1-2x spread       | Velocidade importa mais que preço perfeito; slippage é custo do edge |
| 8   | Choppy         | NÃO OPERAR                           | Se pego posicionado: market para sair                | N/A         | 1-3x spread       | Sair na primeira oportunidade; aceitar slippage                      |
| 9   | Crisis         | Market (para sair)                   | Sair na primeira janela de liquidez                  | Máxima      | 2-5x spread       | Aceitar qualquer preço; sobrevivência > otimização                   |
| 10  | Recovery       | Limit escalonado                     | Entrar em tranches: 1/3, 1/3, 1/3                    | Média       | 0.5-1x spread     | Urgência moderada; recovery é gradual                                |
| 11  | Distribution   | Limit no ask (para vender)           | Vender em rallies intraday; escalonado               | Média       | 0.5x spread       | Vender em força, não em fraqueza                                     |
| 12  | Accumulation   | Limit no bid (para comprar)          | Comprar em dips; escalonado 1/3                      | Baixa       | Mínimo            | Paciência; accumulation dura semanas                                 |
| 13  | Blow-off       | Trailing stop automático             | Stop agressivo; saída automática                     | Alta        | 1-2x spread       | Sem intervenção manual; deixar o stop mecânico decidir               |

### Algoritmos de Execução Avançados por Regime

**TWAP (Time-Weighted Average Price):** dividir a ordem em partes iguais executadas ao longo de um período de tempo. Ideal para regimes de baixa urgência (Ranging, Mean-Reverting, Accumulation) onde o objetivo é minimizar impacto de preço.

**VWAP (Volume-Weighted Average Price):** executar a ordem proporcional ao volume de mercado. Ideal para Trending (seguir o fluxo natural do mercado) e Recovery (entrar gradualmente acompanhando o volume). Evitar em Crisis (volume é anormal e errático).

**Implementation Shortfall / Arrival Price:** minimizar a diferença entre o preço de decisão e o preço de execução. Balanceia timing risk vs. market impact. Ideal para Breakout (urgência alta mas quer minimizar slippage) e Distribution/Accumulation (posições grandes que precisam ser executadas sem mover o mercado).

**Iceberg Orders:** mostrar apenas uma fração do tamanho total da ordem. Essencial em Accumulation e Distribution quando o tamanho da posição é grande relativo à liquidez. Se a posição total é >5% do volume diário médio, usar iceberg para evitar sinalizar intenção.

**Ordens Escalonadas (Scaling In/Out):** já mencionadas no documento principal para Accumulation (1/3, 1/3, 1/3) e Distribution. Formalizar: cada tranche deve ser executada em sessões diferentes e preferencialmente em momentos de liquidez oposta à intenção (comprar no dip da abertura, vender no rally da abertura).

### Perspectiva 1H

No 1H, a execução é mais sensível ao horário do dia:

- **Primeira hora (abertura):** liquidez alta mas volátil. Spreads apertam rápido mas ordens podem ser executadas a preços que revertem em minutos. Usar limit orders com paciência. Exceção: saída de posições em Crisis — usar market.
- **Meio do dia (11:30-14:00 EST):** liquidez mais baixa, spreads podem alargar. Evitar execução de ordens grandes. Bom para colocar limit orders passivas que executam ao longo do tempo.
- **Última hora (power hour):** liquidez retorna. Movimentos direcionais frequentemente acontecem aqui. Bom momento para executar na direção do regime do dia.

### Perspectiva 1D

No diário, a execução intraday é menos relevante (o preço de entrada importa menos quando o holding period é de dias a semanas). Porém, para posições grandes (>1% do volume diário), dividir a execução em 2-3 dias usando TWAP ou VWAP para minimizar impacto.

---

## Regime para Renda Fixa e Curva de Juros

### Regimes mais frequentes em Renda Fixa

**Regimes mais frequentes:** Ranging (quando expectativas de política monetária estão estáveis), Trending (alinhado a ciclos de aperto/afrouxamento do banco central), Mean-Reverting (yields tendem a reverter a médias de longo prazo).

**Regimes menos frequentes:** Blow-off (apenas em crises soberanas ou hyperinflation), Choppy (em torno de reuniões do FOMC com incerteza alta).

### Regimes da Curva de Juros

A forma da curva de juros é uma das variáveis macro mais informativas para regimes de outros asset classes. Quatro estados principais:

**Bull Steepening (yields caindo, curto cai mais que longo):** expectativa de corte de juros. Favorece risk-on em equities. Trending Up em bonds. Recovery provável em equities se vindo de crise.

**Bear Steepening (yields subindo, longo sobe mais que curto):** expectativa de inflação ou prêmio de prazo subindo. Perigoso para equities (custo de capital subindo). Pode acompanhar Trending Down em equities ou Distribution.

**Bull Flattening (yields caindo, longo cai mais que curto):** flight-to-quality clássico. Longo prazo buscado como safe haven. Confirma Crisis/Risk-Off em equities.

**Bear Flattening (yields subindo, curto sobe mais que longo):** aperto monetário ativo. Fed subindo taxa. Inversão da curva iminente. Historicamente antecede recessão em 12-18 meses.

**Inversão (yield curto > yield longo):** sinal mais confiável de recessão futura. Quando a curva inverte, equities podem continuar subindo por 6-18 meses antes da recessão/bear market começar.

### Features da Curva para Detecção de Regime em Outros Ativos

**Slope (inclinação):**

```
Slope = Yield_10Y - Yield_2Y
```

- Slope positivo e subindo → expansão → Trending Up em equities.
- Slope se achatando → aperto → cautela.
- Slope negativo (inversão) → recessão à frente → Distribution ou late-cycle.

**Curvature (curvatura):**

```
Curvature = 2 × Yield_5Y - Yield_2Y - Yield_10Y
```

Curvatura elevada → belly da curva precificando incerteza acima do interpolado. Frequentemente antecede transições de política monetária.

**Nível absoluto de rates:**

- Rates em máximas com curva flat → restritivo → risco de Trending Down em equities.
- Rates em mínimas com curva steep → acomodatício → favorece Trending Up em equities.

**Real rates (nominal - breakeven inflation):**
Real rates subindo agressivamente é o cenário mais negativo para todos os ativos de risco (equities, credit, commodities, crypto). Indica aperto genuíno de condições financeiras.

### Integração ao Framework de Regime

Recomendo incluir três features derivadas da curva de juros no classificador de regime:

1. `yield_curve_slope` = Yield_10Y - Yield_2Y (z-score rolling de 1 ano).
2. `yield_curve_slope_change_20d` = variação do slope nos últimos 20 dias.
3. `real_rate_10y_pct` = percentil do real rate de 10Y no último ano.

Essas features são particularmente úteis para distinguir entre regimes que parecem similares tecnicamente mas têm implicações macro diferentes (ex: Trending Up em ambiente de bull steepening vs. Trending Up em ambiente de bear flattening — o primeiro é sustentável, o segundo é frágil).

### Tabela: Regime da Curva × Regime de Equities

| Regime Curva    | Equities Trending Up           | Equities Ranging                | Equities Trending Down              | Equities Crisis     |
| --------------- | ------------------------------ | ------------------------------- | ----------------------------------- | ------------------- |
| Bull Steepening | Coerente — alta convicção      | Accumulation provável           | Inconsistente — atenção             | Recovery provável   |
| Bear Steepening | Frágil — distribution possível | Incerteza                       | Coerente — custo de capital subindo | Coerente            |
| Bull Flattening | Divergente — cautela           | Cautela                         | Coerente — flight-to-quality        | Muito coerente      |
| Bear Flattening | Late-cycle — sizing reduzido   | Distribution possível           | Coerente — aperto                   | Coerente — recessão |
| Inversão        | Último estágio do bull         | Distribution alta probabilidade | Coerente                            | Muito coerente      |

---

## Robustez via Monte Carlo e Stress Testing de Sequências de Regime

### Conceito

O backtest histórico testa o sistema contra o que aconteceu. O stress testing via Monte Carlo testa contra o que poderia ter acontecido. Isso é crucial porque a distribuição de durações e sequências de regime no período histórico pode não representar o espaço completo de possibilidades — especialmente para eventos de cauda.

### Metodologia

**Step 1: Estimar a Matriz de Transição Empírica**

Usando os dados históricos labelados, calcular a probabilidade de transição entre cada par de regimes:

```
P(i→j) = N(transições de i para j) / N(total de transições saindo de i)
```

Isso produz uma matriz de transição K×K onde K é o número de regimes.

**Step 2: Estimar as Distribuições de Duração**

Para cada regime, estimar a distribuição empírica de duração (usando os dados dos percentis da seção de Regime Duration Distributions como ponto de partida). Ajustar uma distribuição paramétrica (log-normal ou Weibull) para ter uma distribuição contínua generativa.

**Step 3: Simular Sequências de Regime**

```python
# Pseudocódigo
def simular_sequencia(n_periodos, regime_inicial, matriz_transicao, dist_duracao):
    sequencia = []
    regime_atual = regime_inicial
    t = 0
    while t < n_periodos:
        duracao = sample(dist_duracao[regime_atual])
        sequencia.extend([regime_atual] * min(duracao, n_periodos - t))
        t += duracao
        if t < n_periodos:
            regime_atual = sample_categorica(matriz_transicao[regime_atual])
    return sequencia
```

**Step 4: Simular Retornos Condicionados ao Regime**

Para cada regime na sequência simulada, gerar retornos a partir da distribuição empírica de retornos daquele regime (preservando a distribuição de fat tails, não apenas média e variância).

**Step 5: Avaliar o Sistema**

Executar a estratégia regime-conditioned sobre cada sequência simulada e coletar métricas de performance. Repetir 1000-10000 vezes.

### Cenários de Stress para Testar

**1. Crises Mais Frequentes:**
Aumentar P(qualquer → Crisis) em 2-3x. Pergunta: o sistema sobrevive se crises forem 2x mais frequentes que no histórico?

**2. Regimes de Longa Duração:**
Amostrar durações do percentil P90-P99 (cauda direita) em vez da distribuição completa. Pergunta: o que acontece se Low Vol durar 6 meses em vez do típico 2-4 semanas? O time decay em opções compradas seria suportável?

**3. Transições Raras:**
Forçar transições que são raras mas possíveis (Crisis → Blow-off, Low Vol → Crisis). Pergunta: o sistema tem regras para essas transições ou entra em modo NoLabel?

**4. Regime Flickering:**
Simular sequências com transições muito frequentes (duração média 2-3 períodos). Pergunta: os custos de transição consomem todo o alpha? Qual é a duração mínima de regime para que o sistema seja lucrativo?

**5. Correlação Breakdown Simultâneo:**
Combinar crise em equities com correlação stocks-bonds invertida (ambos caem). Pergunta: os hedges do portfólio funcionam ou o sistema depende de correlação negativa que não existe neste cenário?

### Template de Relatório de Stress Test

```
=== REGIME STRESS TEST REPORT ===
Cenário: [nome do cenário]
Simulações: [N]
Período simulado: [anos]

--- DISTRIBUIÇÃO DE RESULTADOS ---
Sharpe médio:           [X.XX] (IC 95%: [X.XX - X.XX])
Sharpe P5 (worst 5%):  [X.XX]
Max DD médio:           [-XX%]
Max DD P95 (worst 5%):  [-XX%]
Prob de drawdown > 20%: [XX%]
Prob de drawdown > 50%: [XX%]
Calmar médio:           [X.XX]

--- VS BASELINE (backtest histórico) ---
Sharpe degradação:      [XX%] pior que histórico
Max DD degradação:      [XX%] pior que histórico

--- REGIME-SPECIFIC STRESS ---
Custo médio por transição de regime: [XX bps]
Transições totais por ano (simulado): [N] (vs [N] histórico)
Regimes onde sistema perde dinheiro consistentemente: [lista]

--- CONCLUSÃO ---
O sistema é robusto ao cenário [nome]? [Sim/Não/Parcialmente]
Recomendações de ajuste: [lista]
```

### Pitfall: Não Confiar Apenas na Matriz de Transição Histórica

A matriz de transição assume que as probabilidades de transição são estacionárias. Na realidade, elas mudam conforme o regime macro (recessão, expansão, mudança de política monetária). Recomendo testar com pelo menos 3 matrizes de transição diferentes:

1. **Full sample:** toda a história disponível.
2. **Expansão:** apenas períodos de crescimento econômico.
3. **Recessão/Stress:** apenas períodos de contração ou crise.

Se o sistema funciona bem com todas as 3 matrizes, é genuinamente robusto. Se depende da matriz de expansão (mais tempo em trending up, menos crises), é frágil.

---

## Multi-Regime State: O Vetor de Regime Completo

### Conceito

O mercado não está em "um" regime — está em múltiplos regimes simultaneamente ao longo de dimensões diferentes. O documento principal já reconhece isso implicitamente (regime no 1H pode diferir do 1D), mas a formalização como vetor de estado permite sistematizar a tomada de decisão.

### Definição do Vetor de Regime

```
RegimeState(t) = {
    regime_direcional_1D:  [0-13],         // da taxonomia principal
    regime_direcional_1H:  [0-13],         // da taxonomia principal
    regime_volatilidade:   [low, normal, high, extreme],
    regime_liquidez:       [liquid, thinning, illiquid, vacuum],
    regime_correlacao:     [normal, convergencia, descorrelacao, rotacao],
    regime_curva_juros:    [bull_steep, bear_steep, bull_flat, bear_flat, inverted],
    gex_sign:              [positivo, neutro, negativo],
    confidence_1D:         [0.0 - 1.0],
    confidence_1H:         [0.0 - 1.0],
    hours_to_event:        [0 - ∞],
    days_to_opex:          [0 - ∞]
}
```

### Regras de Combinação

O sizing efetivo final é o produto dos ajustes de cada dimensão:

```
Sizing_efetivo = Sizing_base(regime_direcional_1D)
                 × Ajuste(regime_1H)
                 × Ajuste(regime_liquidez)
                 × Ajuste(regime_correlacao)
                 × Ajuste(gex)
                 × C(t)     // confidence score
                 × Ajuste(evento)
```

**Exemplo concreto:**

RegimeState = {Trending Up no 1D, Ranging no 1H, liquidez Thinning, correlação Normal, GEX positivo, C=0.75, sem evento próximo}

```
Sizing = 100% (Trending Up 1D)
         × 0.85 (1H Ranging = pullback, não penalizar muito)
         × 0.80 (Thinning liquidity)
         × 1.00 (correlação normal)
         × 1.00 (GEX positivo = estabilizador, não requer ajuste)
         × 0.75 (confidence score)
         × 1.00 (sem evento)
         = 51% do sizing máximo
```

Isso é mais conservador que o sizing puro do regime direcional (100%) e mais informado que uma redução genérica. Cada dimensão contribui com informação específica que justifica o ajuste.

### Tabela de Ajustes Multiplicativos por Dimensão

| Dimensão            | Estado                  | Multiplicador de Sizing    |
| ------------------- | ----------------------- | -------------------------- |
| Regime 1H (se ≠ 1D) | Coerente com 1D         | 1.00                       |
|                     | Levemente conflitante   | 0.85                       |
|                     | Fortemente conflitante  | 0.50                       |
| Liquidez            | Liquid                  | 1.00                       |
|                     | Thinning                | 0.80                       |
|                     | Illiquid                | 0.50                       |
|                     | Vacuum                  | 0.00                       |
| Correlação          | Normal                  | 1.00                       |
|                     | Convergência (risk-on)  | 0.80                       |
|                     | Convergência (risk-off) | 0.60                       |
|                     | Descorrelação anômala   | 0.50                       |
|                     | Rotação setorial        | 1.00 (mas seleção importa) |
| GEX                 | Positivo (na direção)   | 1.00                       |
|                     | Positivo (contra)       | 0.85                       |
|                     | Neutro                  | 1.00                       |
|                     | Negativo (na direção)   | 0.90 (vol amplificada)     |
|                     | Negativo (contra)       | 0.70                       |
| Evento              | > 24h até Tier 1        | 1.00                       |
|                     | 4-24h até Tier 1        | 0.75                       |
|                     | < 4h até Tier 1         | 0.25                       |
|                     | OpEx (dia de)           | 0.75                       |

### Métricas de Custo de Transição

Cada vez que o vetor de regime muda, há custos de rebalanceamento. Calcular e monitorar:

**Custo por transição:**

```
Custo_transicao = |ΔSizing| × Spread_medio + Slippage_estimado + Comissão
```

**Custo total de transições por mês:**

```
Custo_mensal = Σ(Custo_transicao) para todas as transições no mês
```

**Break-even:** o alpha gerado pelo regime-conditioned sizing deve exceder o custo mensal de transições. Se não excede, o sistema está over-trading — considerar filtros de estabilidade mais agressivos (exigir que o regime persista por N períodos antes de agir).

---

## Nota sobre ETFs Alavancados e Inversos

### Problema

ETFs alavancados (2x, 3x) e inversos rebalanceiam diariamente, o que cria decaimento de volatilidade (volatility drag). O regime do ETF alavancado pode divergir do regime do subjacente em horizontes mais longos.

**Exemplo:** se o subjacente está em Ranging (oscilando ±1% por dia), o ETF 3x long está efetivamente em Trending Down por causa do volatility decay. A cada oscilação, o ETF perde um pouco de valor mesmo que o subjacente volte ao ponto de partida.

### Regras para ETFs Alavancados

1. **Nunca manter ETFs alavancados em regimes de Ranging ou Choppy** — o volatility decay garante perda.
2. **Usar apenas em regimes de Trending forte e de curta duração** (dias, não semanas) — a alavancagem amplifica a tendência mas o decay compensa em prazos mais longos.
3. **Para holding periods > 5 dias, modelar o regime do ETF separadamente** — calcular o retorno esperado do ETF considerando o path-dependency (não apenas o retorno do subjacente × alavancagem).
4. **ETFs inversos em Crisis:** parecem ideais mas a execução é traiçoeira. O rebalanceamento diário em vol extremamente alta pode gerar resultados muito diferentes do esperado. Preferir puts ou futuros para hedge em crise.

### Fórmula do Decaimento

```
Retorno_ETF_alavancado ≈ L × Retorno_subjacente - (L² - L)/2 × σ² × T
```

Onde:

- L = fator de alavancagem (2, 3, -1, -2, -3).
- σ² = variância dos retornos diários.
- T = número de dias.

O segundo termo é sempre negativo (exceto para L=1), e cresce com σ² e T. Quanto mais volátil e mais longo o holding, mais o decay prejudica.

---

## Resumo das Novas Seções e Integração

| Nova Seção                       | Onde Integrar no Documento Original                     | Impacto no Modelo                   |
| -------------------------------- | ------------------------------------------------------- | ----------------------------------- |
| GEX e Fluxos de Dealers          | Após "Indicadores Recomendados por Regime"              | Nova feature + ajuste de sizing     |
| Regime de Liquidez               | Nova seção após "Sizing por Regime"                     | Nova dimensão + tabela de interação |
| Order Flow e Microestrutura      | Expandir nota em "Timeframes: 1H vs 1D"                 | Novas features + sinais antecipados |
| Estratégias de Opções por Regime | Nova seção após "Stop Loss Rules por Regime"            | Novo eixo operacional               |
| Regime de Correlação             | Expandir "Correlação entre Regimes de Múltiplos Ativos" | Nova dimensão + ajuste de hedge     |
| Técnicas de Detecção Recentes    | Expandir "Considerações de Implementação"               | Novos modelos + melhor detecção     |
| Regime-Aware Execution           | Nova seção após "Stop Loss Rules"                       | Melhor execução + menos slippage    |
| Renda Fixa e Curva de Juros      | Expandir "Asset-Class Specific Notes"                   | Novas features macro                |
| Monte Carlo e Stress Testing     | Expandir "Backtest Framework Template"                  | Robustez + confiança no sistema     |
| Multi-Regime State               | Nova seção final antes de "Referência Rápida"           | Formalização do vetor de regime     |
