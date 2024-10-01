from typing import Callable
from typing import Tuple
from typing import Optional
from typing import Any
import threading
from data_ingress.common.logging_.to_log_file import log_debug, log_error_traceback
from data_ingress.common.threads.threads_helper_exceptions import StartingThreadFailed

class ThreadStarter:

    def start_thread(self, target: Callable[..., None], args_tuple: Tuple[Any, ...], generator_id: int) -> Optional[threading.Thread]:
        log_debug(self.start_thread, f'Creating thread for generator id: {generator_id}')
        try:
            new_started_thread: threading.Thread = threading.Thread(target=target, args=args_tuple)
            new_started_thread.start()
        except Exception as e:
            log_error_traceback(self.start_thread)
            raise StartingThreadFailed(self.start_thread, str(e), generator_id) from e
        else:
            log_debug(self.start_thread, f'Creating thread for generator id: {generator_id} - Done!')
            return new_started_thread