import os
import time

for i in range(3):  # aca crea 3 procesos hijos
    pid = os.fork()
    if pid == 0:
        print(f"Hijo {i+1}: PID = {os.getpid()}")
        time.sleep(2)
        exit()

for _ in range(3):
    os.wait()  #espera a todos sus hijos
print("Padre finaliza")