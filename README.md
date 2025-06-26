# 🧾 **Documentação – Simulador de CLP com Esteira Seletora de Caixas**

## Autores

Gabriel Paredes Ferreira, Vitor Augusto Gonçalves Reis e Kelmson Leandro Rodrigues

## 📌 Objetivo

Simular o comportamento de um CLP (Controlador Lógico Programável), um interpretador de linguagem de Lista de Instruções (IL), variáveis internas (entradas, saídas, memórias, temporizadores e contadores) e um ambiente gráfico simulando uma esteira seletora de caixas.

---

## 🗂 Estrutura do Projeto

| Arquivo / Módulo         | Função Principal                                                                |
| ------------------------ | ------------------------------------------------------------------------------- |
| `CLPSimulator`           | Núcleo lógico do CLP: entradas, saídas, timers, contadores e modo de varredura. |
| `ILInterpreter`          | Interpretador de linguagem IL (Lista de Instrução).                             |
| `CLPGUI`                 | Interface gráfica com botões, LEDs, editor de código e simulação.               |
| `open_simulation_window` | Simulação visual da esteira seletora.                                           |
| `__main__`               | Inicia a aplicação com interface Tkinter.                                       |

Para rodar a aplicação, basta baixar o projeto e rodar gui.py. A aplicação também pode ser feita a partir dele, e já foi criada e disponibilizada para o professor.

---

## 🔁 Ciclo de Varredura do CLP

1. Lê as entradas.
2. Executa o programa IL.
3. Atualiza os temporizadores.
4. Atualiza os contadores.
5. Atualiza as saídas.
6. Espera 0,1s antes da próxima varredura.

---

## 💻 Componentes da Interface (CLPGUI)

### Entradas e Saídas

* **I0 – I7**: Entradas digitais simuladas por checkbuttons.
* **Q0 – Q7**: Saídas digitais, exibidas com LED (cor de fundo `green` ou `gray`).

### Controles

* **RUN / STOP / PROGRAM**: Modos de operação do CLP.
* **Carregar / Salvar / Executar Programa**: Gerenciamento do código IL.

### Data Table

Tabela com todas as variáveis em tempo real:

* Entradas, Saídas, Memórias
* Temporizadores (`T0` a `T31`) com preset, acumulador, e status "done"
* Contadores (`C0` a `C31`) com preset, acumulador, e status "done"

---

## 🎮 Simulação da Esteira Seletora

* **Caixas de diferentes pesos** circulam pela esteira.
* **Sensor de presença (I1)** detecta caixas.
* **I2 / I3** indicam se a caixa é média ou pesada.
* **Q1** aciona o fechamento do portão da esteira.
* **Q2** aciona o pistão para desviar caixas médias.
* **Q3** aciona o pistão para desviar caixas pesadas.
* A lógica de desvio depende das saídas do CLP.

### Contadores do Sistema

* `total_passaram`, `total_desviadas`, `total_normais`
* `desviadas_medio_var`, `desviadas_pesado_var`

Esses valores são mapeados para **memórias internas**:

* `M10`: caixas peso médio desviadas
* `M11`: caixas peso pesado desviadas
* `M20`: total de caixas que passaram
* `M21`: caixas que foram desviadas (desviadas médio e desviadas pesado)
* `M22`: total de caixas entregues

---

## 🧠 Comandos IL Suportados

### Lógicos

* `LD`, `LDN`, `AND`, `ANDN`, `OR`, `ORN`, `NOT`, `OUT`

### Temporizadores

* `TON Tn X` → Temporizador On Delay
* `TOF Tn X` → Temporizador Off Delay

### Contadores

* `CTU Cn X` → Contador ascendente
* `CTD Cn X` → Contador descendente

---

## 🧪 Exemplos de Código IL

[Link para o README contendo os códigos IL exemplo](./data/README.md)

---

## 🔘 Botões Manuais I5, I6, I7

Botões na simulação para controlar manualmente as entradas:

* `I5`: Gatilho manual (ex: para ligar esteira ou contar eventos)
* `I6`, `I7`: Outros controles customizáveis (ex: reset, pistões manuais)

---

## 🛠 Possíveis Expansões Futuras

* Criação de perfis de caixa com peso ajustável.
* Exportação dos dados da simulação para CSV.
* Mais cenários de simulação.

---
