import time
from datetime import datetime


def get_timestamp() -> float:
    timestamp = time.time()
    return timestamp


def get_formatted_timestamp() -> str:
    timestamp: float = get_timestamp()
    current_time: str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return current_time
