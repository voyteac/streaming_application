import time
from datetime import datetime

class RealTimestampGenerator:
    def get_timestamp(self) -> float:
        timestamp = time.time()
        return timestamp

    def get_formatted_timestamp(self) -> str:
        timestamp: float = self.get_timestamp()
        return self.format_given_timestamp(timestamp)

    def format_given_timestamp(self, timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def get_date_component_from_timestamp(self, timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

    def get_time_component_from_timestamp(self, timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
