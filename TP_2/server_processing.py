
import socketserver
import multiprocessing
import argparse
import logging
import os
import time
import sys
from concurrent.futures import ProcessPoolExecutor

# --- Dependencias Internas ---
from common.protocol import deserialize_message, serialize_message, ProcessingTask
from processor import generate_screenshot, analyze_performance, process_images 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DEFAULT_PROCESSES = os.cpu_count()
PROCESS_POOL = None 

# --- Lógica de Procesamiento ---

def cpu_intensive_work(task: ProcessingTask):
    """
    Función que ejecuta todas las operaciones intensivas en el proceso worker.
    """
    logging.info(f"Proceso {os.getpid()} - Tarea {task.task_id[:8]}: Iniciando procesamiento para {task.url}")
    
    try:
        screenshot_base64 = generate_screenshot(task.url) 
        
        performance_data = analyze_performance(task.url)
        
        thumbnails_base64 = process_images(task.url, task.html_content) 
        
        processing_data = {
            "screenshot": screenshot_base64,
            "performance": performance_data,
            "thumbnails": thumbnails_base64
        }
        
        logging.info(f"Proceso {os.getpid()} - Tarea {task.task_id[:8]}: Procesamiento completado.")
        return processing_data

    except Exception as e:
        logging.error(f"Proceso {os.getpid()} - Tarea {task.task_id[:8]}: Error en el procesamiento intensivo: {e}")
        return {"status": "failed", "error": str(e)}

# --- Servidor de Sockets (Manejo de I/O) ---

class ProcessingTCPHandler(socketserver.BaseRequestHandler):
    """
    Maneja las conexiones TCP entrantes (I/O) y delega el trabajo (CPU) al Pool.
    """
    
    def handle(self):
        global PROCESS_POOL
        if PROCESS_POOL is None:
            logging.error("Pool de procesos no inicializado.")
            return

        try:
            header = self.request.recv(8)
            if len(header) < 8:
                return 
            message_len = int.from_bytes(header, byteorder='big')
            
            full_message = self.request.recv(message_len, socketserver.socket.MSG_WAITALL)

            task_data = deserialize_message(full_message)
            
            if not isinstance(task_data, ProcessingTask):
                 raise TypeError("Mensaje recibido no es un objeto ProcessingTask.")
            
            task = task_data
            logging.info(f"Recibida tarea {task.task_id[:8]} de Servidor A. Enviando a Pool...")

            result = PROCESS_POOL.apply(cpu_intensive_work, (task,))

            response = serialize_message(result)
            self.request.sendall(response)
            
        except Exception as e:
            logging.error(f"Error al manejar la conexión/serialización con Servidor A: {e}")
            error_response = serialize_message({"status": "failed", "error": f"Error de protocolo en Servidor B: {e}"})
            try:
                self.request.sendall(error_response)
            except:
                pass

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Combina Threading (para manejar múltiples conexiones I/O) con el servidor TCP."""
    allow_reuse_address = False

def main():
    global PROCESS_POOL
    parser = argparse.ArgumentParser(description="Servidor de Procesamiento Distribuido")
    parser.add_argument('-i', '--ip', required=True, help="Dirección de escucha")
    parser.add_argument('-p', '--port', type=int, required=True, help="Puerto de escucha")
    parser.add_argument('-n', '--processes', type=int, default=DEFAULT_PROCESSES, 
                        help=f"Número de procesos en el pool (default: {DEFAULT_PROCESSES})")

    args = parser.parse_args()

    PROCESS_POOL = multiprocessing.Pool(args.processes)
    
    try:
        logging.info(f"Iniciando servidor de procesamiento en {args.ip}:{args.port} con {args.processes} procesos...")
        with ThreadedTCPServer((args.ip, args.port), ProcessingTCPHandler) as server:
            server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Servidor detenido por el usuario.")
    except Exception as e:
        logging.error(f"Fallo grave del servidor de procesamiento: {e}")
        
    finally:
        if PROCESS_POOL:
            PROCESS_POOL.close()
            PROCESS_POOL.join()
            logging.info("Pool de procesos cerrado y liberado.")

if __name__ == '__main__':
    main()