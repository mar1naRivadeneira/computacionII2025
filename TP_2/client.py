
import aiohttp
import asyncio
import argparse
import time
import json
import sys

SERVER_URL = "http://127.0.0.1:8000" 
DELAY = 3 

def make_output_readable(result: dict) -> dict:
    """Recorta las cadenas Base64 largas y listas extensas para legibilidad en consola."""
    MAX_LENGTH_B64 = 50 
    MAX_LINKS_TO_SHOW = 10 

    readable_result = result.copy()
    
    if readable_result.get('scraping_data', {}).get('links'):
        original_links = readable_result['scraping_data']['links']
        original_count = len(original_links)
        
        if original_count > MAX_LINKS_TO_SHOW:
            readable_result['scraping_data']['links'] = (
                original_links[:MAX_LINKS_TO_SHOW] + 
                [f"... ({original_count - MAX_LINKS_TO_SHOW} enlaces omitidos) ..."]
            )
        
    processing_data = readable_result.get('processing_data', {})

    if processing_data.get('screenshot'):
        original_len = len(processing_data['screenshot'])
        processing_data['screenshot'] = (
            processing_data['screenshot'][:MAX_LENGTH_B64] + 
            f"... [Recortado: {original_len - MAX_LENGTH_B64} chars] ..."
        )
    
    if processing_data.get('thumbnails'):
        new_thumbs = []
        for thumb in processing_data['thumbnails']:
            original_len = len(thumb)
            new_thumbs.append(
                thumb[:MAX_LENGTH_B64] + 
                f"... [Recortado: {original_len - MAX_LENGTH_B64} chars] ..."
            )
        processing_data['thumbnails'] = new_thumbs
        
    readable_result['processing_data'] = processing_data
    return readable_result

async def request_scrape_job(session: aiohttp.ClientSession, url: str) -> str:
    """Solicita un nuevo trabajo de scraping usando POST y devuelve el task_id."""
    print(f"-> Solicitando scraping para: {url}")
    
    async with session.post(f"{SERVER_URL}/scrape", json={"url": url}) as response:
        data = await response.json()
        if response.status == 202 and 'task_id' in data:
            print(f"<- Tarea aceptada. Task ID: {data['task_id']}")
            return data['task_id']
        else:
            print(f"Error al solicitar tarea (HTTP {response.status}): {data.get('message', 'Desconocido')}")
            return None

async def check_status(session: aiohttp.ClientSession, task_id: str):
    """Consulta el estado de una tarea por ID, mostrando info de caché."""
    async with session.get(f"{SERVER_URL}/status/{task_id}") as response:
        data = await response.json()
        status = data.get('status', 'failed')
        cache_info = data.get('cache_info', {})
        hits = cache_info.get('hits', '-')
        misses = cache_info.get('misses', '-')
        
        print(f"   [Task {task_id[:8]}] Estado: {status} | Cache H/M: {hits}/{misses}")
        return status

async def get_result(session: aiohttp.ClientSession, task_id: str) -> dict:
    """Obtiene el resultado final de una tarea completada o fallida."""
    async with session.get(f"{SERVER_URL}/result/{task_id}") as response:
        data = await response.json()
        if response.status == 200:
            return data
        else:
            print(f"Error al obtener resultado: {data.get('message', 'Resultado no disponible')}")
            return None

async def main_client(url: str, max_attempts: int = 30):
    """Bucle principal del cliente para solicitar y seguir una tarea."""
    async with aiohttp.ClientSession() as session:
        
        task_id = await request_scrape_job(session, url)
        if not task_id:
            return

        attempts = 0
        status = 'pending'
        while status not in ('completed', 'failed') and attempts < max_attempts:
            await asyncio.sleep(DELAY)
            status = await check_status(session, task_id)
            attempts += 1
        
        if status in ('completed', 'failed'):
            print("\n Tarea COMPLETADA (o fallida). Obteniendo resultado final...")
            result = await get_result(session, task_id)
            if result:
                readable_result = make_output_readable(result) 
                print(json.dumps(readable_result, indent=2))
        else:
            print("\n Se excedió el número máximo de intentos. La tarea aún está en curso o falló.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Cliente de Prueba para el Sistema de Scraping Asíncrono Avanzado")
    parser.add_argument('url', type=str, help="URL a ser scrapeada (ej: https://www.google.com). Use comillas si la URL contiene caracteres especiales como '()'.")
    
    args = parser.parse_args()
    
    try:
        asyncio.run(main_client(args.url))
    except KeyboardInterrupt:
        print("\nCliente detenido.")
    except Exception as e:
        print(f"Error fatal del cliente: {e}")