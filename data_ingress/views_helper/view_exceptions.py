from typing import Callable
from data_ingress.common.logging_.to_log_file import log_error


class BaseViewsException(Exception):
    def __init__(self, exception_message: str, method: Callable, log_message: str):
        super().__init__(exception_message)
        self.exception_message: str = exception_message
        self.method: Callable = method
        log_error(self.method, f'{log_message} - Failed: {self.exception_message}')


class ClearingDatabaseFailed(BaseViewsException):
    def __init__(self, exception_message: str, method: Callable):
        super().__init__(exception_message, method, 'Clearing database failed!')