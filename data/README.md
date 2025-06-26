# // Código 1: Esteira sempre ligada, desvia apenas caixas pesadas
LD TRUE
OUT Q1
LD I1
AND I3
OUT Q3
NOT
OUT Q1

# // Código 2: Desvia médias e pesadas
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

# // Código 3: Manual com Botões - Desbloquea esteita, medio, pesado

LD I5
OUT Q1
LD I6
OUT Q2
LD I7
OUT Q3

# // Código 4: Depois de 30 segundos os pesados passam e os medios não.

LD TRUE
OUT Q1
LD TRUE
TON T0 300
LD T0
OUT Q2
LD I1
AND I3
ANDN T0          
OUT Q3

# // Código 5: Deixa passar tudo, até contar 5 caixas, depois aciona os 2 pistões
LD TRUE
OUT Q1
LD M20
ANDN M10        
CTU C0 5        
LD M20
OUT M10        
LD C0
OUT Q2          
LD C0
OUT Q3          
