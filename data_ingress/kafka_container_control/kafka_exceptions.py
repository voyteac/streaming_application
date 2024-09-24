from typing import Callable
from data_ingress.common.logging_.to_log_file import log_error


class InitializeKafkaConsumerFailed(Exception):
    def __init__(self, exception_message: str, function: Callable):
        super().__init__(exception_message)
        self.exception_message: str = exception_message
        self.function: Callable = function
        log_error(self.function, f'Initializing Kafka Consumer - Failed: {self.exception_message}')


class LoadingMessageFromKafkaToDbFailed(Exception):
    def __init__(self, exception_message: str, function: Callable):
        super().__init__(exception_message)
        self.exception_message: str = exception_message
        self.function: Callable = function
        log_error(self.__class__, f'Loading message to database - Failed')


class InitializeKafkaProducerFailed(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        log_error(self.__class__, f'Initializing Kafka Producer - Failed: {self.message}')


class StartingContainerFailed(Exception):
    def __init__(self, function: Callable, exception_message: str, container_name: str):
        super().__init__(exception_message)
        self.function: Callable = function
        self.exception_message: str = exception_message
        self.container_name: str = container_name
        log_error(self.function, f'Starting {self.container_name} container- Failed! Error: {self.exception_message}')

class LoadingMessageToKafkaFailed(Exception):
    def __init__(self, function: Callable, exception_message: str):
        super().__init__(exception_message)
        self.function: Callable = function
        self.exception_message: str = exception_message
        log_error(self.function, f'Loading data to Kafka - Failed with error: {self.exception_message}')

class ErrorDuringCheckingDockerEnvironmentForKafka(Exception):
    def __init__(self, function: Callable, exception_message: str):
        super().__init__(exception_message)
        self.function: Callable = function
        self.exception_message: str = exception_message
        log_error(self.function, f'Cannot check docker setup for Kafka (problem with containers names?) Failed with error: {self.exception_message}')