from kafka import KafkaProducer
from kafka.errors import KafkaError
from kafka.errors import KafkaTimeoutError
from kafka.errors import NoBrokersAvailable
from typing import Optional
from typing import Tuple
import queue

from streaming_app.config import kafka_config
from data_ingress.common.google_protobuf.gpb_event_decomposer import GpbEventDecomposer
from data_ingress.common.logging_.to_log_file import log_debug, log_info, log_error, log_error_traceback
from data_ingress.kafka_container_control.kafka_exceptions import (InitializeKafkaProducerFailed,
                                                                   LoadingMessageToKafkaFailed)


class CustomKafkaProducer:
    def __init__(self):
        self.api_version: Tuple[int, int, int] = kafka_config.producer_api_version
        self.bootstrap_servers: str = kafka_config.bootstrap_servers
        self.even_client_id_topic_name: str = kafka_config.even_client_id_topic_name
        self.odd_client_id_topic_name: str = kafka_config.odd_client_id_topic_name

        self.gbp_event_decomposer = GpbEventDecomposer()


    def initialize_kafka_producer(self) -> Optional[KafkaProducer]:
        log_debug(self.initialize_kafka_producer, 'Initializing Kafka Producer')
        try:
            producer: KafkaProducer = KafkaProducer(bootstrap_servers=self.bootstrap_servers,
                                                    api_version=self.api_version)
        except NoBrokersAvailable as e:
            log_error(self.initialize_kafka_producer, 'No brokers available: {}'.format(e))
            log_error_traceback(self.initialize_kafka_producer)
            raise
        except KafkaTimeoutError as e:
            log_error(self.initialize_kafka_producer, 'Kafka timeout error: {}'.format(e))
            log_error_traceback(self.initialize_kafka_producer)
            raise
        except KafkaError as e:
            log_error(self.initialize_kafka_producer, 'General Kafka error: {}'.format(e))
            log_error_traceback(self.initialize_kafka_producer)
            raise
        except Exception as e:
            log_error(self.initialize_kafka_producer, 'An unexpected error occurred: {}'.format(e))
            log_error_traceback(self.initialize_kafka_producer)
            raise InitializeKafkaProducerFailed(str(e)) from e
        else:
            log_debug(self.initialize_kafka_producer, 'Initializing Kafka Producer - Done')
            return producer


    def load_data_to_kafka(self, kafka_producer: KafkaProducer, data_queue: queue.Queue):
        log_info(self.load_data_to_kafka, 'Loading data to Kafka')
        data: bytes = self.get_data_from_queue(data_queue)
        gpb_message_json: str = self.gbp_event_decomposer.decompose_gpb_event(data)
        kafka_topic = self.determine_topic_based_on_data(data)
        log_debug(self.load_data_to_kafka, 'Topic: {kafka_topic}')
        try:
            kafka_producer.send(kafka_topic, gpb_message_json.encode('utf-8'))
            kafka_producer.flush()
            log_info(self.load_data_to_kafka, 'Loading data to Kafka - Done!')
        except Exception as e:
            log_error_traceback(self.load_data_to_kafka)
            raise LoadingMessageToKafkaFailed(self.load_data_to_kafka, str(e))



    def determine_topic_based_on_data(self, data: bytes) -> str:
        log_debug(self.determine_topic_based_on_data, 'Determining the Kafka topic')
        unique_client_id: int = self.gbp_event_decomposer.get_unique_client_id(data)
        if unique_client_id % 2 == 0:
            log_debug(self.determine_topic_based_on_data,
                      f'Determining the Kafka topic - Done: {self.even_client_id_topic_name}')
            return self.even_client_id_topic_name
        else:
            log_debug(self.determine_topic_based_on_data,
                      f'Determining the Kafka topic - Done: {self.odd_client_id_topic_name}')
            return self.odd_client_id_topic_name


    def get_data_from_queue(self, data_queue: queue.Queue) -> bytes:
        log_debug(self.get_data_from_queue, 'Getting data from queue')
        data: bytes = data_queue.get()
        log_debug(self.load_data_to_kafka, f'Getting data from queue - Got it - Data: {data}')
        return data
