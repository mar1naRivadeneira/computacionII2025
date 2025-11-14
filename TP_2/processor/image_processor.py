import base64
import requests
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Optional
import logging

MAX_THUMBNAILS = 5
THUMBNAIL_SIZE = (100, 100) 

def process_images(url: str, html_content: str) -> List[str]:
    """
    Extrae las imágenes del HTML, las descarga (requests) y genera thumbnails (Pillow).
    """
    logging.info(f"[Processor] Procesando imágenes de: {url}")
    
    try:
        soup = BeautifulSoup(html_content, 'lxml')
    except Exception as e:
        logging.error(f"Error [Images]: Fallo al parsear HTML: {e}")
        return []

    image_urls = []
    for img_tag in soup.find_all("img", src=True):
        src = img_tag['src']
        if src and not src.startswith('data:'):
            full_url = urljoin(url, src)
            image_urls.append(full_url)
    
    # Limita y asegura URLs únicas
    unique_urls = list(dict.fromkeys(image_urls))[:MAX_THUMBNAILS]
    
    thumbnails_b64 = []
    headers = {
        'User-Agent': 'TP2-Advanced-Scraper/1.0'
    }

    for img_url in unique_urls:
        thumb = _download_and_resize(img_url, headers)
        if thumb:
            thumbnails_b64.append(thumb)
            
    return thumbnails_b64

def _download_and_resize(img_url: str, headers: dict) -> Optional[str]:
    """
    Helper: Descarga la imagen (bloqueante), la redimensiona y devuelve base64.
    """
    try:
        response = requests.get(img_url, timeout=10, headers=headers, stream=True)
        response.raise_for_status()
        
        image_data = BytesIO(response.content)
        
        with Image.open(image_data) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            img.thumbnail(THUMBNAIL_SIZE)
            
            buffered = BytesIO()
            img.save(buffered, format="PNG") 
            
            return base64.b64encode(buffered.getvalue()).decode('utf-8')
            
    except requests.exceptions.RequestException as e:
        logging.warning(f"Error [Images]: Fallo al descargar {img_url}: {e}")
        return None
    except UnidentifiedImageError:
        logging.warning(f"Error [Images]: No se pudo identificar formato de imagen en {img_url}")
        return None
    except Exception as e:
        logging.error(f"Error [Images]: Fallo inesperado al procesar {img_url}: {e}")
        return None