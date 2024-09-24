import threading
from typing import Callable
from typing import Tuple
from typing import Optional
from typing import Any

from data_ingress.logging_.to_log_file import log_debug, log_error, log_error_traceback


class StartingThreadFailed(Exception):
    def __init__(self, function: Callable, exception_message: str, thread_name: str):
        super().__init__(exception_message)
        self.function: Callable = function
        self.exception_message: str = exception_message
        self.thread_name: str = thread_name
        log_error(function, f'Creating a {thread_name} thread - Failed!')

def start_thread(target: Callable[..., None], args_tuple: Tuple[Any, ...], thread_name: str) -> Optional[threading.Thread]:
    log_debug(start_thread, f'Creating {thread_name} thread')
    try:
        new_thread: threading.Thread = threading.Thread(target=target, args=args_tuple)
        new_thread.start()
    except Exception as e:
        log_error_traceback(start_thread)
        raise StartingThreadFailed(start_thread, str(e), thread_name) from e
    else:
        log_debug(start_thread, f'Creating {thread_name} thread - Done!')
        return new_thread
