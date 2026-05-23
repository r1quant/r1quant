
An Explicit Solution to Black–Scholes Implied Volatility

Por Wolfgang Schadner, April 28, 2026.

**Contexto e problema.** A fórmula de Black–Scholes é explícita no sentido volatilidade → preço, mas o mercado precisa quase sempre do caminho inverso: dado um preço observado de opção, qual a volatilidade implícita que o reproduz. Desde Black & Scholes (1973), a volatilidade implícita virou a convenção-padrão para cotar e comparar opções entre strikes, vencimentos, ativos e datas — ela aparece em precificação de derivativos, asset pricing empírico, previsão de volatilidade, gestão de risco, modelagem da superfície de volatilidade, estudos de retorno de opções e testes de prêmio de risco. Apesar disso, o inverso de Black–Scholes sempre foi tratado como um *problema de inversão numérica* (uma busca de raiz). A literatura produziu aproximações e expansões assintóticas (Li, 2008), limites analíticos superiores/inferiores (Tehranchi, 2016), algoritmos iterativos altíssima-eficiência — com o *Let's be rational* de Jäckel (2015, 2024) como referência de ponta — e representações exatas porém *implícitas* via séries infinitas (Cui et al., 2021). Gerhold (2012) chegou a mostrar que a volatilidade implícita não é *D-finita*, o que descarta uma classe ampla de formas fechadas usuais. Em todos esses casos, a vol implícita continuava sendo "o valor que um solver devolve". O autor afirma apresentar a primeira solução explícita em forma fechada.

**O resultado central.** Para uma call de preço $C$, strike $K$, forward $F$, fator de desconto $D$ e maturidade $T$, com preço normalizado $c = C/(DF)$ e log-moneyness forward $k = \log(K/F)$:

$$\sigma(K,C) = \frac{2}{\sqrt{T}}\left[\mathcal{F}^{-1}_{IG}\!\left(\tfrac{1-c}{m};\ \tfrac{2}{|k|},\ 1\right)\right]^{-1/2},\quad m=\begin{cases}1 & K>F\\ K/F & K<F\end{cases}$$

No nível at-the-forward ($K=F$) ela colapsa para $\sigma = \tfrac{2}{\sqrt{T}}\,\Phi^{-1}\!\big(\tfrac{c+1}{2}\big)$. A única operação não elementar é a função quantil da Gaussiana Inversa $\mathcal{F}^{-1}_{IG}$, disponível em bibliotecas numéricas/estatísticas padrão. Não há chute inicial, iteração nem aproximação.

**A derivação.** Definindo a volatilidade total $v=\sigma\sqrt{T}$, o preço normalizado de uma call é $c_{BS}(k,v)=\Phi(-k/v+v/2)-e^k\Phi(-k/v-v/2)$. A chave é notar que a *função de sobrevivência* de uma Gaussiana Inversa, avaliada em $\lambda=1$, $\mu=2/k$ e $x=4/v^2$, coincide exatamente com essa expressão para $k>0$ — ou seja, $c_{BS}(k,v)=1-\mathcal{F}_{IG}(4/v^2;\,2/k,1)$. Inverter essa identidade dá $v$ diretamente em função do quantil. O caso ITM ($k<0$) é resolvido mapeando a call para sua contraparte OTM (via $1-\tilde c=(1-c)F/K$), e a versão para puts sai da paridade put–call, com o argumento de probabilidade passando a ser $(e^k-p)/m$.

**Interpretação probabilística.** A identidade dá também uma leitura probabilística do *próprio preço* da call: para $k>0$, $c_{BS}=\mathbb{P}(Y_k>4/v^2)$ com $Y_k\sim IG(2/k,1)$. E $Y_k$ tem a distribuição do *tempo de primeira passagem* de um movimento browniano com drift $k/2$ até o nível 1. Reescrevendo em espaço de variância ($Z_k=4/Y_k$, com $Z_k$ Gaussiana Inversa Generalizada), o preço da call é $\mathbb{P}(Z_k<v^2)$ — isto é, a probabilidade de a variância implícita "ultrapassar" uma barreira de variância induzida pela moneyness. Isso difere das leituras em espaço de retorno (como o delta, ou a interpretação de Carr & Madan, 2009): aqui a afirmação probabilística vive no *espaço de variância*, e a vol implícita é simplesmente o quantil correspondente nessa escala.

**Avaliação numérica.** O autor testa numa grade determinística de $v\in\{0.01,0.05,\dots,2.00\}$ e deltas $\Delta\in\{0.05,\dots,0.95\}$, totalizando 328 casos, comparando contra o *Let's be rational* de Jäckel (2024) — um benchmark severo, já que o algoritmo atinge precisão dupla máxima em cerca de duas iterações. Ambos recuperam a vol à precisão de máquina (erro absoluto médio $2.24\times10^{-16}$ contra $2.12\times10^{-16}$ de Jäckel). Em velocidade, a fórmula explícita gasta 0,305 µs por avaliação contra 1,038 µs, ou seja, **cerca de 3,4× mais rápida**, mantendo a precisão de máquina.

**Significado e ressalvas.** A contribuição não altera o conteúdo econômico de Black–Scholes; apenas esclarece seu inverso. A vol implícita continua sendo "a volatilidade que faz o modelo bater o preço observado", mas o cálculo deixa de precisar ser descrito como busca de raiz e passa a ser um *transformação distribucional direta* do preço de mercado. Vale notar que se trata de um preprint de abril/2026 (v1, single-author), com afirmação de pioneirismo "ao melhor do meu conhecimento" — algo a confirmar via revisão por pares — e que a precisão prática depende da qualidade da rotina de quantil da IG da biblioteca usada (na minha verificação, o `scipy` reproduziu os resultados, com um aviso benigno apenas em casos muito próximos do at-the-forward para $v$ minúsculo).

## O código

Implementei a fórmula em Python 3.13 e validei: nos mesmos 328 casos, o erro médio deu **3,07×10⁻¹⁶** — mesma ordem do paper — e os round-trips de call/put recuperam a vol até a 15ª casa decimal. O arquivo traz `implied_vol_call` e `implied_vol_put` (as fórmulas das Eqs. 1, 2 e 9), funções de preço Black–Scholes para gerar exemplos, e um bloco de demonstração que reproduz o teste de recuperação da Seção 3. Um detalhe de implementação importante: a parametrização do `scipy.stats.invgauss` difere da do paper — como o paper usa $\mu=2/|k|$ e $\lambda=1$, basta passar `mu=2/|k|, scale=1.0` (documentei isso no cabeçalho).

```python
"""
Solução explícita para a volatilidade implícita de Black-Scholes.

Implementa a fórmula fechada de:

    Wolfgang Schadner, "An Explicit Solution to Black-Scholes Implied
    Volatility", arXiv:2604.24480v1 [q-fin.MF], 27 abr. 2026.

A ideia central é reconhecer o preço normalizado de uma call como a função
de sobrevivência de uma distribuição Gaussiana Inversa (IG). Invertendo essa
identidade, a volatilidade implícita total v = sigma * sqrt(T) sai diretamente
da função quantil da IG, sem chute inicial, iteração, aproximação ou série.

Fórmula (call), Eq. (1) do paper:

    sigma(K, C) = (2 / sqrt(T)) * [ F_IG^{-1}( (1 - c) / m ;  2/|k|, 1 ) ]^{-1/2}

onde
    c = C / (D * F)        preço normalizado da call
    k = log(K / F)         log-moneyness forward
    m = 1        se K > F  (call OTM)
    m = K / F    se K < F  (call ITM)

No nível at-the-forward (K = F) ela colapsa para a Eq. (2):

    sigma(K=F, C) = (2 / sqrt(T)) * Phi^{-1}( (c + 1) / 2 )

Requer Python >= 3.13 e SciPy.

NOTA SOBRE A PARAMETRIZAÇÃO DA IG
---------------------------------
O paper usa IG(mean = mu, shape = lambda). Aqui mu = 2/|k| e lambda = 1.
O `scipy.stats.invgauss` usa (mu_scipy, scale) tal que a relação com a IG de
média `mean` e forma `shape` é:  mu_scipy = mean / shape,  scale = shape.
Como shape = 1, temos mu_scipy = 2/|k| e scale = 1.0.
"""

from __future__ import annotations

import math
import warnings
from dataclasses import dataclass

from scipy.stats import invgauss, norm

# Abaixo deste |k| tratamos como at-the-forward e usamos a Eq. (2).
_ATM_TOL: float = 1e-12

type Number = float | int


def _ig_quantile(q: float, abs_k: float) -> float:
    """Quantil F_IG^{-1}(q ; mu = 2/|k|, lambda = 1) na parametrização do paper."""
    return float(invgauss.ppf(q, mu=2.0 / abs_k, scale=1.0))


def implied_vol_call(
    price: Number, strike: Number, forward: Number,
    maturity: Number, discount: Number = 1.0,
) -> float:
    """
    Volatilidade implícita anualizada de uma CALL europeia.

    Parâmetros
    ----------
    price     : preço observado da call (C)
    strike    : strike (K)
    forward   : preço forward do ativo (F)
    maturity  : tempo até o vencimento em anos (T)
    discount  : fator de desconto (D), default 1.0. Relação com o spot:
                S = D * F * exp(delta * T), com dividend yield contínuo delta.

    Retorna
    -------
    sigma : volatilidade implícita anualizada.
    """
    c = price / (discount * forward)            # preço normalizado, Eq. (1)
    k = math.log(strike / forward)              # log-moneyness forward

    if abs(k) < _ATM_TOL:                        # caso at-the-forward, Eq. (2)
        return (2.0 / math.sqrt(maturity)) * norm.ppf((c + 1.0) / 2.0)

    m = 1.0 if k > 0.0 else strike / forward     # K>F -> OTM ; K<F -> ITM
    arg = (1.0 - c) / m                          # nível de probabilidade
    total_var_inv = _ig_quantile(arg, abs(k))    # F_IG^{-1}(...)
    v = 2.0 / math.sqrt(total_var_inv)           # volatilidade implícita TOTAL
    return v / math.sqrt(maturity)               # sigma = v / sqrt(T)


def implied_vol_put(
    price: Number, strike: Number, forward: Number,
    maturity: Number, discount: Number = 1.0,
) -> float:
    """
    Volatilidade implícita anualizada de uma PUT europeia, via Eq. (9).

    Usa a paridade put-call c - p = 1 - e^k. O argumento de probabilidade
    do quantil IG passa a ser (e^k - p) / m.
    """
    p = price / (discount * forward)
    k = math.log(strike / forward)

    if abs(k) < _ATM_TOL:                        # em K=F a paridade dá c = p
        return (2.0 / math.sqrt(maturity)) * norm.ppf((p + 1.0) / 2.0)

    m = 1.0 if k > 0.0 else strike / forward
    arg = (math.exp(k) - p) / m                  # Eq. (9)
    total_var_inv = _ig_quantile(arg, abs(k))
    v = 2.0 / math.sqrt(total_var_inv)
    return v / math.sqrt(maturity)


# ---------------------------------------------------------------------------
# Preço Black-Scholes (apenas para gerar exemplos e checar o round-trip).
# ---------------------------------------------------------------------------

def bs_call_price(
    sigma: Number, strike: Number, forward: Number,
    maturity: Number, discount: Number = 1.0,
) -> float:
    """Preço Black-Scholes de uma call europeia, Eq. (3) reescalada por D*F."""
    v = sigma * math.sqrt(maturity)
    k = math.log(strike / forward)
    c = norm.cdf(-k / v + v / 2.0) - math.exp(k) * norm.cdf(-k / v - v / 2.0)
    return discount * forward * c


def bs_put_price(
    sigma: Number, strike: Number, forward: Number,
    maturity: Number, discount: Number = 1.0,
) -> float:
    """Preço da put via paridade put-call:  P = C - D*(F - K)."""
    return bs_call_price(sigma, strike, forward, maturity, discount) \
        - discount * (forward - strike)


# ---------------------------------------------------------------------------
# Demonstração: reproduz o teste de recuperação na grade de deltas do paper.
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class RecoveryStats:
    n_cases: int
    mean_abs_error: float
    max_abs_error: float


def recovery_test() -> RecoveryStats:
    """
    Recria a Seção 3 do paper: para uma grade de (v, Delta), gera o preço da
    call e verifica de volta a vol implícita. Erro esperado ~1e-16 (precisão
    de máquina).
    """
    F, T, D = 100.0, 1.0, 0.97
    vs = [0.01] + [round(0.05 * i, 2) for i in range(1, 41)]      # 0.05 .. 2.00
    deltas = [0.05, 0.20, 0.30, 0.45, 0.55, 0.70, 0.80, 0.95]

    errors: list[float] = []
    # scipy.invgauss.ppf pode emitir um warning benigno para |k| minúsculo
    # (mu = 2/|k| enorme); o valor retornado continua correto.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        for v in vs:
            sigma = v / math.sqrt(T)
            for delta in deltas:
                k = v * (v / 2.0 - norm.ppf(delta))     # relação delta, Eq. (13)
                K = F * math.exp(k)
                C = bs_call_price(sigma, K, F, T, D)
                recovered_v = implied_vol_call(C, K, F, T, D) * math.sqrt(T)
                errors.append(abs(recovered_v - v))

    return RecoveryStats(
        n_cases=len(errors),
        mean_abs_error=sum(errors) / len(errors),
        max_abs_error=max(errors),
    )


def main() -> None:
    # 1) Um único exemplo, ponta a ponta.
    F, T, D, sigma_true = 100.0, 0.5, 0.98, 0.32
    K = 110.0
    C = bs_call_price(sigma_true, K, F, T, D)
    P = bs_put_price(sigma_true, K, F, T, D)

    print("Exemplo único (call OTM, K > F)")
    print(f"  inputs : F={F}  K={K}  T={T}  D={D}  sigma_verdadeiro={sigma_true}")
    print(f"  preço da call C        = {C:.10f}")
    print(f"  vol implícita (call)   = {implied_vol_call(C, K, F, T, D):.15f}")
    print(f"  vol implícita (put)    = {implied_vol_put(P, K, F, T, D):.15f}")
    print()

    # 2) Teste de recuperação na grade de deltas (Seção 3 do paper).
    stats = recovery_test()
    print("Teste de recuperação na grade de deltas")
    print(f"  casos                  = {stats.n_cases}")
    print(f"  erro absoluto médio    = {stats.mean_abs_error:.3e}")
    print(f"  erro absoluto máximo   = {stats.max_abs_error:.3e}")


if __name__ == "__main__":
    main()
```