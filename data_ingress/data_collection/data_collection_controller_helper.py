import socket
import queue
import threading

from kafka import KafkaProducer
from kafka import KafkaConsumer

from streaming_app.config import tcp_config
from data_ingress.kafka_container_control.kafka_producer import CustomKafkaProducer
from data_ingress.kafka_container_control.kafka_consumer import CustomKafkaConsumer
from data_ingress.common.tcp_operations.tcp_helper import TcpHelper
from data_ingress.common.logging_.to_log_file import log_debug, log_info, log_error_traceback
from data_ingress.common.threads.threads_helper import ThreadsHelper
from data_ingress.data_collection.data_collection_controller_exceptions import (DataFlowFromTcpServerToKafkaFailed,
                                                                                StreamingToKafkaFailed,
                                                                                TcpConnectionHandlingFailed,
                                                                                PutToKafkaFailed)


class DataCollectionControllerHelper:
    def __init__(self):
        self.tcp_to_kafka_data_queue: queue.Queue = queue.Queue()
        self.client_host: str = tcp_config.client_host
        self.port: int = tcp_config.port
        self.received_data_buffer: int = tcp_config.received_data_buffer

        self.thread_helper = ThreadsHelper()
        self.kafka_producer = CustomKafkaProducer()
        self.kafka_consumer = CustomKafkaConsumer()
        self.tcp_helper = TcpHelper()

    def start_data_flow(self, stop_streaming_flag: threading.Event) -> None:
        log_info(self.start_data_flow, f'Starting a data flow from TCP server to Kafka')

        kafka_producer: KafkaProducer = self.kafka_producer.initialize_kafka_producer()
        kafka_consumer: KafkaConsumer = self.kafka_consumer.initialize_kafka_consumer()
        tcp_socket: socket.socket = self.tcp_helper.create_tcp_socket()

        try:
            tcp_socket.bind((self.client_host, self.port))
            tcp_socket.listen()
            tcp_socket.settimeout(1.0)
            while not stop_streaming_flag.is_set():
                self.start_streaming_to_kafka(kafka_consumer, kafka_producer, tcp_socket)
        except Exception as e:
            log_error_traceback(self.start_data_flow)
            raise DataFlowFromTcpServerToKafkaFailed(str(e), self.start_data_flow) from e
        finally:
            self.tcp_helper.close_tcp_socket(tcp_socket)

    def start_streaming_to_kafka(self, kafka_consumer: KafkaConsumer, kafka_producer: KafkaProducer,
                                 tcp_socket: socket.socket) -> None:
        log_info(self.start_streaming_to_kafka, 'Starting streaming to Kafka')
        self.thread_helper.start_thread(self.kafka_consumer.start_consuming, (kafka_consumer,),
                                        'kafka_container_control consumer')
        self.thread_helper.start_thread(self.kafka_producer.load_data_to_kafka,
                                        (kafka_producer, self.tcp_to_kafka_data_queue),
                                        'kafka_container_control producer')
        try:
            tcp_connection: socket.socket = self.tcp_helper.accept_tcp_connection(tcp_socket)
            self.thread_helper.start_thread(self.handle_tcp_connection, (tcp_connection, self.tcp_to_kafka_data_queue),
                                            'TCP connection')
        except socket.timeout:
            pass
        except Exception as e:
            log_error_traceback(self.start_streaming_to_kafka)
            raise StreamingToKafkaFailed(str(e), self.start_streaming_to_kafka) from e

    def handle_tcp_connection(self, tcp_connection: socket.socket, tcp_to_kafka_data_queue_arg: queue.Queue) -> None:
        log_info(self.handle_tcp_connection, 'Handling tcp connection...')
        with tcp_connection:
            try:
                while True:
                    received_data: bytes = self.tcp_helper.receive_data_via_tcp(tcp_connection,
                                                                                self.received_data_buffer)
                    if not received_data:
                        break
                    self.send_data_to_kafka(received_data, tcp_to_kafka_data_queue_arg)
            except Exception as e:
                log_error_traceback(self.handle_tcp_connection)
                raise TcpConnectionHandlingFailed(str(e), self.handle_tcp_connection)

    def send_data_to_kafka(self, data: bytes, tcp_to_kafka_data_queue_arg: queue.Queue) -> None:
        log_debug(self.send_data_to_kafka, f'Put data to kafka_container_control queue thread')
        try:
            tcp_to_kafka_data_queue_arg.put(data)
        except Exception as e:
            log_error_traceback(self.send_data_to_kafka)
            raise PutToKafkaFailed(str(e), self.send_data_to_kafka)
        else:
            log_debug(self.send_data_to_kafka, f'Put data to kafka_container_control queue thread - Done!')
