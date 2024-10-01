from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
import threading

from data_ingress.container_control.kafka_docker_service_controller import KafkaDockerServiceController
from data_ingress.data_collection.data_collection_controller_helper import DataCollectionControllerHelper
from data_ingress.common.threads.thread_started import ThreadStarter
from data_ingress.common.logging_.to_log_file import log_info, log_warning

from data_ingress.container_control.common import docker_service_config_json_parser
from streaming_app.config import containers_config


class DataCollectionController:
    def __init__(self):
        self.stop_streaming_flag = threading.Event()
        self.streaming_thread = None

        self.helper = DataCollectionControllerHelper()
        self.threads_helper = ThreadStarter()
        self.kafka_container_controller = KafkaDockerServiceController()

        data_collection_config = containers_config.data_collection
        self.data_collection_config = docker_service_config_json_parser.DockerServiceConfigJsonParser(data_collection_config)


    def start_data_collection(self, request: HttpRequest) -> HttpResponse:
        log_info(self.start_data_collection, 'Starting data collection...')
        self.stop_streaming_flag.clear()
        is_kafka_container_running = self.kafka_container_controller.get_kafka_docker_service_status()

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
        return redirect(self.data_collection_config.get_redirect_pattern())


    def stop_data_collection(self, request: HttpRequest) -> HttpResponse:
        log_info(self.stop_data_collection, 'Stopping data collection')
        self.stop_streaming_flag.set()
        if self.streaming_thread and self.streaming_thread.is_alive():
            self.streaming_thread.join()
        log_info(self.stop_data_collection, 'Data collection stopped')
        self.set_streaming_status_to_stopped(request)
        return redirect(self.data_collection_config.get_redirect_pattern())

    def set_streaming_status_to_started(self, request: HttpRequest) -> None:
        request.session[self.data_collection_config.get_session_storage_key()] = self.data_collection_config.get_session_status_started()

    def set_streaming_status_to_stopped(self, request: HttpRequest) -> None:
        request.session[self.data_collection_config.get_session_storage_key()] = self.data_collection_config.get_session_status_stopped()

data_collection_controller = DataCollectionController()
