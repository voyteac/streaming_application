import json
from typing import Optional
from typing import Tuple

from kafka import KafkaConsumer
from kafka.errors import KafkaError
from kafka.errors import KafkaTimeoutError
from kafka.errors import NoBrokersAvailable

from common.logging_.to_log_file import log_debug, log_info, log_error, log_error_traceback
from data_ingress.kafka_streaming.compose_db_msg_from_kafka_msg import compose_db_msg_from_kafka_msg
from data_ingress.kafka_streaming.kafka_exceptions import (InitializeKafkaConsumerFailed,
                                                           LoadingMessageFromKafkaToDbFailed, SavingToDatabaseFailed)
from data_ingress.models import MetricsDataModelsLoader
from streaming_app.config import kafka_config


class CustomKafkaConsumer:
    def __init__(self):
        self.bootstrap_servers: str = kafka_config.bootstrap_servers
        self.consumer_api_version: Tuple[int, int, int] = kafka_config.consumer_api_version
        self.even_client_id_topic_name: str = kafka_config.even_client_id_topic_name
        self.odd_client_id_topic_name: str = kafka_config.odd_client_id_topic_name

    def initialize_kafka_consumer(self) -> Optional[KafkaConsumer]:
        log_debug(self.initialize_kafka_consumer, 'Initializing Kafka Consumer')
        try:
            consumer: KafkaConsumer = KafkaConsumer(bootstrap_servers=self.bootstrap_servers,
                                                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                                    api_version=self.consumer_api_version
                                                    )
            consumer.subscribe([self.even_client_id_topic_name, self.odd_client_id_topic_name])
        except NoBrokersAvailable as e:
            log_error(self.initialize_kafka_consumer, 'No brokers available: {}'.format(e))
            log_error_traceback(self.initialize_kafka_consumer)
            raise
        except KafkaTimeoutError as e:
            log_error(self.initialize_kafka_consumer, 'Kafka timeout error: {}'.format(e))
            log_error_traceback(self.initialize_kafka_consumer)
            raise
        except KafkaError as e:
            log_error(self.initialize_kafka_consumer, 'General Kafka error: {}'.format(e))
            log_error_traceback(self.initialize_kafka_consumer)
            raise
        except Exception as e:
            log_error_traceback(self.initialize_kafka_consumer)
            raise InitializeKafkaConsumerFailed(str(e), self.initialize_kafka_consumer) from e
        else:
            log_debug(self.initialize_kafka_consumer, 'Initializing Kafka Consumer - Done!')
            return consumer

    def start_consuming(self, kafka_consumer: KafkaConsumer) -> None:
        log_info(self.initialize_kafka_consumer, 'Staring consuming...!')
        try:
            for kafka_message in kafka_consumer:
                try:
                    database_message: MetricsDataModelsLoader = compose_db_msg_from_kafka_msg(kafka_message)
                    load_kafka_message_to_database(database_message)
                    log_info(self.initialize_kafka_consumer, 'Staring consuming... - Done!')
                    break
                except Exception as exception:
                    log_error_traceback(self.start_consuming)
                    raise LoadingMessageFromKafkaToDbFailed(str(exception), __name__) from exception
        except ValueError:
            pass
        except Exception as exception:
            log_error_traceback(self.start_consuming)
            raise LoadingMessageFromKafkaToDbFailed(str(exception), self.start_consuming) from exception


def load_kafka_message_to_database(database_message: MetricsDataModelsLoader) -> None:
    log_info(load_kafka_message_to_database, 'Loading message to database_handling')
    try:
        log_debug(load_kafka_message_to_database, "Saving a message to database")
        database_message.save()
    except Exception as e:
        log_error_traceback(load_kafka_message_to_database)
        raise SavingToDatabaseFailed(str(e), load_kafka_message_to_database) from e
    else:
        log_debug(load_kafka_message_to_database, "Saving a message to database - Done")
        log_info(load_kafka_message_to_database, 'Loading message to database_handling - Done')
