import time
from typing import Dict, Optional, List
from subprocess import CompletedProcess

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from streaming_app.config import kafka_config

from data_ingress.common.logging_.to_log_file import log_debug, log_info, log_error_traceback, log_warning
from data_ingress.kafka_container_control.kafka_exceptions import (StartingContainerFailed,
                                                                   ErrorDuringCheckingDockerEnvironmentForKafka)

from data_ingress.common.wsl_operations.wsl_commands import CommandExecutor
from data_ingress.common.tcp_operations.tcp_helper import TcpHelper

class KafkaContainerController:
    def __init__(self):
        self.kafka_container_name: str = kafka_config.kafka_container_name
        self.zookeeper_container_name: str = kafka_config.zookeeper_container_name
        self.wsl_command_kafka_start: str = kafka_config.wsl_command_kafka_start
        self.zookeeper_host: str = kafka_config.zookeeper_host
        self.zookeeper_port: int = kafka_config.zookeeper_port
        self.wsl_command_zookeeper_start: str = kafka_config.wsl_command_zookeeper_start
        self.zookeeper_launch_retry_timer: int = kafka_config.zookeeper_launch_retry_timer
        self.max_retries: int = kafka_config.zookeeper_set_max_retries
        self.wsl_command_kafka_stop: str = kafka_config.wsl_command_kafka_stop
        self.wsl_confirm__string_kafka_stopped: str = kafka_config.wsl_confirm__string_kafka_stopped

        self.tcp_helper = TcpHelper()
        self.wsl_command_executor = CommandExecutor()

    def get_kafka_container_status(self) -> bool:
        running_containers_status: Dict = self.get_running_docker_container_status()
        log_debug(self.get_kafka_container_status, f'running_containers_status: {running_containers_status}')
        if self.check_kafka_environment_status(running_containers_status):
            return True
        else:
            return False

    def get_running_docker_container_status(self) -> Dict:
        result: CompletedProcess = self.wsl_command_executor.execute_command(
            kafka_config.wsl_command_to_get_container_status)
        containers_lines: List[str] = result.stdout.strip().split('\n')
        log_debug(self.get_running_docker_container_status, f'containers_lines: {containers_lines}')
        containers_status: Dict = self.conclude_container_status_from_output(containers_lines)
        return containers_status

    def conclude_container_status_from_output(self, containers_lines: List[str]) -> Dict:
        containers_status: Dict = {}
        is_kafka_container_up: bool = any(self.kafka_container_name in line for line in containers_lines)
        is_zookeeper_container_up: bool = any(self.zookeeper_container_name in line for line in containers_lines)
        log_debug(self.conclude_container_status_from_output, f'is_kafka_container_up: {is_kafka_container_up}')
        log_debug(self.conclude_container_status_from_output, f'is_zookeeper_container_up: {is_zookeeper_container_up}')
        if is_kafka_container_up and is_zookeeper_container_up:
            for line in containers_lines:
                name, status = line.split(': ')
                containers_status[name] = 'Up' in status
        else:
            containers_status = {
                self.kafka_container_name: False,
                self.zookeeper_container_name: False
            }
        log_debug(self.get_running_docker_container_status, f'containers_status: {containers_status}')
        return containers_status

    def check_kafka_environment_status(self, running_containers_status: Dict) -> bool:
        try:
            is_kafka_cont_running: bool = running_containers_status[self.kafka_container_name]
            is_zookeeper_cont_running: bool = running_containers_status[self.zookeeper_container_name]
            kafka_environment_status: bool = is_kafka_cont_running and is_zookeeper_cont_running
        except Exception as e:
            raise ErrorDuringCheckingDockerEnvironmentForKafka(self.check_kafka_environment_status, str(e))
        else:
            log_debug(self.check_kafka_environment_status, f'Is kafka container running?: {is_kafka_cont_running}')
            log_debug(self.check_kafka_environment_status,
                      f'Is zookeeper container running?: {is_zookeeper_cont_running}')
            log_debug(self.check_kafka_environment_status, f'checking status: {kafka_environment_status}')
            return kafka_environment_status

    def start_kafka_container(self, request: HttpRequest) -> Optional[HttpResponse]:
        log_info(self.start_kafka_container, 'Starting Kafka!')
        is_zookeeper_started: bool = self.start_zookeeper_container()
        try:
            if is_zookeeper_started:
                self.wsl_command_executor.execute_command(self.wsl_command_kafka_start)
                log_info(self.start_kafka_container, 'Starting Kafka - Started!')
                self.set_kafka_container_status_to_started(request)
                return redirect('data-ingress')
            else:
                raise StartingContainerFailed(self.start_kafka_container,
                                              f'is_zookeeper_started: {is_zookeeper_started}',
                                              self.zookeeper_container_name)
        except Exception as e:
            log_error_traceback(self.start_kafka_container)
            raise StartingContainerFailed(self.start_kafka_container, str(e), self.kafka_container_name) from e

    def start_zookeeper_container(self) -> bool:
        log_info(self.start_kafka_container, 'Starting Zookeeper !')
        self.wsl_command_executor.execute_command(self.wsl_command_zookeeper_start)
        retries: int = 0
        while retries < self.max_retries:
            if self.tcp_helper.is_tcp_port_open(self.zookeeper_host, self.zookeeper_port):
                log_info(self.start_kafka_container, 'Zookeeper is running.')
                return True
            log_warning(self.start_zookeeper_container,
                        f'Waiting for Zookeeper... (attempt {retries + 1}/{self.max_retries})')
            time.sleep(self.zookeeper_launch_retry_timer)
            retries += 1
        else:
            raise StartingContainerFailed(self.start_zookeeper_container,
                                          'Zookeeper failed to start in time.', self.zookeeper_container_name)

    def stop_kafka_container(self, request: HttpRequest) -> HttpResponse:
        log_info(self.start_kafka_container, 'Stopping Kafka Container')
        cmd_result: CompletedProcess = self.wsl_command_executor.execute_command(self.wsl_command_kafka_stop)
        if self.wsl_confirm__string_kafka_stopped in cmd_result.stdout.strip().split('\n'):
            self.set_kafka_container_status_to_stopped(request)
            log_info(self.stop_kafka_container, 'Stopping Kafka Container - Stopped')
        else:
            log_info(self.stop_kafka_container, 'Stopping Kafka Container - Not stopped - command output: {cmd_result}')
        return redirect('data-ingress')

    def set_kafka_container_status_to_stopped(self, request: HttpRequest) -> None:
        request.session['kafka_container_status'] = 'stopped'

    def set_kafka_container_status_to_started(self, request: HttpRequest) -> None:
        request.session['kafka_container_status'] = 'started'


kafka_container_controller = KafkaContainerController()