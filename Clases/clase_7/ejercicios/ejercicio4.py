import threading
import signal
import time
import os

pausado = False
lock = threading.Lock()

def handler_usr1(signum, frame):
    global pausado
    with lock:
        pausado = True
        print("Recibido SIGUSR1: pausa activada.")

def handler_usr2(signum, frame):
    global pausado
    with lock:
        pausado = False
        print("Recibido SIGUSR2: pausa desactivada.")

def contador():
    global pausado
    for i in range(30, 0, -1):
        with lock:
            if not pausado:
                print(f"Contador: {i}")
            else:
                print("Pausado...")
        time.sleep(1)

if __name__ == "_main_":
    signal.signal(signal.SIGUSR1, handler_usr1)
    signal.signal(signal.SIGUSR2, handler_usr2)

    print(f"PID principal: {os.getpid()}")
    t = threading.Thread(target=contador)
    t.start()
    t.join()