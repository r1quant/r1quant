# Resumo detalhado — *The Art of Quantitative Finance Vol. 2* (Gerhard Larcher)

## Primeira parte: Capítulo 1 — "Volatilities" (Volatilidades)

O livro, escrito por Gerhard Larcher (Universidade Johannes Kepler de Linz) e publicado pela Springer em 2023, tem como subtítulo *Volatilities, Stochastic Analysis and Valuation Tools* e se divide em três grandes capítulos. A primeira parte — o **Capítulo 1, "Volatilities"** — é dedicada inteiramente ao conceito de volatilidade, do mais elementar (volatilidade histórica) ao mais sofisticado (índices de volatilidade como o VIX e seus derivativos).

## Segunda parte: Capítulo 2 — "Extensions of the Black-Scholes Theory to Other Types of Options"

A segunda parte do livro estende a teoria de Black-Scholes, vista até aqui apenas para calls e puts plain vanilla, a tipos de opções mais complexos. O fio condutor é sempre o mesmo princípio: o preço justo de um derivativo é o valor esperado descontado do seu payoff sob a medida risco-neutra. Em alguns casos esse valor esperado tem fórmula fechada; na maioria, ele precisa ser aproximado — e o método de eleição para isso, especialmente para opções dependentes da trajetória, é o **método de Monte Carlo**, que ocupa boa parte do capítulo. Os temas cobertos são: opções de câmbio, opções sobre futuros, opções americanas, opções dependentes da trajetória (exóticas), Monte Carlo e suas variantes, e opções multi-ativo.

## Terceira (e última) parte: Capítulo 3 — "Fundamentals: Stochastic Analysis and Applications, Interest Rate Dynamics, and Basic Principles of Pricing Interest Rate Derivatives"

A última parte do livro é a mais teórica e fornece as ferramentas matemáticas que faltavam: uma introdução intuitiva à **análise estocástica** (cálculo de Itô, martingales, Feynman-Kac) e sua aplicação à **modelagem de taxas de juros** e à **precificação de derivativos de juros**. É o terceiro termo do subtítulo do livro ("stochastic analysis"). O autor avisa repetidamente que aborda esses campos profundos apenas de forma heurística e intuitiva, sem rigor matemático completo, recomendando os livros de Björk e Steele para aprofundamento.

---

# Part 1 - Volatilities

## Volatilidade histórica e suas limitações (seções 1.1–1.4)

O capítulo abre definindo volatilidade, em sentido amplo, como uma medida de quão fortemente o preço de um ativo flutua, usada em gestão de risco, gestão de carteiras, precificação de derivativos e classificação de fundos. Larcher logo adverte que essa definição intuitiva é "severamente falha", pois existem tipos muito diferentes de volatilidade.

A **volatilidade histórica** é construída assim: divide-se um intervalo [0, T] em N partes de comprimento *dt*, calculam-se os retornos contínuos (logarítmicos) *aᵢ = log(Aᵢ₊₁/Aᵢ)*, sua média (a "tendência" μ) e seu desvio-padrão σ. O desvio-padrão por *dt* é depois "anualizado" dividindo por √dt. Sob a hipótese de retornos normais e independentes, há regras de probabilidade conhecidas (68,27% dentro de ±1σ, 95,45% dentro de ±2σ, 99,73% dentro de ±3σ).

O ponto central é que **essa hipótese de normalidade e independência geralmente não vale**. Larcher demonstra isso com dados reais (S&P 500 de 1957–2017, DAX, EuroStoxx50 e IBM): a volatilidade anualizada calculada a partir de dados diários, semanais, mensais e anuais dá valores diferentes (tende a cair quanto mais longo o período de cálculo), provando que não existe uma "volatilidade anualizada bem definida" única.

O método histórico "ingênuo" (calcular o desvio-padrão de uma janela móvel de *n* dias) tem uma falha grave, ilustrada com o crash de 17 de outubro de 1987: um evento extremo isolado mantém a volatilidade histórica artificialmente alta por muito tempo, especialmente para janelas longas (n = 200 dias), que reagem com grande atraso. Janelas curtas (n = 10) reagem rápido, mas ignoram o passado e fazem o evento "desaparecer" abruptamente após *n* dias. A média histórica das volatilidades do S&P 500 desde 1957 é cerca de **13,93%**, ficando a maior parte do tempo entre 5% e 30%, com picos acima de 50% em apenas três episódios extremos: outubro de 1987, a crise financeira de 2008 e a primeira onda da Covid em 2020.

## Modelos ARCH/GARCH (seção 1.2)

Para corrigir essa deficiência, introduz-se o conceito de dar **peso decrescente aos retornos mais antigos**. Nos modelos ARCH, atribuem-se pesos não-negativos α₀ ≥ α₁ ≥ … e um peso β para uma média de longo prazo *sigL²*. Uma escolha comum é αᵢ = λ·αᵢ₋₁, com λ entre 0 e 1 (a J.P. Morgan sugere λ = 0,94): λ próximo de 1 dá mais peso ao passado. O parâmetro β controla quanto se ancora na média de longo prazo. Larcher mostra que, com isso, o estimador é não-viesado (seu valor esperado iguala a média de longo prazo estimada) e que o ARCH dissipa "explosões de volatilidade" de forma contínua e plausível, sendo mais calmo que a histórica curta, porém mais reativo que a longa. O modelo **GARCH(1,1)** é mencionado como alternativa próxima, mas não detalhado.

## Uso e previsão da volatilidade (seções 1.3–1.5)

Aqui o autor recapitula *para que* serve a volatilidade: classificação de risco de produtos estruturados (ex.: a lei austríaca de fundos exige sete classes de risco baseadas na volatilidade dos retornos semanais dos últimos 5 anos), gestão de risco (cálculo do Value at Risk, VaR) e, sobretudo, precificação de derivativos via Black-Scholes/modelo de Wiener.

Surge então a pergunta-chave: **qual estimativa em t=0 (histórica? ARCH?) melhor prevê a volatilidade realizada futura?** Em experimentos com o S&P 500, a autocorrelação de primeira ordem da volatilidade de 21 dias é 0,658 — positiva e significativa (volatilidades tendem a persistir), decaindo nas ordens seguintes (0,537, 0,449…). O melhor horizonte de previsão tem comprimento parecido com o do período a prever. Um modelo ARCH bem calibrado (n=55, β=0, λ=0,95) eleva a correlação previsão/realizado para impressionantes **0,93**. O autor enfatiza que esses testes são superficiais e ilustrativos.

A seção 1.5 prepara o terreno para Dupire: a volatilidade que entra em Black-Scholes é o desvio-padrão (anualizado) do retorno do ativo subjacente em [0, T]. Mas e se a volatilidade variar ao longo da vida do derivativo? O proof original de Black-Scholes pressupunha volatilidade constante.

## O modelo de Dupire — volatilidade dependente de tempo e preço (seção 1.6)

Esta é uma seção teórica central. Larcher apresenta dois teoremas de **Bruno Dupire**:

- **Teorema 1.1 (volatilidade dependente do tempo σ(t)):** o preço justo de um derivativo europeu pode ser calculado sem conhecer σ(t) explicitamente — basta conhecer o valor médio de σ²(t), ou seja, (1/T)∫₀ᵀσ²(t)dt. E esse valor médio pode ser estimado *a posteriori* pela própria volatilidade histórica. As fórmulas de call e put mantêm a mesma forma, substituindo a σ constante pela média integral. O autor deriva isso heurísticamente, discretizando [0,T] e usando a propriedade da soma de variáveis normais independentes, chegando a uma soma de Riemann que converge para a integral.

- **Teorema 1.2 (volatilidade dependente de tempo *e* preço σ(t, S(t))):** o preço justo já não tem fórmula fechada, mas é solução de uma **equação diferencial parcial** (uma generalização da EDP de Black-Scholes), com condição de contorno F(T,s) = Φ(s).

## Volatilidade implícita (seções 1.7–1.10)

Em vez de estimar a volatilidade a partir de dados históricos, pode-se **invertê-la a partir dos preços de mercado dos derivativos**. Escrevendo o preço como F(0) = BS(T, σ(T), Φ), a **volatilidade implícita** σ(T) é o valor que reproduz o preço observado. Não há fórmula explícita, mas resolve-se numericamente.

O fato empírico crucial: se o mercado fosse perfeitamente eficiente e o modelo de Wiener fosse exato, *todas* as opções sobre o mesmo subjacente com o mesmo vencimento dariam a *mesma* volatilidade implícita. Mas não dão — em tabelas reais da Interactive Brokers (out/2018), a volatilidade implícita do S&P 500 cai conforme o strike sobe (de 25,3% para 18,9%). Larcher discute três explicações possíveis: (a) discordância entre participantes, (b) opções mal precificadas, ou (c) o S&P 500 não segue o modelo de Wiener — concluindo que, em mercados líquidos, a causa principal é (c), as imperfeições do modelo de Wiener (caudas pesadas, dependências). Isso conecta-se à hipótese dos mercados eficientes de Eugene Fama (~1970).

A seção 1.8 prova um resultado elegante de não-arbitragem: a volatilidade implícita de uma **call** é necessariamente igual à da **put** de mesmo strike e vencimento, independentemente do modelo, decorrente da paridade put-call.

A seção 1.9 classifica os padrões: **volatility skew** (linha decrescente, típica de ações e índices), **volatility smile** (forma simétrica em U, típica de câmbio, ex.: EUR/USD) e a **volatility surface** (superfície 3D em função do strike/S₀ e do tempo até o vencimento). Skews tendem a ser menos acentuados para vencimentos mais longos.

A seção 1.10 mostra como **inferir a distribuição de preços antecipada pelo mercado** a partir da curva de volatilidade. Usando um portfólio de spread vertical (call long em strike *x*, call short em *x+ε*), deriva-se que W(S(T) > x) = −e^(rT)·C′(x), e a densidade implícita é f(y) = S₀·T·e^(yT)·e^(rT)·C″(...). Conclusão qualitativa importante: **um volatility skew indica caudas pesadas** (maior probabilidade de eventos muito pequenos e muito grandes do que a normal). O cálculo prático, porém, é numericamente instável e exige uma função interpoladora C bem-comportada (duas vezes diferenciável, C″ > 0).

## Índices de volatilidade e o VIX (seções 1.11–1.13)

Apresentam-se os índices de volatilidade (VIX para o S&P 500, VXN para o NASDAQ-100, VXD, VDAX-NEW, VSTOXX, VSMI). O VIX, calculado pela CBOE, mudou de metodologia: até 2003 usava volatilidades implícitas Black-Scholes de opções do S&P 100; desde 2003 usa um método **independente de modelo** (desenvolvido pela Goldman Sachs), o que tem a vantagem de tornar o próprio VIX um produto financeiro replicável e hedgeável. A média de longo prazo do VIX desde 1990 é **19,48%**, com picos próximos de 80% em 2008 e 2020 e um valor retroativo do VXO de **mais de 150% em 19/out/1987**.

A seção 1.12 examina as propriedades estatísticas: o retorno diário do VIX tem desvio-padrão de ~7% (muito maior que o ~1% do S&P 500), com caudas muito pesadas. Um ponto sutil e importante: a volatilidade anual *real* do VIX (46,53%) **não pode** ser extrapolada dos retornos diários pela normalização usual √252 (que daria 111,1%), porque os retornos do VIX violam fortemente a hipótese de independência e normalidade — sua alta volatilidade ocorre sobretudo no "micro" (oscilações diárias).

A seção 1.13 trata da **correlação VIX–SPX**, corrigindo um equívoco comum (que constava até na Wikipédia alemã, alterada por instigação do autor). A verdade não é que o VIX prevê o SPX, mas o contrário: quedas do SPX provocam alta da volatilidade implícita (puts ficam mais caras), logo **a volatilidade implícita reage ao subjacente, não vice-versa**. A correlação mais forte é entre os retornos diários do mesmo dia (~ −0,70). Estatísticas notáveis: dos 875 dias em que o SPX caiu mais de 1%, o VIX subiu em 834; dos 936 dias em que o SPX subiu mais de 1%, o VIX caiu em 869. O autor propõe modelar essa relação por σₜ = σ₀·(S₀/Sₜ)^a, com **a ≈ 4** ajustando-se surpreendentemente bem aos dados reais (especialmente em janelas de até ~100 dias).

## Aplicações práticas (seções 1.14–1.17)

A seção 1.14 calcula como a volatilidade variável σ(t,s) altera os "gregos". Para o delta de uma call, surge um termo aditivo extra: Δ = N(d₁) + e^(−r(T−t))·K·φ(d₂)·σ′(t,s)·√(T−t). Como σ′ tende a ser negativa (volatilidade cai quando o preço sobe), **o delta de uma call pode até ficar negativo** em certas faixas (efeito mais pronunciado para a=4), pois a alta da volatilidade num preço baixo pode superar o efeito do preço sobre o valor da opção.

A seção 1.15 estuda o **hedge combinando SPX e VIX**. Como o VIX sobe quando o SPX cai, uma carteira mista deveria reduzir o risco. O autor inclui um excelente *excursus* sobre **complexidade de algoritmos**: o cálculo "ingênuo" do *maximum drawdown* (MDD) é de ordem quadrática (~N²/2 pares), mas existe um algoritmo de **complexidade linear** (calculando recursivamente o máximo à esquerda U(t) e o mínimo à direita D(t) de cada ponto). Aproveita para discutir o problema do caixeiro-viajante e o famoso problema P versus NP. Resultados: o MDD do S&P 500 puro foi de −56,78% (out/2007 a mar/2009). Comparando estratégias com o **Sharpe ratio** ((μ−r)/σ), apenas a mistura com 20% de VIX se mostrou interessante (Sharpe levemente superior ao SPX puro, 0,26 vs 0,25, com drawdown menor, −43,44%).

A seção 1.16 confirma um achado central: **a volatilidade implícita (VIX) sistematicamente superestima a volatilidade realizada subsequente**. As correlações VIX/volatilidade histórica (~0,86) e VIX/realizada (~0,77) são altas. Disso surgem estratégias de "arbitragem de volatilidade": vender opções "caras" sistematicamente, vender opções com delta-hedge, ou negociar *volatility/variance swaps* (que pagam a diferença entre volatilidade realizada e implícita, independentes da direção do mercado).

A seção 1.17 detalha um exemplo concreto dessa ideia: o **CBOE S&P 500 PutWrite Index**, que vende sistematicamente puts ATM mensais sobre o S&P 500 e reinveste o caixa em T-Bills. Lucra-se com o prêmio quando o mercado sobe, estagna ou cai pouco; perde-se quando o S&P 500 cai bastante. Historicamente (desde 1986), apresentou retorno superior (9,89% a.a. vs 7,72%), com Sharpe de 0,54 vs 0,27 e drawdown menor (−37,09% vs −56,56%).

## Metodologia de cálculo do VIX e derivativos sobre o VIX (seções 1.18–1.22)

A seção 1.18 é tecnicamente densa: explica a **fórmula efetiva do VIX**, calculada (a cada minuto) a partir dos preços de mercado de um portfólio ponderado de puts OTM e calls OTM do S&P 500 com dois vencimentos (T₁ < 30 dias < T₂), combinados por pesos ω₁, ω₂. O ponto brilhante da derivação: mostra que esse portfólio replica aproximadamente o payoff (2e^(rT)/T)·[S_T/S₀ − 1 − log(S_T/S₀)], cujo preço justo no modelo de Black-Scholes é exatamente σ̄² (a variância do subjacente). Por isso o VIX **não depende de modelo** e pode ser perfeitamente replicado/hedgeado com opções do S&P 500.

A seção 1.19 trata, em tom de excursus, das **anomalias de preço**, em especial o "efeito fim de semana" (volatilidade tende a ser maior nas segundas-feiras). Cita ainda o efeito janeiro, efeito do clima, momentum e *small-firm effect*, observando que muitas anomalias enfraqueceram desde a virada do milênio. Nos dados do S&P 500 (1990–2018), o único efeito robusto encontrado é o VIX mais alto às segundas-feiras.

As seções 1.20–1.22 cobrem os derivativos do VIX. **Futuros de VIX** (ticker VX, multiplicador 1000, desde 2004) são o modo mais eficiente de negociar o VIX; o autor questiona a afirmação da CBOE de que eles "refletem a expectativa de mercado", argumentando que, por não-arbitragem, o strike justo é em princípio bem-definido — embora desvios ocorram pela dificuldade de replicação contínua e pela propriedade de **reversão à média** do VIX. Inclui um experimento fictício de trading de reversão à média (com parâmetros "distância" d e "ratio"), que apresenta bom desempenho histórico, exceto se iniciado no começo da crise de 2008. **Opções de VIX** (europeias, tamanho de contrato US$ 100) são analisadas; como o modelo de Wiener é inadequado para o VIX (não captura a reversão à média), o autor menciona que modelos como o de **Heston** seriam apropriados (a serem vistos depois, com ferramentas de análise estocástica). Para estimar a volatilidade do VIX, usa-se o **VVIX** (volatilidade da volatilidade). O capítulo encerra (1.22) com um exemplo de estratégia combinando opções de SPX e VIX: assumindo a relação σₜ = σ₀·(S₀/Sₜ)⁴, mostra que combinar 30 contratos de call de VIX *long* com 1 put de SPX *short* gera uma função de lucro consistentemente positiva — uma construção que ilustra a profunda ligação econômica entre os dois instrumentos.

## Fio condutor do capítulo

A primeira parte conduz o leitor por uma progressão lógica: parte da medida histórica "ingênua" de volatilidade, expõe suas falhas, refina-a com ARCH/GARCH, generaliza a teoria de precificação para volatilidade variável (Dupire), e então introduz o conceito conceitualmente oposto e mais poderoso — a **volatilidade implícita** —, culminando no VIX, seus derivativos e suas aplicações em hedge e arbitragem. O estilo é deliberadamente intuitivo e heurístico (o autor adia o rigor matacial da análise estocástica para o Capítulo 3), recheado de dados empíricos reais do S&P 500 e de exemplos de telas da Interactive Brokers e da Bloomberg.

--- 

# Part 2 — "Extensions of the Black-Scholes Theory to Other Types of Options"

## Opções de câmbio (FX) — seção 2.2

Uma opção de câmbio tem como subjacente uma taxa de câmbio X(t) (preço de uma moeda estrangeira em euros). O ponto central é que **manter a moeda estrangeira gera um rendimento contínuo** à taxa livre de risco estrangeira r_f, de modo que se usa a segunda versão de Black-Scholes (com pagamentos), com q = r_f. A dinâmica risco-neutra é então S̃(T) = S(0)·e^((r−r_f−σ²/2)T + σ√T·w), e seguem-se fórmulas explícitas de call e put (com d̃₁, d̃₂ contendo o termo r−r_f). O autor calcula a volatilidade implícita de uma put real sobre o dólar (3/dez/2018): com r = −0,46% (euro) e r_f = 2,18% (dólar), obtém vol implícita de ~9,7%–10,4%. Há um alerta prático importante, ilustrado com uma opção real do Commerzbank: as especificações de produtos de câmbio variam (qual moeda é o numerário, conversão do payoff na expiração, estilo americano), e isso muda materialmente o payoff e o preço — é preciso ler as especificações com cuidado.

## Opções sobre futuros — seção 2.3

Aqui o subjacente é um derivativo (um contrato futuro). Como **comprar um futuro custa zero**, é difícil dizer diretamente qual versão de Black-Scholes usar. Larcher resolve isso via um modelo binomial de um passo aplicado ao *strike* do futuro K(t), e mostra que uma opção sobre futuro é precificada exatamente como uma opção sobre um ativo com pagamento contínuo à taxa q = r. A dinâmica risco-neutra do strike é K̃(T) = K(0)·e^(−σ²/2·T + σ√T·w) (sem termo de drift r), e há fórmulas explícitas de call e put. Um resultado elegante: quando a expiração da opção coincide com a do futuro (T_O = T_F), a opção sobre o futuro vale exatamente o mesmo que a opção sobre o subjacente. Ressalva: para futuros de taxa de juros (ex.: Bund futures), o modelo de Wiener não é adequado.

## Opções americanas — seções 2.4 a 2.6

Esta é uma seção teórica densa. Primeiro, dois resultados de exercício antecipado (Teorema 2.9): se r ≥ 0, uma **call americana** sem pagamentos vale o mesmo que a europeia e nunca deve ser exercida antecipadamente (pois C_a(t) > S(t) − K = payoff de exercício imediato); analogamente, se r ≤ 0, a **put americana** iguala a europeia.

No caso geral, não há fórmula fechada — usa-se o método de **backwardation** (indução regressiva) no modelo binomial, que aproxima o modelo de Wiener com precisão arbitrária. Em cada nó, compara-se o payoff de exercício imediato f̃ com o valor de continuação (o valor europeu f^(e) calculado um passo adiante); exerce-se se e somente se f̃ for maior, e o valor americano no nó é o máximo dos dois. Larcher **prova rigorosamente** (no modelo de dois passos, generalizável por indução) que essa regra "lógica" é de fato financeiramente ótima, usando argumentos de arbitragem com portfólios replicantes em ambas as direções. Apresenta o algoritmo recursivo completo para N passos e estende a ideia para **opções bermudanas** (exercício permitido apenas em datas predefinidas).

A seção 2.5 traz um exemplo numérico em modelo de dois passos (valor americano 57,5 vs europeu 55) e mostra a convergência da aproximação binomial conforme N cresce (estabilizando em ~236,3 no exemplo). A seção 2.6 trata do **hedge de opções americanas**: análogo ao europeu, mas executado dinamicamente passo a passo. Curiosamente, se o detentor age "contra a teoria" (não exerce quando deveria, ou vice-versa), o vendedor que hedgeou corretamente pode até embolsar lucro extra.

## Opções dependentes da trajetória (exóticas) — seções 2.7 a 2.14

A seção 2.7 define e classifica as principais opções exóticas, cujo payoff depende de toda (ou parte) da trajetória do preço:

As **opções asiáticas** têm payoff baseado na média (aritmética ou geométrica) do preço em vários instantes — ex.: as TAPOs negociadas na London Metal Exchange. As **opções lookback** dependem do mínimo ou máximo do preço durante a vida da opção. As **opções barreira** (up-and-out, down-and-out, up-and-in, down-and-in) são calls/puts ordinárias que se tornam inválidas (ou só válidas) caso o preço cruze uma barreira L em algum momento.

A seção 2.8 enuncia o **Teorema 2.12 — a fórmula de Black-Scholes para opções path-dependent**: F(0) = e^(−rT)·E[Φ((S̃_t)_{t∈[0,T]})], com S̃ seguindo a dinâmica risco-neutra. A prova é "plausibilizada" precificando no modelo binomial de três passos, onde o preço é a soma, sobre todos os caminhos possíveis, do payoff de cada caminho ponderado pela sua probabilidade artificial (risco-neutra). A seção 2.9 traz um exemplo numérico (put asiática aritmética em modelo de três passos, europeia e americana).

A seção 2.10 aborda a **complexidade** de precificar exóticas. No caso geral, um modelo binomial de N passos tem 2^(N+1)−2 caminhos — já com 30 passos são ~2 bilhões de caminhos, inviável. Porém, para certas opções (como as lookback), o número de payoffs *distintos* em cada nó é "relativamente pequeno". Larcher apresenta um algoritmo engenhoso de três passos (determinar mínimos potenciais, "desdobrar" o grafo, fazer backwardation) que reduz a complexidade de ~2 bilhões para ~N⁴/16 nós (cerca de 50 mil para N=30). A seção 2.11 ilustra isso com uma lookback americana num modelo de quatro passos (valor final 8,375).

As seções 2.12 e 2.13 dão **fórmulas explícitas** para alguns casos. Para opções barreira, há quatro fórmulas que relacionam o preço da versão com barreira ao preço sem barreira, usando o fator (L/s)^(2r/σ²−1) e uma versão "espelhada" da opção em L²/s. Para a **opção asiática geométrica** (com pontos de medição equidistantes), Larcher faz uma derivação completa e bonita: o payoff geométrico transforma-se, via propriedades de somas de variáveis normais, no payoff de uma call plain vanilla ordinária com **parâmetros modificados** σ̃ = σ·√((1+1/M)(2+1/M)/6) e r̃ (ambos sempre ≤ aos originais). Como a média geométrica ≤ média aritmética (prova de Pólya incluída), uma call asiática geométrica vale sempre menos que a aritmética. A seção 2.14 observa brevemente que o hedge dessas opções segue por diferenciação da fórmula (quando existe) ou por estimativa via Monte Carlo.

## O método de Monte Carlo — seções 2.15 a 2.27

Esta é a espinha dorsal numérica do capítulo. A seção 2.15 explica o **princípio básico**: para aproximar E(Y), geram-se N realizações de Y e toma-se a média. Para uma call plain vanilla, basta simular o preço final (um número aleatório por cenário). Um insight prático importante: o erro de Monte Carlo costuma ser **menor que o erro de uma estimativa imprecisa da volatilidade** — trocar σ de 0,30 para 0,29/0,31 altera o preço mais do que o ruído da simulação.

A seção 2.16 distingue dois casos em opções path-dependent: (a) payoff dependente de pontos fixos predefinidos (asiáticas) — basta simular nesses pontos; (b) payoff dependente de toda a trajetória (barreira, lookback) — é preciso **discretizar** a trajetória em s pontos, o que introduz um erro de discretização adicional. As seções 2.17 e 2.18 trazem exemplos (asiática geométrica e barreira down-and-out). O exemplo da barreira é instrutivo: com S(0)=100 a convergência é ótima com apenas 12 pontos amostrais, mas com S(0)=65 (perto da barreira L=60) são necessários **1000 pontos** para um resultado aceitável, com custo computacional muito maior. A seção 2.19 conecta isso à prática real: barreiras estão embutidas em **certificados turbo e bonus** (ex.: um Classic TURBO warrant do Commerzbank é uma put barreira up-and-out sobre o DAX), e o preço Monte Carlo (10,11 €) bate com a cotação real (10,15 €).

A seção 2.20 trata da **estimativa dos gregos por Monte Carlo**. Duas abordagens: (1) aproximar o quociente diferencial [F(s+h)−F(s)]/h — instável, pois h aparece no denominador e exige escolhas delicadas; (2) **diferenciar a função payoff** e simular o valor esperado da derivada — muito mais eficiente e sem erro de discretização (para o delta de uma call, basta simular E[1_{x≥K}·...]). O gamma é o caso difícil: a abordagem (2) falha (a derivada segunda do payoff é infinita em K), e a melhor saída é estimar o delta em dois pontos via MC e tomar o quociente diferencial — mas mesmo assim os resultados pedem cautela. A seção 2.21 aplica o delta-hedging por MC à asiática geométrica.

A seção 2.22 é teórica e fundamental: **quão bom é o Monte Carlo?** Via teorema do limite central (ilustrado com o lançamento de dados), demonstra-se que o erro estocástico é da ordem de **σ/√N**. Consequência prática célebre: melhorar a precisão por um fator de 10 exige aumentar N por um fator de 100. O σ é a "complexidade" intrínseca do problema, independente de N.

As seções 2.23 a 2.25 são um excurso sobre **números aleatórios** e **Quasi-Monte Carlo (QMC)**. Os geradores modernos (baseados em teoria dos números; obras de referência de Knuth e Niederreiter) são confiáveis. Introduz-se o conceito de **discrepância** de um conjunto de pontos (entre 1/N e 1): sequências verdadeiramente aleatórias têm discrepância da ordem de 1/√N, enquanto sequências de **baixa discrepância** (como os conjuntos de Hammersley, construídos pela representação de n em bases primas, ou os melhores conjuntos de Niederreiter/Sobol) atingem ordens próximas de 1/N. QMC pode superar MC, mas tem limitações: não serve para simular trajetórias com muitas dependências entre pontos sucessivos.

As seções 2.26 e 2.27 cobrem **redução de variância**. As duas técnicas principais — *importance sampling* (reescrever o problema com uma densidade g proporcional a X·f, reduzindo σ) e *control variates* (usar uma variável auxiliar Y de valor esperado conhecido e fortemente correlacionada com X, obtendo σ(Z) = σ(X)·√(1−ρ²)) — modificam o problema sem alterar o resultado, mas reduzindo o desvio-padrão. O exemplo da seção 2.27 usa a asiática geométrica (de valor exato conhecido) como control variate para precificar a asiática aritmética: com ρ ≈ 0,98–0,999, a convergência acelera dramaticamente.

## Opções multi-ativo — seções 2.28 a 2.31

A última parte trata de opções sobre vários subjacentes (ex.: payoff dependente do máximo de d ações, ou opções de troca). O desafio é que os ativos são **correlacionados**, então os ruídos W^(i) não podem ser independentes. A solução (seção 2.29) é a **decomposição de Cholesky**: constrói-se cada W^(i) como combinação linear de variáveis independentes w^(1),...,w^(d), com coeficientes a_{i,j} escolhidos de modo a reproduzir exatamente a matriz de correlação M (condição: M positiva definida; obtém-se C tal que C·Cᵀ = M, sempre triangular inferior). O autor exemplifica manualmente o caso 2D (W^(2) = ρ·w^(1) + √(1−ρ²)·w^(2)) e o caso 3D via Mathematica.

A seção 2.30 enuncia a fórmula de Black-Scholes multi-ativo (Teorema 2.17), e a seção 2.31 fecha o capítulo com um exemplo concreto: uma opção sobre o máximo de 10 ações correlacionadas, precificada simultaneamente por MC puro, QMC-Hammersley e QMC-Niederreiter. As duas variantes QMC estabilizam muito mais rápido (valor ~38,6) que o MC puro, embora, nas implementações do autor, o QMC tenha levado cerca de cinco vezes mais tempo de execução.

## Fio condutor do capítulo

O Capítulo 2 é essencialmente um catálogo de **ferramentas de avaliação** (o segundo termo do subtítulo do livro). A lógica é progressiva: começa adaptando Black-Scholes a subjacentes "diferentes" mas ainda simples (câmbio, futuros) via o truque do rendimento contínuo q; passa às opções americanas, onde a fórmula fechada cede lugar à backwardation provada por arbitragem; chega às exóticas, cuja complexidade combinatória motiva o método de Monte Carlo; e dedica metade do capítulo a dominar Monte Carlo — sua taxa de erro 1/√N, suas variantes QMC e de redução de variância — culminando nas opções multi-ativo e na decomposição de Cholesky. O estilo permanece intuitivo e empírico, com exemplos reais (Commerzbank, Interactive Brokers) e remissões constantes ao software do autor (app.lsqf.org). O capítulo deixa explicitamente em aberto dois temas — opções americanas path-dependent e derivativos de taxa de juros — que serão retomados no Capítulo 3.

--- 

# Part 3 - "Fundamentals: Stochastic Analysis and Applications, Interest Rate Dynamics, and Basic Principles of Pricing Interest Rate Derivatives"

## Por que modelar juros é diferente — seções 3.1 e 3.2

O modelo de Wiener (movimento browniano geométrico) usado para ações é inadequado para juros: ao simular taxas em horizontes longos (100 anos), ele produz valores irrealisticamente grandes, e além disso nunca permite taxas negativas (que de fato ocorreram nos mercados). Mas o desafio central não é modelar *uma* taxa, e sim a **consistência entre todas elas**: pela ausência de arbitragem, escolher um modelo para a Libor de 6 meses pode restringir, ditar ou até impossibilitar modelos para o swap de 10 anos.

A seção 3.2 introduz, de forma muito gradual, os **processos estocásticos** e sua representação. Com três exemplos discretos, ilustra três estruturas de dependência crescente, culminando na definição de **processo de Markov** (a distribuição futura depende apenas do valor presente, não da trajetória anterior). Estabelece a notação diferencial dS(t) = α·dt + β·dB(t), base de tudo que segue.

## O cálculo de Itô — seções 3.3 e 3.4

A seção 3.3 apresenta vários **modelos de difusão** via sua representação diferencial. Os mais importantes para juros são o **modelo de Ornstein-Uhlenbeck com reversão à média** (dS = a·(m−S)·dt + b·dB: a taxa tende a flutuar em torno de m; *a* controla a velocidade/frequência da reversão, *b* a amplitude) e o **modelo de Cox-Ingersoll-Ross** (dS = a·(m−S)·dt + b·√S·dB, que, sob a condição 2am ≥ b², gera apenas valores positivos — por muito tempo visto como vantagem sobre o OU, até surgirem juros negativos reais). Também são apresentados o crescimento exponencial com capacidade limitada e variantes.

A seção 3.4 é um excurso sobre a ferramenta mais importante da análise estocástica, a **fórmula de Itô**. Larcher mostra que a abordagem "ingênua" do cálculo clássico (regra da cadeia) dá um resultado *errado*: a versão correta para Y(t) = g(t, S(t)) carrega um **termo adicional** g_xx·β²/2·dt, característico dos resultados estocásticos. Aplica a fórmula para verificar que o movimento browniano geométrico é solução de dS = a·S·dt + b·S·dB.

## Fundamentos do mercado de juros — seções 3.7 a 3.9

A seção 3.7 define formalmente o mercado de **títulos zero-cupom** sem atrito: p(t,T) é o preço em t de um título que paga 1 euro em T, com p(T,T) = 1. A partir de p(t,T) derivam-se todas as demais taxas: taxas forward e spot simples (Libor) e contínuas, a **taxa instantânea (short rate)** r(t) = f(t,t) = −∂log p(t,T)/∂T|_{T=t}, e o **processo da conta-corrente** B_t = e^(∫₀ᵗ r(s)ds). Notação importante: a partir daqui, B passa a denotar a conta-corrente e o movimento browniano passa a ser W (não mais B). Resultado-chave: p(t,T) = e^(−∫ₜᵀ f(t,u)du), de modo que **basta modelar p(t,T) (ou f(t,T)) para todos os T** — ou, melhor ainda, perguntar se basta modelar a short rate e derivar tudo o mais por não-arbitragem.

As seções 3.8 e 3.9 precificam **bonds com cupom fixo** (combinação de zero-cupons), **bonds de taxa flutuante** (resultado notável: o preço justo de um floating rate bond em t é simplesmente p(t,T₁)/p(T₀,T₁), e exatamente 1 na emissão) e **swaps de taxa de juros**. A **taxa fair do swap** (swap rate) é R = [1 − p(T₀,Tₙ)] / [δ·Σp(T₀,Tᵢ)].

## A abordagem short-rate e o "market price of risk" — seção 3.10

Esta é a seção teórica central. Assumindo a short rate r(t) como processo de Itô dr = μ·dt + σ·dW, Larcher pergunta se isso basta, por não-arbitragem, para precificar todos os bonds. A resposta é **não — é preciso modelar pelo menos um produto adicional**. A derivação (heurística) é elegante: tomam-se dois bonds de vencimentos S e T, aplica-se Itô a seus preços, e constrói-se um **portfólio dinâmico autofinanciado** cuja escolha de pesos *elimina o componente aleatório* (o termo do browniano). O portfólio resultante é determinístico e, por não-arbitragem, deve render exatamente como a conta-corrente. Disso emerge a equação notável:

(α_T − r)/σ_T = (α_S − r)/σ_S

Ou seja, essa expressão (semelhante a um Sharpe ratio: tendência menos juros dividido por volatilidade) — chamada de **"market price of risk" λ(t)** — é a *mesma para todos os bonds do mercado*, independente do vencimento. Conhecido λ(t) (que decorre de modelar um produto adicional), obtém-se uma **EDP** para o preço de qualquer bond, cuja solução é o valor esperado descontado sob uma "taxa artificial" ř(s) com tendência (μ − λ·σ) — a versão **risco-neutra**. O Teorema 3.5 generaliza isso para qualquer derivativo da short rate.

## Modelos de Vasicek e Hull-White — seções 3.11 a 3.16

A seção 3.12 define a **estrutura afim** de preços de bonds: p(t,T) = e^(A(t,T) − B(t,T)·r(t)). O Teorema 3.6 mostra que, quando μ e σ² são lineares em r, os bonds têm estrutura afim, e A e B satisfazem um sistema de EDOs explícito.

O **modelo de Vasicek** (seção 3.13, dr = (b − a·r)dt + σ·dW) e o **modelo de Hull-White** (seção 3.14, dr = (θ(t) − a·r)dt + σ·dW) são casos lineares e portanto afins, com fórmulas fechadas para A e B. A diferença prática está na **calibração**: no Vasicek os parâmetros constantes a, b são ajustados aos preços de mercado, gerando um sistema sobredeterminado (uma equação por vencimento, só duas incógnitas) que só se satisfaz aproximadamente; no Hull-White, a função θ(s) tem flexibilidade suficiente para **replicar exatamente** a curva de bonds e a curva forward observadas hoje. Larcher distingue cuidadosamente os parâmetros do modelo "real" dos do modelo "risco-neutro" (a difusão σ é a mesma, mas a tendência muda completamente).

A seção 3.15 dá fórmulas de **put-call parity para opções sobre preços de bonds**. A seção 3.16 precifica os derivativos de juros mais negociados: **caps e floors de juros** (e collars). A sacada técnica é mostrar que um **caplet** (que paga δ·max(0, L(Tᵢ₋₁,Tᵢ) − K) com base na Libor fixada em Tᵢ₋₁) é equivalente a (1 + δK) unidades de uma **put sobre o preço do bond Tᵢ** com strike 1/(1+δK) e expiração Tᵢ₋₁ — permitindo aplicar diretamente as fórmulas de bond options. Analogamente, um **floorlet** equivale a calls sobre o bond.

## Reaproveitando a análise estocástica: uma nova prova de Black-Scholes — seções 3.17 a 3.21

Esta sequência usa as ferramentas estocásticas para *re-derivar* Black-Scholes (provada no Volume I via modelo binomial) numa versão mais geral. A seção 3.17 deriva a **EDP de Black-Scholes** pela mesma técnica de portfólio determinístico da seção 3.10 (agora com ativo e derivativo): F_t + r·s·F_s + (σ·s)²/2·F_ss = r·F, com F(T,s) = Φ(s).

Para resolvê-la, são introduzidos três conceitos:
- A seção 3.18 apresenta o **integral estocástico de Itô** ∫f(s)dW(s), via somas de Itô que representam o lucro de uma estratégia de trading dinâmica. Mostra que ∫(W(t))²dW = (W(t))³/3 − ∫W dt (de novo, um termo extra em relação ao cálculo clássico).
- A seção 3.19 introduz **esperança condicional** E(S(w)|S(v)) e **martingale** (processo em que E(S(w)|S(v)) = S(v) — a melhor previsão do futuro é o valor presente, como o lucro esperado de um jogo justo). Prova que o movimento browniano e qualquer integral de Itô são martingales. Apresenta a notação E(·|F_v) das filtrações.
- A seção 3.20 deriva a **fórmula de Feynman-Kac**, descrita pelo autor como uma conexão "espantosa" entre dois campos aparentemente não relacionados: a solução de uma EDP equivale ao valor esperado condicional de um processo estocástico, F(t,x) = e^(r(T−t))·E(Φ(X(T))|X(t)=x). Ilustra com um exemplo resolvido (EDP com condição F(T,x) = x²).

A seção 3.21 colhe os frutos: aplicando Feynman-Kac à EDP de Black-Scholes (com μ = r·s, σ = σ·s), obtém-se a **fórmula de Black-Scholes** como valor esperado descontado do payoff sob a dinâmica risco-neutra — uma segunda prova "direta", sem o desvio pelo modelo binomial.

## Mercados completos e incompletos — seções 3.22 a 3.25

A seção 3.22 dá ainda uma terceira prova, mostrando que o **modelo de Black-Scholes é um mercado completo**: o preço justo do derivativo não depende de ele ser ou não continuamente negociável, e a estratégia de hedge perfeito é justamente o **delta-hedging** (manter F_s(t,S(t)) unidades do subjacente). A seção 3.23 generaliza para o **modelo de Black-Scholes multidimensional** (Teorema 3.14): com d ativos correlacionados governados por d brownianos independentes e matriz de covariância invertível, o mercado é completo. O ponto conceitual é a contagem de fontes de aleatoriedade versus produtos: se há **menos brownianos que ativos**, surge redundância/arbitragem (reduz-se o sistema); se há **mais brownianos que ativos**, o mercado em geral deixa de ser completo (produtos insuficientes para eliminar todas as fontes de risco).

As seções 3.24 e 3.25 tratam de **mercados incompletos**. O exemplo canônico é o **modelo trinomial de um passo**: com S(0) = 90 podendo ir a 150, 100 ou 50, tentar replicar o payoff de uma call (strike 80) leva a um sistema de **três equações e duas incógnitas, sem solução** — a opção não pode ser replicada. Em mercados incompletos, em geral não há um preço justo único; o que se obtém é (1) um **intervalo [a,b]** de preços livre de arbitragem, ou (2), usando dados de mercado adicionais, eventualmente um preço único mesmo para derivativos não replicáveis. A seção 3.25 ilustra o caso de subjacente não negociável.

O capítulo encerra apontando que esses fundamentos serão aplicados em estudos de caso no Volume III, e remete também a temas de gestão de risco (Value-at-Risk) e seleção de portfólio (Markowitz, Merton) mencionados na introdução.

## Fio condutor do capítulo e do livro

O Capítulo 3 é o alicerce teórico que dá rigor (heurístico) a tudo que veio antes. A lógica é: primeiro mostra por que juros exigem modelos diferentes (reversão à média), constrói o cálculo de Itô como linguagem, e o aplica de duas formas paralelas — à modelagem de juros (short rate → market price of risk → estrutura afim → Vasicek/Hull-White → caps e floors) e à re-derivação de Black-Scholes via Feynman-Kac. Termina discutindo *quando* a teoria funciona (completude) e o que fazer quando não funciona (mercados incompletos). Os três pilares de análise estocástica — fórmula de Itô, martingales, Feynman-Kac — são os mesmos que sustentam toda a finança quantitativa moderna.

