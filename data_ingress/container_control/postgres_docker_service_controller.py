from typing import Dict


from streaming_app.config import containers_config
from data_ingress.container_control.common.docker_service_monitor import DockerServiceMonitor
from data_ingress.container_control.common.docker_service_controller import DockerServiceController

class PostgresDockerServiceController:
    def __init__(self):
        self.postgres_service_data: Dict = containers_config.postgres_service_data

        self.postgres_docker_compose_up_cmd: str = containers_config.postgres_docker_compose_up_cmd
        self.postgres_docker_compose_down_cmd: str = containers_config.postgres_docker_compose_down_cmd

        self.container_controller = DockerServiceController(self.postgres_service_data,
                                                            self.postgres_docker_compose_up_cmd,
                                                            self.postgres_docker_compose_down_cmd)

        self.docker_service_monitor = DockerServiceMonitor(self.postgres_service_data)

    def get_postgres_docker_service_status(self) -> bool:
        return self.docker_service_monitor.get_service_status_from_containers()

    def get_postgres_containers_statuses_for_service(self) -> Dict[str, bool]:
        return self.docker_service_monitor.get_containers_statuses_for_service()

    def start_postgres_docker_service(self) -> None:
        return self.container_controller.docker_compose_up_without_http()


postgres_docker_service_controller = PostgresDockerServiceController()
