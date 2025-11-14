
import base64
from playwright.sync_api import sync_playwright

def generate_screenshot(url: str, timeout_ms: int = 30000) -> str:
    """
    Genera un screenshot de TAMAÑO FIJO (800x600) usando Playwright 
    y devuelve la imagen PNG codificada en base64.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            
            context = browser.new_context(viewport={'width': 800, 'height': 600})
            page = context.new_page()
            
            page.goto(url, timeout=timeout_ms, wait_until='load')
            
            screenshot_bytes = page.screenshot(type="png") 
            
            browser.close()
            
            return base64.b64encode(screenshot_bytes).decode('utf-8')
            
    except Exception as e:
        raise RuntimeError(f"Error de screenshot con Playwright: {e}")