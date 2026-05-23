*Original (https://piotrpomorski.substack.com/p/the-ml-algorithms-guide-nobody-asked) em inglês: Piotr Pomorski, "The ML Algorithms Guide Nobody Asked For (But Everyone Needs)". Esta versão é uma adaptação em português com acréscimos, não uma tradução literal.*

# O Guia de Algoritmos de ML Que Ninguém Pediu (Mas Todo Mundo Precisa)

Você terminou o curso de ML, leu todos os notebooks do Kaggle e agora encara dados de produção reais pensando "tá, mas o que eu de fato ajusto aqui?". Existe um abismo entre *saber o que é* gradient boosting e *saber quais hiperparâmetros importam* quando o modelo precisa rodar até segunda-feira.

Este não é um texto de teoria. É o guia de referência rápida — aquele que você salva e volta a consultar quando está de fato construindo modelos às 23h porque o deploy é amanhã cedo. Sem derivações, sem provas. Só o que move a agulha.

A ideia central que ninguém te conta: **a maioria dos algoritmos tem 2 ou 3 parâmetros que importam e uma dúzia que não importa.** Os tutoriais te fizeram acreditar que você precisa entender cada parâmetro. Você não precisa.

---

## Os algoritmos que de fato importam

### Regressão Linear: é só sobre a penalização

Regressão linear regularizada se resume a escolher entre **L1 (Lasso)** e **L2 (Ridge)**:

- **L1 (Lasso)** zera coeficientes exatamente — seleção automática de features, gerando soluções esparsas.
- **L2 (Ridge)** mantém todas as features, mas encolhe os coeficientes proporcionalmente.

O resto é só ajustar a força da regularização (o `alpha` no scikit-learn).

A pegadinha que muita gente ignora: a seleção de features do Lasso soa ótima na teoria, mas vira um problema quando suas features são correlacionadas — o que é quase sempre o caso em dados financeiros de alta frequência. Com preditores correlacionados (lags de preço, retornos em frequências diferentes, indicadores técnicos relacionados), o Lasso escolhe **arbitrariamente** um do grupo e zera os demais. Essa escolha é instável: pequenas mudanças nos dados invertem qual feature sobrevive. Péssimo quando todas carregam sinal legítimo.

O Ridge lida muito melhor com isso: em vez de eleger vencedores e perdedores, ele encolhe os coeficientes correlacionados juntos, de forma suave. É fundamentalmente mais estável sob multicolinearidade — situação padrão em séries temporais financeiras.

**Quando usar Lasso então?** Quando você genuinamente acredita que muitas features são puro ruído e quer eliminação agressiva — trabalho exploratório com centenas de features das quais só um punhado importa, ou quando as features são pouco correlacionadas. Para a maioria da modelagem financeira, Ridge é a escolha mais segura.

> **➕ Acréscimo — Elastic Net e regressão quantílica.** Existe um meio-termo: o **Elastic Net**, que combina L1 + L2 (`l1_ratio` controla a mistura). Ele dá esparsidade *e* estabilidade sob correlação — é frequentemente a melhor escolha "default" quando você está em dúvida entre Lasso e Ridge. Para caudas pesadas/distribuições assimétricas (comum em finanças), a **regressão quantílica** modela quantis em vez da média, sendo robusta a outliers e útil para estimar risco (ex.: prever o quantil 5% para VaR).

---

### Naive Bayes: ninguém liga pro alpha (mas configure mesmo assim)

Naive Bayes tem exatamente um parâmetro do qual se fala: `alpha`, o suavizador (Laplace/Lidstone smoothing). Defina algo entre **0.1 e 1.0** e siga a vida. Esse algoritmo ou funciona pro seu problema, ou não — nenhum ajuste de alpha vai salvá-lo.

A decisão real é se suas features são *condicionalmente independentes*. Provavelmente não são — por isso quase ninguém usa, exceto em **classificação de texto**, onde estranhamente funciona muito bem.

> **➕ Acréscimo — qual variante?** `MultinomialNB` para contagens (texto, bag-of-words/TF-IDF), `BernoulliNB` para features binárias, `GaussianNB` para features contínuas. Vale como *baseline* ultrarrápido antes de partir para modelos pesados.

---

### Árvores de Decisão: o algoritmo que ninguém usa (mas todos deveriam entender)

Segredo: **ninguém coloca uma árvore de decisão isolada em produção.** Ou são simples demais, ou fazem overfitting absurdo. Mas você precisa entendê-las, porque todo o resto é "ensembles sofisticados de árvores".

Os parâmetros principais — `max_depth`, `min_samples_split`, `min_samples_leaf` — controlam overfitting. É literalmente o único trabalho deles. Uma árvore isolada é, na prática, uma ferramenta didática para entender Random Forest e Gradient Boosting.

---

### Random Forest: cinco parâmetros que você não pode ignorar

Aqui o ajuste de hiperparâmetros começa a importar de verdade:

| Parâmetro | O que faz | Ponto de partida |
|---|---|---|
| **`max_depth`** | Profundidade de cada árvore. Mais fundo = mais sinal capturado, mas mais overfitting | 10–20 para dados tabulares |
| **`n_estimators`** | Quantas árvores. Mais é melhor até não compensar o custo | 100, suba até 500 se houver tempo |
| **`max_features`** | O molho secreto. **Não pode ser "todas"** — isso anula a graça do RF. Cada árvore deve ver subconjuntos diferentes | `sqrt(n_features)` (classificação), `n_features/3` (regressão) |
| **`min_samples_split`** | Controla overfitting | Default costuma servir |
| **`min_samples_leaf`** | Controla overfitting | Aumente em dados ruidosos |

Na prática: você acerta o `max_features`, roda um Optuna rápido sobre `n_estimators` e `max_depth`, e está feito. O resto mal mexe a agulha.

> **➕ Acréscimo — Extra Trees e OOB.** As **Extremely Randomized Trees** (`ExtraTreesClassifier/Regressor`) sorteiam também os pontos de corte, o que reduz variância e acelera o treino — vale como alternativa direta ao RF. E o **erro out-of-bag** (`oob_score=True`) te dá uma estimativa de validação quase de graça, sem precisar separar um conjunto extra.

---

### Gradient Boosting: onde a engenharia de ML acontece de verdade

Se Random Forest é a graduação, Gradient Boosting é a pós. Aqui você usa **XGBoost, LightGBM ou CatBoost** e foca em ~8–10 parâmetros que importam:

- Os mesmos parâmetros de árvore (`max_depth`, splits/folhas), **mais**:
- **`learning_rate`** — provavelmente o hiperparâmetro mais importante de todo o ML. Alto demais → overfitting; baixo demais → treino eterno. Comece em **0.1** e reduza se houver overfitting.
- **`alpha` e `lambda`** — regularização L1 e L2, agora aplicadas ao ensemble de árvores.
- **`num_leaves`** — controle mais fino que `max_depth` (mais folhas = mais complexidade). Atenção no LightGBM: mantenha `num_leaves < 2^max_depth`.
- **`subsample` e `colsample_bytree`** — fração de dados/features que cada árvore vê. Regularização via aleatoriedade.
- **`boosting_type`** (LightGBM) — GOSS e DART são sofisticados, mas `gbdt` normalmente resolve.

O ofício real é saber **qual** parâmetro mexer para o seu problema:
- Overfitting? → reduza `learning_rate` e a profundidade.
- Treino lento? → ajuste `n_estimators` e `learning_rate` juntos.
- Ainda com overfitting? → `subsample` e parâmetros de regularização.

> **➕ Acréscimo — três coisas que mudam o jogo:**
> 1. **Early stopping.** Use um conjunto de validação e `early_stopping_rounds` (ex.: 50). Isso te deixa colocar `learning_rate` baixo + `n_estimators` alto e parar automaticamente no ponto ótimo — combo vencedor.
> 2. **Classes desbalanceadas.** Use `scale_pos_weight` (XGBoost/LightGBM) ou `class_weight`/`is_unbalance`. Não confie só em acurácia nesses casos.
> 3. **CatBoost para variáveis categóricas.** Ele faz *target/ordered encoding* nativamente e sofre menos com *target leakage*. Se você tem muitas categóricas de alta cardinalidade, comece por ele e pule o trabalho de encoding manual.

---

### PCA: deixe quieto para séries temporais

PCA em séries temporais costuma ser um erro, a não ser que seja pesquisa ou você realmente saiba o que está fazendo. Séries têm estrutura temporal que o PCA destrói.

Em contrapartida, **PLS (Partial Least Squares)** funciona bem em séries temporais porque considera a relação com a variável-alvo durante a redução de dimensionalidade. É o "primo esperto" do PCA, que prestou atenção na aula.

Quando você *for* usar PCA, eis o que importa:

- **PCA linear** — assume relações lineares entre features.
- **Kernel PCA** — lida com relações não lineares (kernel RBF quando você não faz ideia do que rola no espaço de features).
- **Incremental PCA** — para datasets gigantes; processa em mini-batches.
- **Robust PCA** — separa os dados em low-rank (sinal) + esparso (outliers). Útil quando há muitos outliers contaminando os componentes.

E falando em redução de dimensionalidade: **ICA (Análise de Componentes Independentes)** é o que você usa quando quer features *estatisticamente independentes*, não só não correlacionadas — crucial para separar sinais misturados (ex.: o "problema do coquetel").

> **➕ Acréscimo — visualização vs. modelagem.** Para *visualizar* clusters em alta dimensão, **UMAP** e **t-SNE** costumam revelar estrutura melhor que PCA — mas **só para visualização**: as distâncias resultantes não são confiáveis como features de produção.

---

### k-NN e k-Means: os "k" que importam

**k-NN (vizinhos mais próximos)** tem fama ruim, parte dela merecida — mas seja justo. É conceitualmente simples e um ótimo *baseline*. Não tem fase de treino (*lazy learner*), então você experimenta rápido. Lida bem com multiclasse, é útil para detecção de anomalias (pontos longe dos vizinhos) e funciona em problemas de baixa dimensão.

O problema: essas vantagens são esmagadas pelas desvantagens em produção. A previsão é dolorosamente lenta (calcula distância a todos os pontos de treino), o uso de memória cresce com todo o dataset, e a **maldição da dimensionalidade** bate forte — com muitas features, "mais próximo" perde sentido, pois tudo fica equidistante. É extremamente sensível à escala das features e não deixa modelo interpretável. Ótimo para prototipagem e anomalias; raro em pipelines sérios de previsão.

**k-Means**, por outro lado, é genuinamente útil em produção. Tem exatamente um parâmetro que importa: o **número de clusters (k)**. Use o método do cotovelo, *silhouette score* ou lógica de negócio para escolher k, e deixe rodar. O uso real é **engenharia de features**: encontrar padrões similares para montar *panel datasets* ou usar a pertinência a cluster como feature — não é solução ponta-a-ponta.

> **➕ Acréscimo — sempre padronize antes.** Tanto k-NN quanto k-Means dependem de distância: rode `StandardScaler` antes, ou uma feature de magnitude maior dominará tudo. Se os clusters não forem esféricos ou houver ruído, considere **DBSCAN/HDBSCAN** (não exige definir k e detecta outliers) ou **Gaussian Mixture Models** (clusters elípticos + probabilidade de pertinência).

---

### Support Vector Machine: o último recurso

SVM é o que você tenta quando nada mais funciona e a curiosidade bate. Brincadeira parcial — SVMs vão bem em relações não lineares complexas em espaços de dimensão moderada.

Dois parâmetros importam: **`C`** (força de regularização — quanto maior, menos regularização) e **`kernel`** (linear para relações simples, RBF para "não faço ideia do que acontece"). Na prática: testou, ou funciona ou não, e segue.

> **➕ Acréscimo — não escale = não funciona.** SVM é ainda mais sensível à escala que k-NN; padronize sempre. E cuidado: o custo de treino cresce entre O(n²) e O(n³) — acima de ~50 mil amostras vira inviável. Para regressão, o equivalente é o **SVR**, ótimo como *benchmark* contra a regressão linear.

---

### Redes Neurais: isso é outro post inteiro

Os hiperparâmetros dependem inteiramente do tipo de rede. Mas o padrão básico a memorizar é:

```
camada NN → camada de normalização → camada de dropout
```

Às vezes há uma camada de ativação entre normalização e dropout, às vezes depois de ambas. O essencial: **batch/layer norm** ajuda a estabilidade do treino, **dropout** previne overfitting. Acerte essa estrutura e você está 80% do caminho.

> **➕ Acréscimo — o mínimo que muda resultado.** Para dados tabulares, redes raramente superam o gradient boosting — não comece por elas. Quando usar: **Adam** ou **AdamW** como otimizador, *learning rate scheduling* (cosine/warmup), e **early stopping** valem mais que arquitetura exótica. Para séries temporais, considere antes modelos especializados (N-BEATS, TFT, ou mesmo um bom LightGBM com features de lag) em vez de LSTMs cruas.

---

## Quando de fato usar cada algoritmo

É aqui que as pessoas mais erram — não no algoritmo em si, mas em *quando* usá-lo. As características do seu problema importam mais que o seu algoritmo favorito.

- **Regressão linear regularizada** → dados de **alta frequência**, especialmente séries únicas. Rápida, interpretável, boa quando as relações são aproximadamente lineares. É o que você usa para negociar sinais diretamente. (A matemática de Gauss-Markov não se importa com a distribuição, e sim com os resíduos.) Forex, sinais de HFT, qualquer coisa que peça previsão rápida e tendência correta. Muitos fatores? Comece com Ridge. Caudas pesadas em múltiplos ativos? Considere regressão quantílica.

- **SVR** → ótimo *benchmark* contra a regressão linear. Basicamente "e se a relação não for linear?". Rode os dois, veja quem ganha, talvez faça *ensemble* depois.

- **Ensembles de árvores (RF e Gradient Boosting)** → dados de **baixa frequência** ou *panel datasets*. Lidam com não linearidades, dispensam escalonamento (mas confira) e brilham em previsões semanais/mensais ou dados *cross-sectional*. Por quê? Frequências mais baixas têm mais "dobras" — mudanças de regime, efeitos de limiar, efeitos cumulativos que modelos lineares não capturam. O detalhe: baixa frequência = menos amostras (o que favoreceria modelos lineares); a solução é montar *panel datasets* combinando múltiplos ativos. Boosting costuma superar bagging em pesquisa, mas precisa de mais regularização.

- **Redes neurais** → quando o dataset é *enorme de verdade* (não "temos 5.000 linhas", mas "os dados de treino não cabem na RAM"). Em HFT com containers de GPUs, podem bater métodos lineares — mas muitas vezes a melhora não justifica a complexidade.

- **Clustering** → achar padrões similares para montar *panel datasets*. Agrupe entidades por comportamento e treine modelos por cluster, ou use a pertinência como feature.

- **ARIMA** → o que você usa quando o chefe lembra vagamente da faculdade. Sendo justo, tem seu lugar em previsão univariada simples — mas em geral é usado por "sempre fizemos assim".

O padrão observado: **métodos lineares para negociar sinais diretamente; métodos não lineares para pesquisa e geração de sinais a interpretar.** O gradiente de *trading* → pesquisa acompanha o de alta → baixa frequência.

> **➕ Acréscimo — o erro nº1 em finanças: validação cruzada errada.** Em séries temporais você **nunca** usa k-fold aleatório — isso vaza o futuro para o passado e infla suas métricas. Use **validação *walk-forward*** (`TimeSeriesSplit`) e, em estratégias quantitativas, **Purged K-Fold com embargo** (López de Prado) para eliminar vazamento por sobreposição de janelas. Métrica boa em backtest com CV errado é a forma mais comum de se enganar.

---

## O roadmap real do Engenheiro de ML

Quase todo roadmap por aí mente sobre o que importa. O que você de fato precisa:

- **Matemática** — o suficiente de álgebra linear (transformações), cálculo (otimização) e estatística (para saber quando o modelo está te enganando). Você não precisa derivar tudo do zero, mas precisa entender as fórmulas que usa.
- **Programação** — Python. Outras linguagens existem (Java, R, Julia), mas o ecossistema vive no Python.
- **Bancos de dados** — você precisa de **SQL**. ETL, data warehousing etc. costumam ser problema de outra pessoa; pegue os dados e siga.
- **Bibliotecas de ML** — onde você gasta o tempo de verdade: `scikit-learn` (ML clássico); `Darts`, `mlforecast`, `statsforecast` (séries temporais); `XGBoost`/`LightGBM`/`CatBoost` (boosting); `pandas` (ou `Polars` se for chique); `statsmodels` (testes estatísticos — essenciais para checar se seu sinal é sorte ou sinal real). Para redes: `TensorFlow`+`Keras` (mais fácil) ou `PyTorch` (melhor para NLP/pesquisa).
- **Algoritmos de ML** — progressão do simples ao complexo: comece em regressão linear, vá para métodos de árvore, e só chegue em deep learning quando os dados justificarem. Não pule direto para redes "porque são legais".
- **Visualização** — `Matplotlib` cobre 90%. O resto (PowerBI/Looker/Tableau) é dashboard de outra pessoa. Seu trabalho é o gráfico que mostra se o modelo funciona.

> **➕ Acréscimo — o que falta nessa lista e cobra caro depois:** **controle de versão (Git)**, **rastreamento de experimentos** (MLflow ou Weights & Biases — você *vai* esquecer qual config gerou qual resultado), **validação de dados/contratos de schema** e o básico de **MLOps/monitoramento** (detecção de *data drift* e *concept drift*). Modelo em produção que ninguém monitora apodrece silenciosamente.

---

## Métricas de regressão que de fato importam

A escolha da métrica muda fundamentalmente o que o modelo otimiza.

| Métrica | Quando usar | Cuidado |
|---|---|---|
| **MSE** | Dados limpos, sem outliers. Penaliza muito erros grandes (devido ao quadrado) | Inútil com poucos outliers extremos |
| **RMSE** | Igual ao MSE, mas na mesma unidade do alvo (interpretável) | Mesma sensibilidade a outliers |
| **MAE** | Quando há outliers e você quer robustez; trata todos os erros igualmente | Funciona com valores positivos, zero e negativos |
| **MAPE** | Interpretabilidade ("erra 12% em média") | Só para valores positivos; explode perto de zero |
| **RMSLE** | Valores positivos com distribuição não normal / crescimento exponencial | A transformação log evita que valores grandes dominem |
| **wMAPE** | Erro percentual quando os dados variam ordens de magnitude (pondera pelos valores reais) | Resolve o problema do MAPE com escalas distintas |
| **sMAPE** | Resolve o problema do MAPE com zeros/negativos (fórmula simétrica) | Limitado entre 0 e 200% |
| **R²** | Quando o chefe só conhece essa; proporção da variância explicada | Pode enganar com não linearidade/extrapolação |

O truque é casar a métrica ao problema: previsão de vendas em que 10% de erro em valores pequenos não importa, mas em vendas grandes sim? → **wMAPE**. Outliers reais e importantes? → não use MSE. Apresentar para executivos? → **R²**.

> **➕ Acréscimo — duas métricas que faltaram:**
> - **MASE (Mean Absolute Scaled Error)** — o padrão-ouro em previsão de séries temporais. Compara seu modelo a um *baseline* ingênuo (naïve): MASE < 1 significa que você bate o "prever o último valor". É escala-independente e não quebra com zeros.
> - **Pinball loss (quantile loss)** — a métrica certa quando você prevê *quantis/intervalos* em vez de um ponto, essencial para previsão probabilística e gestão de risco.
> E uma nota: em **classificação**, acurácia engana com classes desbalanceadas. Prefira **F1**, **PR-AUC** (melhor que ROC-AUC quando a classe positiva é rara) e cheque a **calibração** das probabilidades (curva de calibração / Brier score) se você for usar os *scores* como probabilidades reais.

---

## A linha de fundo

ML em produção é menos sobre conhecer todos os algoritmos e mais sobre saber:

1. **Quais 2–3 parâmetros importam** em cada algoritmo;
2. **Quando usar cada algoritmo** com base nas características dos dados;
3. **Quais métricas** se alinham ao problema de negócio real.

Pare de tentar ajustar todo hiperparâmetro — foque nos que importam. Pare de usar redes neurais para tudo — case o algoritmo ao tamanho dos dados e à estrutura do problema. Pare de usar MSE quando há outliers.

O caminho de estudante a engenheiro de ML não é aprender mais algoritmos — é desenvolver a intuição de quais ferramentas servem a quais problemas e onde concentrar o esforço de ajuste. O resto são detalhes.

Agora vá construir algo que realmente funcione.
