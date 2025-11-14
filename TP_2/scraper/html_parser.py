
from bs4 import BeautifulSoup
from typing import Dict, List

def parse_html(html_content: str) -> BeautifulSoup:
    """Inicializa y devuelve el objeto BeautifulSoup usando 'lxml'."""
    return BeautifulSoup(html_content, 'lxml')