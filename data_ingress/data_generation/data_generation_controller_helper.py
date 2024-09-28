from django.http import HttpRequest

import time
import threading
import socket
from typing import Optional
from typing import List

from streaming_app.config import tcp_config
from data_ingress.common.tcp_operations.tcp_helper import TcpHelper

from data_ingress.common.google_protobuf.gpb_event_composer import GpbEventComposer
from data_ingress.common.logging_.to_log_file import log_debug, log_info, log_error


class DataGenerationControllerHelper:
    def __init__(self):
        self.streaming_threads: List[threading.Thread] = []
        self.stop_streaming_flags: List[threading.Event] = []

        self.client_host: str = tcp_config.client_host
        self.port: int = tcp_config.port
        self.default_number_of_tcp_clients: int = tcp_config.default_number_of_tcp_clients
        self.data_generation_pause_period: float = tcp_config.data_generation_pause_period
        self.retry_delay: int = tcp_config.retry_delay

        self.tcp_helper = TcpHelper()
        self.gpb_event_composer = GpbEventComposer()

    def get_number_of_data_generators_from_gui(self, request: HttpRequest) -> int:
        number_of_clients: int = int(request.GET.get('num_streams', self.default_number_of_tcp_clients))
        log_debug(self.get_number_of_data_generators_from_gui, f'number_of_clients: {number_of_clients}')
        return number_of_clients

    def get_stop_flag_thread_instances_for_client(self, number_of_clients: int) -> List[threading.Event]:
        return [threading.Event() for _ in range(number_of_clients)]

    def get_thread_name(self, internal_client_id: int) -> str:
        return f'client {str(internal_client_id)}'

    def send_message_to_server(self, unique_client_id: int, client_name: str, stop_flag: threading.Event) -> None:
        log_info(self.send_message_to_server, f'Starting message sending for {client_name}')
        message_number: int = 0
        tcp_socket: Optional[socket.socket] = None

        while not stop_flag.is_set():
            if tcp_socket is None:
                log_debug(self.send_message_to_server, 'Connecting to server...')
                try:
                    tcp_socket = self.tcp_helper.create_tcp_socket()
                    tcp_socket = self.tcp_helper.connect_to_tcp_socket(tcp_socket, self.client_host, self.port)
                except Exception as e:
                    log_error(self.send_message_to_server, f'Connection error: {e}')
                    tcp_socket = None
                    time.sleep(self.retry_delay)
                    continue

            gpb_event_notification: bytes = self.gpb_event_composer.compose_gpb_event(unique_client_id, message_number, client_name)

            try:
                self.tcp_helper.send_message_to_tcp_socket(tcp_socket, gpb_event_notification)
                message_number += 1
                time.sleep(self.data_generation_pause_period)
            except Exception as e:
                log_error(self.send_message_to_server, f'Error sending message: {e}')
                tcp_socket = None
                time.sleep(self.retry_delay)

        if tcp_socket:
            self.tcp_helper.close_tcp_socket(tcp_socket)

        log_debug(self.send_message_to_server, f'Client {unique_client_id} stopped streaming.')
