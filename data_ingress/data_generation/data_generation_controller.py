from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from typing import List
from threading import Thread

from streaming_app.config import tcp_config
from data_ingress.common.dummy_data.random_data_generator import RandomDataGenerator
from data_ingress.common.logging_.to_log_file import log_debug, log_info, log_warning, log_error
from data_ingress.common.tcp_operations import tcp_helper
from data_ingress.data_generation.data_generation_controller_helper import DataGenerationControllerHelper
from data_ingress.common.threads.threads_helper import ThreadsHelper


# streaming_threads: List[str] = []
# stop_streaming_flag: List[str] = []
#
# client_host: str = tcp_config.client_host
# port: int = tcp_config.port
# default_number_of_tcp_clients: int = tcp_config.default_number_of_tcp_clients
# data_generation_pause_period: int = tcp_config.data_generation_pause_period
# retry_delay: int = tcp_config.retry_delay


class DataGenerationController:
    def __init__(self):
        self.helper = DataGenerationControllerHelper()
        self.threads_helper = ThreadsHelper()
        self.random_data_generator = RandomDataGenerator()

        self.streaming_threads: List[Thread] = []  # Encapsulating globals as instance variables
        self.stop_streaming_flag: List[str] = []

    def start_data_generation(self, request: HttpRequest) -> HttpResponse:
        log_info(self.start_data_generation, 'Start data collection...')

        number_of_clients: int = self.helper.get_number_of_data_generators_from_gui(request)
        unique_event_id_list: List[int] = self.random_data_generator.get_unique_client_id_list(number_of_clients)
        client_name_list: List[str] = self.random_data_generator.get_client_name_id(number_of_clients)

        if not self.streaming_threads:
            self.stop_streaming_flag = self.helper.get_stop_flag_thread_instances_for_client(number_of_clients)

            for internal_client_id in range(number_of_clients):
                thread_name = self.helper.get_thread_name(internal_client_id)
                args = (unique_event_id_list[internal_client_id], client_name_list[internal_client_id],
                        self.stop_streaming_flag[internal_client_id])
                thread = self.threads_helper.start_thread(self.helper.send_message_to_server, args, thread_name)
                self.streaming_threads.append(thread)

        self.set_streaming_status(request, 'started')
        return redirect('data-ingress')

    def stop_data_generation(self, request: HttpRequest) -> HttpResponse:
        log_info(self.stop_data_generation, 'Stopping data collection')
        stop_errors: List[str] = []

        for stop_flag in self.stop_streaming_flag:
            stop_flag.set()

        for single_thread in self.streaming_threads:
            try:
                single_thread.join()
                log_debug(self.stop_data_generation, f'Thread {single_thread.name} stopped successfully.')
            except Exception as e:
                log_error(self.stop_data_generation, f'Error stopping thread {single_thread.name}: {e}')
                stop_errors.append(f"Error stopping {single_thread.name}: {e}")

        self.streaming_threads.clear()
        self.stop_streaming_flag.clear()
        self.set_streaming_status(request, 'stopped')

        if stop_errors:
            log_warning(self.stop_data_generation, 'Data collection stopped with errors: some threads encountered errors during stopping.')
        else:
            log_info(self.stop_data_generation, 'Stopping data collection - Done!')

        return redirect('data-ingress')


    def set_streaming_status(self, request: HttpRequest, status: str) -> None:
        request.session['data_generation_status'] = status


data_generation_controller = DataGenerationController()


