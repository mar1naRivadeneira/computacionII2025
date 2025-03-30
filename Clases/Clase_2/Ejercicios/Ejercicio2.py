import os

for _ in range(2):  #crea dos procesos hijos
    pid = os.fork()
    if pid == 0:
        print(f"Hijo: PID = {os.getpid()}, PPID = {os.getppid()}")
        exit()

os.wait()  
os.wait()  #
print("Padre finaliza")