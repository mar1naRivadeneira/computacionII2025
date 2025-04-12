import os
import random

def pipeline_filtrado():
    r1, w1 = os.pipe()
    r2, w2 = os.pipe()

    pid1 = os.fork()
    if pid1 == 0:  # Proceso 1: generador
        os.close(r1)
        for _ in range(10):
            num = random.randint(1, 100)
            os.write(w1, f"{num}\n".encode())
        os.close(w1)
        exit()

    pid2 = os.fork()
    if pid2 == 0:  # Proceso 2: filtro pares
        os.close(w1)
        os.close(r2)
        while True:
            data = os.read(r1, 1024).decode()
            if not data:
                break
            for linea in data.strip().split('\n'):
                num = int(linea)
                if num % 2 == 0:
                    os.write(w2, f"{num}\n".encode())
        os.close(r1)
        os.close(w2)
        exit()

    os.close(w1)
    os.close(r1)
    os.close(w2)
    while True:
        data = os.read(r2, 1024).decode()
        if not data:
            break
        for linea in data.strip().split('\n'):
            num = int(linea)
            print(f"Cuadrado de {num}: {num ** 2}")
    os.close(r2)
