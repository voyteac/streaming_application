from kafka.consumer.fetcher import ConsumerRecord
from typing import Callable
from common.logging_.to_log_file import log_error


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


class LoadingMessageToKafkaFailed(Exception):
    def __init__(self, function: Callable, exception_message: str):
        super().__init__(exception_message)
        self.function: Callable = function
        self.exception_message: str = exception_message
        log_error(self.function, f'Loading data to Kafka - Failed with error: {self.exception_message}')


class KafkaMessageToDatabaseMessageConversionFailed(Exception):
    def __init__(self, exception_message: str, function: Callable, kafka_msg: ConsumerRecord):
        super().__init__(exception_message)
        self.exception_message: str = exception_message
        self.function: Callable = function
        self.kafka_msg: ConsumerRecord = kafka_msg
        log_error(self.function,f'Converting Kafka message to database_handling message failed {self.exception_message}')
        log_error(self.function, f'Kafka Topic:: {self.kafka_msg.topic}')
        log_error(self.function, f'Kafka Message: {self.kafka_msg.value}')

class SavingToDatabaseFailed(Exception):
    def __init__(self,  exception_message: str, function: Callable):
        super().__init__(exception_message)
        self.exception_message: str = exception_message
        self.function: Callable = function
        log_error(self.function,f'Saving to database_handling failed!')

