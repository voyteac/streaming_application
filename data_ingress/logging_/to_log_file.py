import logging
import traceback

logger = logging.getLogger('streaming_app')


def log_debug(function_name: str, message: str) -> None:
    logger.debug(f'{function_name} -> {message}')


def log_info(function_name: str, message: str) -> None:
    logger.info(f'{function_name} -> {message}')


def log_warning(function_name: str, message: str) -> None:
    logger.warning(f'{function_name} -> {message}')


def log_error(function_name: str, message: str) -> None:
    logger.error(f'{function_name} -> {message}')

def log_error_traceback(function_name: str) -> None:
    logger.error(f'{function_name} -> {traceback.format_exc()}')
