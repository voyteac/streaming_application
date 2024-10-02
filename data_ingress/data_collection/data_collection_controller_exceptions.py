from typing import Callable
from common.logging_.to_log_file import log_error


class BaseDataCollectionControllerException(Exception):
    def __init__(self, exception_message: str, function: Callable, log_message: str):
        super().__init__(exception_message)
        self.exception_message: str = exception_message
        self.function: Callable = function
        log_error(self.function, f'{log_message} - Failed: {self.exception_message}')


class DataFlowFromTcpServerToKafkaFailed(BaseDataCollectionControllerException):
    def __init__(self, exception_message: str, function: Callable):
        super().__init__(exception_message, function, 'Starting a data flow from TCP server to Kafka')


class StreamingToKafkaFailed(BaseDataCollectionControllerException):
    def __init__(self, exception_message: str, function: Callable):
        super().__init__(exception_message, function, 'Starting streaming to Kafka')


class TcpConnectionHandlingFailed(BaseDataCollectionControllerException):
    def __init__(self, exception_message: str, function: Callable):
        super().__init__(exception_message, function, 'Error handling client connection')


class PutToKafkaFailed(BaseDataCollectionControllerException):
    def __init__(self, exception_message: str, function: Callable):
        super().__init__(exception_message, function, 'Put data to Kafka queue thread')
