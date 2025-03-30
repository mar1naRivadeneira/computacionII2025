import os
import time

pid = os.fork()

if pid == 0:  
    time.sleep(3)  
    os.execlp("sh", "sh", "-c", "echo 'Proceso huérfano ejecutando comando crítico'")
else:
    print("Padre finaliza antes que el hijo")