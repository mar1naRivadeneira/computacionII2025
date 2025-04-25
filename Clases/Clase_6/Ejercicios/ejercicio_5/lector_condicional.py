import os
import time
import errno

fifo_path = "/tmp/fifo_condicional"
if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

for intento in range(5):
    try:
        fd = os.open(fifo_path, os.O_RDONLY | os.O_NONBLOCK)
        with os.fdopen(fd, 'r') as fifo:
            for line in fifo:
                print(f"[LEÍDO] {line.strip()}")
        break
    except OSError as e:
        if e.errno == errno.ENXIO:
            print(f"[INTENTO {intento+1}] No hay escritor. Reintentando...")
            time.sleep(1)
        else:
            raise
else:
    print("No se pudo abrir el FIFO tras varios intentos.")