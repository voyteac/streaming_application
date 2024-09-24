import time
from datetime import datetime

class TimestampGenerator:
    def get_timestamp(self) -> float:
        timestamp = time.time()
        return timestamp

    def get_formatted_timestamp(self) -> str:
        timestamp: float = self.get_timestamp()
        current_time: str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return current_time
