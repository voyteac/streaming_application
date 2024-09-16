import logging
import threading

logger = logging.getLogger('streaming_app')


def start_thread(target, args_tuple, thread_name):
    logger.debug(f'{start_thread.__name__} -> Creating {thread_name} thread')
    new_thread = threading.Thread(target=target, args=args_tuple)
    new_thread.start()
    logger.debug(f'{start_thread.__name__} -> Creating {thread_name} thread - Done!')
    return new_thread
