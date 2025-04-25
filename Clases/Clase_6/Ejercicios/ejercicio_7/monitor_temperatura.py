import os
from datetime import datetime

fifo_path = "/tmp/fifo_temp"
log_file = "temperaturas.log"

if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

with open(fifo_path, "r") as fifo, open(log_file, "a") as log:
    for line in fifo:
        temp = float(line.strip())
        timestamp = datetime.now()
        log.write(f"[{timestamp}] Temp: {temp}\n")
        log.flush()
        if temp > 28:
            print(f"[ALERTA] Temperatura alta: {temp}°C")