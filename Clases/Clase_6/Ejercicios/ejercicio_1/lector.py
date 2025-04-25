import os

fifo_path = "/tmp/test_fifo"
if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

print("Esperando datos...")
with open(fifo_path, "r") as fifo:
    for line in fifo:
        print(f"[LEÍDO] {line.strip()}")