from typing import List

from data_ingress.common.google_protobuf.schema import event_notification_pb2 as event_scheme
from data_ingress.common.dummy_data.random_data_generator import RandomDataGenerator
from data_ingress.common.dummy_data.timestamp_generator import RealTimestampGenerator
from common.logging_.to_log_file import log_debug, log_error
from data_ingress.common.dummy_data.metric_value_generator import MetricValuesGenerator

class ErrorDuringGpbEventCompose(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class GpbEventComposer:
    def __init__(self, number_of_generators):
        self.random_data_generator = RandomDataGenerator()
        self.timestamp_utility = RealTimestampGenerator()
        self.metric_values_generator = MetricValuesGenerator()
        number_of_generators: int = number_of_generators
        self.unique_client_id_list: List[int] = self.random_data_generator.get_unique_client_id_list(number_of_generators)
        self.client_name_list: List[str] = self.random_data_generator.get_client_name_id(number_of_generators)


    def compose_event(self, generator_id: int, message_number: int, next_kpi_value: float) -> bytes:
        log_debug(self.compose_event, 'composing a serialized google protobuf event notification')


        unique_client_id = self.unique_client_id_list[generator_id]
        client_name = self.client_name_list[generator_id]
        timestamp: float = self.timestamp_utility.get_timestamp()
        metric_values: List[float] = self.metric_values_generator.get_metrics_values()


        try:
            gpb_event = event_scheme.EventNotification(
                unique_client_id=unique_client_id,
                timestamp=timestamp,
                message_number=message_number,
                client_name=client_name,
                metric_0=next_kpi_value,
                metric_1=metric_values[1],
                metric_2=metric_values[2],
                metric_3=metric_values[3],
                metric_4=metric_values[4],
                metric_5=metric_values[5],
                metric_6=metric_values[6],
                metric_7=metric_values[7],
                metric_8=metric_values[8],
                metric_9=metric_values[9],
                metric_10=metric_values[10],
                metric_11=metric_values[11]
            )
            serialized_to_string_gpb_event: bytes = gpb_event.SerializeToString()
        except ErrorDuringGpbEventCompose as e:
            log_error(self.compose_event, f'Compose_serialized_gpb_event failed: {e}')
        else:
            self.log_message_content(unique_client_id, message_number, client_name, timestamp, metric_values)
            log_debug(self.compose_event, f'Serialized_to_string_gpb_event: {serialized_to_string_gpb_event}')
            return serialized_to_string_gpb_event



    def log_message_content(self, unique_client_id: int, message_number: int, client_name: str, timestamp: float,
                            metric_values: List[float]) -> None:

        log_debug(self.log_message_content, f'unique_client_id: {unique_client_id}')
        log_debug(self.log_message_content, f'message_number: {message_number}')
        log_debug(self.log_message_content, f'client_name: {client_name}')
        log_debug(self.log_message_content, f'timestamp: {timestamp}')

        for metric_id, metric in enumerate(metric_values):
            log_debug(self.log_message_content, f'metric_{metric_id}: {metric}')