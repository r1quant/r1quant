# Roteiro Intensivo (1 Mês): Regimes de Mercado Financeiro

**Foco: Do zero ao funcional em 4 semanas**

---

## Filosofia deste roteiro

Com apenas 1 mês, a estratégia muda completamente: em vez de construir fundamentos profundos e depois subir, vamos direto ao que importa para **detectar regimes e usar isso em trading**, aprendendo a teoria sob demanda conforme a necessidade aparece.

**Regra de ouro:** 50% leitura, 50% código. Todo dia.

---

## Semana 1 — Intuição e Ferramentas (dias 1–7)

**Objetivo:** Entender o que são regimes, montar o ambiente e rodar seus primeiros modelos.

### Leitura (escolha UM como guia principal)

- **Ernest Chan — _Algorithmic Trading_** — Leia os capítulos 1–3. Dá o panorama de trading sistemático, backtesting e gestão de risco de forma prática e acessível. Pule demonstrações matemáticas densas; foque no "como usar".

### Prática

- Monte seu ambiente Python: `numpy`, `pandas`, `matplotlib`, `statsmodels`, `hmmlearn`, `arch` (para GARCH).
- Baixe dados históricos de um ativo (S&P 500 via `yfinance`).
- Calcule retornos log, volatilidade rolling (20 e 60 dias) e visualize.
- Implemente um GARCH(1,1) com o pacote `arch`. Observe como a volatilidade condicional muda ao longo do tempo — isso já é uma forma primitiva de detectar regimes.

### Conceitos-chave para absorver

- Retornos log vs. retornos simples
- Volatilidade condicional vs. realizada
- Clusters de volatilidade (por que existem e o que significam)

---

## Semana 2 — Hidden Markov Models na Prática (dias 8–14)

**Objetivo:** Implementar um HMM de 2 estados e interpretar os regimes.

### Leitura

- **Kevin Murphy — _Probabilistic Machine Learning: An Introduction_** (gratuito online) — Leia **apenas** o capítulo 29 (State-Space Models) ou, se preferir algo mais curto, leia o tutorial clássico de Rabiner (1989) — _"A Tutorial on Hidden Markov Models and Selected Applications"_ (disponível gratuitamente, ~30 páginas essenciais).

### Prática

- Use `hmmlearn` (Python) para ajustar um `GaussianHMM` de 2 estados aos retornos diários do S&P 500.
- Visualize: plote o preço do ativo com cores diferentes para cada regime.
- Interprete: um estado terá média positiva e baixa variância (bull/calmo), o outro terá média negativa ou nula e alta variância (bear/turbulento).
- Experimente com 3 estados e compare.
- Calcule a matriz de transição e entenda: qual a probabilidade de permanecer no regime atual? Qual a duração esperada de cada regime?

### Conceitos-chave para absorver

- O que é um estado latente (oculto)
- Algoritmo de Viterbi (decodificação do caminho mais provável)
- Forward-backward (probabilidades filtradas)
- Seleção de número de estados (BIC/AIC)

---

## Semana 3 — Conectando Regimes a Estratégias (dias 15–21)

**Objetivo:** Usar o regime detectado para tomar decisões de trading ou alocação.

### Leitura

- **Marcos López de Prado — _Advances in Financial Machine Learning_** — Leia os capítulos 3 (labeling), 7 (cross-validation em finanças) e 17 (structural breaks / CUSUM). Não leia o livro inteiro; esses 3 capítulos bastam por agora.

### Prática

- Construa uma estratégia simples: "esteja comprado no ativo quando o HMM indica regime bull; vá para caixa (ou hedge) quando indica regime bear."
- **Cuidado com look-ahead bias!** Use apenas dados disponíveis até o momento para estimar o regime. Retreine o modelo em janelas rolling ou expanding.
- Faça um backtest honesto: compare a estratégia regime-switching contra buy-and-hold.
- Métricas: Sharpe ratio, max drawdown, % de tempo em cada regime.
- Implemente o CUSUM test de López de Prado para detectar structural breaks — compare com os regimes do HMM.

### Conceitos-chave para absorver

- Look-ahead bias e por que é fatal
- Walk-forward / expanding window para modelos de regime
- A diferença entre regime detectado em tempo real vs. retrospectivo (filtered vs. smoothed probabilities)

---

## Semana 4 — Refinamento e Robustez (dias 22–30)

**Objetivo:** Testar a robustez, explorar variações e consolidar.

### Leitura

- **Andrew Ang — _Asset Management_** — Leia os capítulos sobre regimes e fatores (Parte II). Dá a perspectiva de como gestores profissionais pensam sobre regimes na alocação.
- Leia 2–3 papers aplicados (escolha os que mais interessam):
  - Nystrup et al. (2017) — HMMs com parâmetros variantes no tempo
  - Bulla & Bulla (2006) — Hidden Semi-Markov Models
  - Guidolin & Timmermann (2007) — Alocação multi-regime

### Prática

- Teste seu modelo em outros ativos/mercados (renda fixa, commodities, FX).
- Adicione features ao HMM: em vez de só retornos, alimente com retornos + volatilidade realizada + spread de crédito.
- Compare com abordagens simples: regime baseado em média móvel de 200 dias, ou em VIX acima/abaixo de um threshold.
- Documente tudo em um Jupyter Notebook limpo — será sua referência futura.

### Conceitos-chave para absorver

- Overfitting em modelos de regime (poucos dados, muitos estados)
- A importância de simplicidade (2 estados costumam ser suficientes)
- Regime ≠ previsão (o modelo detecta onde você está, não para onde vai)

---

## Recursos Essenciais (apenas o necessário)

| Recurso                                          | Por quê                                             |
| ------------------------------------------------ | --------------------------------------------------- |
| **Ernest Chan — _Algorithmic Trading_**          | Visão prática de trading sistemático                |
| **Murphy — _Probabilistic ML_ (online, grátis)** | Teoria de HMMs bem explicada                        |
| **López de Prado — _Advances in Financial ML_**  | Structural breaks + boas práticas de ML em finanças |
| **Andrew Ang — _Asset Management_**              | Perspectiva de alocação com regimes                 |
| **Rabiner (1989) — Tutorial de HMMs**            | A melhor introdução técnica em ~30 páginas          |
| **hmmlearn (Python)**                            | Implementação prática de HMMs                       |
| **arch (Python)**                                | Modelos GARCH                                       |

---

## Cronograma Diário Sugerido

Assumindo ~2–3 horas por dia:

| Hora                          | Atividade                                                                                                         |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Primeira hora                 | Leitura focada (capítulo ou paper do dia)                                                                         |
| Segunda hora                  | Implementação em Python do que leu                                                                                |
| Terceira hora (se disponível) | Experimentação livre: mude parâmetros, teste outros ativos, quebre o modelo de propósito para entender os limites |

---

## O que NÃO fazer neste mês

- **Não** tente dominar a matemática do algoritmo EM — use a biblioteca e entenda a intuição.
- **Não** leia Hamilton inteiro — é para referência futura.
- **Não** tente mais de 3 estados no HMM sem um motivo muito claro.
- **Não** gaste tempo com deep learning para regimes agora — HMMs são mais interpretáveis e suficientes para começar.
- **Não** otimize hiperparâmetros excessivamente — isso leva a overfitting e consome tempo.

---

## Após o mês: próximos passos

Se quiser continuar aprofundando depois:

1. Volte ao **Tsay** e **Hamilton** para solidificar a teoria.
2. Explore modelos bayesianos (Frühwirth-Schnatter).
3. Adicione regimes a um portfólio multi-ativo real.
4. Estude microestrutura se o interesse for intraday.

> **Lembre-se:** Em 1 mês você não vai dominar o assunto, mas vai ter um modelo funcional, intuição sólida e, principalmente, vai saber o que ainda precisa aprender — e isso vale muito.
