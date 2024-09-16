import socket
import logging
import threading

logger = logging.getLogger('streaming_app')


def create_tcp_socket():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    logger.debug(f'{create_tcp_socket.__name__} -> TCP socket created')
    return tcp_socket

def connect_to_tcp_socket(tcp_socket, host, port):
    try:
        tcp_socket.connect((host, port))
        logger.debug(f'{close_tcp_socket.__name__} -> Connected to {host}:{port}')
        return tcp_socket
    except socket.error as e:
        logger.error(f'{close_tcp_socket.__name__} -> Error connecting to {host}:{port} - {e}')


def close_tcp_socket(tcp_socket):
    tcp_socket.close()
    logger.debug(f'{close_tcp_socket.__name__} -> TCP connection closed')

def receive_data_via_tcp(tcp_connection, buffer_size):
    return tcp_connection.recv(buffer_size)


def send_message_to_tcp_socket(tcp_socket, message):
    try:
        tcp_socket.sendall(message)
        logger.debug(f'{send_message_to_tcp_socket.__name__} -> Message sent!')
    except socket.error as e:
        logger.error(f'{send_message_to_tcp_socket.__name__} -> Error sending message: {e}')


def accept_tcp_connection(tcp_socket):
    tcp_connection, tcp_address = tcp_socket.accept()
    logger.info(f'{accept_tcp_connection .__name__} -> TCP socket opened with address: {tcp_address}')
    return tcp_connection


def start_thread(target, args_tuple, thread_name):
    logger.debug(f'{start_thread.__name__} -> Creating {thread_name} thread')
    new_thread = threading.Thread(target=target, args=args_tuple)
    new_thread.start()
    logger.debug(f'{start_thread.__name__} -> Creating {thread_name} thread - Done!')
    return new_thread
