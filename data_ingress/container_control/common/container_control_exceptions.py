from typing import Callable

from data_ingress.common.logging_.to_log_file import log_error


class StartingContainerFailed(Exception):
    def __init__(self, function: Callable, exception_message: str, container_name: str):
        super().__init__(exception_message)
        self.function: Callable = function
        self.exception_message: str = exception_message
        self.container_name: str = container_name
        log_error(self.function, f'Starting {self.container_name} container - Failed! Error: {self.exception_message}')

class StoppingContainerFailed(Exception):
    def __init__(self, function: Callable, exception_message: str, container_name: str):
        super().__init__(exception_message)
        self.function: Callable = function
        self.exception_message: str = exception_message
        self.container_name: str = container_name
        log_error(self.function, f'Stopping {self.container_name} container - Failed! Error: {self.exception_message}')

