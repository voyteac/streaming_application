from streaming_app.protobuf_schema import event_notification_pb2 as event_scheme
import json
from typing import Optional

from data_ingress.logging_.to_log_file import log_debug, log_error, log_error_traceback


class ErrorDuringGpbEventDecompose(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        log_error(self.__class__.__name__, f'Decomposing GPB event notification to JSON - Failed: {self.message}')

class ErrorDuringDecomposingUniqueClientId(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        log_error(self.__class__.__name__, f'Decomposing unique_client_id - Failed')


def decompose_gpb_event(data: bytes) -> str:
    log_debug(decompose_gpb_event.__name__,f'Decomposing GPB event notification to JSON, data: {data}')
    try:
        gpb_event_notification: event_scheme.EventNotification = parse_gpb_event_notification_to_string(data)
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
    except Exception as e:
        log_error_traceback(decompose_gpb_event.__name__)
        raise ErrorDuringGpbEventDecompose(str(e)) from e
    else:
        log_debug(decompose_gpb_event.__name__, f'decomposed_gpb_event_notification_json: {decomposed_gpb_event_notification_json}')
        return decomposed_gpb_event_notification_json



def get_unique_client_id(data) -> Optional[int]:
    try:
        log_debug(decompose_gpb_event.__name__, 'Decomposing unique_client_id')
        gpb_event_notification: event_scheme.EventNotification = parse_gpb_event_notification_to_string(data)
        unique_client_id: int = gpb_event_notification.unique_client_id
    except Exception as exception:
        log_error_traceback(get_unique_client_id.__name__)
        raise ErrorDuringDecomposingUniqueClientId(str(exception)) from exception
    else:
        log_debug(decompose_gpb_event.__name__, f'Decomposing unique_client_id - Done! Value: {unique_client_id}')
        return unique_client_id


def parse_gpb_event_notification_to_string(data: event_scheme.EventNotification) -> event_scheme.EventNotification:
    log_debug(decompose_gpb_event.__name__, 'Parsing GPB event notification')
    try:
        gpb_event_notification: event_scheme.EventNotification = event_scheme.EventNotification()
        gpb_event_notification.ParseFromString(data)
    except Exception as exception:
        log_error_traceback(parse_gpb_event_notification_to_string.__name__)
        raise ErrorDuringGpbEventDecompose(str(exception)) from exception
    else:
        log_debug(decompose_gpb_event.__name__, 'Parsing GPB event notification - Done!')
        return gpb_event_notification