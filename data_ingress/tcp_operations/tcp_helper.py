import socket

from data_ingress.logging_.to_log_file import log_debug, log_error


def create_tcp_socket() -> socket.socket:
    tcp_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    log_debug(create_tcp_socket.__name__, 'TCP socket created')
    return tcp_socket


def connect_to_tcp_socket(tcp_socket: socket.socket, host: str, port: int) -> socket.socket:
    try:
        tcp_socket.connect((host, port))
        log_debug(connect_to_tcp_socket.__name__, f'Connected to {host}:{port}')
        return tcp_socket
    except socket.error as e:
        log_error(connect_to_tcp_socket.__name__, f'Error connecting to {host}:{port} - {e}')


def close_tcp_socket(tcp_socket: socket.socket) -> None:
    tcp_socket.close()
    log_debug(close_tcp_socket.__name__, 'TCP connection closed')


def receive_data_via_tcp(tcp_connection: socket.socket, buffer_size: int) -> bytes:
    received_data: bytes = tcp_connection.recv(buffer_size)
    log_debug(receive_data_via_tcp.__name__, f'received_data: {received_data}')
    return received_data


def send_message_to_tcp_socket(tcp_socket: socket.socket, message: bytes) -> None:
    try:
        tcp_socket.sendall(message)
        log_debug(send_message_to_tcp_socket.__name__, 'Message sent!')
    except socket.error as e:
        log_error(send_message_to_tcp_socket.__name__, f'Error sending message: {e}')


def accept_tcp_connection(tcp_socket: socket.socket) -> socket.socket:
    tcp_connection, tcp_address = tcp_socket.accept()
    log_debug(accept_tcp_connection.__name__, f'TCP socket opened with address: {tcp_address}')
    return tcp_connection


def check_tcp_socket(host_: str, port_: int, timeout: int = 1) -> bool:
    socket_to_check = create_tcp_socket()
    socket_to_check.settimeout(timeout)
    try:
        socket_to_check.connect((host_, port_))
        return True
    except (socket.timeout, socket.error):
        return False
    finally:
        close_tcp_socket(socket_to_check)


def is_tcp_port_open(host_: str, port_: int, timeout=5) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        result: int = sock.connect_ex((host_, port_))
        return result == 0
