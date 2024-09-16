import logging

from django.shortcuts import redirect
from streaming_app.config import kafka_config
from data_ingress.kafka.wsl_operations import execute_command_on_wsl

logger = logging.getLogger('streaming_app')


def kafka_container_check():
    logger.info(f'{kafka_container_check.__name__} -> Checking kafka container status.')
    running_containers_status = get_running_docker_container_status()
    is_kafka_container_running = check_kafka_environment_status(running_containers_status)
    if is_kafka_container_running:
        logger.info(f'{kafka_container_check.__name__} -> Checking kafka container status - Running!')
        return True
    else:
        logger.info(f'{kafka_container_check.__name__} -> Checking kafka container status  - Not Running!')
        return False


def get_running_docker_container_status():
    logger.info(f'{get_running_docker_container_status.__name__} -> Get running Kafka container status')

    result = execute_command_on_wsl(kafka_config.wsl_command_to_get_container_status)
    containers_lines = result.stdout.strip().split('\n')

    logger.debug(f'{get_running_docker_container_status.__name__} -> Containers_lines: {containers_lines}')

    containers_status = conclude_container_status_from_output(containers_lines)

    logger.info(f'{get_running_docker_container_status.__name__} -> Container status is : {containers_status}')
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


def start_kafka_container(request):
    logger.info(f'{start_kafka_container.__name__} -> Starting Kafka Container')

    execute_command_on_wsl(kafka_config.wsl_command_kafka_start)
    request.session['kafka_container_status'] = 'started'

    logger.info(f'{start_kafka_container.__name__} -> Starting Kafka Container - Started!')
    return redirect('control-panel')


def stop_kafka_container(request):
    logger.info(f'{stop_kafka_container.__name__} -> Stopping Kafka Container')

    execute_command_on_wsl(kafka_config.wsl_command_kafka_stop)
    request.session['kafka_container_status'] = 'stopped'

    logger.info(f'{stop_kafka_container.__name__} -> Stopping Kafka Container - Stopped')
    return redirect('control-panel')
