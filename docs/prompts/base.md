1. **Defina um papel** para a IA ("atue como…").
2. **Dê contexto específico** — números, prazos, restrições, dados reais. Sem isso, resposta genérica.
3. **Peça estrutura na saída** — itens numerados forçam clareza.
4. **Force premissas, riscos e lacunas** — é onde a IA expõe o que não sabe.
5. **Conversa, não pergunta única** — refine em iterações. Pode levar 10–20 idas e vindas.

---

## 2. Template genérico

Use quando nenhum template específico serve. Cobre 70% dos casos.

```
Atue como [papel/especialidade].

CONTEXTO
[situação, números, restrições, prazo, objetivo concreto]

ENTREGUE
1. Recomendação principal
2. Premissas que você está assumindo
3. Riscos e o que pode dar errado
4. O que invalidaria essa recomendação
5. Que informações estão faltando e onde você está mais incerto

Antes de começar, me pergunte o que ficou ambíguo no contexto.
Não invente premissas sobre o que eu não declarei.
```

## Perguntas (segunda rodada)

Reutilizáveis em qualquer domínio. Use depois da primeira resposta.

- "Critique sua própria resposta como um reviewer hostil da área."
- "Liste correlações e dependências entre os itens que você propôs. Quero diversificação, não redundância."
- "Quais das suas premissas são mais frágeis? Em que cenário cada uma quebra?"
- "Que informações adicionais mudariam **materialmente** sua resposta?"
- "Me dê uma versão alternativa que privilegie [X] em vez de [Y]. Compare trade-offs."
- "Refaça assumindo que [premissa importante] é falsa."
- "Liste o que você NÃO recomendaria fazer e por quê."

---

## Anti-padrões

Releia isso quando estiver com pressa.

- ❌ Pergunta aberta sem contexto numérico ("como devo investir?", "qual indicador usar?").
- ❌ Aceitar a primeira resposta como final. Sempre pelo menos uma rodada de crítica.
- ❌ Confiar em cálculos numéricos sem conferir — modelo soa autoritativo mesmo errando.
- ❌ Esquecer de pedir premissas/lacunas. É a parte mais valiosa.
- ❌ Copiar template da internet sem adaptar ao seu contexto real.
- ❌ Misturar muitas perguntas num prompt só. Uma intenção clara por turno.
- ❌ Não dizer o **propósito final** ("isso vai virar feature de ML", "isso vai pra um cliente"). Muda completamente o output.

---

## Notas para manter este documento

- Só adicionar template novo depois de tê-lo usado **com sucesso** numa conversa real.
- Se um template não foi usado em 6 meses, deletar.
- Princípios e anti-padrões são estáveis. Templates evoluem.