import os
import signal
import time
import random
from multiprocessing import Process

def handler(signum, frame):
    print(f"Padre recibió la señal {signum} de un hijo (PID no directo, ver consola).")

def hijo(signal_type):
    time.sleep(random.randint(1, 3))
    print(f"Hijo PID {os.getpid()} enviando señal {signal_type}")
    os.kill(os.getppid(), signal_type)

if __name__ == "_main_":
    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR2, handler)
    signal.signal(signal.SIGTERM, handler)

    señales = [signal.SIGUSR1, signal.SIGUSR2, signal.SIGTERM]
    procesos = []

    for sig in señales:
        p = Process(target=hijo, args=(sig,))
        p.start()
        procesos.append(p)

    for p in procesos:
        p.join()

    print("Todos los hijos terminaron.")