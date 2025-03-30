import os
import time

pid = os.fork()

if pid == 0:
    time.sleep(5)  # Espera a que el padre termine
    print(f"Hijo huérfano: PID = {os.getpid()}, nuevo PPID = {os.getppid()}")
else:
    print("Padre finaliza inmediatamente")