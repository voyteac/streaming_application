import logging
import subprocess
import time
import socket
import traceback
from django.shortcuts import redirect
from streaming_app.config import kafka_config
from data_ingress.kafka.wsl_operations import execute_command_on_wsl

logger = logging.getLogger('streaming_app')


def kafka_container_check():
    # logger.info(f'{kafka_container_check.__name__} -> Checking kafka container status.')
    running_containers_status = get_running_docker_container_status()
    is_kafka_container_running = check_kafka_environment_status(running_containers_status)
    if is_kafka_container_running:
        # logger.info(f'{kafka_container_check.__name__} -> Checking kafka container status - Running!')
        return True
    else:
        # logger.info(f'{kafka_container_check.__name__} -> Checking kafka container status  - Not Running!')
        return False


def get_running_docker_container_status():
    # logger.info(f'{get_running_docker_container_status.__name__} -> Get running Kafka container status')

    result = execute_command_on_wsl(kafka_config.wsl_command_to_get_container_status)
    containers_lines = result.stdout.strip().split('\n')

    # logger.debug(f'{get_running_docker_container_status.__name__} -> Containers_lines: {containers_lines}')

    containers_status = conclude_container_status_from_output(containers_lines)

    # logger.info(f'{get_running_docker_container_status.__name__} -> Container status is : {containers_status}')
    return containers_status


def conclude_container_status_from_output(containers_lines):
    containers_status = {}
    if (any(kafka_config.kafka_container_name in line for line in containers_lines) and any(
            kafka_config.zookeeper_container_name in line for line in containers_lines)):
        for line in containers_lines:
            name, status = line.split(': ')
            containers_status[name] = 'Up' in status
            logger.debug(f'{get_running_docker_container_status.__name__} -> name: {name}, status: {status}')
    else:
        containers_status = {
            kafka_config.kafka_container_name: False,
            kafka_config.zookeeper_container_name: False
        }
    return containers_status


def check_kafka_environment_status(running_containers_status):
    is_kafka_cont_running = running_containers_status[kafka_config.kafka_container_name]
    is_zookeeper_cont_running = running_containers_status[kafka_config.zookeeper_container_name]
    kafka_environment_status = is_kafka_cont_running and is_zookeeper_cont_running

    logger.debug(f'{check_kafka_environment_status.__name__} -> Is kafka running?: {is_kafka_cont_running}')
    logger.debug(f'{check_kafka_environment_status.__name__} -> Is zookeeper running?: {is_zookeeper_cont_running}')
    logger.debug(f'{check_kafka_environment_status.__name__} -> checking status: {kafka_environment_status}')
    return kafka_environment_status


def is_port_open(host, port, timeout=5):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        return result == 0


def start_kafka_container(request):
    logger.info(f'{start_kafka_container.__name__} -> Starting Kafka !')

    is_zookeeper_started = start_zookeeper_container()

    command_kafka = kafka_config.wsl_command_kafka
    try:
        if is_zookeeper_started:
            execute_command_on_wsl(command_kafka)
            request.session['kafka_container_status'] = 'started'
            logger.info(f'{start_kafka_container.__name__} -> Starting Kafka - Started!')
            return redirect('data-ingress')
        else:
            logger.error(f'{start_kafka_container.__name__} -> Kafka not started - problems with Zookeeper')
    except subprocess.CalledProcessError as e:
        logger.error(f'{start_kafka_container.__name__} -> Error occurred: {e.stderr.decode("utf-8")}')
        return None


def start_zookeeper_container():
    logger.info(f'{start_zookeeper_container.__name__} -> Starting Zookeeper !')

    zookeeper_host = kafka_config.zookeeper_host
    zookeeper_port = kafka_config.zookeeper_port
    command_zookeeper = kafka_config.wsl_command_zookeeper
    zookeeper_launch_retry_timer = kafka_config.zookeeper_launch_retry_timer
    max_retries = kafka_config.zookeeper_set_max_retries

    execute_command_on_wsl(command_zookeeper)

    retries = 0
    while retries < max_retries:
        if is_port_open(zookeeper_host, zookeeper_port):
            logger.info(f'{start_zookeeper_container.__name__} -> Zookeeper is running.')
            return True
        logger.debug(
            f'{start_zookeeper_container.__name__} -> Waiting for Zookeeper... (attempt {retries + 1}/{max_retries})')
        time.sleep(zookeeper_launch_retry_timer)
        retries += 1
    else:
        logger.error(f'{start_zookeeper_container.__name__} -> Zookeeper failed to start in time.')
        return False


def stop_kafka_container(request):
    logger.info(f'{stop_kafka_container.__name__} -> Stopping Kafka Container')

    cmd_result = execute_command_on_wsl(kafka_config.wsl_command_kafka_stop)
    if kafka_config.wsl_confirm_kafka_stopped in cmd_result.stdout.strip().split('\n'):
        request.session['kafka_container_status'] = 'stopped'
        logger.info(f'{stop_kafka_container.__name__} -> Stopping Kafka Container - Stopped')
    else:
        logger.error(f'{stop_kafka_container.__name__} -> Stopping Kafka Container - Not stopped - command output: {cmd_result}')
    return redirect('data-ingress')
