
import time
import random
from typing import Dict

def analyze_performance(url: str) -> Dict:
    """
    Simula el análisis de rendimiento de la página. (CPU-bound)
    """

    time.sleep(random.uniform(0.1, 0.5)) 
    
    performance_data = {
        "load_time_ms": random.randint(500, 5000),
        "total_size_kb": random.randint(500, 5500),
        "num_requests": random.randint(15, 150) 
    }
    
    return performance_data