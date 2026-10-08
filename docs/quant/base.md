
# Information Coefficient (Coeficiente de Informação) - IC 

O IC mede a habilidade preditiva de um sinal ou fator de trading (como um indicador técnico ou fundamentalista). Ele calcula a correlação entre as previsões do seu modelo e os retornos reais dos ativos no período seguinte.


## Como o IC é Calculado e Interpretado

Geralmente, o IC utiliza a correlação de postos de Spearman para avaliar se a ordem de classificação (ranking) das previsões corresponde à ordem dos melhores retornos.

A fórmula baseia-se na correlação entre as previsões e os retornos:

\(\text{IC}=\rho (\text{Previsão}_{t},\text{Retorno}_{t+1})\)

A interpretação do seu valor segue a lógica estatística:

- +1.0: Previsão perfeita. O fator acertou exatamente a ordem de quais ativos subiriam mais.
- 0.0: Sem poder preditivo. O sinal funciona como o cara ou coroa (puro ruído).
- -1.0: Previsão perfeitamente invertida. (Basta inverter o sinal para ter um modelo perfeito).

## O que é um "Bom IC" no Trading Quantitativo?

No mundo real de fundos quantitativos, os valores de IC são surpreendentemente baixos devido à alta eficiência dos mercados.

- IC > 0.02 (2%): Já é considerado um sinal útil e potencialmente lucrativo.
- IC > 0.05 (5%): É considerado um fator excelente e muito forte.
- IC > 0.10 (10%): Extremamente raro em horizontes de tempo curtos; costuma indicar look-ahead bias (vazamento de dados futuros no teste) ou erro no backtest.


