
import pickle
from typing import Any

class ProcessingTask:
    """
    Estructura de datos que encapsula la información enviada del 
    Servidor A (Scraping) al Servidor B (Procesamiento).
    """
    def __init__(self, task_id: str, url: str, html_content: str):
        self.task_id = task_id
        self.url = url
        self.html_content = html_content  
    
    def __repr__(self):
        return f"ProcessingTask(id={self.task_id[:8]}, url={self.url})"


def serialize_message(data: Any) -> bytes:
    """
    Serializa los datos usando pickle y añade un encabezado de 8 bytes 
    con la longitud del mensaje.
    Protocolo: [8 bytes de longitud (big-endian)] [Payload pickle]
    """
    try:
        payload = pickle.dumps(data)
        header = len(payload).to_bytes(8, byteorder='big')
        return header + payload
    except Exception as e:
        raise RuntimeError(f"Error al serializar el mensaje con pickle: {e}")


def deserialize_message(data: bytes) -> Any:
    """
    Deserializa los datos binarios recibidos.
    """
    try:
        return pickle.loads(data)
    except pickle.UnpicklingError as e:
        raise ValueError(f"Error al deserializar el mensaje (Pickle): {e}")
    except Exception as e:
        raise RuntimeError(f"Error desconocido al deserializar: {e}")