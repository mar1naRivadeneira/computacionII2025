
from bs4 import BeautifulSoup
from typing import Dict, List

def extract_metadata(soup: BeautifulSoup) -> Dict:
    """
    Extrae el título, enlaces, meta tags relevantes, cantidad de imágenes 
    y estructura de headers (H1-H6).
    """
    data = {}
    
    data['title'] = soup.title.string.strip() if soup.title else "N/A"
    
    data['links'] = [a.get('href') for a in soup.find_all('a') if a.get('href')]
    
    meta_tags = {}
    for meta in soup.find_all('meta'):
        name = meta.get('name')
        if name in ['description', 'keywords']:
            meta_tags[name] = meta.get('content', '').strip()
            
        property_tag = meta.get('property')
        if property_tag and property_tag.startswith('og:'):
            meta_tags[property_tag] = meta.get('content', '').strip()
            
    data['meta_tags'] = meta_tags
    
    data['images_count'] = len(soup.find_all('img'))
    
    structure = {}
    for i in range(1, 7):
        header_tag = f'h{i}'
        structure[header_tag] = len(soup.find_all(header_tag))
    data['structure'] = structure
    
    return data