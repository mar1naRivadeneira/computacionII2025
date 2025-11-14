
import pytest
import base64
import os
import io
from PIL import Image

from processor import generate_screenshot, analyze_performance, process_images
from common.protocol import ProcessingTask

TEST_URL = "https://example.com"

MOCK_HTML = f"""
<html><body>
<img src="{TEST_URL}/mock_image.png">
</body></html>
"""

def test_generate_screenshot_returns_base64():
    """Verifica que Playwright toma la captura y devuelve base64."""
    
    try:
        b64_image = generate_screenshot(TEST_URL)
        
        assert isinstance(b64_image, str)
        assert len(b64_image) > 1000 
        
        decoded = base64.b64decode(b64_image)
        assert decoded.startswith(b'\x89PNG')
        
    except Exception as e:
        pytest.fail(f"Fallo en la prueba de screenshot (¿Playwright no instalado?): {e}")


def test_analyze_performance_structure():
    """Verifica que la función de rendimiento devuelve la estructura requerida."""
    data = analyze_performance(TEST_URL)
    
    assert 'load_time_ms' in data
    assert 'total_size_kb' in data
    assert 'num_requests' in data
    assert isinstance(data['load_time_ms'], int)
    assert data['load_time_ms'] > 0 

def test_process_images_returns_list():
    """Verifica que la lógica de thumbnails se ejecuta y devuelve una lista de strings."""    
    thumbnails = process_images(TEST_URL, MOCK_HTML)

    assert isinstance(thumbnails, list)

    if thumbnails:
        assert isinstance(thumbnails[0], str)
        assert len(thumbnails[0]) > 50