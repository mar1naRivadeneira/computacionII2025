import os

def servidor_operaciones():
    r1, w1 = os.pipe()
    r2, w2 = os.pipe()

    pid = os.fork()
    if pid == 0:
        os.close(w1)
        os.close(r2)
        while True:
            expr = os.read(r1, 1024).decode()
            if expr == "exit":
                break
            try:
                resultado = str(eval(expr))
            except:
                resultado = "Error"
            os.write(w2, resultado.encode())
        os.close(r1)
        os.close(w2)
    else:
        os.close(r1)
        os.close(w2)
        while True:
            operacion = input("Ingresa operación: ")
            os.write(w1, operacion.encode())
            if operacion == "exit":
                break
            res = os.read(r2, 1024).decode()
            print(f"Resultado: {res}")
        os.close(w1)
        os.close(r2)