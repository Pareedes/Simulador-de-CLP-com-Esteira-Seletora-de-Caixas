import time
import threading

from il_intepreter import ILInterpreter


class CLPSimulator:
    def __init__(self):
        # Memórias
        self.inputs = [False] * 8   # I0.0 até I0.7
        self.outputs = [False] * 8  # Q0.0 até Q0.7
        self.memories = [False] * 32  # M0.0 até M31
        self.timers = {f"T{i}": {"preset": 0, "acc": 0, "enabled": False, "done": False, "last_state": False} for i in range(32)}
        self.counters = {f"C{i}": {"preset": 0, "acc": 0, "enabled": False, "done": False, "last_state": False} for i in range(32)}

        # Programa carregado (Lista de Instrução)
        self.program = []

        # Estados
        self.running = False
        self.mode = "STOP"  # STOP | RUN | PROGRAM

        # Thread da varredura
        self.scan_thread = None

        self.il = ILInterpreter(self)

    def load_program(self, program_lines):
        self.program = program_lines

    def start(self):
        if self.mode == "RUN" and not self.running:
            self.running = True
            self.scan_thread = threading.Thread(target=self.scan_cycle)
            self.scan_thread.start()

    def stop(self):
        self.running = False
        if self.scan_thread:
            self.scan_thread.join()

    def set_mode(self, mode):
        if mode in ["RUN", "STOP", "PROGRAM"]:
            self.mode = mode
            if mode != "RUN":
                self.stop()
        else:
            print("Modo inválido!")

    def scan_cycle(self):
        while self.running:
            # 1 - Ler Entradas

            # 2 - Executar programa
            self.execute_program()

            # 3 - Atualizar timers e contadores
            self.update_timers()
            self.update_counters()

            # 4 - Atualizar saídas

            # 5 - Espera
            time.sleep(0.1)

    def set_timer(self, name, preset, enabled):
        if name in self.timers:
            self.timers[name]["preset"] = preset
            self.timers[name]["enabled"] = enabled

    def get_timer_done(self, name):
        return self.timers.get(name, {}).get("done", False)

    def set_counter(self, name, preset, enabled):
        if name in self.counters:
            self.counters[name]["preset"] = preset
            self.counters[name]["enabled"] = enabled

    def get_counter_done(self, name):
        return self.counters.get(name, {}).get("done", False)

    # Métodos auxiliares para o interpretador acessar timers/contadores

    def execute_program(self):
        # Aqui será chamado o interpretador da Lista de Instrução
        for line in self.program:
            print(f"Executando: {line}")
        # (Lógica ainda não implementada)

    def execute_program(self):
        self.il.execute(self.program)

    def update_timers(self):
        for name, timer in self.timers.items():
            if timer["enabled"]:
                if not timer["last_state"]:
                    timer["acc"] = 0  # reset accumulator on rising edge
                timer["acc"] += 0.1  # increment by scan time (100ms)
                if timer["acc"] >= timer["preset"]:
                    timer["done"] = True
                else:
                    timer["done"] = False
                timer["last_state"] = True
            else:
                timer["acc"] = 0
                timer["done"] = False
                timer["last_state"] = False

    def update_counters(self):
        for name, counter in self.counters.items():
            if counter["enabled"] and not counter["last_state"]:
                counter["acc"] += 1
                if counter["acc"] >= counter["preset"]:
                    counter["done"] = True
            counter["last_state"] = counter["enabled"]

    

    def reset(self):
        self.inputs = [False] * 8
        self.outputs = [False] * 8
        self.memories = [False] * 32
        self.timers.clear()
        self.counters.clear()
