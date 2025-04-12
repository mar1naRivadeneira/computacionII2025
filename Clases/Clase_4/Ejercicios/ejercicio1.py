import os

def eco_simple():
    r1, w1 = os.pipe()
    r2, w2 = os.pipe()

    pid = os.fork()

    if pid == 0:
        os.close(w1)
        os.close(r2)
        msg = os.read(r1, 1024).decode()
        os.write(w2, msg.encode())
        os.close(r1)
        os.close(w2)
    else:
        os.close(r1)
        os.close(w2)
        mensaje = "Hola desde el padre"
        os.write(w1, mensaje.encode())
        respuesta = os.read(r2, 1024).decode()
        print(f"Padre recibió: {respuesta}")
        os.close(w1)
        os.close(r2)