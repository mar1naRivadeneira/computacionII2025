import os
import time

fifo_path = "/tmp/fifo_multi"
nombre = "Productor 2"  

with open(fifo_path, "w") as fifo:
    for i in range(5):
        fifo.write(f"{nombre} dice hola {i+1}\n")
        fifo.flush()
        time.sleep(1)