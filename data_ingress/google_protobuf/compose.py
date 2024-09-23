from typing import List

from streaming_app.protobuf_schema import event_notification_pb2 as event_scheme
from data_ingress.data_generator.random_data import get_metric_value
from data_ingress.data_generator.time_data import get_timestamp
from data_ingress.logging_.to_log_file import log_debug, log_error

class ErrorDuringGpbEventCompose(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def compose_gpb_event(unique_client_id: int, message_number: int, client_name: str) -> bytes:
    log_debug(compose_gpb_event.__name__, 'composing a serialized google protobuf event notification')

    timestamp: float = get_timestamp()
    metric_values: List[float] = get_metrics_values()
    log_message_content(unique_client_id, message_number, client_name, timestamp, metric_values)

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
        log_error(compose_gpb_event.__name__, f'Compose_serialized_gpb_event failed: {e}')
    else:

        log_debug(compose_gpb_event.__name__, f'Serialized_to_string_gpb_event: {serialized_to_string_gpb_event}')
        return serialized_to_string_gpb_event



def get_metrics_values()-> List[float]:
    metric_values: List[float] = [
        get_metric_value(0, 1, 4),  # metric_0
        get_metric_value(-1, 1, 4),  # metric_1
        get_metric_value(-10, 10, 3),  # metric_2
        get_metric_value(-100, 100, 1),  # metric_3
        get_metric_value(-1000, 1000, 0),  # metric_4
        get_metric_value(-100, 0, 1),  # metric_5
        get_metric_value(-1000, -500, 0),  # metric_6
        get_metric_value(0, 1000, 0),  # metric_7
        get_metric_value(0, 100, 2),  # metric_8
        get_metric_value(0, 10000, 0),  # metric_9
        get_metric_value(0, 100000, 0),  # metric_10
        get_metric_value(-100000, 100000, 0)  # metric_11
    ]
    return metric_values

def log_message_content(unique_client_id: int, message_number: int, client_name: str, timestamp: float,
                        metric_values: List[float]) -> None:

    log_debug(log_message_content.__name__, f'unique_client_id: {unique_client_id}')
    log_debug(log_message_content.__name__, f'message_number: {message_number}')
    log_debug(log_message_content.__name__, f'client_name: {client_name}')
    log_debug(log_message_content.__name__, f'timestamp: {timestamp}')

    for metric_id, metric in enumerate(metric_values):
        log_debug(log_message_content.__name__, f'metric_{metric_id}: {metric}')