
import asyncio
import argparse
import logging
import uuid
import json
from datetime import datetime, timezone
from urllib.parse import urlparse

from aiohttp import web, ClientTimeout, ClientSession
from async_lru import alru_cache
from aiolimiter import AsyncLimiter 

from common.protocol import serialize_message, deserialize_message, ProcessingTask 
from scraper import fetch_url, parse_html, extract_metadata 

PROCESSING_SERVER_IP = '127.0.0.1' 
PROCESSING_SERVER_PORT = 9001 
SCRAPING_TIMEOUT = 30 
CACHE_TTL = 3600 
CACHE_MAX_SIZE = 512
RATE_LIMIT_PER_MINUTE = 5 
RATE_LIMIT_INTERVAL = 60 

TASK_STORE = {} 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def setup_background_tasks(app: web.Application):
    """Función de 'startup' para crear la ClientSession y el Rate Limiter."""
    app['http_session'] = ClientSession(
        timeout=ClientTimeout(total=SCRAPING_TIMEOUT),
        headers={'User-Agent': 'TP2-Advanced-Scraper/1.0'}
    )
    app['domain_limiters'] = {}
    
async def cleanup_background_tasks(app: web.Application):
    """Función de 'cleanup' para cerrar la ClientSession."""
    await app['http_session'].close()
    
def get_domain_limiter(app: web.Application, url: str) -> AsyncLimiter:
    """Obtiene o crea un Rate Limiter para el dominio de la URL."""
    try:
        domain = urlparse(url).netloc
    except Exception:
        domain = "default"

    if domain not in app['domain_limiters']:
        logging.info(f"[RateLimit] Creando nuevo limiter para dominio: {domain}")
        app['domain_limiters'][domain] = AsyncLimiter(
            RATE_LIMIT_PER_MINUTE, RATE_LIMIT_INTERVAL
        )
    return app['domain_limiters'][domain]


@alru_cache(maxsize=CACHE_MAX_SIZE, ttl=CACHE_TTL)
async def perform_full_analysis(app: web.Application, url: str) -> dict:
    """
    Función de trabajo central cacheada. Implementa el Rate Limiting.
    """
    logging.info(f"[Cache] MISS para {url}. Ejecutando análisis completo.")

    limiter = get_domain_limiter(app, url)
    
    await limiter.acquire()
    logging.info(f"[RateLimit] Permiso adquirido para {url}.")
    
    html_content = await fetch_url(app['http_session'], url, timeout=SCRAPING_TIMEOUT) 
    
    if not html_content:
        raise Exception("HTML content is empty.")
        
    soup = parse_html(html_content)
    scraping_data = extract_metadata(soup)
    
    processing_task = ProcessingTask(str(uuid.uuid4()), url, html_content) 
    
    processing_result = await connect_to_processor(processing_task)

    if processing_result.get("status") == "failed":
         raise Exception(f"Fallo reportado por Servidor B: {processing_result.get('error')}")

    full_result = {
        "url": url,
        "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "scraping_data": scraping_data,
        "processing_data": processing_result,
        "status": "success"
    }
    
    return full_result


async def connect_to_processor(data):
    """Establece conexión asíncrona con el Servidor B y maneja protocolo."""
    try:
        proc_host = PROCESSING_SERVER_IP
        proc_port = PROCESSING_SERVER_PORT
        
        reader, writer = await asyncio.open_connection(proc_host, proc_port)
        
        message = serialize_message(data)
        writer.write(message)
        await writer.drain()
        
        header = await asyncio.wait_for(reader.readexactly(8), timeout=10)
        message_len = int.from_bytes(header, byteorder='big')
        
        response_data = await asyncio.wait_for(reader.readexactly(message_len), timeout=300) 
        
        writer.close()
        await writer.wait_closed()
        
        return deserialize_message(response_data)
        
    except Exception as e:
        logging.error(f"Error en la comunicación con Servidor B: {e}")
        return {"error": f"Error de comunicación/protocolo con Servidor B: {e}", "status": "failed"}

async def process_task_and_store(task_id, url, app):
    """Tarea de fondo que realiza la lógica de análisis y guarda el resultado (Bonus 1)."""
    TASK_STORE[task_id]["status"] = "scraping"
    
    try:
        result = await perform_full_analysis(app, url)
        
        TASK_STORE[task_id]["result"] = result
        TASK_STORE[task_id]["status"] = "completed"
        is_cached = 'MISS' if perform_full_analysis.cache_info().misses > perform_full_analysis.cache_info().hits else 'HIT'
        logging.info(f"Tarea {task_id} para {url} completada ({is_cached}).")
        
    except Exception as e:
        error_result = {
            "url": url,
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "status": "failed",
            "error": str(e)
        }
        TASK_STORE[task_id]["result"] = error_result
        TASK_STORE[task_id]["status"] = "failed"
        logging.error(f"Tarea {task_id} falló en el análisis/procesamiento: {e}")


async def handle_scrape_request(request):
    """Handler principal (POST /scrape). Inicia la tarea y devuelve ID (Bonus 1)."""
    try:
        data = await request.json()
        url = data.get('url')
    except Exception:
        return web.json_response({"status": "error", "message": "JSON inválido."}, status=400)
        
    if not url:
        return web.json_response({"status": "error", "message": "Parámetro 'url' requerido."}, status=400)

    task_id = str(uuid.uuid4())
    TASK_STORE[task_id] = {"status": "pending", "result": None, "url": url, "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')}

    asyncio.create_task(process_task_and_store(task_id, url, request.app))

    return web.json_response({"status": "accepted", "task_id": task_id, "message": "Procesamiento iniciado."}, status=202)


async def handle_status(request):
    """Consulta el estado de una tarea por ID (Bonus Track 1)."""
    task_id = request.match_info.get('task_id')
    task_info = TASK_STORE.get(task_id)
    if not task_info:
        return web.json_response({"status": "error", "message": "Task ID no encontrado."}, status=404)
    
    status_response = {
        "task_id": task_id,
        "status": task_info["status"],
        "timestamp": task_info["timestamp"],
        "url": task_info["url"],
        "cache_info": perform_full_analysis.cache_info()._asdict() 
    }
    return web.json_response(status_response)

async def handle_result(request):
    """Devuelve el resultado final de una tarea completada (Bonus Track 1)."""
    task_id = request.match_info.get('task_id')
    task_info = TASK_STORE.get(task_id)
    if not task_info:
        return web.json_response({"status": "error", "message": "Task ID no encontrado."}, status=404)
    
    status = task_info["status"]
    if status != "completed" and status != "failed":
        return web.json_response({"status": status, "message": f"Tarea en estado: {status}"}, status=202)
    
    return web.json_response(task_info["result"])


def main():
    global PROCESSING_SERVER_IP, PROCESSING_SERVER_PORT

    parser = argparse.ArgumentParser(description="Servidor de Scraping Web Asíncrono Avanzado")
    parser.add_argument('-i', '--ip', required=True, help="Dirección de escucha (soporta IPv4/IPv6)")
    parser.add_argument('-p', '--port', type=int, required=True, help="Puerto de escucha")
    parser.add_argument('-w', '--workers', type=int, default=10, help="Número de workers (default: 10)") # Workers de aiohttp
    parser.add_argument('--proc-host', type=str, default=PROCESSING_SERVER_IP, help="Host del Servidor de Procesamiento (Parte B)")
    parser.add_argument('--proc-port', type=int, default=PROCESSING_SERVER_PORT, help="Puerto del Servidor de Procesamiento (Parte B)")
    
    args = parser.parse_args()

    PROCESSING_SERVER_IP = args.proc_host
    PROCESSING_SERVER_PORT = args.proc_port

    app = web.Application()
    app['scraper_semaphore'] = asyncio.Semaphore(args.workers)
    
    app.router.add_post('/scrape', handle_scrape_request) 
    app.router.add_get('/status/{task_id}', handle_status)
    app.router.add_get('/result/{task_id}', handle_result)

    app.on_startup.append(setup_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    
    web.run_app(app, host=args.ip, port=args.port)

if __name__ == '__main__':
    main()