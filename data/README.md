# 1 Simulador Peso:
- Código comum para o funcionamento da esteira.

# 2 SimuladorPesoContadores:

        // Liga esteira se já passaram 5 caixas OU se há caixa leve sobre o sensor
        LD I5
        OUT Q1
        LD I1
        ANDN I2
        ANDN I3
        OUT Q1

        // Desvia caixas médias
        LD I1
        AND I2
        OUT Q2
        NOT
        OUT Q1

        // Desvia caixas pesadas
        LD I1
        AND I3
        OUT Q3
        NOT
        OUT Q1

        // Conta caixas desviadas (I6 ativa a cada 3 desviadas)
        LD I6
        CTU C0 3
        OUT M0

        // Quando M0 ativa, aciona Q4 por 1s (TON)
        LD M0
        TON T0 10
        OUT Q4

- Q é ativado quando há uma caixa pesada sobre o sensor (I1 AND I2).
- Q1 é desligado enquanto Q2 está ativo (NOT OUT Q1).
- Q1 é ligado para caixas leves ou quando já passaram 5 caixas.
- O restante do código de contadores permanece igual.

