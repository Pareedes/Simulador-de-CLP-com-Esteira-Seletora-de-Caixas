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
        self.text_program = tk.Text(frame_program, width=50, height=20)
        self.text_program.pack()

        # Botões de controle
        btn_run = ttk.Button(frame_control, text="RUN", command=lambda: self.set_mode("RUN"))
        btn_run.grid(row=0, column=0, padx=5, pady=5)

        btn_stop = ttk.Button(frame_control, text="STOP", command=lambda: self.set_mode("STOP"))
        btn_stop.grid(row=0, column=1, padx=5, pady=5)

        btn_program = ttk.Button(frame_control, text="PROGRAM", command=lambda: self.set_mode("PROGRAM"))
        btn_program.grid(row=0, column=2, padx=5, pady=5)

        btn_load = ttk.Button(frame_control, text="Carregar", command=self.load_program)
        btn_load.grid(row=0, column=3, padx=5, pady=5)

        btn_save = ttk.Button(frame_control, text="Salvar", command=self.save_program)
        btn_save.grid(row=0, column=4, padx=5, pady=5)

        btn_exec = ttk.Button(frame_control, text="Executar Programa", command=self.load_program_from_text)
        btn_exec.grid(row=0, column=5, padx=5, pady=5)

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

    def set_mode(self, mode):
        self.clp.set_mode(mode)
        if mode == "RUN":
            self.clp.start()
        else:
            self.clp.stop()

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


if __name__ == "__main__":
    root = tk.Tk()
    app = CLPGUI(root)
    root.mainloop()
