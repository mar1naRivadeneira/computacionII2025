
import aiohttp
from aiohttp import ClientSession, ClientTimeout
import logging
import asyncio 

async def fetch_url(session: ClientSession, url: str, timeout: int = 30) -> str:
    """
    Realiza una petición GET asíncrona usando una sesión compartida.
    """
    timeout_obj = ClientTimeout(total=timeout)
    logging.info(f"Fetching URL: {url}")
    
    try:
        async with session.get(url, allow_redirects=True, timeout=timeout_obj) as response:
            response.raise_for_status() 
            html_content = await response.text()
            return html_content

    except aiohttp.ClientConnectorError as e:
        raise ConnectionError(f"Error de conexión: {e}")
    except aiohttp.ClientResponseError as e:
        raise RuntimeError(f"Error HTTP {e.status}: {e.message} para {url}")
    
    except asyncio.TimeoutError as e:
        raise TimeoutError(f"Timeout (>{timeout}s) al cargar la URL: {url}")
    
    except Exception as e:
        raise Exception(f"Error desconocido al scrapear: {e}")