import logging

from streaming_app.config import tcp_config
from data_ingress.tcp_operations.tcp_server import check_tcp_socket
from django.shortcuts import render
from data_ingress.kafka.kafka_container_control import kafka_container_check

logger = logging.getLogger('streaming_app')


def control_panel(request):
    log_start(control_panel.__name__)

    tcp_status = check_tcp_socket(tcp_config.server_host, tcp_config.port)
    kafka_status = kafka_container_check()
    streaming_status = request.session.get('streaming_status', 'stopped')

    log_debug(control_panel.__name__, 'streaming_status', streaming_status)

    context = build_context(streaming_status, kafka_status, tcp_status)

    log_debug(control_panel.__name__, 'context', context)

    return render(request, 'data_ingress.html', context)


def log_start(function_name):
    logger.info(f'{function_name} -> START! / REFRESH!')


def log_debug(function_name, variable_name, value):
    logger.debug(f'{function_name} -> {variable_name}: {value}')


def get_streaming_message(status):
    return 'Streaming is ongoing!' if status == 'started' else 'Streaming is NOT started!'


def get_kafka_message(is_kafka_running):
    if is_kafka_running:
        return 'Kafka container is running!', 'started'
    else:
        return 'Kafka container is NOT running', 'stopped'


def get_tcp_message(is_tcp_opened):
    if is_tcp_opened:
        return 'Data Collection is started!', 'started'
    else:
        return 'Data Collection is NOT started!', 'stopped'


def build_context(streaming_status, is_kafka_running, is_tcp_opened):
    streaming_message = get_streaming_message(streaming_status)
    kafka_message, kafka_container_status = get_kafka_message(is_kafka_running)
    tcp_server_message, tcp_server_status = get_tcp_message(is_tcp_opened)

    return {
        'streaming_message': streaming_message,
        'kafka_message': kafka_message,
        'tcp_server_message': tcp_server_message,
        'streaming_status': streaming_status,
        'kafka_container_status': kafka_container_status,
        'tcp_server_status': tcp_server_status
    }
