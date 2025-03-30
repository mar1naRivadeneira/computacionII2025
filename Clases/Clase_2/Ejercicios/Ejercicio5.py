import os
import time

pid = os.fork()

if pid == 0:
    print("Hijo finaliza")
    exit()
else:
    print("Padre espera 5 segundos antes de hacer wait()")
    time.sleep(5)
    os.wait()  # va a agarrar el proceso zombi
    print("Padre finaliza")