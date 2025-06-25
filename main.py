from clp_core import CLPSimulator
import time

if __name__ == "__main__":
    clp = CLPSimulator()

    # Define entrada I0.0 como True
    clp.inputs[0] = True
    clp.memories[0] = True

    programa = [
        "LD I0.0",
        "AND M0.0",
        "OUT Q0.0"
    ]

    clp.load_program(programa)

    clp.set_mode("RUN")
    clp.start()

    try:
        while True:
            print(f"Entradas: {clp.inputs}")
            print(f"Memórias: {clp.memories}")
            print(f"Saídas: {clp.outputs}")
            time.sleep(1)
    except KeyboardInterrupt:
        clp.stop()
        print("Simulador parado.")

