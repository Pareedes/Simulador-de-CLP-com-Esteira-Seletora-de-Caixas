O projeto consiste em montar um ambiente de simulação de um CLP no computador. O ambiente deve conter um interface interativa para operar as entradas e saídas disponíveis no simulador de processo industrial. 

O  ambiente  de  simulação  pode  tomar  como  referência  os  ambientes  de  simulação  de  outros programas, como LogixPro.

O Simulador de CLP permitir o uso dos seguintes itens: 
    • funções lógicas básicas: 
        o NÃO (NOT), 
        o OU (OR) 
        o E (AND), 
    • memórias booleanas locais, no mínimo 32 
        • temporizadores, com base de tempo em 0,1s, no mínimo 32 
        o ON DELAY - retardo na ativação 
        o OFF DELAY - retardo na desativação 
    • Contadores, no mínimo 32  
        o Progressivo - UP 
        o Regressivo - DOWN

O  programa  de  ter  uma  ferramenta  para  visualizar  todas  as  variáveis  do  sistema, no formato da Data Table do LogixPro.

O  programa  simulador  deve  ser  comportar  como  um  CLP  convencional,  respeitando  o ciclo de varredura do sistema:

0 - inicializar o sistema 
1 - ler as entradas e armazenar numa memória imagem 
2 - processar o programa do usuário e salvar as alterações da saída na memória imagem de saída 
3 - atualizar as saídas a partir da memória imagem de saída 
4 - retornar o item 1

O simulador deve ter alguns modos de operação como no CLP convencional, são eles: 
    • Modo Programação (PROGRAM) - permite que o programa lógico seja alterado. 

Neste modo, não há leitura e nem escrita nas saídas físicas. 
    • Modo Parado (STOP)-  o sistema para o programa lógico criado pelo usuário. 
    • Modo Operação (RUN)-  o sistema roda o programa lógico criado pelo usuário. 

O simulador deve permitir salvar e carregar programas escritos previamente. 
A linguagem de programação do CLP deve ser Lista de Instrução