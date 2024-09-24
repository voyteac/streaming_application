from typing import Callable
from typing import Tuple
from typing import Optional
from typing import Any
import threading
from data_ingress.common.logging_.to_log_file import log_debug, log_error_traceback
from data_ingress.common.threads.threads_helper_exceptions import StartingThreadFailed

class ThreadsHelper:

    def start_thread(self, target: Callable[..., None], args_tuple: Tuple[Any, ...], thread_name: str) -> Optional[
        threading.Thread]:
        log_debug(self.start_thread, f'Creating {thread_name} thread')
        try:
            new_thread: threading.Thread = threading.Thread(target=target, args=args_tuple)
            new_thread.start()
        except Exception as e:
            log_error_traceback(self.start_thread)
            raise StartingThreadFailed(self.start_thread, str(e), thread_name) from e
        else:
            log_debug(self.start_thread, f'Creating {thread_name} thread - Done!')
            return new_thread