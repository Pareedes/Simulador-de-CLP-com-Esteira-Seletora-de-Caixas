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

                // Desvia caixas médias (setpoint médio)
                LD I1
                AND I2
                OUT Q2
                NOT
                OUT Q1

                // Desvia caixas pesadas (setpoint pesado)
                LD I1
                AND I3
                OUT Q3
                NOT
                OUT Q1

                // Conta caixas desviadas médias (M10 ativa a cada 3 desviadas médias)
                LD M10
                CTU C0 3
                OUT M2

                // Conta caixas desviadas pesadas (M11 ativa a cada 2 desviadas pesadas)
                LD M11
                CTU C1 2
                OUT M3

                // Quando M2 ativa, aciona Q4 por 1s (TON)
                LD M2
                TON T0 10
                OUT Q4

                // Quando M3 ativa, aciona Q5 por 1s (TON)
                LD M3
                TON T1 10
                OUT Q5

Q1: Liga a esteira se já passaram 5 caixas (I5) ou se há caixa leve sobre o sensor (I1 ANDN I2 ANDN I3).
Q2: Desvia caixas médias (I2 ativo, ou seja, peso entre setpoint médio e pesado).
Q3: Desvia caixas pesadas (I3 ativo, ou seja, peso maior ou igual ao setpoint pesado).
M10: Memória que armazena o número de caixas desviadas pelo setpoint médio (atualizada pela simulação).
M11: Memória que armazena o número de caixas desviadas pelo setpoint pesado (atualizada pela simulação).
C0: Contador que conta grupos de 3 caixas desviadas médias (M10).
C1: Contador que conta grupos de 2 caixas desviadas pesadas (M11).
M2: Memória auxiliar para indicar quando C0 atingiu 3 (pode ser usada para alarmes, etc).
M3: Memória auxiliar para indicar quando C1 atingiu 2.
Q4: Ativado por 1 segundo (TON T0 10) sempre que 3 caixas médias forem desviadas.
Q5: Ativado por 1 segundo (TON T1 10) sempre que 2 caixas pesadas forem desviadas.

# // Código 1: Esteira sempre ligada, desvia apenas caixas pesadas
LD TRUE
OUT Q1
LD I1
AND I3
OUT Q3
NOT
OUT Q1

# // Código 2: Desvia médias e pesadas, esteira só liga se passaram 5 caixas
LD I5
OUT Q1
LD I1
AND I2
OUT Q2
NOT
OUT Q1
LD I1
AND I3
OUT Q3
NOT
OUT Q1
