import os
import time

pid1 = os.fork()
if pid1 == 0:
    print("Primer hijo ejecutando...")
    time.sleep(2)
    print("Primer hijo finaliza")
    exit()

os.wait()  # aca espera al primer hijo

pid2 = os.fork()
if pid2 == 0:
    print("Segundo hijo ejecutando...")
    time.sleep(2)
    print("Segundo hijo finaliza")
    exit()

os.wait()  #espera al segundo hijo
print("Padre finaliza")