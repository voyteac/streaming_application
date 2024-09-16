from django.shortcuts import redirect

import time
import threading
import logging

from data_ingress.google_protobuf import compose
from streaming_app.config import tcp_config
from data_ingress.tcp_operations.tcp_helper import (send_message_to_tcp_socket, create_tcp_socket,
                                                    connect_to_tcp_socket, close_tcp_socket)
from data_ingress.tcp_operations.data_generator import get_unique_client_id_list, get_client_name_id
from data_ingress.data_streaming.streaming_controls_helper import start_thread

logger = logging.getLogger('streaming_app')

streaming_threads = []
stop_streaming_flag = []


def start_streaming(request):
    global streaming_threads, stop_streaming_flag

    logger.info(f'{start_streaming.__name__} -> Start streaming...')

    number_of_clients = get_number_of_data_generators_from_gui(request)
    unique_event_id_list = get_unique_client_id_list(number_of_clients)
    client_name_list = get_client_name_id(number_of_clients)

    logger.debug(f'{start_streaming.__name__} -> number_of_clients: {number_of_clients}')
    logger.debug(f'{start_streaming.__name__} -> unique_event_id_list: {unique_event_id_list}')
    logger.debug(f'{start_streaming.__name__} -> type of unique_event_id_list: {type(unique_event_id_list)}')
    logger.debug(f'{start_streaming.__name__} -> client_name_list: {client_name_list}')

    if not streaming_threads:
        stop_streaming_flag = get_stop_flag_thread_instances_for_client(number_of_clients)

        [start_thread(send_message_to_server, (unique_event_id_list[internal_client_id],
                                               client_name_list[internal_client_id],
                                               stop_streaming_flag[internal_client_id]),
                      f'client {internal_client_id}')
         for internal_client_id in range(number_of_clients)]

    request.session['streaming_status'] = 'started'
    return redirect('control-panel')


def get_number_of_data_generators_from_gui(request):
    return int(request.GET.get('num_streams', tcp_config.default_number_of_tcp_clients))


def get_stop_flag_thread_instances_for_client(number_of_clients):
    return [threading.Event() for _ in range(number_of_clients)]


def send_message_to_server(unique_client_id, client_name, stop_flag):
    logger.info(f'{send_message_to_server.__name__} -> Sending message to server')
    data_generation_pause_period = tcp_config.data_generation_pause_period
    retry_delay = tcp_config.retry_delay

    message_number = 0
    tcp_socket = None

    while not stop_flag.is_set():
        if tcp_socket is None:
            logger.debug(f'{send_message_to_server.__name__} -> Connecting to server...')
            try:
                tcp_socket = create_tcp_socket()
                tcp_socket = connect_to_tcp_socket(tcp_socket, tcp_config.client_host, tcp_config.port)
            except Exception as e:
                logger.error(f'{send_message_to_server.__name__} -> Connection error: {e}')
                tcp_socket = None
                time.sleep(retry_delay)
                continue

        gpb_event_notification = compose.compose_gpb_event(unique_client_id, message_number, client_name)
        try:
            send_message_to_tcp_socket(tcp_socket, gpb_event_notification)
            message_number += 1
            time.sleep(data_generation_pause_period)
        except Exception as e:
            logger.error(f'{send_message_to_server.__name__} -> Error sending message: {e}')
            tcp_socket = None
            time.sleep(retry_delay)

    if tcp_socket:
        close_tcp_socket(tcp_socket)

    logger.debug(f'{send_message_to_server.__name__} -> Client {unique_client_id} stopped streaming.')


def stop_streaming(request):
    logger.info(f'{stop_streaming.__name__} -> Stopping streaming..')

    global stop_streaming_flag, streaming_threads
    stop_errors = []

    for stop_flag in stop_streaming_flag:
        stop_flag.set()

    for thread in streaming_threads:
        try:
            thread.join()
            logger.info(f'{stop_streaming.__name__} -> Thread {thread.name} stopped successfully.')
        except Exception as e:
            logger.error(f'{stop_streaming.__name__} -> Error stopping thread {thread.name}: {e}')
            stop_errors.append(f"Error stopping {thread.name}: {e}")

    streaming_threads = []
    stop_streaming_flag = []

    request.session['streaming_status'] = 'stopped'
    logger.info(f'{stop_streaming.__name__} -> Streaming stopped.')

    if stop_errors:
        logger.warning(f'{stop_streaming.__name__} -> Some threads encountered errors during stopping.')
    else:
        logger.info(f'{stop_streaming.__name__} -> All threads stopped successfully.')

    return redirect('control-panel')

# def is_tcp_client_running(host, port, timeout_seconds=1):
#     logger.info(f'{is_tcp_client_running.__name__} -> Checking whether TCP client is running.')
#     try:
#         with create_tcp_socket() as tcp_socket:
#             tcp_socket.bind((host, port))
#             tcp_socket.listen()
#             tcp_socket.settimeout(timeout_seconds)
#
#             try:
#                 tcp_connection = accept_tcp_connection(tcp_socket)
#                 # tcp_connection, tcp_address = tcp_socket.accept()
#                 # received_data = tcp_connection.recv(tcp_config.received_data_buffer)
#                 received_data = receive_data_via_tcp(tcp_connection, tcp_config.received_data_buffer)
#                 if not received_data:
#                     tcp_socket.close()
#                     logger.info(f'{is_tcp_client_running.__name__} -> TCP connection closed, no received = TCP client is not running')
#                     return False
#                 close_tcp_socket(tcp_socket)
#                 logger.info(f'{is_tcp_client_running.__name__} -> TCP connection closed, data received = TCP client is running')
#                 return True
#             finally:
#                 logger.info(f'{is_tcp_client_running.__name__} -> TCP connection closed')
#                 close_tcp_socket(tcp_socket)
#     except (socket.timeout, ConnectionRefusedError):
#         logger.error(f'{is_tcp_client_running.__name__} -> Socket timeout - error TCP client is NOT running')
#         return False
#     except Exception as e:
#         logger.error(f'{is_tcp_client_running.__name__} -> Error occurred: {e} - TCP client is NOT running')
#         return False
