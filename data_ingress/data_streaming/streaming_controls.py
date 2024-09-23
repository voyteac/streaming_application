from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

import threading

from data_ingress.kafka.kafka_container_control import kafka_container_check
from data_ingress.tcp_operations.tcp_server import start_data_flow
from data_ingress.data_streaming.streaming_controls_helper import start_thread
from data_ingress.logging_.to_log_file import log_info, log_warning

stop_streaming_flag = threading.Event()
streaming_thread = None


def start_data_collection(request: HttpRequest) -> HttpResponse:
    log_info(start_data_collection.__name__, 'Starting data collection...')
    global streaming_thread, stop_streaming_flag
    stop_streaming_flag.clear()
    is_kafka_container_running: bool = kafka_container_check()

    print(f'streaming_thread: {streaming_thread}')
    # print(f'streaming_thread.is_alive(): {streaming_thread.is_alive()}')
    if is_kafka_container_running or not streaming_thread or not streaming_thread.is_alive():
        streaming_thread = start_thread(start_data_flow, (stop_streaming_flag,), 'streaming')
        log_info(start_data_collection.__name__, 'Data collection started!')
        set_streaming_status_to_started(request)
    else:
        log_warning(start_data_collection.__name__,
                    f'Cannot start data collection - kafka_container_running: {is_kafka_container_running}')
        set_streaming_status_to_stopped(request)
    return redirect('data-ingress')


def set_streaming_status_to_started(request: HttpRequest) -> None:
    request.session['tcp_server_status'] = 'started'


def set_streaming_status_to_stopped(request: HttpRequest) -> None:
    request.session['tcp_server_status'] = 'stopped'


def stop_data_collection(request: HttpRequest) -> HttpResponse:
    log_info(start_data_collection.__name__, 'Stopping data collection')
    global stop_streaming_flag
    stop_streaming_flag.set()
    if streaming_thread and streaming_thread.is_alive():
        streaming_thread.join()
    log_info(start_data_collection.__name__, 'Data collection stopped')
    set_streaming_status_to_stopped(request)
    return redirect('data-ingress')
