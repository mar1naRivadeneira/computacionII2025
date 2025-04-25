import os

fifo_path = "/tmp/fifo_log"
output_file = "output.txt"

if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

with open(fifo_path, "r") as fifo, open(output_file, "w") as log:
    for line in fifo:
        if line.strip().lower() == "exit":
            break
        log.write(line)
        log.flush()

print("Logger cerrado.")