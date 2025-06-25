import re


class ILInterpreter:
    def __init__(self, clp):
        self.clp = clp  # Referência ao CLP (acesso a entradas, saídas, memórias)
        self.acc = False  # Acumulador lógico

    def get_value(self, address):
        """Lê valor de uma variável (I, Q, M) ou constante TRUE/FALSE"""
        if address is None:
            return False
        addr_upper = address.upper()
        if addr_upper == "TRUE":
            return True
        if addr_upper == "FALSE":
            return False
        prefix, index = address[0], address[1:]
        if prefix == "I":
            return self.clp.inputs[int(index)]
        elif prefix == "Q":
            return self.clp.outputs[int(index)]
        elif prefix == "M":
            return self.clp.memories[int(index)]
        else:
            raise ValueError(f"Endereço inválido: {address}")

    def set_value(self, address, value):
        """Escreve valor em uma variável (Q ou M)"""
        prefix, index = address[0], address[1:]
        if prefix == "Q":
            self.clp.outputs[int(index)] = value
        elif prefix == "M":
            self.clp.memories[int(index)] = value
        else:
            raise ValueError(f"Endereço inválido para escrita: {address}")

    def execute(self, program):
        """Executa um programa em Lista de Instrução"""
        self.acc = False  # Reset do acumulador no início de cada varredura

        for line in program:
            line = line.strip()
            if not line or line.startswith("//"):
                continue  # Ignora linha vazia ou comentário

            parts = re.split(r'\s+', line)
            instruction = parts[0].upper()

            operand = parts[1] if len(parts) > 1 else None
            operand2 = parts[2] if len(parts) > 2 else None

            if instruction == "LD":
                self.acc = self.get_value(operand)

            elif instruction == "LDN":
                self.acc = not self.get_value(operand)

            elif instruction == "AND":
                self.acc = self.acc and self.get_value(operand)

            elif instruction == "ANDN":
                self.acc = self.acc and (not self.get_value(operand))

            elif instruction == "OR":
                self.acc = self.acc or self.get_value(operand)

            elif instruction == "ORN":
                self.acc = self.acc or (not self.get_value(operand))

            elif instruction == "NOT":
                self.acc = not self.acc

            elif instruction == "OUT":
                self.set_value(operand, self.acc)

            # Temporizador ON DELAY
            elif instruction == "TON":
                # Exemplo: TON T0 5  (T0, preset 0.5s)
                timer_name = operand
                preset = float(operand2) * 0.1 if operand2 else 0.1
                self.clp.set_timer(timer_name, preset, self.acc)
                self.acc = self.clp.get_timer_done(timer_name)

            # Temporizador OFF DELAY
            elif instruction == "TOF":
                # Exemplo: TOF T0 5
                timer_name = operand
                preset = float(operand2) * 0.1 if operand2 else 0.1
                # Para TOF, habilita quando acc == False
                self.clp.set_timer(timer_name, preset, not self.acc)
                self.acc = self.clp.get_timer_done(timer_name)

            # Contador UP
            elif instruction == "CTU":
                # Exemplo: CTU C0 10
                counter_name = operand
                preset = int(operand2) if operand2 else 1
                self.clp.set_counter(counter_name, preset, self.acc)
                self.acc = self.clp.get_counter_done(counter_name)

            # Contador DOWN
            elif instruction == "CTD":
                # Exemplo: CTD C0 10
                counter_name = operand
                preset = int(operand2) if operand2 else 1
                # Para DOWN, habilita quando acc == False
                self.clp.set_counter(counter_name, preset, not self.acc)
                self.acc = self.clp.get_counter_done(counter_name)

            else:
                print(f"Instrução não reconhecida: {instruction}")
