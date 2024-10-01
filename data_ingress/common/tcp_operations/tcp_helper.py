import socket
import time
from typing import Optional

from data_ingress.common.logging_.to_log_file import log_debug, log_error
from streaming_app.config import tcp_config


class TcpHelper:
    def __init__(self):
        self.server_host: str = tcp_config.server_host
        self.server_port: int = tcp_config.port
        self.msg_send_retry_delay: int = tcp_config.msg_send_retry_delay
        self.client_host: str = tcp_config.client_host
        self.client_port: int = tcp_config.port
        self.connection_attempt_retry_count: int = tcp_config.connection_attempt_retry_count
        self.max_connection_retries: int = tcp_config.max_connection_retries

    def attempt_tcp_socket_connection(self) -> Optional[socket.socket]:
        log_debug(self.attempt_tcp_socket_connection, 'Connecting to server...')
        try:
            tcp_socket = self.create_tcp_socket()
            tcp_socket = self.connect_to_tcp_socket(tcp_socket, self.client_host, self.client_port)
            self.connection_attempt_retry_count = 0
            return tcp_socket
        except Exception as e:
            log_error(self.attempt_tcp_socket_connection, f'Connection error: {e}')
            self.connection_attempt_retry_count += 1
            if self.connection_attempt_retry_count >= self.max_connection_retries:
                log_error(self.attempt_tcp_socket_connection, f'Max retries reached. Stopping the loop.')
                return None

            time.sleep(self.msg_send_retry_delay)
        return None

    def create_tcp_socket(self) -> socket.socket:
        tcp_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        log_debug(self.create_tcp_socket, 'TCP socket created')
        return tcp_socket

    def connect_to_tcp_socket(self, tcp_socket: socket.socket, host: str, port: int) -> Optional[socket.socket]:
        try:
            tcp_socket.connect((host, port))
            log_debug(self.connect_to_tcp_socket, f'Connected to {host}:{port}')
            return tcp_socket
        except socket.error as e:
            log_error(self.connect_to_tcp_socket, f'Error connecting to {host}:{port} - {e}')
            return None

    def close_tcp_socket(self, tcp_socket: socket.socket) -> None:
        tcp_socket.close()
        log_debug(self.close_tcp_socket, 'TCP connection closed')

    def receive_data_via_tcp(self, tcp_connection: socket.socket, buffer_size: int) -> bytes:
        received_data: bytes = tcp_connection.recv(buffer_size)
        log_debug(self.receive_data_via_tcp, f'received_data: {received_data}')
        return received_data

    def send_message_to_tcp_socket(self, tcp_socket: socket.socket, message: bytes) -> None:
        try:
            tcp_socket.sendall(message)
            log_debug(self.send_message_to_tcp_socket, 'Message sent!')
        except socket.error as e:
            log_error(self.send_message_to_tcp_socket, f'Error sending message: {e}')

    def accept_tcp_connection(self, tcp_socket: socket.socket) -> socket.socket:
        tcp_connection, tcp_address = tcp_socket.accept()
        log_debug(self.accept_tcp_connection, f'TCP socket opened with address: {tcp_address}')
        return tcp_connection

    def check_tcp_socket(self, timeout: int = 1) -> bool:
        socket_to_check = self.create_tcp_socket()
        socket_to_check.settimeout(timeout)
        try:
            socket_to_check.connect((self.server_host, self.server_port))
            return True
        except (socket.timeout, socket.error):
            return False
        finally:
            self.close_tcp_socket(socket_to_check)

    def is_tcp_port_open(self, host_: str, port_: int, timeout=5) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result: int = sock.connect_ex((host_, port_))
            return result == 0
