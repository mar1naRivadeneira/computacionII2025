import os
import threading
from datetime import datetime

fifo_out = "/tmp/chat_b"
fifo_in = "/tmp/chat_a"
nombre = "B"

for path in [fifo_out, fifo_in]:
    if not os.path.exists(path):
        os.mkfifo(path)

def recibir():
    with open(fifo_in, "r") as fifo:
        for line in fifo:
            print(f"[{datetime.now()}] Usuario B: {line.strip()}")

def enviar():
    with open(fifo_out, "w") as fifo:
        while True:
            msg = input()
            if msg.strip() == "/exit":
                break
            fifo.write(msg + "\n")
            fifo.flush()

threading.Thread(target=recibir, daemon=True).start()
enviar()