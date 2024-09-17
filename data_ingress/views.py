import logging

from streaming_app.config import tcp_config
from data_ingress.tcp_operations.tcp_server import check_tcp_socket
from data_ingress.tcp_operations.data_generator import get_formatted_timestamp
from django.shortcuts import render
from data_ingress.kafka.kafka_container_control import kafka_container_check
from data_ingress.database.postgresql_operations import clear_table


logger = logging.getLogger('streaming_app')


def data_ingress(request):
    log_start(data_ingress.__name__)

    tcp_status = check_tcp_socket(tcp_config.server_host, tcp_config.port)
    kafka_status = kafka_container_check()
    streaming_status = request.session.get('streaming_status', 'stopped')

    log_debug(data_ingress.__name__, 'streaming_status', streaming_status)

    button_clicked, click_time = was_button_clicked(request)

    log_debug(data_ingress.__name__, 'button_clicked', button_clicked)

    context = build_context(streaming_status, kafka_status, tcp_status, button_clicked, click_time)

    log_debug(data_ingress.__name__, 'context: ', context)

    return render(request, 'data_ingress.html', context)

def was_button_clicked(request):
    button_clicked = False
    click_time = None
    if request.method == 'POST' and 'action' in request.POST:
        action = request.POST['action']
        if action == 'click':
            button_clicked = True
            click_time = get_formatted_timestamp()
            clear_table()
    return button_clicked, click_time

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


def build_context(streaming_status, is_kafka_running, is_tcp_opened, button_clicked, click_time):
    streaming_message = get_streaming_message(streaming_status)
    kafka_message, kafka_container_status = get_kafka_message(is_kafka_running)
    tcp_server_message, tcp_server_status = get_tcp_message(is_tcp_opened)

    return {
        'streaming_message': streaming_message,
        'kafka_message': kafka_message,
        'tcp_server_message': tcp_server_message,
        'streaming_status': streaming_status,
        'kafka_container_status': kafka_container_status,
        'tcp_server_status': tcp_server_status,
        'button_clicked': button_clicked,
        'click_time': click_time, # to be improved
    }

def action_on_click():
    print("DUPA!")