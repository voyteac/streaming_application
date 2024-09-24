import time
from typing import Dict, Optional, Callable
from typing import List
from subprocess import CompletedProcess

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from streaming_app.config import kafka_config
from data_ingress.kafka.wsl_operations import execute_command_on_wsl
from data_ingress.tcp_operations.tcp_helper import is_tcp_port_open
from data_ingress.logging_.to_log_file import log_debug, log_info, log_error, log_error_traceback, log_warning

kafka_container_name: str = kafka_config.kafka_container_name
zookeeper_container_name: str = kafka_config.zookeeper_container_name
wsl_command_kafka_start: str = kafka_config.wsl_command_kafka_start
zookeeper_host: str = kafka_config.zookeeper_host
zookeeper_port: int = kafka_config.zookeeper_port
wsl_command_zookeeper_start: str = kafka_config.wsl_command_zookeeper_start
zookeeper_launch_retry_timer: int = kafka_config.zookeeper_launch_retry_timer
max_retries: int = kafka_config.zookeeper_set_max_retries
wsl_command_kafka_stop: str = kafka_config.wsl_command_kafka_stop
wsl_confirm__string_kafka_stopped: str = kafka_config.wsl_confirm__string_kafka_stopped


class StartingContainerFailed(Exception):
    def __init__(self, function: Callable, exception_message: str, container_name: str):
        super().__init__(exception_message)
        self.function: Callable = function
        self.exception_message: str = exception_message
        self.container_name: str = container_name
        log_error(function, f'Starting {self.container_name} container- Failed! Error: {self.exception_message}')


def kafka_container_check() -> bool:
    running_containers_status: Dict = get_running_docker_container_status()
    if check_kafka_environment_status(running_containers_status):
        return True
    else:
        return False


def get_running_docker_container_status() -> Dict:
    result: CompletedProcess = execute_command_on_wsl(kafka_config.wsl_command_to_get_container_status)
    containers_lines: List[str] = result.stdout.strip().split('\n')
    containers_status: Dict = conclude_container_status_from_output(containers_lines)
    return containers_status


def conclude_container_status_from_output(containers_lines: List[str]) -> Dict:
    containers_status: Dict = {}
    is_kafka_container_up: bool = any(kafka_container_name in line for line in containers_lines)
    is_zookeeper_container_up: bool = any(zookeeper_container_name in line for line in containers_lines)
    if is_kafka_container_up and is_zookeeper_container_up:
        for line in containers_lines:
            name, status = line.split(': ')
            containers_status[name] = 'Up' in status
    else:
        containers_status = {
            kafka_container_name: False,
            zookeeper_container_name: False
        }
    log_debug(get_running_docker_container_status, f'containers_status: {containers_status}')
    return containers_status


def check_kafka_environment_status(running_containers_status: Dict) -> bool:
    is_kafka_cont_running: bool = running_containers_status[kafka_container_name]
    is_zookeeper_cont_running: bool = running_containers_status[zookeeper_container_name]
    kafka_environment_status: bool = is_kafka_cont_running and is_zookeeper_cont_running

    log_debug(check_kafka_environment_status, f'Is kafka running?: {is_kafka_cont_running}')
    log_debug(check_kafka_environment_status, f'Is zookeeper running?: {is_zookeeper_cont_running}')
    log_debug(check_kafka_environment_status, f'checking status: {kafka_environment_status}')

    return kafka_environment_status


def start_kafka_container(request: HttpRequest) -> Optional[HttpResponse]:
    log_info(start_kafka_container, 'Starting Kafka!')
    is_zookeeper_started: bool = start_zookeeper_container()
    try:
        if is_zookeeper_started:
            execute_command_on_wsl(wsl_command_kafka_start)
            log_info(start_kafka_container, 'Starting Kafka - Started!')
            set_kafka_container_status_to_started(request)
            return redirect('data-ingress')
        else:
            raise StartingContainerFailed(start_kafka_container,
                                          f'is_zookeeper_started: {is_zookeeper_started}',
                                          zookeeper_container_name)
    except Exception as e:
        log_error_traceback(start_kafka_container)
        raise StartingContainerFailed(start_kafka_container, str(e), kafka_container_name) from e


def set_kafka_container_status_to_started(request: HttpRequest) -> None:
    request.session['kafka_container_status'] = 'started'


def start_zookeeper_container() -> bool:
    log_info(start_kafka_container, 'Starting Zookeeper !')
    execute_command_on_wsl(wsl_command_zookeeper_start)
    retries: int = 0
    while retries < max_retries:
        if is_tcp_port_open(zookeeper_host, zookeeper_port):
            log_info(start_kafka_container, 'Zookeeper is running.')
            return True
        log_warning(start_zookeeper_container, f'Waiting for Zookeeper... (attempt {retries + 1}/{max_retries})')
        time.sleep(zookeeper_launch_retry_timer)
        retries += 1
    else:
        raise StartingContainerFailed(start_zookeeper_container,
                                      'Zookeeper failed to start in time.', zookeeper_container_name)


def stop_kafka_container(request: HttpRequest) -> HttpResponse:
    log_info(start_kafka_container, 'Stopping Kafka Container')
    cmd_result: CompletedProcess = execute_command_on_wsl(wsl_command_kafka_stop)
    if wsl_confirm__string_kafka_stopped in cmd_result.stdout.strip().split('\n'):
        set_kafka_container_status_to_stopped(request)
        log_info(stop_kafka_container, 'Stopping Kafka Container - Stopped')
    else:
        log_info(stop_kafka_container, 'Stopping Kafka Container - Not stopped - command output: {cmd_result}')
    return redirect('data-ingress')


def set_kafka_container_status_to_stopped(request: HttpRequest) -> None:
    request.session['kafka_container_status'] = 'stopped'
