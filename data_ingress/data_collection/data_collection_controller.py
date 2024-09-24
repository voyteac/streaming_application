from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
import threading

from data_ingress.kafka_container_control.kafka_container_controller import KafkaContainerController
from data_ingress.data_collection.data_collection_controller_helper import DataCollectionControllerHelper
from data_ingress.common.threads.threads_helper import ThreadsHelper
from data_ingress.common.logging_.to_log_file import log_info, log_warning


class DataCollectionController:
    def __init__(self):
        self.stop_streaming_flag = threading.Event()
        self.streaming_thread = None

        self.helper = DataCollectionControllerHelper()
        self.threads_helper = ThreadsHelper()
        self.kafka_container_controller = KafkaContainerController()

    def start_data_collection(self, request: HttpRequest) -> HttpResponse:
        log_info(self.start_data_collection, 'Starting data collection...')
        self.stop_streaming_flag.clear()
        is_kafka_container_running = self.kafka_container_controller.get_kafka_container_status()

        if is_kafka_container_running or not self.streaming_thread or not self.streaming_thread.is_alive():
            self.streaming_thread = self.threads_helper.start_thread(self.helper.start_data_flow,
                                                 (self.stop_streaming_flag,),
                                                 'streaming')
            log_info(self.start_data_collection, 'Data collection started!')
            self.set_streaming_status_to_started(request)
        else:
            log_warning(self.start_data_collection,
                        f'Cannot start data collection - kafka_container_running: {is_kafka_container_running}')
            self.set_streaming_status_to_stopped(request)
        return redirect('data-ingress')


    def stop_data_collection(self, request: HttpRequest) -> HttpResponse:
        log_info(self.stop_data_collection, 'Stopping data collection')
        self.stop_streaming_flag.set()
        if self.streaming_thread and self.streaming_thread.is_alive():
            self.streaming_thread.join()
        log_info(self.stop_data_collection, 'Data collection stopped')
        self.set_streaming_status_to_stopped(request)
        return redirect('data-ingress')

    def set_streaming_status_to_started(self, request: HttpRequest) -> None:
        request.session['data_collection_status'] = 'started'

    def set_streaming_status_to_stopped(self, request: HttpRequest) -> None:
        request.session['data_collection_status'] = 'stopped'

data_collection_controller = DataCollectionController()
