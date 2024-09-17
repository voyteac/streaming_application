from kafka import KafkaProducer
import logging
import traceback

from streaming_app.config import kafka_config
from data_ingress.google_protobuf.decompose import decompose_gpb_event, get_unique_client_id

logger = logging.getLogger('streaming_app')


def initialize_kafka_producer():
    logger.debug(f'{initialize_kafka_producer.__name__} -> Initializing Kafka Producer')
    try:
        producer = KafkaProducer(
            bootstrap_servers=kafka_config.bootstrap_servers,
            api_version=kafka_config.api_version
        )
        logger.debug(f'{initialize_kafka_producer.__name__} -> Initializing Kafka Producer - Done')
        return producer
    except Exception as e:
        logger.error(f'{initialize_kafka_producer.__name__} -> Error initializing Kafka producer: {e}')
        logger.error(f'{initialize_kafka_producer.__name__} -> {traceback.format_exc()}')
        return None


def load_data_to_kafka(kafka_producer, data_queue):
    logger.info(f'{load_data_to_kafka.__name__} -> Loading data to kafka')
    data = data_queue.get()
    logger.debug(f'{load_data_to_kafka.__name__} -> Data: {data}')
    gpb_message_json = decompose_gpb_event(data)

    kafka_topic = determine_topic_based_on_data(data)

    logger.debug(f'{load_data_to_kafka.__name__} -> Topic: {kafka_topic}')
    try:
        kafka_producer.send(kafka_topic, gpb_message_json.encode('utf-8'))
        kafka_producer.flush()
        logger.info(f'{load_data_to_kafka.__name__} -> Loading data to kafka - Done!')
    except Exception as e:
        logger.error(f'{initialize_kafka_producer.__name__} -> Failed to send message to Kafka: {e}')
        logger.error(f'{load_data_to_kafka.__name__} -> {traceback.format_exc()}')

def determine_topic_based_on_data(data):
    unique_client_id = get_unique_client_id(data)
    if unique_client_id % 2 == 0:
        return kafka_config.even_client_id_topic_name
    else:
        return kafka_config.odd_client_id_topic_name

