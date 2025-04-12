import os

def chat_bidireccional():
    r1, w1 = os.pipe()
    r2, w2 = os.pipe()

    pid = os.fork()

    if pid == 0:
        os.close(w1)
        os.close(r2)
        while True:
            msg = os.read(r1, 1024).decode()
            if msg == "exit":
                break
            print(f"Hijo recibió: {msg}")
            respuesta = input("Hijo responde: ")
            os.write(w2, respuesta.encode())
        os.close(r1)
        os.close(w2)
    else:
        os.close(r1)
        os.close(w2)
        while True:
            msg = input("Padre dice: ")
            os.write(w1, msg.encode())
            if msg == "exit":
                break
            resp = os.read(r2, 1024).decode()
            print(f"Padre recibió: {resp}")
        os.close(w1)
        os.close(r2)