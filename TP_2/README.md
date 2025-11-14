# Sistema Distribuido de Scraping y Análisis Web Avanzado (TP2)

Este proyecto implementa un sistema distribuido y asíncrono en Python para la extracción, análisis y procesamiento de información de sitios web. La arquitectura es robusta, escalable y eficiente, utilizando concurrencia (`asyncio`) y paralelismo (`multiprocessing`).

## Arquitectura y Componentes Clave

El sistema opera en un modelo de dos servidores con comunicación transparente al cliente (Parte C):

| Componente | Archivo | Rol y Tecnologías Clave |
| :--- | :--- | :--- |
| **Servidor A (Asyncio)** | `server_scraping.py` | Extracción, API, Cola de Tareas, Caché, y Rate Limiting. Utiliza `aiohttp`, `async-lru`, `aiolimiter`. |
| **Servidor B (Procesamiento)** | `server_processing.py` | Ejecución paralela de operaciones intensivas (CPU-bound) como *screenshots*, análisis de rendimiento y procesamiento de imágenes. Utiliza `multiprocessing.Pool` y **Playwright**. |
| **Comunicación A <-> B** | `common/protocol.py` | IPC con Sockets TCP y serialización `pickle` (Protocolo: Longitud + Payload). |
| **Cliente de Prueba** | `client.py` | Interactúa con el Servidor A a través del sistema de cola (`/status`, `/result`). |

## ⚙️ 1. Configuración y Requisitos

### 1.1 Entorno

Asegúrate de tener Python 3.10+ y un entorno virtual (`venv`) activado.

### 1.2 Instalación de Dependencias

```bash
pip install -r requirements.txt
```

### 1.3 Instalación de Playwright (Motores de Navegador)

Playwright requiere la instalación de los navegadores binarios para tomar capturas:

```bash
playwright install
```

-----

##  2. Ejecución del Sistema

El sistema debe iniciarse en el siguiente orden, utilizando **tres terminales** separadas desde el directorio raíz (`TP_2`).

### Terminal 1: Iniciar Servidor B (Procesamiento)

```bash
python server_processing.py -i 127.0.0.1 -p 9001 -n 4
```

### Terminal 2: Iniciar Servidor A (Scraping y API)

```bash
python server_scraping.py -i 0.0.0.0 -p 8000 --proc-host 127.0.0.1 --proc-port 9001
```

### Terminal 3: Ejecutar Cliente de Prueba

Use **comillas simples** (`'`) para las URLs que contengan caracteres especiales (como paréntesis).

```bash
# Prueba 1: Cache MISS (Lenta)
python client.py 'https://en.wikipedia.org/wiki/Distributed_computing'

# Prueba 2: Cache HIT (Rápida)
python client.py 'https://en.wikipedia.org/wiki/Distributed_computing'
```

-----

## 🧪 3. Pruebas Unitarias

El proyecto incluye pruebas para los módulos principales utilizando **`pytest`**.

1. Asegúrese de tener `pytest` instalado (`pip install pytest pytest-asyncio`).
2. Ejecute las pruebas desde el directorio raíz, asegurando que Python pueda encontrar los paquetes:

```bash
export PYTHONPATH=$PWD
pytest tests/
```

-----
