from typing import List

from data_ingress.common.google_protobuf.schema import event_notification_pb2 as event_scheme
from data_ingress.common.dummy_data.random_data_generator import RandomDataGenerator
from data_ingress.common.dummy_data.timestamp_generator import RealTimestampGenerator
from data_ingress.common.logging_.to_log_file import log_debug, log_error

class ErrorDuringGpbEventCompose(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class GpbEventComposer:
    def __init__(self):
        self.random_data_generator = RandomDataGenerator()
        self.timestamp_utility = RealTimestampGenerator()

    def compose_gpb_event(self, unique_client_id: int, message_number: int, client_name: str) -> bytes:
        log_debug(self.compose_gpb_event, 'composing a serialized google protobuf event notification')

        timestamp: float = self.timestamp_utility.get_timestamp()
        metric_values: List[float] = self.get_metrics_values()

        try:
            gpb_event = event_scheme.EventNotification(
                unique_client_id=unique_client_id,
                timestamp=timestamp,
                message_number=message_number,
                client_name=client_name,
                metric_0=metric_values[0],
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
            log_error(self.compose_gpb_event, f'Compose_serialized_gpb_event failed: {e}')
        else:
            self.log_message_content(unique_client_id, message_number, client_name, timestamp, metric_values)
            log_debug(self.compose_gpb_event, f'Serialized_to_string_gpb_event: {serialized_to_string_gpb_event}')
            return serialized_to_string_gpb_event



    def get_metrics_values(self)-> List[float]:
        metric_values: List[float] = [
            self.random_data_generator.get_metric_value(0, 1, 2),  # metric_0
            self.random_data_generator.get_metric_value(-1, 1, 4),  # metric_1
            self.random_data_generator.get_metric_value(-10, 10, 3),  # metric_2
            self.random_data_generator.get_metric_value(-100, 100, 1),  # metric_3
            self.random_data_generator.get_metric_value(-1000, 1000, 0),  # metric_4
            self.random_data_generator.get_metric_value(-100, 0, 1),  # metric_5
            self.random_data_generator.get_metric_value(-1000, -500, 0),  # metric_6
            self.random_data_generator.get_metric_value(0, 1000, 0),  # metric_7
            self.random_data_generator.get_metric_value(0, 100, 2),  # metric_8
            self.random_data_generator.get_metric_value(0, 10000, 0),  # metric_9
            self.random_data_generator.get_metric_value(0, 100000, 0),  # metric_10
            self.random_data_generator.get_metric_value(-100000, 100000, 0)  # metric_11
        ]
        return metric_values

    def log_message_content(self, unique_client_id: int, message_number: int, client_name: str, timestamp: float,
                            metric_values: List[float]) -> None:

        log_debug(self.log_message_content, f'unique_client_id: {unique_client_id}')
        log_debug(self.log_message_content, f'message_number: {message_number}')
        log_debug(self.log_message_content, f'client_name: {client_name}')
        log_debug(self.log_message_content, f'timestamp: {timestamp}')

        for metric_id, metric in enumerate(metric_values):
            log_debug(self.log_message_content, f'metric_{metric_id}: {metric}')