import logging
import traceback
from typing import Callable

logger = logging.getLogger('streaming_app')


def log_debug(function: Callable, message: str) -> None:
    function_name = get_function_name(function)
    logger.debug(f'{function_name} -> {message}')


def log_info(function: Callable, message: str) -> None:
    function_name = get_function_name(function)
    logger.info(f'{function_name} -> {message}')


def log_warning(function: Callable, message: str) -> None:
    function_name = get_function_name(function)
    logger.warning(f'{function_name} -> {message}')


def log_error(function: Callable, message: str) -> None:
    function_name = get_function_name(function)
    logger.error(f'{function_name} -> {message}')


def log_error_traceback(function: Callable) -> None:
    function_name = get_function_name(function)
    logger.error(f'{function_name} -> {traceback.format_exc()}')


def get_function_name(function: Callable) -> str:
    return function.__name__
