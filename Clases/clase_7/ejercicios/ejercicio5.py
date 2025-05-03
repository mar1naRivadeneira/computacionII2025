import os
import signal
import time
import multiprocessing
from collections import deque

cola_trabajos = deque()

def productor(pid_consumidor):
    for i in range(5):
        mensaje = f"Trabajo {i+1} generado a las {time.time()}"
        print(f"[Productor] Generando: {mensaje}")
        cola_trabajos.append(mensaje)
        os.kill(pid_consumidor, signal.SIGUSR1)
        time.sleep(0.5)

def handler_usr1(signum, frame):
    if cola_trabajos:
        trabajo = cola_trabajos.popleft()
        print(f"[Consumidor] Recibido: {trabajo}")
        time.sleep(1)
    else:
        print("[Consumidor] Señal recibida pero sin trabajo en cola.")

def consumidor():
    signal.signal(signal.SIGUSR1, handler_usr1)
    print(f"PID consumidor: {os.getpid()}")
    while True:
        signal.pause()

if __name__ == "_main_":
    consumidor_proc = multiprocessing.Process(target=consumidor)
    consumidor_proc.start()

    time.sleep(1)  
    productor(os.getpid())

    consumidor_proc.terminate()
    consumidor_proc.join()