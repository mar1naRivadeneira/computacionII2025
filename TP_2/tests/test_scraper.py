
import pytest
import asyncio
from aiohttp import ClientSession
import json
from bs4 import BeautifulSoup
from scraper import fetch_url, parse_html, extract_metadata 

TEST_URL = "https://example.com" 

MOCK_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Title</title>
    <meta name="description" content="Test description">
    <meta property="og:title" content="Open Graph Test">
</head>
<body>
    <h1>Header 1 Content</h1>
    <h2>Header 2 Content</h2>
    <a href="/link1">Link 1</a>
    <img src="/image1.png">
    <img src="/image2.png">
</body>
</html>
"""

@pytest.mark.asyncio
async def test_fetch_url_success():
    """Verifica que fetch_url se conecta y obtiene datos."""
    async with ClientSession() as session:
        html = await fetch_url(session, TEST_URL, timeout=10)
        assert "Example Domain" in html
        assert isinstance(html, str)

@pytest.mark.asyncio
async def test_fetch_url_timeout():
    """Verifica el manejo de timeout (simulando un servidor muy lento)."""
    async with ClientSession() as session:
        slow_url = "http://httpbin.org/delay/5"
        with pytest.raises(TimeoutError): 
            await fetch_url(session, slow_url, timeout=2) 

def test_parse_html_and_extract_metadata():
    """Verifica que el parsing y la extracción devuelven la estructura correcta."""
    soup = parse_html(MOCK_HTML)
    data = extract_metadata(soup)
    
    assert data['title'] == "Test Title"
    assert 'links' in data and len(data['links']) == 1
    
    assert data['meta_tags']['description'] == "Test description"
    assert data['meta_tags']['og:title'] == "Open Graph Test"
    
    assert data['images_count'] == 2
    
    assert data['structure']['h1'] == 1
    assert data['structure']['h2'] == 1
    assert data['structure']['h3'] == 0