import json
import logging
import traceback

from kafka import KafkaConsumer
from kafka.errors import KafkaError

from streaming_app.config import kafka_config
from data_ingress.database.loader import load_message_to_database

logger = logging.getLogger('streaming_app')


def initialize_kafka_consumer():
    logger.debug(f'{initialize_kafka_consumer.__name__} -> Initializing Kafka Consumer')
    try:
        consumer = KafkaConsumer(kafka_config.topic_name,
                                 bootstrap_servers=kafka_config.bootstrap_servers,
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                 api_version=(0, 10)
                                 )
        logger.debug(f'{initialize_kafka_consumer.__name__} -> Initializing Kafka Consumer - Done!')
        return consumer
    except Exception as e:
        logger.error(f'{initialize_kafka_consumer.__name__} -> Error initializing Kafka producer: {e}')
        logger.error(f'{initialize_kafka_consumer.__name__} -> {traceback.format_exc()}')
        return None


def start_consuming(kafka_consumer):
    try:
        for kafka_message in kafka_consumer:
            try:
                logger.info(f'{start_consuming.__name__} -> Loading to DB')
                load_message_to_database(kafka_message)
                logger.info(f'{start_consuming.__name__} -> Loaded to DB - DONE!')
                break
            except ValueError as e:
                logger.error(f'{start_consuming.__name__} -> ValueError processing message: {e}')
                logger.error(f'{start_consuming.__name__} -> Message causing error: {kafka_message.value}')
                logger.error(f'{start_consuming.__name__} -> {traceback.format_exc()}')
            except KeyError as ke:
                logger.error(f'{start_consuming.__name__} -> KeyError processing message: {ke:}')
                logger.error(f'{start_consuming.__name__} -> Message causing error: {kafka_message.value}')
                logger.error(f'{start_consuming.__name__} -> {traceback.format_exc()}')
    except KafkaError as ke:
        logger.error(f'{start_consuming.__name__} -> Kafka error occurred: {ke}')
        logger.error(f'{start_consuming.__name__} -> {traceback.format_exc()}')
    except ValueError:
        pass
    except Exception as e:
        logger.error(f'{start_consuming.__name__} -> Unexpected error: {e}')
        logger.error(f'{start_consuming.__name__} -> {traceback.format_exc()}')
