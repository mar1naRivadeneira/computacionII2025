import os

def simulador_shell(cmd1, cmd2):
    r, w = os.pipe()
    pid = os.fork()

    if pid == 0:
        os.dup2(w, 1)  # Redirige stdout al pipe
        os.close(r)
        os.execvp(cmd1[0], cmd1)
    else:
        pid2 = os.fork()
        if pid2 == 0:
            os.dup2(r, 0)  # Redirige stdin al pipe
            os.close(w)
            os.execvp(cmd2[0], cmd2)
        else:
            os.close(r)
            os.close(w)
            os.wait()
            os.wait()