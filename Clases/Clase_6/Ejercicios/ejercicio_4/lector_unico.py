import os

fifo_path = "/tmp/fifo_multi"
if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

with open(fifo_path, "r") as fifo:
    for line in fifo:
        print(f"[RECEBIDO] {line.strip()}")