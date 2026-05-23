Microstructural Foundation of Rough Log-Normal Volatility Models, por Paul P. Hager, Ulrich Horst, Thomas Wagenhofer e Wei Xu (março de 2026, arXiv:2603.13170)

## 1. Em uma frase

O artigo constrói uma **fundação microestrutural para o modelo *rough Bergomi*** (volatilidade rough log-normal): partindo de um mercado em que ordens chegam segundo um **processo de Poisson** e exercem **impacto lento e duradouro sobre a volatilidade**, os autores provam que, após reescalonamento, o par (log-preço, log-volatilidade) **converge fracamente** para um modelo de volatilidade rough log-normal — e, crucialmente, quantificam a **velocidade dessa convergência** (taxas de erro *fraco*), algo inédito na literatura microestrutural rough.

---

## 2. Contexto: o que é "volatilidade rough" e por que importa

Na última década, a *volatilidade rough* tornou-se um dos avanços mais influentes em finanças quantitativas. A motivação empírica vem de duas observações:

1. **Gatheral (2006)** documentou que a superfície de volatilidade implícita exibe um *skew* de curtíssimo prazo muito íngreme, que os modelos clássicos de volatilidade estocástica markoviana só reproduziam à custa de uma parametrização excessiva.
2. **Gatheral, Jaisson e Rosenbaum (2018)** mostraram estatisticamente que a log-volatilidade se comporta como um **movimento browniano fracionário (fBm)** com parâmetro de Hurst $H \approx 0{,}1$ — bem abaixo do valor browniano $H=1/2$. Ou seja, as trajetórias de volatilidade são **muito mais "ásperas" (rough)** do que se supunha.

A partir daí, **Bayer, Friz e Gatheral (2016)** introduziram o **rough Bergomi**, em que a volatilidade é dirigida por um fBm e gera naturalmente o *skew* íngreme observado. Sob a medida física $\mathbb{P}$:

$$\frac{dS_t}{S_t} = \sqrt{v_t}\, dW_t, \qquad \frac{v_t}{v_0} = e^{\,2\sigma_v B^H_t},$$

com $B^H$ um fBm de Hurst $H \in (0, 1/2)$ correlacionado com $W$, e $\sigma_v>0$ o *vol-of-vol*. O fBm admite a representação de **Mandelbrot–van Ness**:

$$B^H_t = \frac{1}{c_H}\left[\int_0^t (t-s)^{H-\frac12}\,dB_s + \int_{-\infty}^0\Big((t-s)^{H-\frac12}-(-s)^{H-\frac12}\Big)\,dB_s\right],$$

onde $c_H = \big(\Gamma(2H+1)\sin(\pi H)\big)^{-1/2}\Gamma(H+\tfrac12)$ é uma constante de normalização.

**Por que log-normal (Bergomi) e não Heston?** Modelos rough log-normais capturam melhor a dinâmica empírica do *smile* — em particular a assintótica do *at-the-money skew* e do *skew-stickiness ratio* — do que o rough Heston. Esse era justamente o argumento original de Bergomi (Tipo I vs. Tipo II), que se transfere *mutatis mutandis* para o cenário rough.

---

## 3. A questão central e a contribuição

A literatura anterior sobre fundações microestruturais de volatilidade rough (iniciada por **Jaisson e Rosenbaum, 2016**) baseava-se em **processos de Hawkes auto-excitantes quase instáveis**: o impacto de uma ordem se propaga *indiretamente*, gerando ordens-filhas em cascata, e o limite macroscópico produz volatilidade rough. Esses modelos levam tipicamente ao **rough Heston**.

Este artigo é o **primeiro a estabelecer um limite de escala para modelos rough log-normais** (rough Bergomi). A escolha-chave de modelagem é **abandonar os processos de Hawkes** e adotar **chegadas de Poisson** com impacto **direto** sobre a volatilidade:

- Estabelecer uma fundação para o modelo log-normal reduz-se essencialmente a estabelecer uma fundação para o **próprio fBm** — um arcabouço matemático bem mais simples.
- As chegadas de Poisson são clássicas em microestrutura de mercado desde **Garman (1976)**, que descreveu agentes como um "ensemble estatístico" gerando ordens segundo um Poisson.
- Acima de tudo, o cenário de Poisson **permite calcular taxas de erro fraco** via uma fórmula de **Clark–Ocone** para processos de Poisson, o que parece inviável para dinâmicas tipo Hawkes (devido à auto-excitação).

---

## 4. O modelo microestrutural orientado por ordens

Ordens de compra/venda chegam segundo um processo de Poisson $N$ de taxa unitária em $\mathbb{R}$, com tempos $\cdots < \tau_{-1} < \tau_0 \le 0 < \tau_1 < \tau_2 < \cdots$. A $k$-ésima ordem:

- **desloca o log-preço** por $J_k$ vezes a volatilidade;
- **desloca a log-volatilidade** por $\xi_k$.

As sequências $\{J_k\}$ e $\{\xi_k\}$ são i.i.d., **centradas** e **sem assimetria** (*no skew*), mas $J$ e $\xi$ podem ser **correlacionados** (essa correlação gera a correlação $\rho$ entre preço e volatilidade no limite — o "efeito alavancagem").

A hipótese decisiva é o **kernel de cauda pesada**, que faz o impacto decair lentamente:

$$\phi(t) = (1+t)^{\,H-\frac12}, \qquad H \in (0, 1/2], \qquad \phi(t)=0 \text{ para } t<0.$$

A dinâmica do log-preço $\widetilde P$ e da log-volatilidade $\widetilde V$ é (Eq. 1.3):

$$\widetilde P_t = \sum_{k=1}^{N_t} J_k\, e^{\widetilde V_{\tau_k^-}}, \qquad
\widetilde V_t = \sum_{k=1}^{N_t} \xi_k\,\phi(t-\tau_k) + \sum_{k=-\infty}^{0}\xi_k\big(\phi(t-\tau_k)-\phi(-\tau_k)\big).$$

Em palavras: a volatilidade total é uma **média ponderada de impactos passados** (contraste com a literatura anterior, em que a volatilidade *desencadeava* novo fluxo de ordens).

### Decomposição aditiva — a ideia central

Como $V_t = V_0\, e^{\log(V_t/V_0)}$, a log-volatilidade se decompõe em dois processos independentes de tratar:

$$\widetilde V^0_t = \sum_{k=-\infty}^{0}\xi_k\big(\phi(t-\tau_k)-\phi(-\tau_k)\big) \quad\text{(impacto de ordens anteriores a 0)},$$
$$\widetilde V^1_t = \sum_{k=1}^{N_t}\xi_k\,\phi(t-\tau_k) \quad\text{(impacto de ordens posteriores a 0)}.$$

Após reescalonamento, a soma $\widetilde V^0+\widetilde V^1$ converge precisamente para o fBm na forma de Mandelbrot–van Ness (os dois termos correspondem às duas integrais da representação).

---

## 5. Reescalonamento e o resultado de convergência fraca

Define-se a família reescalonada (Definition 2.3), com kernels $\phi_n$ que coincidem assintoticamente com $\phi$:

$$\widetilde P^{(n)}_t = \int_0^t\!\!\int_{\mathbb{R}^2} e^{\widetilde V^{(n)}_{s^-}}\frac{u}{\sqrt n}\,N(n\cdot ds, du, dv),$$
$$\widetilde V^{(n)}_t = \int_0^t\!\!\int_{\mathbb{R}^2}\phi_n(t-s)\frac{v}{\sqrt n}\,N(n\cdot ds, du, dv) + \int_{-\infty}^0\!\!\int_{\mathbb{R}^2}\big(\phi_n(t-s)-\phi_n(-s)\big)\frac{v}{\sqrt n}\,N(n\cdot ds, du, dv).$$

O **kernel de referência** é $\phi_n(t)=(n^{-1}+t)^{\,H-1/2}$, cujo limite pontual é $\phi_\infty(t)=t^{\,H-1/2}$.

### Hipóteses (Assumption 2.1 e 2.5)

Sobre a medida de intensidade $\mathbb{P}(du,dv)$ dos saltos: **centrada**, **segundos momentos conhecidos** ($\sigma_p^2$ para o preço, $\sigma_v^2$ para a vol), **sem skew** e **sem skew misto**, **caudas (sub-)gaussianas** e **estrutura de correlação** $\sigma_p\sigma_v\rho = \int uv\,\mathbb{P}(du,dv)$. Uma gaussiana bivariada centrada satisfaz todas. Sobre os kernels $\phi_n$: positividade e majorante por $(1/n+t)^{H-1/2}$, monotonicidade com derivada controlada, continuidade uniforme e convergência em $L^2$ para $\phi_\infty$.

### Teorema 2.7 (convergência fraca)

O processo reescalonado $(\widetilde P^{(n)}, \widetilde V^{(n)})$ **converge fracamente**, no espaço de Skorokhod $D([0,T];\mathbb{R}^2)$, para o modelo rough Bergomi:

$$\widetilde P^*_t = \int_0^t \sigma_p\, e^{\widetilde V^*_s}\,dW_s, \qquad \widetilde V^*_t = \sigma_v\, c_H\, B^H_t,$$

com $W$ browniano padrão, $B^H$ um fBm de Hurst $H$ e correlação $\rho$ entre $W$ e $B$. Ou seja, **o microestrutural de Poisson tem como limite macroscópico exatamente o rough Bergomi**.

---

## 6. Estratégia da prova de convergência (Seção 3)

O desafio técnico não é o preço (que segue por argumentos padrão de martingais e o teorema de continuidade, uma vez conhecida a convergência da volatilidade), mas a **C-tightness** (*tightness* com pontos de acumulação contínuos) da sequência de volatilidades reescalonadas. O obstáculo conhecido desde Jaisson–Rosenbaum: os incrementos da volatilidade **não satisfazem a condição de momento usual** para garantir C-tightness.

A prova procede em blocos:

- **A-priori estimates (Seção 3.1):** uma desigualdade tipo BDG para integrais em relação a medidas aleatórias de Poisson compensadas (Lemma 3.1) e a **integrabilidade exponencial** da log-volatilidade mais a integrabilidade polinomial do log-preço (Lemma 3.2).
- **C-tightness de $\widetilde V^{(n),0}$ (Seção 3.2):** longe do instante inicial usa-se o critério de Kolmogorov–Chentsov; **no instante inicial**, prova-se convergência uniforme em probabilidade a zero em $[0,\epsilon]$ para $\epsilon$ pequeno (Proposições 3.4 e 3.5).
- **C-tightness de $\widetilde V^{(n),1}$ (Seção 3.3):** aplica-se o critério recém-estabelecido por **Horst, Xu e Zhang (2023)** para processos càdlàg (Lemma 3.6), verificando as condições via Lemmas 3.8 e 3.9.
- **Distribuições de dimensão finita (Seção 3.4):** Lemma 3.10 mostra, via funções características, que as f.d.d. convergem às do fBm; juntando com a C-tightness conclui-se o Teorema 2.7 (Seção 3.5).

---

## 7. Taxas de erro fraco (a contribuição quantitativa)

Tendo o limite, o interesse passa a **avaliar payoffs** $\Phi$ no pré-limite e no limite, controlando o **erro fraco**:

$$\big|\,\mathbb{E}[\Phi(\widetilde P^{(n)})] - \mathbb{E}[\Phi(\widetilde P^*)]\,\big|.$$

Se esse erro decai rapidamente, o **próprio modelo microestrutural torna-se um esquema de simulação alternativo** aos clássicos (Euler, Milstein), com a vantagem extra de manter uma **interpretação econômica clara**.

### Por que isso é difícil e relevante

- O fBm é apenas $H$-Hölder contínuo, então aproximações de ponto-esquerdo/médio atingem, no melhor caso, **erro forte de ordem $H$** (Euler–Maruyama) ou $2H$ (Milstein).
- Em geral o **erro fraco decai ao dobro da taxa do erro forte**. Bayer, Hall e Tempone (2022) obtêm $H+1/2$ via aproximações markovianas; Gassiat (2023) e Friz–Salkeld–Wagenhofer (2025) obtêm **$3H+1/2$** explorando a fórmula de **Clark–Ocone** (representação martingal da volatilidade) para deduzir uma **fórmula de momentos** do log-preço. Bonesini, Jacquier e Pannier (2026) também chegam a $3H+1/2$.
- O ganho prático é enorme. Para $H\approx 0{,}1$: **dobrar a precisão forte** exige $2^{1/H}=2^{10}\approx 1000\times$ mais passos; já **dobrar a precisão fraca** exige apenas $2^{1/(3H+1/2)}\approx 2{,}4\times$.

### Teorema 2.8 (taxa de erro fraco do modelo)

Existe uma família de kernels $\{\widehat\phi_n\}$ tal que, para todo $N\in\mathbb{N}$ e $t\in[0,T]$,

$$\big|\,\mathbb{E}\big[(\widetilde P^{(n)}_t)^N\big] - \mathbb{E}\big[(\widetilde P^*_t)^N\big]\,\big| \;\le\; C\cdot
\begin{cases}
n^{-\frac13-\frac{4H}{3-6H}} & H\in(0,1/4),\\[4pt]
n^{-1}\log(n) & H=1/4,\\[4pt]
n^{-1} & H\in(1/4,1/2).
\end{cases}$$

**Observações importantes:**
- A taxa **depende da escolha específica dos kernels**. O kernel ingênuo $\phi_n(t)=(n^{-\alpha}+t)^{H-1/2}$ satisfaz as hipóteses mas dá apenas $n^{-2H\alpha}$ — bem mais lento (Remark 2.9). O kernel ótimo "adiciona massa" perto de zero de forma controlada.
- As taxas dependem **fortemente** da dinâmica de Poisson; os autores não sabem como estendê-las a chegadas tipo Hawkes (e, portanto, ao rough Heston).
- Sob a hipótese de **simetria (no-skew)**, o cenário markoviano clássico dá erro fraco de ordem $1$ (Döbler–Peccati, 2018), mas esses resultados não cobrem os **kernels de convolução** que geram a estrutura não-markoviana aqui. Métodos de Stein, por exemplo, requerem um gerador que não está disponível nem para o limite nem para o pré-limite.

---

## 8. As ferramentas da prova das taxas (Seção 4)

A prova usa um **argumento triangular**, comparando os momentos de três objetos: o pré-limite $\widetilde P^{(n)}$, um **rough Bergomi aproximado** $\widetilde P^{*,(n)}$ (com fBm de kernel $\phi_n$, "no meio"), e o limite $\widetilde P^*$.

1. **Fórmula de Clark–Ocone para Poisson (Seção 4.1):** baseada em Zhang (2009). Define-se o operador-diferença $D_{(u,t)}F = F\circ\varepsilon^+_{(u,t)} - F$ (que adiciona um salto em $(u,t)$ — o análogo de Poisson da derivada de Malliavin), levando à representação $F = \mathbb{E}[F] + \int \mathbb{E}[D_{(u,t)}F\,|\,\mathcal F_{t^-}]\,\tilde\mu(du,dt)$ (Lemma 4.3, Corollary 4.4).

2. **Fórmula de momentos (Seções 4.2 e Apêndice A.1):** combinando uma recursão de momentos do log-preço (Lemma 4.5) com as técnicas de Friz–Salkeld–Wagenhofer, obtém-se (Theorem 4.6) uma representação dos momentos $\mathbb{E}[(\widetilde P_T)^N]$ como somas, sobre "palavras" $w$ num alfabeto $\{I,J\}$, de integrais sobre simplexos de produtos de kernels — válida para os três modelos.

3. **Comparação termo a termo (Seção 4.2.2):** chega-se ao bound (Eq. 2.8/4.6)

$$\big|\,\mathbb{E}[(\widetilde P^{(n)}_t)^N]-\mathbb{E}[(\widetilde P^*_t)^N]\,\big| \;\lesssim\; \star(n)+\diamond(n)+\square(n)+\triangle(n),$$

onde, intuitivamente:
- $\star(n)$ controla o **4º momento integrado** dos kernels (o "blow-up" na origem),
- $\diamond(n)$ e $\square(n)$ controlam as **diferenças das covariâncias**,
- $\triangle(n) = \lVert \phi_n - \phi_\infty\rVert_{L^1}$ controla a **distância $L^1$** ao kernel de Volterra.

Como subproduto, obtém-se uma **fórmula de momentos (aproximada) para o próprio modelo microestrutural**, potencialmente útil para inferência estatística a partir de dados de *limit order book*.

---

## 9. O kernel ótimo e a otimalidade da taxa (Seção 4.3)

A família que minimiza a soma dos quatro funcionais (Eq. 4.19) é

$$\widehat\phi_n(t) = \sqrt{\phi_\infty^2(t+n^{-\beta}) + c_1\big(\phi_\infty^2(t+n^{-\beta})-\phi_\infty^2(2n^{-\beta})\big)_+},$$

com $\phi_\infty(t)=t^{H-1/2}$, a constante $c_1 = (2^{2H}-1-2^{2H}H)^{-1}$ (positiva para $H\le 1$, Eq. 4.20) e o expoente ótimo $\beta = \tfrac{2}{3-6H}$. As intuições de projeto:
- o **deslocamento** $n^{-\beta}$ regulariza a singularidade na origem (controla $\star$, a norma $L^4$);
- o **termo $c_1$** adiciona massa perto de zero para aproximar as covariâncias (controla $\square$) sem estragar a norma $L^4$;
- fora de uma vizinhança de zero, $\widehat\phi_n$ coincide com $\phi_\infty$, mantendo $\triangle$ pequeno.

O Lemma 4.13 verifica que $\widehat\phi_n$ satisfaz as hipóteses; o Theorem 4.14 calcula $\star(n)\lesssim n^{-1+\beta-4H\beta}$ e $\diamond+\square+\triangle\lesssim n^{-\beta(H+1/2)}$, e a escolha $\beta=\tfrac{2}{3-6H}$ equilibra ambos, recuperando a taxa do Theorem 2.8. Por fim, o **Lemma 4.15 prova a otimalidade**: para *qualquer* sequência de kernels admissíveis, $\star(n)+\diamond(n)\gtrsim n^{-\frac13-\frac{4H}{3-6H}}$ — logo a taxa não pode ser melhorada pela escolha dos kernels (embora o bound intermediário 4.6 talvez não seja perfeitamente justo).

---

## 10. Simulações numéricas (Seção 2.3)

- **Figuras 1–2:** trajetórias típicas de log-preço e log-vol negativamente correlacionados ($H=0{,}15$, $\rho=-0{,}7$), para saltos gaussianos ($n=10$) e Bernoulli ($n=20$), com kernel $\phi_n(t)=(1/n+t)^{H-1/2}$ (volatilidade-limite = fBm de **Riemann–Liouville**, pois assume-se impacto nulo antes de 0).
- **Figura 3:** vizinhanças de Skorokhod ilustrando que, para intensidade grande, a trajetória se aproxima visualmente de uma função contínua.
- **Figura 4:** valida o **erro fraco do 4º momento** via o polinômio de Hermite $H_4(x)=x^4-6x^2+3$, comparando o estimador de Monte Carlo (esquema de Poisson, $M=2\times 10^7$ amostras) com um valor de referência do esquema de Euler (5000 passos, $3{,}2\times10^7$ amostras). Para $H=0{,}15$ e $H=0{,}30$, o erro simulado permanece dentro das bandas de confiança da taxa teórica, **sugerindo que a taxa provada é, de fato, exata (sharp)**.

---

## 11. Significância, limitações e perspectivas

**Significância.** É o primeiro limite de escala microestrutural para modelos **rough log-normais**, conectando uma narrativa econômica de fluxo de ordens ao rough Bergomi. Ao trocar Hawkes por Poisson, ganha-se tratabilidade analítica e, sobretudo, **taxas de erro fraco** — algo novo na literatura rough microestrutural. O modelo microestrutural pode, então, servir como **esquema de simulação** com interpretação econômica.

**Limitações.** As taxas dependem essencialmente da estrutura de Poisson e de hipóteses de simetria (no-skew); os autores **não** sabem estendê-las a Hawkes / rough Heston. Nem o limite nem o pré-limite são semimartingales, o que impede métodos clássicos (Stein, Talay–Tubaro) e exige o aparato de Clark–Ocone. O impacto antes do tempo zero é geralmente desprezado nas simulações (uso da fBm de Riemann–Liouville).

**Perspectivas.** A fórmula de momentos aproximada para o modelo microestrutural pode alimentar **inferência estatística a partir de dados de order book**; estender as taxas a fluxos de ordens auto-excitantes permanece em aberto.

---

## 12. Mini-glossário de notação

| Símbolo | Significado |
|---|---|
| $H$ | parâmetro de Hurst, $H\in(0,1/2]$; quanto menor, mais "rough" |
| $\phi(t),\,\phi_n(t),\,\phi_\infty(t)$ | kernels de impacto; $\phi_\infty(t)=t^{H-1/2}$ (Volterra/Riemann–Liouville) |
| $J_k,\,\xi_k$ | saltos i.i.d. de preço e de log-vol da $k$-ésima ordem |
| $\sigma_p,\,\sigma_v$ | desvios-padrão de $J$ e $\xi$ |
| $\rho$ | correlação preço–vol (efeito alavancagem) |
| $\widetilde P^{(n)},\widetilde V^{(n)}$ | log-preço e log-vol reescalonados (pré-limite) |
| $\widetilde P^*,\widetilde V^*$ | modelo-limite (rough Bergomi) |
| $\star,\diamond,\square,\triangle$ | funcionais que controlam o erro fraco |

---

## 13. Sobre o código Python que acompanha este resumo

1. **Kernels** de referência $\phi_n(t)=(1/n+t)^{H-1/2}$ e **otimizado** $\widehat\phi_n$ (Eq. 4.19–4.20).
2. **`simulate_micro_path`** — uma trajetória do modelo microestrutural reescalonado (log-vol e log-preço), com saltos gaussianos ou Bernoulli, reproduzindo qualitativamente as Figuras 1–2.
3. **`simulate_micro_terminal`** — o valor terminal $\widetilde P^{(n)}_T$ (vetorizado por trajetória) para o experimento de erro fraco.
4. **`simulate_limit_terminal`** — esquema de Euler para o modelo-limite (fBm de Riemann–Liouville), eficiente em memória.
5. **`weak_error_experiment`** + **`plot_weak_error`** — estimativa do erro fraco do 4º momento via $H_4$, comparada com a taxa teórica $1/3+4H/(3-6H)$ (versão *leve* de demonstração; o artigo usa $M\sim 10^7$ amostras).

> **Nota técnica.** A simulação do log-vol é intrinsecamente $O(K^2)$ por trajetória (com $K\sim n$ chegadas), pois o kernel **não é exponencial** — não há recursão markoviana. Isso é a própria assinatura da volatilidade rough. Por isso a demonstração usa $n$ e $M$ modestos; os gráficos resultantes são qualitativamente corretos, ainda que ruidosos. A escala vertical das trajetórias segue diretamente a definição reescalonada do artigo (com $\mathrm{Var}(\widetilde V^{(n)}_t)\approx \sigma_v^2\int_0^t\phi_n^2$), podendo diferir da escala mostrada nas figuras do paper conforme os parâmetros usados.

```python
r"""
Fundação microestrutural de modelos de volatilidade rough log-normal (rough Bergomi)
====================================================================================

Implementação ilustrativa do modelo de Hager, Horst, Wagenhofer & Xu (2026),
"Microstructural Foundation of Rough Log-Normal Volatility Models", arXiv:2603.13170.

A ideia central:
  * Ordens de compra/venda chegam segundo um processo de Poisson de taxa n em [0, T].
  * A k-ésima ordem desloca o log-preço por J_k * volatilidade e o log-vol por xi_k.
  * O impacto de cada ordem sobre a volatilidade futura decai LENTAMENTE segundo um
    kernel de cauda pesada phi_n(t) ~ (1/n + t)^{H-1/2}, com H em (0, 1/2].
  * Após reescalonamento (preco/sqrt(n), vol/n^H), o par (log-preco, log-vol)
    converge fracamente para o modelo rough Bergomi:
        V*_t  = sigma_v * (RL-fBm)_t,
        P*_t  = sigma_p * \int_0^t e^{V*_s} dW_s,
    onde RL-fBm é o movimento browniano fracionário de Riemann-Liouville
    (assumindo, como no paper, impacto nulo antes do tempo zero).
"""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib

matplotlib.use("Agg")  # backend sem display, para salvar PNGs
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import Generator, default_rng


# ---------------------------------------------------------------------------
# 1. Kernels
# ---------------------------------------------------------------------------
def phi_benchmark(t: np.ndarray, n: int, H: float) -> np.ndarray:
    """Kernel de referência phi_n(t) = (1/n + t)^{H-1/2} para t >= 0, e 0 caso contrário.

    Este é o kernel "benchmark" da Eq. (2.7). O seu limite pontual é
    phi_inf(t) = t^{H-1/2}, o kernel de Riemann-Liouville.
    """
    t = np.asarray(t, dtype=float)
    out = np.zeros_like(t)
    pos = t >= 0.0
    out[pos] = (1.0 / n + t[pos]) ** (H - 0.5)
    return out


def phi_optimized(t: np.ndarray, n: int, H: float, beta: float | None = None) -> np.ndarray:
    """Família de kernels OTIMIZADOS da Eq. (4.19), que atinge a taxa de erro fraco
    1/3 + 4H/(3 - 6H).

        phi_hat_n(t) = sqrt( phi_inf^2(t + n^{-beta})
                             + c1 * ( phi_inf^2(t + n^{-beta}) - phi_inf^2(2 n^{-beta}) )_+ )

    com phi_inf(x) = x^{H-1/2}, c1 dado pela Eq. (4.20) e beta = 2/(3 - 6H).
    """
    if beta is None:
        beta = 2.0 / (3.0 - 6.0 * H)
    t = np.asarray(t, dtype=float)
    nb = float(n) ** (-beta)
    c1 = 1.0 / (2.0 ** (2 * H) - 1.0 - 2.0 ** (2 * H) * H)

    def phi2(x: np.ndarray) -> np.ndarray:
        return x ** (2 * H - 1.0)

    tt = np.maximum(t, 0.0)
    base = phi2(tt + nb)
    extra = c1 * np.maximum(base - phi2(2.0 * nb), 0.0)
    inner = np.where(t >= 0.0, base + extra, 0.0)
    return np.sqrt(np.maximum(inner, 0.0))


# ---------------------------------------------------------------------------
# 2. Parâmetros do modelo
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ModelParams:
    H: float = 0.15          # parâmetro de Hurst em (0, 1/2]
    rho: float = -0.7        # correlação entre saltos de preço (J) e de vol (xi)
    sigma_J: float = 1.0     # desvio-padrão dos saltos de preço  (sigma_p)
    sigma_xi: float = 0.5    # desvio-padrão dos saltos de vol     (sigma_v)
    T: float = 1.0           # horizonte temporal


def _draw_correlated_jumps(
    K: int, p: ModelParams, rng: Generator, jump_kind: str = "gaussian"
) -> tuple[np.ndarray, np.ndarray]:
    """Sorteia K pares (J_k, xi_k) i.i.d., centrados, sem skew e com correlação rho.

    jump_kind:
      - "gaussian": ambos gaussianos correlacionados.
      - "bernoulli": xi_k = +-sigma_xi (Rademacher), J_k gaussiano correlacionado.
    """
    z = rng.standard_normal((K, 2))
    j_std = z[:, 0]
    xi_std = p.rho * z[:, 0] + np.sqrt(max(0.0, 1.0 - p.rho ** 2)) * z[:, 1]
    J = p.sigma_J * j_std
    if jump_kind == "gaussian":
        xi = p.sigma_xi * xi_std
    elif jump_kind == "bernoulli":
        # aplica o sinal ao salto gaussiano -> +-1, escalado por sigma_xi
        xi = p.sigma_xi * np.sign(xi_std)
        xi[xi == 0.0] = p.sigma_xi
    else:
        raise ValueError(f"jump_kind desconhecido: {jump_kind!r}")
    return J, xi


# ---------------------------------------------------------------------------
# 3. Simulação de uma trajetória (log-vol e log-preço) numa grade temporal
# ---------------------------------------------------------------------------
def simulate_micro_path(
    n: int,
    p: ModelParams,
    rng: Generator,
    grid_size: int = 500,
    kernel: str = "benchmark",
    jump_kind: str = "gaussian",
) -> dict[str, np.ndarray]:
    """Simula uma trajetória do modelo microestrutural reescalonado.

    Sem impacto antes do tempo zero (V^0 = 0), como nas simulações do paper.
    Devolve a grade temporal e as trajetórias de log-vol e log-preço (càdlàg).
    """
    phi = phi_benchmark if kernel == "benchmark" else phi_optimized

    # Chegadas de Poisson de taxa n em [0, T]: numero ~ Poisson(n*T)
    K = int(rng.poisson(n * p.T))
    if K == 0:
        t = np.linspace(0.0, p.T, grid_size)
        return {"t": t, "log_vol": np.zeros_like(t), "log_price": np.zeros_like(t)}
    taus = np.sort(rng.uniform(0.0, p.T, size=K))
    J, xi = _draw_correlated_jumps(K, p, rng, jump_kind)

    # log-vol logo ANTES de cada chegada: V_{tau_k-} = (1/sqrt(n)) sum_{j<k} xi_j phi_n(tau_k - tau_j)
    D = taus[:, None] - taus[None, :]              # D[k, j] = tau_k - tau_j
    M = np.tril(phi(D, n, p.H), k=-1)              # apenas j < k (triângulo inferior estrito)
    V_pre = (M @ xi) / np.sqrt(n)                  # V_{tau_k-}

    # Incrementos de log-preço: dP_k = J_k * exp(V_{tau_k-}) / sqrt(n)
    dP = J * np.exp(V_pre) / np.sqrt(n)

    # Avaliação numa grade: somas càdlàg sobre as chegadas <= t
    t = np.linspace(0.0, p.T, grid_size)
    idx = np.searchsorted(taus, t, side="right")   # numero de chegadas <= t

    # log-preço acumulado nos instantes de chegada
    cumP = np.concatenate([[0.0], np.cumsum(dP)])
    log_price = cumP[idx]

    # log-vol numa grade: V_t = (1/sqrt(n)) sum_{tau_k <= t} xi_k phi_n(t - tau_k)
    # (avaliacao vetorizada t x K; grade pequena, custo aceitavel)
    Dtg = t[:, None] - taus[None, :]               # (grid, K)
    Phitg = phi(Dtg, n, p.H)                        # phi=0 para argumento negativo
    log_vol = (Phitg @ xi) / np.sqrt(n)

    return {"t": t, "log_vol": log_vol, "log_price": log_price}


# ---------------------------------------------------------------------------
# 4. Valor terminal do log-preço (para o experimento de erro fraco)
# ---------------------------------------------------------------------------
def simulate_micro_terminal(
    n: int,
    p: ModelParams,
    n_paths: int,
    rng: Generator,
    kernel: str = "optimized",
    jump_kind: str = "gaussian",
) -> np.ndarray:
    """Amostra n_paths valores terminais P~^{(n)}_T do modelo microestrutural."""
    phi = phi_benchmark if kernel == "benchmark" else phi_optimized
    out = np.empty(n_paths)
    sqn = np.sqrt(n)
    for m in range(n_paths):
        K = int(rng.poisson(n * p.T))
        if K == 0:
            out[m] = 0.0
            continue
        taus = np.sort(rng.uniform(0.0, p.T, size=K))
        J, xi = _draw_correlated_jumps(K, p, rng, jump_kind)
        D = taus[:, None] - taus[None, :]
        M = np.tril(phi(D, n, p.H), k=-1)
        V_pre = (M @ xi) / sqn
        out[m] = np.sum(J * np.exp(V_pre)) / sqn
    return out


# ---------------------------------------------------------------------------
# 5. Esquema de Euler para o modelo-limite (rough Bergomi com RL-fBm)
# ---------------------------------------------------------------------------
def simulate_limit_terminal(
    p: ModelParams,
    n_paths: int,
    rng: Generator,
    n_steps: int = 200,
    batch: int = 20_000,
) -> np.ndarray:
    r"""Esquema de Euler (left-point) para o valor terminal P*_T do modelo-limite:

        V*_t = sigma_v * \int_0^t (t - s)^{H-1/2} dB_s   (RL-fBm),
        P*_t = sigma_p * \int_0^t e^{V*_s} dW_s,    corr(dW, dB) = rho.

    A convolução RL é montada como uma matriz triangular pequena (n_steps x n_steps)
    e os caminhos são gerados em lotes para limitar o uso de memória.
    """
    dt = p.T / n_steps
    t = np.linspace(0.0, p.T, n_steps + 1)

    # matriz de convolução A[i, j] = (t_i - t_j)^{H-1/2} para j < i, i,j em 0..m-1
    ti = t[:n_steps][:, None]
    tj = t[:n_steps][None, :]
    lag = np.where(ti > tj, ti - tj, 1.0)
    A = np.where(ti > tj, lag ** (p.H - 0.5), 0.0)

    out = np.empty(n_paths)
    done = 0
    while done < n_paths:
        b = min(batch, n_paths - done)
        z1 = rng.standard_normal((b, n_steps))
        z2 = rng.standard_normal((b, n_steps))
        dB = np.sqrt(dt) * z1
        dW = np.sqrt(dt) * (p.rho * z1 + np.sqrt(max(0.0, 1.0 - p.rho ** 2)) * z2)

        # V*_{t_i} = sigma_v * (dB @ A.T)[:, i]   (V*_{t_0} = 0)
        V = p.sigma_xi * (dB @ A.T)                 # (b, n_steps)
        out[done : done + b] = p.sigma_J * np.sum(np.exp(V) * dW, axis=1)
        done += b
    return out


# ---------------------------------------------------------------------------
# 6. Polinómio de Hermite de grau 4 e experimento de erro fraco
# ---------------------------------------------------------------------------
def hermite4(x: np.ndarray) -> np.ndarray:
    """H_4(x) = x^4 - 6 x^2 + 3 (Hermite probabilista)."""
    return x ** 4 - 6.0 * x ** 2 + 3.0


def theoretical_rate(H: float) -> float:
    """Expoente da taxa de erro fraco do Teorema 2.8.

        H < 1/4  -> 1/3 + 4H/(3 - 6H)
        H = 1/4  -> 1 (com correção logarítmica)
        H > 1/4  -> 1
    """
    if H < 0.25:
        return 1.0 / 3.0 + 4.0 * H / (3.0 - 6.0 * H)
    return 1.0


def weak_error_experiment(
    p: ModelParams,
    ns: list[int],
    n_paths_micro: int,
    n_paths_limit: int,
    rng: Generator,
    kernel: str = "optimized",
) -> dict[str, np.ndarray]:
    """Estima |E[H_4(P~^{(n)}_T)] - E[H_4(P*_T)]| para vários n e compara com a taxa."""
    ref = np.mean(hermite4(simulate_limit_terminal(p, n_paths_limit, rng, n_steps=300)))
    errors = np.empty(len(ns))
    for k, n in enumerate(ns):
        samples = simulate_micro_terminal(n, p, n_paths_micro, rng, kernel=kernel)
        errors[k] = abs(np.mean(hermite4(samples)) - ref)
    return {"ns": np.asarray(ns, dtype=float), "errors": errors, "ref": ref}


# ---------------------------------------------------------------------------
# 7. Figuras
# ---------------------------------------------------------------------------
def plot_sample_paths(seed: int = 7) -> None:
    rng = default_rng(seed)
    p = ModelParams(H=0.15, rho=-0.7, sigma_J=1.0, sigma_xi=0.5)

    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    for col, (n, kind, label) in enumerate(
        [(10, "gaussian", "Gauss, n=10"), (20, "bernoulli", "Bernoulli, n=20")]
    ):
        path = simulate_micro_path(n, p, rng, kernel="benchmark", jump_kind=kind)
        axes[0, col].plot(path["t"], path["log_price"], lw=1.0, color="C0")
        axes[0, col].set_title(f"Log-Preço ({label})")
        axes[1, col].plot(path["t"], path["log_vol"], lw=1.0, color="C3")
        axes[1, col].set_title(f"Log-Vol ({label})")
        for r in (0, 1):
            axes[r, col].set_xlabel("t")
            axes[r, col].grid(alpha=0.3)
    fig.suptitle("Trajetórias do modelo microestrutural (kernel φₙ(t)=(1/n+t)^{H-1/2})")
    fig.tight_layout()
    fig.savefig("fig_sample_paths.png", dpi=130)
    plt.close(fig)


def plot_convergence_logvol(seed: int = 11) -> None:
    """Ilustra que, ao aumentar n, a log-vol microestrutural fica cada vez mais
    próxima de uma trajetória contínua e 'rugosa' (RL-fBm)."""
    p = ModelParams(H=0.15, rho=-0.7, sigma_xi=0.5)
    fig, ax = plt.subplots(figsize=(9, 5))
    for n in (10, 50, 200, 1000):
        rng = default_rng(seed)  # mesma semente -> mesma 'aleatoriedade base'
        path = simulate_micro_path(n, p, rng, grid_size=600, kernel="benchmark")
        ax.plot(path["t"], path["log_vol"], lw=1.0, label=f"n = {n}")
    ax.set_title("Convergência da log-volatilidade reescalonada (H = 0.15)")
    ax.set_xlabel("t")
    ax.set_ylabel("log-vol")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig("fig_convergence_logvol.png", dpi=130)
    plt.close(fig)


def plot_weak_error(seed: int = 3) -> None:
    rng = default_rng(seed)
    ns = [4, 8, 16, 32, 64, 128]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, H in zip(axes, (0.15, 0.30)):
        p = ModelParams(H=H, rho=-1.0, sigma_J=1.0, sigma_xi=0.05)
        res = weak_error_experiment(
            p, ns, n_paths_micro=3000, n_paths_limit=120_000, rng=rng, kernel="optimized"
        )
        exp = theoretical_rate(H)
        ns_arr, err = res["ns"], res["errors"]
        # constante ajustada para alinhar a reta teórica à nuvem de pontos
        const = np.exp(np.mean(np.log(err) + exp * np.log(ns_arr)))
        ax.loglog(ns_arr, err, "o-", color="C0", label="Erro de Monte Carlo (Poisson)")
        ax.loglog(ns_arr, const * ns_arr ** (-exp), "k--",
                  label=f"Taxa teórica n^(-{exp:.3f})")
        ax.set_title(f"Erro fraco do 4º momento (H = {H})")
        ax.set_xlabel("n")
        ax.set_ylabel("erro absoluto")
        ax.grid(alpha=0.3, which="both")
        ax.legend()
    fig.suptitle("Taxa de erro fraco: 1/3 + 4H/(3−6H)  (demonstração leve)")
    fig.tight_layout()
    fig.savefig("fig_weak_error.png", dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 8. Execução principal
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("1) Trajetórias de amostra (Gauss e Bernoulli)...")
    plot_sample_paths()

    print("2) Convergência da log-volatilidade ao crescer n...")
    plot_convergence_logvol()

    print("3) Experimento (leve) de erro fraco do 4º momento...")
    plot_weak_error()

    print("Pronto. Figuras salvas: fig_sample_paths.png, "
          "fig_convergence_logvol.png, fig_weak_error.png")
    print(f"   Expoente teórico H=0.15 -> {theoretical_rate(0.15):.4f}")
    print(f"   Expoente teórico H=0.30 -> {theoretical_rate(0.30):.4f}")
```