import socket
import threading
import time
from typing import List
from typing import Optional

from data_ingress.common.google_protobuf.gpb_event_composer import GpbEventComposer
from data_ingress.common.logging_.to_log_file import log_debug, log_info, log_error
from data_ingress.common.tcp_operations.tcp_helper import TcpHelper
from streaming_app.config import tcp_config


class DataGeneratorMessageSender:

    def __init__(self, number_of_generators: int):
        self.tcp_helper = TcpHelper()
        self.gpb_event_composer = GpbEventComposer(number_of_generators)

        self.streaming_threads: List[threading.Thread] = []
        self.stop_streaming_flags: List[threading.Event] = []

        self.default_number_of_tcp_clients: int = tcp_config.default_number_of_tcp_clients
        self.data_generation_pause_period: float = tcp_config.data_generation_pause_period

        self.msg_send_retry_delay = tcp_config.msg_send_retry_delay

    def send_message_to_server(self, generator_id: int, stop_flag: threading.Event) -> None:
        log_info(self.send_message_to_server, f'Starting message sending for generator {generator_id}')
        message_number: int = 0
        tcp_socket: Optional[socket.socket] = None

        while not stop_flag.is_set():
            if tcp_socket is None:
                tcp_socket = self.tcp_helper.attempt_tcp_socket_connection()

            try:
                gpb_event_notification: bytes = self.gpb_event_composer.compose_event(generator_id, message_number)
                self.tcp_helper.send_message_to_tcp_socket(tcp_socket, gpb_event_notification)
                message_number += 1
                time.sleep(self.data_generation_pause_period)
            except Exception as e:
                log_error(self.send_message_to_server, f'Error sending message: {e}')
                tcp_socket = None
                time.sleep(self.msg_send_retry_delay)

        if tcp_socket:
            self.tcp_helper.close_tcp_socket(tcp_socket)
        log_debug(self.send_message_to_server, f'Starting message sending for generator {generator_id} - STOPPED.')
