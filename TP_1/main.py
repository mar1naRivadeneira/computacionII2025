import multiprocessing
import time
import random
import hashlib
import json
from datetime import datetime
import statistics
import os

# ---------- Función para generar una muestra biométrica ----------
def generar_muestra():
    # 15% de probabilidad de generar datos fuera de rango para pruebas
    if random.random() < 0.15:
        return {
            "timestamp": datetime.now().isoformat(),
            "frecuencia": random.randint(180, 220),  # puede superar 200
            "presion": [random.randint(180, 220), random.randint(70, 110)],  # sistólica puede superar 200
            "oxigeno": random.randint(85, 105)  # puede estar fuera de 90-100
        }
    # Resto del tiempo datos normales
    return {
        "timestamp": datetime.now().isoformat(),
        "frecuencia": random.randint(60, 180),
        "presion": [random.randint(110, 180), random.randint(70, 110)],
        "oxigeno": random.randint(90, 100)
    }

# ---------- Cálculo del hash para encadenar bloques ----------
def calcular_hash(prev_hash, datos, timestamp):
    bloque_str = json.dumps(datos, sort_keys=True) + prev_hash + timestamp
    return hashlib.sha256(bloque_str.encode()).hexdigest()

# ---------- Proceso de análisis de señales ----------
def analizador(tipo, pipe, queue):
    ventana = []  

    while True:
        dato = pipe.recv()
        if dato is None:
            break  # Señal de finalización

        # Extraer el valor según el tipo de señal
        if tipo == "frecuencia":
            valor = dato["frecuencia"]
        elif tipo == "presion":
            valor = dato["presion"][0]  # Solo sistólica
        elif tipo == "oxigeno":
            valor = dato["oxigeno"]

        ventana.append((dato["timestamp"], valor))

        if len(ventana) > 30:
            ventana.pop(0)

        # Calcular estadísticas
        valores = [v for _, v in ventana]
        media = statistics.mean(valores)
        desv = statistics.stdev(valores) if len(valores) > 1 else 0.0

        # Enviar resultado al verificador
        queue.put({
            "tipo": tipo,
            "timestamp": dato["timestamp"],
            "media": round(media, 2),
            "desv": round(desv, 2)
        })

# ---------- Proceso verificador y constructor de bloques ----------
def verificador(queue_a, queue_b, queue_c):
    blockchain = []
    prev_hash = "0" * 64  
    contador = 1
    buffer_resultados = {}  # Guarda resultados hasta tener las 3 métricas por timestamp

    while contador <= 60:
        # Recibe un resultado de cualquiera de las colas
        for queue in (queue_a, queue_b, queue_c):
            res = queue.get()
            ts = res["timestamp"]

            if ts not in buffer_resultados:
                buffer_resultados[ts] = {}

            buffer_resultados[ts][res["tipo"]] = {
                "media": res["media"],
                "desv": res["desv"]
            }

            # Si ya tenemos las 3 métricas para este timestamp, creamos bloque
            if len(buffer_resultados[ts]) == 3:
                datos = {
                    "frecuencia": buffer_resultados[ts]["frecuencia"],
                    "presion": buffer_resultados[ts]["presion"],
                    "oxigeno": buffer_resultados[ts]["oxigeno"]
                }

                # Verificar condiciones de alerta
                motivos_alerta = []
                if datos["frecuencia"]["media"] >= 200:
                    motivos_alerta.append("frecuencia")
                if not (90 <= datos["oxigeno"]["media"] <= 100):
                    motivos_alerta.append("oxígeno")
                if datos["presion"]["media"] >= 200:
                    motivos_alerta.append("presión")

                alerta = len(motivos_alerta) > 0

                bloque = {
                    "timestamp": ts,
                    "datos": datos,
                    "alerta": alerta,
                    "prev_hash": prev_hash
                }
               
                bloque["hash"] = calcular_hash(prev_hash, datos, ts)
                prev_hash = bloque["hash"]
                blockchain.append(bloque)

                if alerta:
                    print(f"[Bloque {contador}] Hash: {bloque['hash'][:8]}... | Alerta: {', '.join(motivos_alerta)} fuera de rango")
                else:
                    print(f"[Bloque {contador}] Hash: {bloque['hash'][:8]}... | Alerta: false")

                contador += 1
                buffer_resultados.pop(ts)  # Eliminamos del buffer
                break  # Volvemos al while para esperar el siguiente bloque

    with open("blockchain.json", "w") as f:
        json.dump(blockchain, f, indent=2)

# ---------- Proceso Principal ----------
if __name__ == "__main__":
    # Crea pipes para enviar datos a cada analizador
    parent_a, child_a = multiprocessing.Pipe()
    parent_b, child_b = multiprocessing.Pipe()
    parent_c, child_c = multiprocessing.Pipe()

    # Crea queues para recibir resultados de los analizadores
    queue_a = multiprocessing.Queue()
    queue_b = multiprocessing.Queue()
    queue_c = multiprocessing.Queue()

    # Crear procesos para los analizadores
    procA = multiprocessing.Process(target=analizador, args=("frecuencia", child_a, queue_a))
    procB = multiprocessing.Process(target=analizador, args=("presion", child_b, queue_b))
    procC = multiprocessing.Process(target=analizador, args=("oxigeno", child_c, queue_c))

    verif = multiprocessing.Process(target=verificador, args=(queue_a, queue_b, queue_c))

    # Inicia todos los procesos
    procA.start()
    procB.start()
    procC.start()
    verif.start()

    for _ in range(60):
        muestra = generar_muestra()
        parent_a.send(muestra)
        parent_b.send(muestra)
        parent_c.send(muestra)
        time.sleep(1)

    # Señal de finalización a los analizadores
    parent_a.send(None)
    parent_b.send(None)
    parent_c.send(None)

    # Espera que todos los procesos terminen
    procA.join()
    procB.join()
    procC.join()
    verif.join()