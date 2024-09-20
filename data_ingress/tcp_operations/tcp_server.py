import socket
import queue
import threading
from kafka import KafkaProducer
from kafka import KafkaConsumer

from streaming_app.config import tcp_config
from data_ingress.tcp_operations.tcp_helper import create_tcp_socket, close_tcp_socket, accept_tcp_connection, receive_data_via_tcp, check_tcp_socket
from data_ingress.kafka.kafka_producer import initialize_kafka_producer, load_data_to_kafka
from data_ingress.kafka.kafka_consumer import start_consuming
from data_ingress.kafka.kafka_consumer import initialize_kafka_consumer
from data_ingress.data_streaming.streaming_controls_helper import start_thread
from data_ingress.logging_.to_log_file import log_debug, log_info, log_error, log_error_traceback

tcp_to_kafka_data_queue: queue.Queue = queue.Queue()
client_host: str = tcp_config.client_host
port: int = tcp_config.port
received_data_buffer: int = tcp_config.received_data_buffer


class DataFlowFromTcpServerToKafkaFailed(Exception):
    def __init__(self, exception_message: str, function_name: str):
        super().__init__(exception_message)
        self.exception_message: str = exception_message
        self.function_name: str = function_name
        log_error(self.function_name,
                  f'Starting a data flow from TCP server to Kafka - Failed: {self.exception_message}')


class StreamingToKafkaFailed(Exception):
    def __init__(self, exception_message: str, function_name: str):
        super().__init__(exception_message)
        self.exception_message: str = exception_message
        self.function_name: str = function_name
        log_error(self.function_name, f'Starting streaming to Kafka - Failed: {self.exception_message}')


class TcpConnectionHandlingFailed(Exception):
    def __init__(self, exception_message: str, function_name: str):
        super().__init__(exception_message)
        self.exception_message: str = exception_message
        self.function_name: str = function_name
        log_error(self.function_name, f'Error handling client connection: {self.exception_message}')


class PutToKafkaFailed(Exception):
    def __init__(self, exception_message: str, function_name: str):
        super().__init__(exception_message)
        self.exception_message: str = exception_message
        self.function_name: str = function_name
        log_error(self.function_name, f'Put data to kafka queue thread - Failed: {self.exception_message}')


def start_data_flow(stop_streaming_flag: threading.Event) -> None:
    log_info(start_data_flow.__name__, f'Starting a data flow from TCP server to Kafka')

    kafka_producer: KafkaProducer = initialize_kafka_producer()
    kafka_consumer: KafkaConsumer = initialize_kafka_consumer()
    tcp_socket: socket.socket = create_tcp_socket()

    try:
        tcp_socket.bind((client_host, port))
        tcp_socket.listen()
        tcp_socket.settimeout(1.0)
        while not stop_streaming_flag.is_set():
            start_streaming_to_kafka(kafka_consumer, kafka_producer, tcp_socket)
    except Exception as e:
        log_error_traceback(start_data_flow.__name__)
        raise DataFlowFromTcpServerToKafkaFailed(str(e), start_data_flow.__name__) from e
    finally:
        close_tcp_socket(tcp_socket)


def start_streaming_to_kafka(kafka_consumer: KafkaConsumer, kafka_producer: KafkaProducer,
                             tcp_socket: socket.socket) -> None:
    log_info(start_streaming_to_kafka.__name__, 'Starting streaming to Kafka')
    start_thread(start_consuming, (kafka_consumer,), 'kafka consumer')
    start_thread(load_data_to_kafka, (kafka_producer, tcp_to_kafka_data_queue), 'kafka producer')
    try:
        tcp_connection: socket.socket = accept_tcp_connection(tcp_socket)
        start_thread(handle_tcp_connection, (tcp_connection, tcp_to_kafka_data_queue), 'TCP connection')
    except socket.timeout:
        pass
    except Exception as e:
        log_error_traceback(start_streaming_to_kafka.__name__)
        raise StreamingToKafkaFailed(str(e), start_streaming_to_kafka.__name__) from e
        # return


def handle_tcp_connection(tcp_connection: socket.socket, tcp_to_kafka_data_queue_arg: queue.Queue) -> None:
    log_info(handle_tcp_connection.__name__, 'Handling tcp connection...')
    with tcp_connection:
        try:
            while True:
                received_data: bytes = receive_data_via_tcp(tcp_connection, received_data_buffer)
                if not received_data:
                    break
                send_data_to_kafka(received_data, tcp_to_kafka_data_queue_arg)
        except Exception as e:
            log_error_traceback(handle_tcp_connection.__name__)
            raise TcpConnectionHandlingFailed(str(e), handle_tcp_connection.__name__)


def send_data_to_kafka(data: bytes, tcp_to_kafka_data_queue_arg: queue.Queue) -> None:
    log_debug(send_data_to_kafka.__name__, f'Put data to kafka queue thread')
    try:
        tcp_to_kafka_data_queue_arg.put(data)
    except Exception as e:
        log_error_traceback(send_data_to_kafka.__name__)
        raise PutToKafkaFailed(str(e), send_data_to_kafka.__name__)
    else:
        log_debug(handle_tcp_connection.__name__, f'Put data to kafka queue thread - Done!')



