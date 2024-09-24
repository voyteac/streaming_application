from typing import Callable
from data_ingress.common.logging_.to_log_file import log_error



class StartingThreadFailed(Exception):
    def __init__(self, function: Callable, exception_message: str, thread_name: str):
        super().__init__(exception_message)
        self.function: Callable = function
        self.exception_message: str = exception_message
        self.thread_name: str = thread_name
        log_error(function, f'Creating a {thread_name} thread - Failed!')
