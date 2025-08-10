import json
import hashlib
import os

# genera el hash de un bloque usando los datos, el hash previo y el timestamp
def calcular_hash(prev_hash, datos, timestamp):
    bloque_str = json.dumps(datos, sort_keys=True) + prev_hash + timestamp
    return hashlib.sha256(bloque_str.encode()).hexdigest()

# Verifica si existe el archivo con la blockchain
def verificar_cadena():
    if not os.path.exists("blockchain.json"):
        print("No se encontró blockchain.json")
        return

    with open("blockchain.json", "r") as f:
        blockchain = json.load(f)
    
    # Inicializa contadores
    corruptos = 0
    alertas = 0
    freq_total = 0
    pres_total = 0
    oxi_total = 0

    for i, bloque in enumerate(blockchain):
        datos = bloque["datos"]
        timestamp = bloque["timestamp"]
        prev_hash = "0" * 64 if i == 0 else blockchain[i - 1]["hash"]

        #verifica la integridad del hash
        esperado = calcular_hash(prev_hash, datos, timestamp)
        if bloque["hash"] != esperado:
            corruptos += 1

        if bloque["alerta"]:
            alertas += 1

        freq_total += datos["frecuencia"]["media"]
        pres_total += datos["presion"]["media"]
        oxi_total += datos["oxigeno"]["media"]

    total = len(blockchain)
    
    # Genera un reporte con estadísticas
    reporte = (
        " Reporte de Verificación de Blockchain Biométrica\n"
        "===============================================\n"
        f"{'Cantidad total de bloques:':30} {total}\n"
        f"{'Bloques con alertas:':30} {alertas}\n"
        f"{'Bloques corruptos:':30} {corruptos}\n"
        "\n"
        f"{'Promedio frecuencia cardíaca:':30} {round(freq_total / total, 2)} bpm\n"
        f"{'Promedio presión sistólica:':30} {round(pres_total / total, 2)} mmHg\n"
        f"{'Promedio saturación de oxígeno:':30} {round(oxi_total / total, 2)} %\n"
        "===============================================\n"
    )

    with open("reporte.txt", "w") as f:
        f.write(reporte)

    print("Verificación completada.\n")
    print(reporte)

#ejecuta la verificaciion
if __name__ == "__main__":
    verificar_cadena()