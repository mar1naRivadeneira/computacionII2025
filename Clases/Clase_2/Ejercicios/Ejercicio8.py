import os
import time

def atender_cliente(n):
    print(f"Atendiendo cliente {n} (PID: {os.getpid()})")
    time.sleep(3)
    print(f"Cliente {n} atendido")

for cliente in range(5):  
    pid = os.fork()
    if pid == 0:
        atender_cliente(cliente + 1)
        exit()

while True:  
    try:
        os.wait()
    except ChildProcessError:
        break

print("Servidor finaliza")