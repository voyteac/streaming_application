from django.db import IntegrityError

import logging
import traceback

from data_ingress.models import DataBaseLoader

logger = logging.getLogger('streaming_app')


def load_message_to_database(kafka_msg):
    logger.info(f'{load_message_to_database.__name__} -> Loading message to database')
    try:
        unique_client_id = str(kafka_msg.value.get('unique_client_id')) + "_" + str(
            kafka_msg.value.get('message_number'))
        kafka_unique_client_id = kafka_msg.value.get('unique_client_id')
        kafka_timestamp = kafka_msg.value.get('timestamp')
        kafka_message_number = kafka_msg.value.get('message_number')
        kafka_client_name = kafka_msg.value.get('client_name')
        kafka_metric_0 = kafka_msg.value.get('metric_0')
        kafka_metric_1 = kafka_msg.value.get('metric_1')
        kafka_metric_2 = kafka_msg.value.get('metric_2')
        kafka_metric_3 = kafka_msg.value.get('metric_3')
        kafka_metric_4 = kafka_msg.value.get('metric_4')
        kafka_metric_5 = kafka_msg.value.get('metric_5')
        kafka_metric_6 = kafka_msg.value.get('metric_6')
        kafka_metric_7 = kafka_msg.value.get('metric_7')
        kafka_metric_8 = kafka_msg.value.get('metric_8')
        kafka_metric_9 = kafka_msg.value.get('metric_9')
        kafka_metric_10 = kafka_msg.value.get('metric_10')
        kafka_metric_11 = kafka_msg.value.get('metric_11')

        database_message = DataBaseLoader(
            internal_unique_client_id=unique_client_id,
            unique_client_id=kafka_unique_client_id,
            timestamp=kafka_timestamp,
            message_number=kafka_message_number,
            client_name=kafka_client_name,
            metric_0=kafka_metric_0,
            metric_1=kafka_metric_1,
            metric_2=kafka_metric_2,
            metric_3=kafka_metric_3,
            metric_4=kafka_metric_4,
            metric_5=kafka_metric_5,
            metric_6=kafka_metric_6,
            metric_7=kafka_metric_7,
            metric_8=kafka_metric_8,
            metric_9=kafka_metric_9,
            metric_10=kafka_metric_10,
            metric_11=kafka_metric_11
        )
        logger.info(f'{load_message_to_database.__name__} -> Kafka message {kafka_msg}')
        try:
            database_message.save()
            logger.info(
                f'{load_message_to_database.__name__} -> For unique client id: {kafka_unique_client_id}, saved message with number: {kafka_message_number}.')
        except IntegrityError as ie:
            logger.error(
                f'{load_message_to_database.__name__} -> For unique client id: {kafka_unique_client_id} message with number: {kafka_message_number} already exists in the database.')
            logger.info(f'{load_message_to_database.__name__} -> Integrity Error: {ie}')
            logger.error(f'{load_message_to_database.__name__} -> {traceback.format_exc()}')
    except Exception as e:
        logger.error(f'{load_message_to_database.__name__} -> Loading to db failed with error {e}')
        logger.error(f'{load_message_to_database.__name__} -> Kafka Topic:: {kafka_msg.topic}')
        logger.error(f'{load_message_to_database.__name__} -> Kafka Message: {kafka_msg.value}')
        logger.error(f'{load_message_to_database.__name__} -> {traceback.format_exc()}')
