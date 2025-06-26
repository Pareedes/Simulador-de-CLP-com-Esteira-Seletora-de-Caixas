import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from clp_core import CLPSimulator
import threading


class CLPGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de CLP")

        self.clp = CLPSimulator()

        self.build_ui()

        # Atualização periódica da interface
        self.update_gui()

    def build_ui(self):
        # Frames principais
        frame_io = ttk.LabelFrame(self.root, text="Entradas e Saídas")
        frame_io.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        frame_program = ttk.LabelFrame(self.root, text="Editor de Programa")
        frame_program.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        frame_control = ttk.LabelFrame(self.root, text="Controle")
        frame_control.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Entradas
        ttk.Label(frame_io, text="Entradas").grid(row=0, column=0)
        self.input_buttons = []
        for i in range(8):
            btn = ttk.Checkbutton(
                frame_io,
                text=f"I{i}",
                command=lambda idx=i: self.toggle_input(idx)
            )
            btn.grid(row=i + 1, column=0, sticky="w")
            self.input_buttons.append(btn)

        # Saídas
        ttk.Label(frame_io, text="Saídas").grid(row=0, column=1)
        self.output_labels = []
        for i in range(8):
            lbl = tk.Label(frame_io, text=f"Q{i}", bg="gray", width=6)
            lbl.grid(row=i + 1, column=1, sticky="w")
            self.output_labels.append(lbl)

        # Editor de programa
        self.text_program = tk.Text(frame_program, width=50, height=20, state="disabled")
        self.text_program.pack()

        # Botões de controle
        self.btn_run = ttk.Button(frame_control, text="RUN", command=lambda: self.set_mode("RUN"))
        self.btn_run.grid(row=0, column=0, padx=5, pady=5)

        self.btn_stop = ttk.Button(frame_control, text="STOP", command=lambda: self.set_mode("STOP"))
        self.btn_stop.grid(row=0, column=1, padx=5, pady=5)

        self.btn_program = ttk.Button(frame_control, text="PROGRAM", command=lambda: self.set_mode("PROGRAM"))
        self.btn_program.grid(row=0, column=2, padx=5, pady=5)

        btn_load = ttk.Button(frame_control, text="Carregar", command=self.load_program)
        btn_load.grid(row=0, column=3, padx=5, pady=5)

        btn_save = ttk.Button(frame_control, text="Salvar", command=self.save_program)
        btn_save.grid(row=0, column=4, padx=5, pady=5)

        btn_exec = ttk.Button(frame_control, text="Executar Programa", command=self.load_program_from_text)
        btn_exec.grid(row=0, column=5, padx=5, pady=5)

        btn_sim = ttk.Button(self.root, text="Simulação Esteira", command=self.open_simulation_window)
        btn_sim.grid(row=3, column=0, columnspan=2, pady=10)

        # Data Table de variáveis
        frame_table = ttk.LabelFrame(self.root, text="Data Table (Variáveis)")
        frame_table.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        columns = ("Tipo", "Nome", "Valor", "Preset", "Acumulado", "Done")
        self.table = ttk.Treeview(frame_table, columns=columns, show="headings", height=20)
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=90)
        self.table.pack(fill="x")

    def toggle_input(self, idx):
        self.clp.inputs[idx] = not self.clp.inputs[idx]

    def update_input_buttons(self):
        # Sincroniza os botões de entrada com o estado real das entradas
        for i, btn in enumerate(self.input_buttons):
            if self.clp.inputs[i]:
                btn.state(['selected'])
            else:
                btn.state(['!selected'])

    def set_mode(self, mode):
        self.clp.set_mode(mode)
        if mode == "RUN":
            self.clp.start()
        else:
            self.clp.stop()
        if mode == "PROGRAM":
            self.clp.reset()
            self.text_program.config(state="normal")
            self.update_input_buttons()  # <-- Adicione esta linha
        else:
            self.text_program.config(state="disabled")
        self.update_mode_buttons()

    def update_mode_buttons(self):
        # Reseta estilos
        self.btn_run.config(style="TButton")
        self.btn_stop.config(style="TButton")
        self.btn_program.config(style="TButton")

        # Cria estilos customizados se ainda não existem
        style = ttk.Style()
        style.map("Run.TButton", background=[("active", "green"), ("!active", "green")])
        style.map("Stop.TButton", background=[("active", "red"), ("!active", "red")])
        style.map("Program.TButton", background=[("active", "blue"), ("!active", "blue")])

        # Destaca o botão do modo atual
        if self.clp.mode == "RUN":
            self.btn_run.config(style="Run.TButton")
        elif self.clp.mode == "STOP":
            self.btn_stop.config(style="Stop.TButton")
        elif self.clp.mode == "PROGRAM":
            self.btn_program.config(style="Program.TButton")

    def load_program_from_text(self):
        code = self.text_program.get("1.0", tk.END)
        lines = [line.strip() for line in code.splitlines() if line.strip()]
        self.clp.load_program(lines)

    def load_program(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Arquivo de programa", "*.il"), ("Todos os arquivos", "*.*")]
        )
        if filepath:
            with open(filepath, "r") as f:
                code = f.read()
                self.text_program.delete("1.0", tk.END)
                self.text_program.insert(tk.END, code)
                self.load_program_from_text()

    def save_program(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".il",
            filetypes=[("Arquivo de programa", "*.il"), ("Todos os arquivos", "*.*")]
        )
        if filepath:
            code = self.text_program.get("1.0", tk.END)
            with open(filepath, "w") as f:
                f.write(code)

    def update_gui(self):
        # Atualiza LEDs das saídas
        for i, lbl in enumerate(self.output_labels):
            lbl.config(bg="green" if self.clp.outputs[i] else "gray")

        # Atualiza Data Table
        self.table.delete(*self.table.get_children())

        # Entradas
        for i, val in enumerate(self.clp.inputs):
            self.table.insert("", "end", values=("Entrada", f"I{i}", val, "-", "-", "-"))
        # Saídas
        for i, val in enumerate(self.clp.outputs):
            self.table.insert("", "end", values=("Saída", f"Q{i}", val, "-", "-", "-"))
        # Memórias
        for i, val in enumerate(self.clp.memories):
            self.table.insert("", "end", values=("Memória", f"M{i}", val, "-", "-", "-"))
        # Timers
        for name, timer in self.clp.timers.items():
            self.table.insert(
                "", "end",
                values=(
                    "Timer",
                    name,
                    "",
                    f"{timer['preset']:.1f}s",
                    f"{timer['acc']:.1f}s",
                    timer['done']
                )
            )
        # Contadores
        for name, counter in self.clp.counters.items():
            self.table.insert(
                "", "end",
                values=(
                    "Contador",
                    name,
                    "",
                    counter['preset'],
                    counter['acc'],
                    counter['done']
                )
            )

        # Loop de atualização
        self.root.after(200, self.update_gui)
        self.update_mode_buttons()

    def open_simulation_window(self):
        sim_win = tk.Toplevel(self.root)
        sim_win.title("Ambiente de Simulação: Esteira Seletora de Caixas")
        canvas = tk.Canvas(sim_win, width=600, height=200, bg="white")
        canvas.pack()

        # Contadores de caixas
        total_passaram = tk.IntVar(value=0)
        total_desviadas = tk.IntVar(value=0)
        total_normais = tk.IntVar(value=0)

        # Controle de setpoint
        tk.Label(sim_win, text="Setpoint (kg):").pack(side="left")
        setpoint_var = tk.IntVar(value=5)
        setpoint_spin = tk.Spinbox(sim_win, from_=1, to=10, textvariable=setpoint_var, width=3)
        setpoint_spin.pack(side="left")

        # Exibição dos contadores
        frame_count = tk.Frame(sim_win)
        frame_count.pack(side="bottom", fill="x")
        tk.Label(frame_count, text="Total Passaram:").pack(side="left")
        tk.Label(frame_count, textvariable=total_passaram, width=4).pack(side="left")
        tk.Label(frame_count, text=" | Desviadas:").pack(side="left")
        tk.Label(frame_count, textvariable=total_desviadas, width=4).pack(side="left")
        tk.Label(frame_count, text=" | Entregues:").pack(side="left")
        tk.Label(frame_count, textvariable=total_normais, width=4).pack(side="left")

        # Variáveis de simulação
        boxes = []
        esteira_on = False
        pistao_on = False

        # Para uso como entradas digitais do CLP
        self.caixas_passaram = 0
        self.caixas_desviadas = 0
        self.caixas_normais = 0

        # Definição de pesos e cores
        pesos_cores = [
            (1, "blue"),
            (4, "green"),
            (5, "orange"),
            (8, "purple")
        ]

        def add_box():
            import random
            peso, cor = random.choice(pesos_cores)
            boxes.append({"x": 10, "peso": peso, "cor": cor, "desviado": False, "y": 110})

        def update_sim():
            nonlocal esteira_on, pistao_on
            if self.clp.mode != "RUN":
                draw_sim()
                sim_win.after(100, update_sim)
                return

            esteira_on = self.clp.outputs[1]  # Q1
            pistao_on = self.clp.outputs[2]   # Q2

            presenca = False
            peso_caixa = 0
            for box in boxes:
                sobre_sensor = 240 < box["x"] < 260 and not box["desviado"]
                if sobre_sensor:
                    presenca = True
                    peso_caixa = box["peso"]
                    # Se pistão ativado e peso >= setpoint, desvia a caixa
                    if pistao_on and box["peso"] >= setpoint_var.get():
                        box["desviado"] = True

                # Só move a caixa se:
                # - Ela não está sobre o sensor, ou
                # - A esteira está ligada
                if not sobre_sensor or esteira_on:
                    if not box["desviado"]:
                        box["x"] += 5
                # Se desviado, move para baixo (expulsão)
                if box["desviado"]:
                    box["y"] += 10  # move para baixo acumulativamente

            self.clp.inputs[1] = presenca
            self.clp.inputs[2] = (peso_caixa >= setpoint_var.get()) if presenca else False

            # Contagem de caixas
            count_passaram = total_passaram.get()
            count_desviadas = total_desviadas.get()
            count_normais = total_normais.get()
            novas_caixas = []
            for box in boxes:
                # Caixa desviada saiu da tela
                if box["desviado"] and box["y"] >= 200:
                    count_passaram += 1
                    count_desviadas += 1
                # Caixa normal saiu da esteira
                elif not box["desviado"] and box["x"] >= 570:
                    count_passaram += 1
                    count_normais += 1
                else:
                    novas_caixas.append(box)
            boxes[:] = novas_caixas

            total_passaram.set(count_passaram)
            total_desviadas.set(count_desviadas)
            total_normais.set(count_normais)

            # Atualiza variáveis para uso no CLP (exemplo: entradas I6, I7, I5)
            self.clp.inputs[5] = count_passaram >= 5   # I5: 5 caixas passaram
            self.clp.inputs[6] = count_desviadas >= 3  # I6: 3 caixas desviadas
            self.clp.inputs[7] = count_normais >= 2    # I7: 2 caixas normais

            if not boxes or boxes[-1]["x"] > 120:
                add_box()

            draw_sim()
            sim_win.after(100, update_sim)

        def draw_sim():
            canvas.delete("all")
            # Esteira
            canvas.create_rectangle(0, 100, 600, 140, fill="gray")
            # Sensor de presença
            canvas.create_rectangle(250, 90, 260, 150, fill="yellow" if self.clp.inputs[1] else "white")
            # Pistão
            if pistao_on:
                canvas.create_rectangle(260, 70, 290, 100, fill="red")
            # Caixas
            for box in boxes:
                y1 = box.get("y", 110)
                y2 = y1 + 25 if not box["desviado"] else y1 + 25
                canvas.create_rectangle(box["x"], y1, box["x"]+30, y2, fill=box["cor"], outline="black")
                canvas.create_text(box["x"]+15, y1+10, text=f"{box['peso']}kg", fill="white", font=("Arial", 8, "bold"))

        add_box()
        update_sim()

if __name__ == "__main__":
    root = tk.Tk()
    app = CLPGUI(root)
    root.mainloop()
