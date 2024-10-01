from typing import Callable
from data_ingress.common.logging_.to_log_file import log_error



class StartingThreadFailed(Exception):
    def __init__(self, function: Callable, exception_message: str, generator_id: int):
        super().__init__(exception_message)
        self.function: Callable = function
        self.exception_message: str = exception_message
        self.generator_id: int = generator_id
        log_error(function, f'Creating thread for generator id: {generator_id} - Failed!')
