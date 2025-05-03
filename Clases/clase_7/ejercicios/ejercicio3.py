import signal
import time

def main():
    print("Ignorando SIGINT (Ctrl+C) por 5 segundos...")
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    time.sleep(5)

    print("Restaurando manejo por defecto de SIGINT.")
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    print("Presioná Ctrl+C para finalizar.")
    while True:
        time.sleep(1)

if __name__ == "_main_":
    main()