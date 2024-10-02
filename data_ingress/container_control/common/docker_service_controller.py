from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from typing import Dict
from common.logging_.to_log_file import log_info, log_error_traceback
from data_ingress.common.wsl_operations.wsl_commands import CommandExecutor
from data_ingress.container_control.common.container_control_exceptions import StartingContainerFailed, StoppingContainerFailed

from data_ingress.container_control.common.docker_service_config_json_parser import DockerServiceConfigJsonParser

class DockerServiceController:
    def __init__(self, kafka_service_data: Dict, docker_compose_up_wsl_cmd: str, docker_compose_down_wsl_cmd: str):

        config_parser = DockerServiceConfigJsonParser(kafka_service_data)
        self.service_name: str = config_parser.get_service_info_name()

        self.service_session_storage_key = config_parser.get_session_storage_key()
        self.session_storage_value_started = config_parser.get_session_status_started()
        self.session_storage_value_stopped = config_parser.get_session_status_stopped()
        self.redirect_pattern = config_parser.get_redirect_pattern()

        self.docker_compose_up_wsl_cmd: str = docker_compose_up_wsl_cmd
        self.docker_compose_down_wsl_cmd: str = docker_compose_down_wsl_cmd
        self.wsl_command_executor = CommandExecutor()

    def docker_compose_up(self, request: HttpRequest) -> HttpResponse:
        log_info(self.docker_compose_up, f'Starting {self.service_name} service!')
        try:
            self.wsl_command_executor.execute_command(self.docker_compose_up_wsl_cmd)
        except Exception as e:
            log_error_traceback(self.docker_compose_up)
            raise StartingContainerFailed(self.docker_compose_up, str(e), self.service_name) from e
        else:
            self.set_container_status(request, self.session_storage_value_started)
            log_info(self.docker_compose_up, f'Starting {self.service_name} container - Done!')
            return redirect(self.redirect_pattern)

    def docker_compose_down(self, request: HttpRequest) -> HttpResponse:
        log_info(self.docker_compose_down, f'Stopping {self.service_name} container!')
        try:
            self.wsl_command_executor.execute_command(self.docker_compose_down_wsl_cmd)
        except Exception as e:
            log_error_traceback(self.docker_compose_down)
            raise StoppingContainerFailed(self.docker_compose_down, str(e), self.service_name) from e
        else:
            self.set_container_status(request, self.session_storage_value_stopped)
            log_info(self.docker_compose_down, f'Stopping {self.service_name} container - Done!')
            return redirect(self.redirect_pattern)

    def set_container_status(self, request: HttpRequest, session_storage_value: str) -> None:
        request.session[self.service_session_storage_key] = session_storage_value


    def docker_compose_up_without_http(self) -> None:
        log_info(self.docker_compose_up_without_http, f'Starting {self.service_name} service without impact on UI!')
        try:
            self.wsl_command_executor.execute_command(self.docker_compose_up_wsl_cmd)
        except Exception as e:
            log_error_traceback(self.docker_compose_up)
            raise StartingContainerFailed(self.docker_compose_up, str(e), self.service_name) from e
        else:
            log_info(self.docker_compose_up, f'Starting {self.service_name} container - Done!')
            return redirect(self.redirect_pattern)