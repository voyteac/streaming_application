from threading import Thread
from typing import List

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from common.logging_.to_log_file import log_debug, log_info, log_warning, log_error
from data_ingress.common.threads.thread_started import ThreadStarter
from data_ingress.container_control.common import docker_service_config_json_parser
from data_ingress.data_generation.data_generation_controller_helper import DataGenerationControllerHelper
from data_ingress.data_generation.data_generator_message_sender import DataGeneratorMessageSender
from streaming_app.config import containers_config


class DataGenerationController:
    def __init__(self):
        self.helper = DataGenerationControllerHelper()
        self.thread_starter = ThreadStarter()

        self.data_generation_threads: List[Thread] = []
        self.stop_data_generation_flag: List[str] = []

        data_generation_config = containers_config.data_generation
        data_generation_config = docker_service_config_json_parser.DockerServiceConfigJsonParser(data_generation_config)
        self.session_started = data_generation_config.get_session_status_started()
        self.session_stopped = data_generation_config.get_session_status_stopped()
        self.redirection_pattern = data_generation_config.get_redirect_pattern()
        self.data_generations_status = data_generation_config.get_session_storage_key()

    def start_data_generation(self, request: HttpRequest) -> HttpResponse:
        log_info(self.start_data_generation, 'Start data generation...')

        number_of_generators: int = self.helper.get_number_of_data_generators_from_gui(request)
        sender = DataGeneratorMessageSender(number_of_generators)

        if not self.data_generation_threads:
            self.stop_data_generation_flag = self.helper.get_stop_flag_thread_instances_for_client(number_of_generators)

            for generator_id in range(number_of_generators):

                stop_flag = self.stop_data_generation_flag[generator_id]
                args = (generator_id, stop_flag)
                thread = self.thread_starter.start_thread(sender.send_message_to_server, args, generator_id)
                self.data_generation_threads.append(thread)

        self._set_data_generation_session_status(request, self.session_started)
        return redirect(self.redirection_pattern)

    def stop_data_generation(self, request: HttpRequest) -> HttpResponse:
        log_info(self.stop_data_generation, 'Stopping data generation')
        stop_errors: List[str] = []

        for stop_flag in self.stop_data_generation_flag:
            stop_flag.set()

        for single_thread in self.data_generation_threads:
            try:
                single_thread.join()
                log_debug(self.stop_data_generation, f'Thread {single_thread.name} stopped successfully.')
            except Exception as e:
                log_error(self.stop_data_generation, f'Error stopping thread {single_thread.name}: {e}')
                stop_errors.append(f"Error stopping {single_thread.name}: {e}")

        self.data_generation_threads.clear()
        self.stop_data_generation_flag.clear()

        self._set_data_generation_session_status(request, self.session_started)

        if stop_errors:
            log_warning(self.stop_data_generation,
                        'Data generation stopped with errors: some threads encountered errors during stopping.')
        else:
            log_info(self.stop_data_generation, 'Stopping data generation - Done!')

        return redirect(self.redirection_pattern)

    def _set_data_generation_session_status(self, request: HttpRequest, status: str) -> None:
        request.session[self.data_generations_status] = status


data_generation_controller = DataGenerationController()
