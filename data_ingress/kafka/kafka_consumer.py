import json
from typing import Tuple
from typing import Optional

from kafka import KafkaConsumer
from kafka.errors import KafkaError
from kafka.errors import KafkaTimeoutError
from kafka.errors import NoBrokersAvailable

from data_ingress.tcp_operations.tcp_client import start_streaming
from streaming_app.config import kafka_config
from data_ingress.database.loader import save_kafka_message_to_database
from data_ingress.logging_.to_log_file import log_debug, log_info, log_error, log_error_traceback

bootstrap_servers: str = kafka_config.bootstrap_servers
consumer_api_version: Tuple[int, int, int] = kafka_config.consumer_api_version
even_client_id_topic_name: str = kafka_config.even_client_id_topic_name
odd_client_id_topic_name: str = kafka_config.odd_client_id_topic_name


class InitializeKafkaConsumerFailed(Exception):
    def __init__(self, exception_message: str, function_name: str):
        super().__init__(exception_message)
        self.exception_message: str = exception_message
        self.function_name: str = function_name
        log_error(self.function_name, f'Initializing Kafka Consumer - Failed: {self.exception_message}')

class LoadingMessageFromKafkaToDbFailed(Exception):
    def __init__(self, exception_message: str, function_name: str):
        super().__init__(exception_message)
        self.exception_message: str = exception_message
        self.function_name: str = function_name
        log_error(self.__class__.__name__, f'Loading message to database - Failed')


def initialize_kafka_consumer() -> Optional[KafkaConsumer]:
    log_debug(initialize_kafka_consumer.__name__, 'Initializing Kafka Consumer')
    try:
        consumer: KafkaConsumer = KafkaConsumer(bootstrap_servers=bootstrap_servers,
                                                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                                api_version=consumer_api_version
                                                )
        consumer.subscribe([even_client_id_topic_name, odd_client_id_topic_name])
    except NoBrokersAvailable as e:
        log_error(initialize_kafka_consumer.__name__, 'No brokers available: {}'.format(e))
        log_error_traceback(initialize_kafka_consumer.__name__)
        raise
    except KafkaTimeoutError as e:
        log_error(initialize_kafka_consumer.__name__, 'Kafka timeout error: {}'.format(e))
        log_error_traceback(initialize_kafka_consumer.__name__)
        raise
    except KafkaError as e:
        log_error(initialize_kafka_consumer.__name__, 'General Kafka error: {}'.format(e))
        log_error_traceback(initialize_kafka_consumer.__name__)
        raise
    except Exception as e:
        log_error_traceback(initialize_kafka_consumer.__name__)
        raise InitializeKafkaConsumerFailed(str(e), initialize_kafka_consumer.__name__) from e
    else:
        log_debug(initialize_kafka_consumer.__name__, 'Initializing Kafka Consumer - Done!')
        return consumer


def start_consuming(kafka_consumer: KafkaConsumer) -> None:
    log_info(initialize_kafka_consumer.__name__, 'Staring consuming...!')
    try:
        for kafka_message in kafka_consumer:
            try:
                save_kafka_message_to_database(kafka_message)
                log_info(initialize_kafka_consumer.__name__, 'Staring consuming... - Done!')
                break
            except Exception as exception:
                log_error_traceback(start_streaming.__name__)
                raise LoadingMessageFromKafkaToDbFailed(str(exception), __name__) from exception
    except ValueError:
        pass
    except Exception as exception:
        log_error_traceback(start_streaming.__name__)
        raise LoadingMessageFromKafkaToDbFailed(str(exception), start_consuming.__name__) from exception
