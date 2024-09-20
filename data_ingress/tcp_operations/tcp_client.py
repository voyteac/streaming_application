from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

import time
import threading
import socket
from typing import Optional
from typing import List


from streaming_app.config import tcp_config
from data_ingress.tcp_operations.tcp_helper import (send_message_to_tcp_socket, create_tcp_socket,
                                                    connect_to_tcp_socket, close_tcp_socket)
from data_ingress.tcp_operations.data_generator import get_unique_client_id_list, get_client_name_id
from data_ingress.data_streaming.streaming_controls_helper import start_thread
from data_ingress.google_protobuf import compose
from data_ingress.logging_.to_log_file import log_debug, log_info, log_warning, log_error

streaming_threads: List[str] = []
stop_streaming_flag: List[str] = []

client_host: str = tcp_config.client_host
port: int = tcp_config.port
default_number_of_tcp_clients: int = tcp_config.default_number_of_tcp_clients
data_generation_pause_period: int = tcp_config.data_generation_pause_period
retry_delay: int = tcp_config.retry_delay


def start_streaming(request: HttpRequest) -> HttpResponse:
    log_info(start_streaming.__name__, 'Start streaming...')

    global streaming_threads
    global stop_streaming_flag

    number_of_clients: int = get_number_of_data_generators_from_gui(request)
    unique_event_id_list: List[int] = get_unique_client_id_list(number_of_clients)
    client_name_list: List[str] = get_client_name_id(number_of_clients)

    if not streaming_threads:

        stop_streaming_flag = get_stop_flag_thread_instances_for_client(number_of_clients)

        [start_thread(send_message_to_server, (unique_event_id_list[internal_client_id],
                                               client_name_list[internal_client_id],
                                               stop_streaming_flag[internal_client_id]),
                      get_thread_name(internal_client_id))
         for internal_client_id in range(number_of_clients)]
    set_streaming_status(request)

    return redirect('data-ingress')


def set_streaming_status(request: HttpRequest) -> None:  # to improve
    request.session['streaming_status'] = 'started'


def get_stop_flag_thread_instances_for_client(number_of_clients: int) -> list:
    return [threading.Event() for _ in range(number_of_clients)]


def get_thread_name(internal_client_id: int) -> str:
    return f'client {str(internal_client_id)}'


def get_number_of_data_generators_from_gui(request: HttpRequest) -> int:
    number_of_clients: int = int(request.GET.get('num_streams', default_number_of_tcp_clients))
    log_debug(get_number_of_data_generators_from_gui.__name__, f'number_of_clients: {number_of_clients}')
    return number_of_clients


def send_message_to_server(unique_client_id: int, client_name: str, stop_flag: threading.Event) -> None:
    log_info(send_message_to_server.__name__, 'Sending message to server')

    message_number: int = 0
    tcp_socket: Optional[socket.socket] = None

    while not stop_flag.is_set():
        if tcp_socket is None:
            log_debug(send_message_to_server.__name__, 'Connecting to server...')
            try:
                tcp_socket = create_tcp_socket()
                tcp_socket = connect_to_tcp_socket(tcp_socket, client_host, port)
            except Exception as e:
                log_error(send_message_to_server.__name__, f'Connection error: {e}')
                tcp_socket = None
                time.sleep(retry_delay)
                continue

        gpb_event_notification: bytes = compose.compose_gpb_event(unique_client_id, message_number, client_name)
        try:
            send_message_to_tcp_socket(tcp_socket, gpb_event_notification)
            message_number += 1
            time.sleep(data_generation_pause_period)
        except Exception as e:
            log_error(send_message_to_server.__name__, f'Error sending message: {e}')
            tcp_socket = None
            time.sleep(retry_delay)

    if tcp_socket:
        close_tcp_socket(tcp_socket)
    log_debug(send_message_to_server.__name__, f'Client {unique_client_id} stopped streaming.')



def stop_streaming(request: HttpRequest) -> HttpResponse:

    log_info(stop_streaming.__name__, 'Stopping streaming...')
    global stop_streaming_flag, streaming_threads

    stop_errors: List[str] = []

    for stop_flag in stop_streaming_flag:
        stop_flag.set()

    for single_thread in streaming_threads:
        try:
            single_thread.join()
            log_info(stop_streaming.__name__, f'Thread {single_thread.name} stopped successfully.')
        except Exception as e:
            log_error(stop_streaming.__name__, f'Error stopping thread {single_thread.name}: {e}')
            stop_errors.append(f"Error stopping {single_thread.name}: {e}")

    streaming_threads = []
    stop_streaming_flag = []

    request.session['streaming_status'] = 'stopped'

    log_info(stop_streaming.__name__, 'Streaming stopped.')

    if stop_errors:
        log_warning(stop_streaming.__name__, 'Some threads encountered errors during stopping.')
    else:
        log_info(stop_streaming.__name__, 'All threads stopped successfully.')

    return redirect('data-ingress')
