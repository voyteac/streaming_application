import socket
import queue
import logging
import traceback

from streaming_app.config import tcp_config
from data_ingress.tcp_operations.tcp_helper import create_tcp_socket, close_tcp_socket, accept_tcp_connection
from data_ingress.kafka.kafka_producer import initialize_kafka_producer, load_data_to_kafka
from data_ingress.kafka.kafka_consumer import start_consuming
from data_ingress.kafka.kafka_consumer import initialize_kafka_consumer
from data_ingress.data_streaming.streaming_controls_helper import start_thread

logger = logging.getLogger('streaming_app')
tcp_to_kafka_data_queue = queue.Queue()


def start_data_flow(stop_streaming_flag):
    logger.info(
        f'{start_data_flow.__name__} -> Opening TCP socket for host: {tcp_config.client_host} and port: {tcp_config.port}')

    kafka_producer = initialize_kafka_producer()
    kafka_consumer = initialize_kafka_consumer()

    try:
        tcp_socket = create_tcp_socket()
        tcp_socket.bind((tcp_config.client_host, tcp_config.port))
        tcp_socket.listen()
        tcp_socket.settimeout(1.0)
        while not stop_streaming_flag.is_set():
            start_streaming_to_kafka(kafka_consumer, kafka_producer, tcp_socket)
    finally:
        close_tcp_socket(tcp_socket)


def start_streaming_to_kafka(kafka_consumer, kafka_producer, tcp_socket):
    start_thread(start_consuming, (kafka_consumer,), 'kafka consumer')
    start_thread(load_data_to_kafka, (kafka_producer, tcp_to_kafka_data_queue), 'kafka producer')
    try:
        tcp_connection = accept_tcp_connection(tcp_socket)
        start_thread(handle_tcp_connection, (tcp_connection, tcp_to_kafka_data_queue), 'TCP connection')
    except socket.timeout:
        pass
    except Exception as e:
        logger.error(f'{start_data_flow.__name__} -> Socket error: {e}')
        logger.error(f'{start_data_flow.__name__} -> {traceback.format_exc()}')
        return


def handle_tcp_connection(tcp_connection, tcp_to_kafka_data_queue_arg):
    logger.info(f'{handle_tcp_connection.__name__} -> Handling tcp connection')
    received_data_buffer = tcp_config.received_data_buffer
    with tcp_connection:
        try:
            while True:
                received_data = tcp_connection.recv(received_data_buffer)
                logger.debug(f'{handle_tcp_connection.__name__} -> received_data: {received_data}')
                if not received_data:
                    break
                logger.debug(
                    f'{handle_tcp_connection.__name__} -> Put data to kafka thread queue: {received_data_buffer}')
                tcp_to_kafka_data_queue_arg.put(received_data)
        except Exception as e:
            logger.error(f'{handle_tcp_connection.__name__} -> Error handling client connection: {e}')
            logger.error(f'{handle_tcp_connection.__name__} -> {traceback.format_exc()}')


def check_tcp_socket(host, port, timeout=1):
    logger.info(f'{check_tcp_socket.__name__} -> Checking if TCP socket is opened.')
    socket_to_check = create_tcp_socket()
    socket_to_check.settimeout(timeout)
    try:
        socket_to_check.connect((host, port))
        logger.debug(f'{check_tcp_socket.__name__} -> Testing - Opened!')
        logger.info(f'{check_tcp_socket.__name__} -> Checking if TCP socket is opened - Opened.')
        return True
    except (socket.timeout, socket.error) as err:
        logger.debug(f'{check_tcp_socket.__name__} -> Testing - Closed! {err}')
        logger.info(f'{check_tcp_socket.__name__} -> Checking if TCP socket is opened - Closed')
        return False
    finally:
        socket_to_check.close()
        logger.debug(f'{check_tcp_socket.__name__} -> Testing - Closed!')
