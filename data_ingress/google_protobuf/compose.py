import logging
import traceback

from streaming_app.protobuf_schema import event_notification_pb2
from data_ingress.tcp_operations.data_generator import get_metric_value, get_timestamp

logger = logging.getLogger('streaming_app')


def compose_gpb_event(unique_client_id, message_number, client_name):
    logger.debug(f'{compose_gpb_event.__name__} -> composing a serialized google protobuf event notification')

    timestamp = get_timestamp()

    metric_values = [
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

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(
            f'{compose_gpb_event.__name__} -> unique_client_id: {unique_client_id}, '
            f'message_number: {message_number}, client_name: {client_name}, timestamp: {timestamp}')
        for metric_id, metric in enumerate(metric_values):
            logger.debug(f'{compose_gpb_event.__name__} -> metric_{metric_id}: {metric}')

    try:
        gpb_event = event_notification_pb2.EventNotification(
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

        serialized_to_string_gpb_event = gpb_event.SerializeToString()

        logger.debug(
            f'{compose_gpb_event.__name__} -> gpb_event.SerializeToString(): {serialized_to_string_gpb_event}')
        return serialized_to_string_gpb_event

    except TypeError as tE:
        logger.error(f'{compose_gpb_event.__name__} -> Compose_serialized_gpb_event failed: {tE}')
        logger.error(f'{compose_gpb_event.__name__} -> {traceback.print_exc()}')
