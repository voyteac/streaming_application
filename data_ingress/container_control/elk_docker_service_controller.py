from typing import Dict

from django.http import HttpRequest, HttpResponse

from streaming_app.config import containers_config
from data_ingress.container_control.common.docker_service_monitor import DockerServiceMonitor
from data_ingress.container_control.common.docker_service_controller import DockerServiceController

class ElkDockerServiceController:
    def __init__(self):
        self.elk_service_data: Dict = containers_config.elk_service_data

        self.elk_docker_compose_up_wsl_cmd: str = containers_config.elk_docker_compose_up_wsl_cmd
        self.elk_docker_compose_down_wsl_cmd: str = containers_config.elk_docker_compose_down_wsl_cmd

        self.container_controller = DockerServiceController(self.elk_service_data, self.elk_docker_compose_up_wsl_cmd,
                                                            self.elk_docker_compose_down_wsl_cmd)

        self.docker_service_monitor = DockerServiceMonitor(self.elk_service_data)

    def get_elk_docker_service_status(self) -> bool:
        return self.docker_service_monitor.get_service_status_from_containers()

    def get_elk_containers_statuses_for_service(self) -> Dict[str, bool]:
        return self.docker_service_monitor.get_containers_statuses_for_service()

    def start_elk_docker_service(self, request: HttpRequest) -> HttpResponse:
        return self.container_controller.docker_compose_up(request)

    def stop_elk_docker_service(self, request: HttpRequest) -> HttpResponse:
        return self.container_controller.docker_compose_down(request)


elk_docker_service_controller = ElkDockerServiceController()
