import signal
import atexit
import time
import os

def despedida():
    print("Proceso finalizando. Gracias por usar el programa.")

def handler_sigterm(signum, frame):
    print("Recibido SIGTERM.")
    exit(0)

atexit.register(despedida)
signal.signal(signal.SIGTERM, handler_sigterm)

print(f"PID del proceso: {os.getpid()}")
print("Esperando SIGTERM...")
while True:
    time.sleep(1)