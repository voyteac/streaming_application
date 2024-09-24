from kafka import KafkaProducer
from kafka.errors import KafkaError
from kafka.errors import KafkaTimeoutError
from kafka.errors import NoBrokersAvailable
from typing import Optional
from typing import Tuple
import queue

from streaming_app.config import kafka_config
from data_ingress.google_protobuf.decompose import decompose_gpb_event, get_unique_client_id
from data_ingress.logging_.to_log_file import log_debug, log_info, log_error, log_error_traceback

api_version: Tuple[int, int, int] = kafka_config.producer_api_version
bootstrap_servers: str = kafka_config.bootstrap_servers
even_client_id_topic_name: str = kafka_config.even_client_id_topic_name
odd_client_id_topic_name: str = kafka_config.odd_client_id_topic_name


class InitializeKafkaProducerFailed(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        log_error(self.__class__, f'Initializing Kafka Producer - Failed: {self.message}')


def initialize_kafka_producer() -> Optional[KafkaProducer]:
    log_debug(initialize_kafka_producer, 'Initializing Kafka Producer')
    try:
        producer: KafkaProducer = KafkaProducer(bootstrap_servers=bootstrap_servers, api_version=api_version)
    except NoBrokersAvailable as e:
        log_error(initialize_kafka_producer, 'No brokers available: {}'.format(e))
        log_error_traceback(initialize_kafka_producer)
        raise
    except KafkaTimeoutError as e:
        log_error(initialize_kafka_producer, 'Kafka timeout error: {}'.format(e))
        log_error_traceback(initialize_kafka_producer)
        raise
    except KafkaError as e:
        log_error(initialize_kafka_producer, 'General Kafka error: {}'.format(e))
        log_error_traceback(initialize_kafka_producer)
        raise
    except Exception as e:
        log_error(initialize_kafka_producer, 'An unexpected error occurred: {}'.format(e))
        log_error_traceback(initialize_kafka_producer)
        raise InitializeKafkaProducerFailed(str(e)) from e
    else:
        log_debug(initialize_kafka_producer, 'Initializing Kafka Producer - Done')
        return producer


def load_data_to_kafka(kafka_producer: KafkaProducer, data_queue: queue.Queue):
    log_info(load_data_to_kafka, 'Loading data to kafka')
    data: bytes = get_data_from_queue(data_queue)
    gpb_message_json: str = decompose_gpb_event(data)
    kafka_topic = determine_topic_based_on_data(data)
    log_debug(load_data_to_kafka, 'Topic: {kafka_topic}')
    try:
        kafka_producer.send(kafka_topic, gpb_message_json.encode('utf-8'))
        kafka_producer.flush()
        log_info(load_data_to_kafka, 'Loading data to kafka - Done!')
    except Exception as e:
        log_error(initialize_kafka_producer, f'Failed to send message to Kafka: {e}')
        log_error_traceback(initialize_kafka_producer)


def determine_topic_based_on_data(data: bytes) -> str:
    log_debug(determine_topic_based_on_data, 'Determining the Kafka topic')
    unique_client_id: int = get_unique_client_id(data)
    if unique_client_id % 2 == 0:
        log_debug(determine_topic_based_on_data,
                  f'Determining the Kafka topic - Done: {even_client_id_topic_name}')
        return even_client_id_topic_name
    else:
        log_debug(determine_topic_based_on_data,
                  f'Determining the Kafka topic - Done: {odd_client_id_topic_name}')
        return odd_client_id_topic_name


def get_data_from_queue(data_queue: queue.Queue) -> bytes:
    log_debug(get_data_from_queue, 'Getting data from queue')
    data: bytes = data_queue.get()
    log_debug(load_data_to_kafka, f'Getting data from queue - Got it - Data: {data}')
    return data
