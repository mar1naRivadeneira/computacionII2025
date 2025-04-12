import os

def contador_palabras(archivo):
    r1, w1 = os.pipe()
    r2, w2 = os.pipe()

    pid = os.fork()

    if pid == 0:
        os.close(w1)
        os.close(r2)
        while True:
            linea = os.read(r1, 1024).decode()
            if not linea:
                break
            count = str(len(linea.strip().split()))
            os.write(w2, count.encode())
        os.close(r1)
        os.close(w2)
    else:
        os.close(r1)
        os.close(w2)
        with open(archivo, 'r') as f:
            for linea in f:
                os.write(w1, linea.encode())
                resultado = os.read(r2, 1024).decode()
                print(f"Palabras: {resultado}")
        os.close(w1)
        os.close(r2)