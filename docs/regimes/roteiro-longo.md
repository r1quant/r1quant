# Roteiro de Estudo: Regimes de Mercado Financeiro

**Foco: Trading Quantitativo & Detecção de Regimes**

---

## Fase 1 — Fundamentos (2–3 meses)

O objetivo aqui é construir a base matemática e estatística sem a qual os modelos de regime ficam opacos. Não pule essa fase.

### 1.1 Probabilidade e Estatística

- **DeGroot & Schervish — _Probability and Statistics_** — Cobertura sólida de distribuições, inferência e estimação. Foque nos capítulos sobre estimação por máxima verossimilhança (MLE) e testes de hipótese, que são a base dos modelos que virão depois.

### 1.2 Álgebra Linear Aplicada

- **Gilbert Strang — _Introduction to Linear Algebra_** — Você vai precisar de autovalores, decomposição matricial e cadeias de Markov. Strang é didático e os vídeos do MIT OCW complementam perfeitamente.

### 1.3 Séries Temporais (introdução)

- **Hyndman & Athanasopoulos — _Forecasting: Principles and Practice_** (gratuito online) — Excelente porta de entrada. Cobre ARIMA, sazonalidade, decomposição e avaliação de modelos de previsão. Não é voltado a finanças, mas constrói a intuição certa.

**Resultado esperado:** Você entende MLE, matrizes de transição, estacionariedade e consegue implementar um ARIMA básico em Python ou R.

---

## Fase 2 — Séries Temporais Financeiras (2–3 meses)

Agora sim entramos no território de finanças quantitativas propriamente.

### 2.1 Referência principal

- **Ruey Tsay — _Analysis of Financial Time Series_ (3ª ed.)** — O livro mais completo sobre o tema. Cubra com atenção especial:
  - Cap. 3: Modelos de volatilidade condicional (GARCH e variantes)
  - Cap. 4: Modelos não-lineares e mudanças de regime
  - Cap. 6: Análise multivariada (DCC-GARCH)
  - Os exercícios em R são excelentes.

### 2.2 Complemento econométrico

- **James Hamilton — _Time Series Analysis_** — Denso, mas indispensável. O capítulo 22 sobre Markov-Switching Models é a referência original da literatura. Leia pelo menos os capítulos sobre modelos de estado (state-space) e filtro de Kalman, que são fundamentais para entender regimes latentes.

### 2.3 Leitura complementar (papers)

- Hamilton (1989) — _"A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle"_ — O paper fundador.
- Ang & Bekaert (2002) — _"Regime Switches in Interest Rates"_ — Aplicação a renda fixa.

**Resultado esperado:** Você implementa um GARCH(1,1) e entende conceitualmente como um modelo Markov-Switching detecta mudanças de regime.

---

## Fase 3 — Modelos de Regime (2–4 meses)

O núcleo do estudo. Aqui você aprende a modelar e detectar regimes formalmente.

### 3.1 Hidden Markov Models (HMMs)

- **Zucchini, MacDonald & Langrock — _Hidden Markov Models for Time Series_** — O melhor livro dedicado a HMMs com aplicações práticas. Cobre estimação via EM (Baum-Welch), seleção de número de estados e diagnóstico. Usa R com pacotes prontos.

### 3.2 Machine Learning probabilístico

- **Kevin Murphy — _Machine Learning: A Probabilistic Perspective_** — Capítulos 17 (HMMs) e 18 (State-Space Models) são referência. Se quiser a versão mais recente, o _Probabilistic Machine Learning: An Introduction_ (2022) está disponível gratuitamente.

### 3.3 Abordagem bayesiana

- **Frühwirth-Schnatter — _Finite Mixture and Markov Switching Models_** — Referência técnica para quem quer ir fundo na estimação bayesiana de modelos de mistura e switching. Avançado, mas muito completo.

### 3.4 Papers aplicados essenciais

- Guidolin & Timmermann (2007) — _"Asset Allocation Under Multivariate Regime Switching"_
- Bulla & Bulla (2006) — _"Stylized Facts of Financial Time Series and Hidden Semi-Markov Models"_
- Nystrup, Madsen & Lindström (2017) — _"Long Memory of Financial Time Series and Hidden Markov Models with Time-Varying Parameters"_

**Resultado esperado:** Você implementa um HMM de 2-3 estados sobre retornos de um ativo, interpreta os regimes como bull/bear ou alta/baixa volatilidade, e avalia a qualidade do modelo.

---

## Fase 4 — Aplicação a Trading e Alocação (2–3 meses)

Agora conectamos a teoria à prática de gestão e trading.

### 4.1 Factor investing e regimes

- **Andrew Ang — _Asset Management: A Systematic Approach to Factor Investing_** — Excelente ponte entre academia e prática. Dedica seções inteiras a como regimes afetam prêmios de risco (value, momentum, volatility) e como adaptar a alocação.

### 4.2 Trading sistemático

- **Ernest Chan — _Algorithmic Trading_** — Abordagem prática com código (Python/MATLAB). Cobre mean-reversion, momentum, e gestão de risco. Útil para implementar estratégias que condicionam sinais ao regime detectado.
- **Ernest Chan — _Quantitative Trading_** — Mais introdutório que o anterior. Bom se você ainda não tem experiência com backtesting.

### 4.3 Machine Learning aplicado a finanças

- **Marcos López de Prado — _Advances in Financial Machine Learning_** — Leitura obrigatória. Capítulos relevantes:
  - Cap. 3: Labeling (triple-barrier method)
  - Cap. 5: Fractionally differentiated features
  - Cap. 7: Cross-validation em finanças (purged k-fold)
  - Cap. 17: Structural breaks (CUSUM tests)
  - A ideia de meta-labeling (Cap. 3 e 6) se conecta diretamente com modelos de regime.

### 4.4 Gestão de risco

- **Attilio Meucci — _Risk and Asset Allocation_** — Avançado, mas a integração entre estimação de distribuições, cenários e regimes é muito bem feita. Os "Meucci Exercises" gratuitos no site dele são um excelente complemento.

**Resultado esperado:** Você constrói uma estratégia de trading ou alocação que condiciona decisões ao regime corrente, com backtesting robusto e gestão de risco.

---

## Fase 5 — Tópicos Avançados (contínuo)

Para quem quer se aprofundar ou seguir carreira em pesquisa.

### 5.1 Deep learning para séries temporais

- **Papers sobre LSTMs, Temporal CNNs e Transformers aplicados a regime detection.** Um bom ponto de partida é o survey de Sezer, Gudelek & Ozbayoglu (2020) — _"Financial Time Series Forecasting with Deep Learning: A Systematic Literature Review"_.

### 5.2 Bayesian Nonparametrics

- **Gelman et al. — _Bayesian Data Analysis_** — Para modelos onde o número de regimes não é fixo a priori (e.g., Infinite HMMs via Dirichlet Process).

### 5.3 Microestrutura e regimes intraday

- **Cartea, Jaimungal & Penalva — _Algorithmic and High-Frequency Trading_** — Se o interesse é trading de alta frequência, este livro cobre modelos de microestrutura com componentes de regime.

### 5.4 Prática contínua

- Acompanhe journals: _Journal of Financial Economics_, _Quantitative Finance_, _Journal of Financial Econometrics_.
- Repositórios no GitHub com implementações de HMMs financeiros (hmmlearn, depmixS4 em R).
- Competições no Kaggle (séries temporais financeiras).

---

> Não tente ler tudo linearmente. Use os livros como referência e alterne entre teoria e implementação. Implemente cada modelo assim que aprender — a compreensão se consolida no código.
