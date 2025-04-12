import os
import random
import time

def generador(pipe_out):
    tipos = ['compra', 'venta']
    for _ in range(5):
        trans = f"{random.randint(1000, 9999)},{random.choice(tipos)},{random.randint(10, 1000)}"
        os.write(pipe_out, (trans + "\n").encode())
        time.sleep(0.5)
    os.close(pipe_out)

def validador(pipe_in, pipe_out):
    while True:
        data = os.read(pipe_in, 1024).decode()
        if not data:
            break
        for linea in data.strip().split('\n'):
            partes = linea.split(',')
            if len(partes) == 3 and partes[2].isdigit():
                os.write(pipe_out, (linea + "\n").encode())
    os.close(pipe_in)
    os.close(pipe_out)

def registrador(pipe_in):
    total = 0
    cantidad = 0
    while True:
        data = os.read(pipe_in, 1024).decode()
        if not data:
            break
        for linea in data.strip().split('\n'):
            _, tipo, monto = linea.split(',')
            total += int(monto)
            cantidad += 1
    print(f"Transacciones válidas: {cantidad}, Monto total: {total}")
    os.close(pipe_in)

def procesamiento_transacciones():
    r1, w1 = os.pipe()
    r2, w2 = os.pipe()

    if os.fork() == 0:
        os.close(r1)
        os.close(r2)
        os.close(w2)
        generador(w1)
        exit()

    if os.fork() == 0:
        os.close(w1)
        os.close(r2)
        validador(r1, w2)
        exit()

    os.close(w1)
    os.close(w2)
    os.close(r1)
    registrador(r2)