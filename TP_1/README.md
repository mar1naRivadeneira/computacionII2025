# Sistema Concurrente de Análisis Biométrico con Blockchain Local

Este sistema simula una prueba de esfuerzo biométrica en tiempo real, analiza los datos en paralelo y los registra en una blockchain local si son válidos.

## Tecnologías utilizadas

- Python 3
- multiprocessing
- json, hashlib, random, statistics

## Arquitectura del sistema

El sistema se compone de procesos concurrentes:

- *Generador*: simula señales biométricas por segundo
- *Analizadores (3 procesos)*: procesan cada tipo de señal (frecuencia cardíaca, presión arterial y saturación de oxígeno)
- *Verificador*: valida los datos y genera un bloque con su hash correspondiente
- *Blockchain*: almacena cada bloque encadenado en un archivo local (blockchain.json)

## Ejecución

Desde la terminal, ejecuta el siguiente comando:

```bash
python3 main.py
```
Esto iniciará la simulación durante 60 segundos. Los bloques se mostrarán por consola y se guardarán automáticamente.

Para verificar la integridad de la blockchain y generar un reporte con los datos biométricos:

```bash
python3 verificar_cadena.py
```

## Archivos generados

- blockchain.json: contiene los bloques generados, con sus datos y hashes.
- reporte.txt: resumen de los bloques generados.

