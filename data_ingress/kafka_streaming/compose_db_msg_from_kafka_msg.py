from kafka.consumer.fetcher import ConsumerRecord

from data_ingress.common.dummy_data.timestamp_generator import RealTimestampGenerator
from common.logging_.to_log_file import log_debug, log_error_traceback
from data_ingress.kafka_streaming.kafka_exceptions import KafkaMessageToDatabaseMessageConversionFailed
from data_ingress.models import MetricsDataModelsLoader


def compose_db_msg_from_kafka_msg(kafka_msg: ConsumerRecord) -> MetricsDataModelsLoader:
    timestamp_generator: RealTimestampGenerator = RealTimestampGenerator()

    log_debug(compose_db_msg_from_kafka_msg, f'Kafka message to database_handling message conversion ...')
    try:
        unique_client_id = get_unique_client_id(kafka_msg)
        kafka_unique_client_id = kafka_msg.value.get('unique_client_id')
        date_component = timestamp_generator.get_date_component_from_timestamp(kafka_msg.value.get('timestamp'))
        time_component = timestamp_generator.get_time_component_from_timestamp(kafka_msg.value.get('timestamp'))
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

        database_message: MetricsDataModelsLoader = MetricsDataModelsLoader(
            internal_unique_client_id=unique_client_id,
            unique_client_id=kafka_unique_client_id,
            date = date_component,
            time = time_component,
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
        log_error_traceback(compose_db_msg_from_kafka_msg)
        raise KafkaMessageToDatabaseMessageConversionFailed(str(e), compose_db_msg_from_kafka_msg,
                                                            kafka_msg) from e
    else:
        log_debug(compose_db_msg_from_kafka_msg,
                  f'Kafka message to database_handling message conversion - Done! Database message\n{kafka_msg}')
        return database_message


def get_unique_client_id(kafka_msg: ConsumerRecord) -> str:
    unique_client_id: str = str(kafka_msg.value.get('unique_client_id'))
    message_number: str = str(kafka_msg.value.get('message_number'))
    return unique_client_id + "_" + message_number

