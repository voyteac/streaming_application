import docker
from docker import DockerClient
from docker.errors import DockerException

from common.logging_.to_log_file import log_error
from streaming_app.config import containers_config


class DockerServiceMonitorHelper:
    def __init__(self):
        self.docker_host: str = containers_config.docker_host
        self.docker_port: str = containers_config.docker_port

    def check_container_status_up(self, container_name: str) -> bool:
        docker_client: DockerClient = self.create_docker_client()
        running_container_names_list: list = self.get_running_container_names_list(docker_client)
        if container_name in running_container_names_list:
            return True
        else:
            return False

    def create_docker_client(self) -> DockerClient:
        try:
            client = docker.DockerClient(base_url='unix://var/run/docker.sock')
            return client
        except DockerException as e:
            log_error(self.create_docker_client, f'Error communicating with Docker daemon: {e}')

    def get_running_container_names_list(self, docker_client: DockerClient) -> list:
        container_list: list = docker_client.containers.list(all=True, filters={'status': 'running'})
        running_container_names = [container.name for container in container_list]
        return running_container_names
