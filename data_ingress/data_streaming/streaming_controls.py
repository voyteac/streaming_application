from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
import threading

from data_ingress.kafka.kafka_container_control import kafka_container_check
from data_ingress.tcp_operations.tcp_server import start_data_flow
from data_ingress.data_streaming.streaming_controls_helper import start_thread
from data_ingress.logging_.to_log_file import log_info, log_warning


class DataCollectionController:
    def __init__(self):
        self.stop_streaming_flag = threading.Event()
        self.streaming_thread = None

    def start_data_collection(self, request: HttpRequest) -> HttpResponse:
        log_info(self.start_data_collection, 'Starting data collection...')
        self.stop_streaming_flag.clear()
        is_kafka_container_running = kafka_container_check()

        if is_kafka_container_running or not self.streaming_thread or not self.streaming_thread.is_alive():
            self.streaming_thread = start_thread(start_data_flow,
                                                 (self.stop_streaming_flag,),
                                                 'streaming')
            log_info(self.start_data_collection, 'Data collection started!')
            self.set_streaming_status_to_started(request)
        else:
            log_warning(self.start_data_collection,
                        f'Cannot start data collection - kafka_container_running: {is_kafka_container_running}')
            self.set_streaming_status_to_stopped(request)
        return redirect('data-ingress')

    def set_streaming_status_to_started(self, request: HttpRequest) -> None:
        request.session['tcp_server_status'] = 'started'

    def set_streaming_status_to_stopped(self, request: HttpRequest) -> None:
        request.session['tcp_server_status'] = 'stopped'

    def stop_data_collection(self, request: HttpRequest) -> HttpResponse:
        log_info(self.stop_data_collection, 'Stopping data collection')
        self.stop_streaming_flag.set()
        if self.streaming_thread and self.streaming_thread.is_alive():
            self.streaming_thread.join()
        log_info(self.stop_data_collection, 'Data collection stopped')
        self.set_streaming_status_to_stopped(request)
        return redirect('data-ingress')


data_collection_manager = DataCollectionController()


def start_data_collection_view(request: HttpRequest) -> HttpResponse:
    return data_collection_manager.start_data_collection(request)


def stop_data_collection_view(request: HttpRequest) -> HttpResponse:
    return data_collection_manager.stop_data_collection(request)
