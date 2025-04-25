import os
import time
from datetime import datetime

fifo_path = "/tmp/fifo_buffer"
if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

last = 0
with open(fifo_path, "r") as fifo:
    for line in fifo:
        num = int(line.strip())
        if last and num != last + 1:
            print(f"[SALTO] Faltó el número {last + 1}")
        print(f"[{datetime.now()}] Recibido: {num}")
        last = num