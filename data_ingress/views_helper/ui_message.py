def get_streaming_message(status: str) -> str:
    return 'Streaming is ongoing!' if status == 'started' else 'Streaming is NOT started!'


def get_kafka_message(is_kafka_running: bool) -> str:
    return 'Kafka container is NOT running!' if is_kafka_running == False else 'Kafka container is running!'


def get_tcp_message(is_tcp_opened: bool) -> str:
    return 'Data Collection is NOT started!' if is_tcp_opened == False else 'Data Collection is started!'
