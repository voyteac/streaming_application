from kafka.consumer.fetcher import ConsumerRecord

from data_ingress.common.logging_.to_log_file import log_debug, log_info, log_error_traceback
from data_ingress.database_handling.compose_db_message_based_on_kafka_msg import compose_db_message_based_on_kafka_msg
from data_ingress.database_handling.database_exception import SavingToDatabaseFailed
from data_ingress.models import MetricsDataModelsLoader


def load_kafka_message_to_database(kafka_msg: ConsumerRecord) -> None:
    log_info(load_kafka_message_to_database, 'Loading message to database_handling')
    database_message: MetricsDataModelsLoader = compose_db_message_based_on_kafka_msg(kafka_msg)
    try:
        log_debug(load_kafka_message_to_database, "Saving a message to database")
        database_message.save()
    except Exception as e:
        log_error_traceback(load_kafka_message_to_database)
        raise SavingToDatabaseFailed(str(e), load_kafka_message_to_database) from e
    else:
        log_debug(load_kafka_message_to_database, "Saving a message to database - Done")
        log_info(load_kafka_message_to_database, 'Loading message to database_handling - Done')
