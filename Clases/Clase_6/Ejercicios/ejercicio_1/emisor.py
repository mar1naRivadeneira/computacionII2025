import os
import time

fifo_path = "/tmp/test_fifo"
with open(fifo_path, "w") as fifo:
    for i in range(3):
        fifo.write(f"Mensaje {i+1}\n")
        fifo.flush()
        time.sleep(1)