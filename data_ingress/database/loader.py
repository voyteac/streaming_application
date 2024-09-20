from kafka.consumer.fetcher import ConsumerRecord

from data_ingress.models import DataBaseLoader
from data_ingress.logging_.to_log_file import log_debug, log_info, log_error, log_error_traceback


class KafkaMessageToDatabaseMessageConversionFailed(Exception):
    def __init__(self, exception_message: str, function_name: str, kafka_msg: ConsumerRecord):
        super().__init__(exception_message)
        self.exception_message: str = exception_message
        self.function_name: str = function_name
        self.kafka_msg: ConsumerRecord = kafka_msg
        log_error(self.function_name,f'Converting Kafka message to database message failed {self.exception_message}')
        log_error(self.function_name, f'Kafka Topic:: {self.kafka_msg.topic}')
        log_error(self.function_name, f'Kafka Message: {self.kafka_msg.value}')

class SavingToDatabaseFailed(Exception):
    def __init__(self,  exception_message: str, function_name: str):
        super().__init__(exception_message)
        self.exception_message: str = exception_message
        self.function_name: str = function_name
        log_error(self.function_name,f'Saving to database failed!')


def save_kafka_message_to_database(kafka_msg: ConsumerRecord) -> None:
    log_info(save_kafka_message_to_database.__name__, 'Loading message to database')

    database_message: DataBaseLoader = get_database_message_from_kafka_message(kafka_msg)
    try:
        database_message.save()
    except Exception as e:
        log_error_traceback(save_kafka_message_to_database.__name__)
        raise SavingToDatabaseFailed(str(e), save_kafka_message_to_database.__name__) from e
    else:
        log_info(save_kafka_message_to_database.__name__, 'Loading message to database - Done')


def get_database_message_from_kafka_message(kafka_msg: ConsumerRecord) -> DataBaseLoader:
    log_debug(get_database_message_from_kafka_message.__name__,f'Kafka message to database message conversion ...')
    try:
        unique_client_id = get_unique_client_id(kafka_msg)
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

        database_message: DataBaseLoader = DataBaseLoader(
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
    except Exception as e:
        log_error_traceback(get_database_message_from_kafka_message.__name__)
        raise KafkaMessageToDatabaseMessageConversionFailed(str(e), get_database_message_from_kafka_message.__name__,
                                                            kafka_msg) from e
    else:
        log_debug(get_database_message_from_kafka_message.__name__, f'Kafka message to database message conversion - Done! Database message\n{kafka_msg}')
        return database_message


def get_unique_client_id(kafka_msg: ConsumerRecord) -> str:
    unique_client_id: str = str(kafka_msg.value.get('unique_client_id'))
    message_number: str = str(kafka_msg.value.get('message_number'))
    return unique_client_id + "_" + message_number
