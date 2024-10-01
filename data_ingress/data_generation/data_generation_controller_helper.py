import threading
from typing import List

from django.http import HttpRequest

from data_ingress.common.logging_.to_log_file import log_debug
from streaming_app.config import tcp_config


class DataGenerationControllerHelper:
    def __init__(self):
        self.default_number_of_tcp_clients: int = tcp_config.default_number_of_tcp_clients

    def get_number_of_data_generators_from_gui(self, request: HttpRequest) -> int:
        number_of_clients: int = int(request.GET.get('num_streams', self.default_number_of_tcp_clients))
        log_debug(self.get_number_of_data_generators_from_gui, f'number_of_clients: {number_of_clients}')
        return number_of_clients

    def get_stop_flag_thread_instances_for_client(self, number_of_clients: int) -> List[threading.Event]:
        return [threading.Event() for _ in range(number_of_clients)]
