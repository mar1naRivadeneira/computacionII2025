import os

pid = os.fork()

if pid == 0:  
    print(f"Hijo: PID = {os.getpid()}, PPID = {os.getppid()}")
else:  
    print(f"Padre: PID = {os.getpid()}, Hijo PID = {pid}")