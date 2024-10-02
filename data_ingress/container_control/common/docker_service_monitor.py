from typing import List
from typing import Dict
from common.logging_.to_log_file import log_info
from data_ingress.container_control.common.docker_service_config_json_parser import DockerServiceConfigJsonParser
from .docker_service_monitor_helper import DockerServiceMonitorHelper

class DockerServiceMonitor:
    def __init__(self, service_data):
        self.service_data: Dict = service_data
        self.genericMonitor = DockerServiceMonitorHelper()

        config_parser = DockerServiceConfigJsonParser(self.service_data)
        self.containers_names_from_service: List[str] = config_parser.get_containers_names()

    def get_service_status_from_containers(self) -> bool:
        containers_statuses: List[bool] = []
        for container in self.containers_names_from_service:
            cont_status = self.genericMonitor.check_container_status_up(container)
            containers_statuses.append(cont_status)
        service_status = all(containers_statuses)
        containers_statuses_str: list = [f'Containers status: {name}: {status} ' for name, status in
                                         zip(self.containers_names_from_service, containers_statuses)]
        log_info(self.get_service_status_from_containers,
                  f'Service status is: {service_status}. {containers_statuses_str}')
        return service_status

    def get_containers_statuses_for_service(self) -> Dict[str, bool]:
        containers_statuses: List[bool] = []
        containers_names_from_service = self.remove_container_heleper(self.containers_names_from_service)
        for container in containers_names_from_service:
            cont_status = self.genericMonitor.check_container_status_up(container)
            containers_statuses.append(cont_status)
        containers_statuses_str: dict = {char: status for char, status in zip(containers_names_from_service, containers_statuses)}
        return containers_statuses_str

    def remove_container_heleper(self, containers: List[str]) -> List[str]: # to improve!
        containers.remove('elk_setup') if 'elk_setup' in containers else containers
        return containers

