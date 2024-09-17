from streaming_app.protobuf_schema import event_notification_pb2
import json
import logging
import traceback

logger = logging.getLogger('streaming_app')


class MyException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def decompose_gpb_event(data):
    logger.debug(f'{decompose_gpb_event.__name__} -> Decomposing GPB event notification to JSON')
    logger.debug(f'{decompose_gpb_event.__name__} -> Data: {data}')

    try:
        gpb_event_notification = event_notification_pb2.EventNotification()
        gpb_event_notification.ParseFromString(data)

        decomposed_gpb_event_notification = {
            'unique_client_id': gpb_event_notification.unique_client_id,
            'timestamp': gpb_event_notification.timestamp,
            'message_number': gpb_event_notification.message_number,
            'client_name': gpb_event_notification.client_name,
            'metric_0': gpb_event_notification.metric_0,
            'metric_1': gpb_event_notification.metric_1,
            'metric_2': gpb_event_notification.metric_2,
            'metric_3': gpb_event_notification.metric_3,
            'metric_4': gpb_event_notification.metric_4,
            'metric_5': gpb_event_notification.metric_5,
            'metric_6': gpb_event_notification.metric_6,
            'metric_7': gpb_event_notification.metric_7,
            'metric_8': gpb_event_notification.metric_8,
            'metric_9': gpb_event_notification.metric_9,
            'metric_10': gpb_event_notification.metric_10,
            'metric_11': gpb_event_notification.metric_11
        }

        decomposed_gpb_event_notification_json = json.dumps(decomposed_gpb_event_notification)
        logger.debug(
            f'{decompose_gpb_event.__name__} -> decomposed_gpb_event_notification_json: {decomposed_gpb_event_notification_json}')

        return decomposed_gpb_event_notification_json
    except Exception as e:
        logger.error(f'{decompose_gpb_event.__name__} -> Decomposing error: {e}')
        logger.error(f'{decompose_gpb_event.__name__} -> {traceback.print_exc()}')


def get_unique_client_id(data):
    try:
        logger.debug(f'{decompose_gpb_event.__name__} -> Decomposing unique_client_id')
        gpb_event_notification = event_notification_pb2.EventNotification()
        gpb_event_notification.ParseFromString(data)
        unique_client_id = gpb_event_notification.unique_client_id
    except MyException as my_exception:
        logger.error(f'{decompose_gpb_event.__name__} -> Decomposing unique_client_id - FAILED:  {my_exception}')
    else:
        logger.debug(f'{decompose_gpb_event.__name__} -> Decomposing unique_client_id: Done {unique_client_id}')
        return unique_client_id

