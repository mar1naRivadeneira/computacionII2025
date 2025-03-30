import os

def encontrar_zombis():
    for pid in os.listdir("/proc"):
        if pid.isdigit():
            try:
                with open(f"/proc/{pid}/status") as f:
                    for line in f:
                        if line.startswith("State:"):
                            if "Z" in line:
                                print(f"Proceso zombi detectado: PID {pid}")
                            break
            except FileNotFoundError:
                pass  

encontrar_zombis()