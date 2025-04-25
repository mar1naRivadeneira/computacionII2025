import os

fifo_path = "/tmp/fifo_log"

with open(fifo_path, "w") as fifo:
    while True:
        line = input("Mensaje: ")
        fifo.write(line + "\n")
        fifo.flush()
        if line.strip().lower() == "exit":
            break