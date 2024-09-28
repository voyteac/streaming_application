from typing import Tuple

bootstrap_servers: str = 'localhost:9092'
producer_api_version: Tuple[int, int, int] = (0, 10, 1)
consumer_api_version: Tuple[int, int, int] = (0, 10, 1)

odd_client_id_topic_name: str = 'odd_client_id_topic'
even_client_id_topic_name: str = 'even_client_id_topic'
