from typing import Dict

from django.http import HttpRequest, HttpResponse

from streaming_app.config import containers_config
from data_ingress.container_control.common.docker_service_monitor import DockerServiceMonitor
from data_ingress.container_control.common.docker_service_controller import DockerServiceController


class KafkaDockerServiceController:
    def __init__(self):
        self.kafka_service_data: Dict = containers_config.kafka_service_data

        self.kafka_docker_compose_up_wsl_cmd: str = containers_config.kafka_docker_compose_up_wsl_cmd
        self.kafka_docker_compose_down_wsl_cmd: str = containers_config.kafka_docker_compose_down_wsl_cmd

        self.container_controller = DockerServiceController(self.kafka_service_data, self.kafka_docker_compose_up_wsl_cmd,
                                                            self.kafka_docker_compose_down_wsl_cmd)

        self.docker_service_monitor = DockerServiceMonitor(self.kafka_service_data)

    def get_kafka_docker_service_status(self) -> bool:
        return self.docker_service_monitor.get_service_status_from_containers()

    def get_kafka_containers_statuses_for_service(self) -> Dict[str, bool]:
        return self.docker_service_monitor.get_containers_statuses_for_service()

    def start_kafka_docker_service(self, request: HttpRequest) -> HttpResponse:
        return self.container_controller.docker_compose_up(request)

    def stop_kafka_docker_service(self, request: HttpRequest) -> HttpResponse:
        return self.container_controller.docker_compose_down(request)


kafka_docker_service_controller = KafkaDockerServiceController()
