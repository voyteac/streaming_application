from django.http import HttpRequest, HttpResponse
from typing import Tuple
from typing import Optional
from typing import Dict

from streaming_app.config import tcp_config
from data_ingress.tcp_operations.tcp_server import check_tcp_socket
from data_ingress.tcp_operations.data_generator import get_formatted_timestamp
from django.shortcuts import render
from data_ingress.kafka.kafka_container_control import kafka_container_check
from data_ingress.database.postgresql_operations import clear_table
from data_ingress.logging_.to_log_file import log_debug, log_info

def data_ingress(request: HttpRequest) -> HttpResponse:
    log_info(data_ingress.__name__, 'START! / REFRESH!')

    tcp_status: bool = check_tcp_socket(tcp_config.server_host, tcp_config.port)
    kafka_status: bool = kafka_container_check()
    streaming_status: str = get_streaming_status(request)
    button_clicked: bool
    click_time: Optional[str]
    button_clicked, click_time = was_button_clicked(request)

    context: Dict = build_context(streaming_status, kafka_status, tcp_status, button_clicked, click_time)

    return render(request, 'data_ingress.html', context)


def build_context(streaming_status: str, is_kafka_running: bool, is_tcp_opened: bool, button_clicked: bool,
                  click_time: Optional[str]) -> Dict:
    context_dict = {
        'streaming_message': get_streaming_message(streaming_status),
        'streaming_status': streaming_status,
        'kafka_message': get_kafka_message(is_kafka_running),
        'kafka_container_status': get_kafka_container_status(is_kafka_running),
        'tcp_server_message': get_tcp_message(is_tcp_opened),
        'tcp_server_status': get_tcp_collection_status_for_ui(is_tcp_opened),
        'button_clicked': button_clicked,
        'click_time': click_time,  # to be improved
    }
    log_debug(data_ingress.__name__, f'context: {str(context_dict)}')
    return context_dict


def get_streaming_message(status: str) -> str:
    return 'Streaming is ongoing!' if status == 'started' else 'Streaming is NOT started!'


def get_streaming_status(request: HttpRequest) -> str:  # to improve
    streaming_status: str = request.session.get('streaming_status', 'stopped')
    log_debug(data_ingress.__name__, f'streaming_status: {streaming_status}')
    return streaming_status


def get_kafka_message(is_kafka_running: bool) -> str:
    if is_kafka_running:
        return 'Kafka container is running!'
    else:
        return 'Kafka container is NOT running'


def get_kafka_container_status(is_kafka_running: bool) -> str:
    if is_kafka_running:
        return 'started'
    else:
        return 'stopped'


def get_tcp_message(is_tcp_opened: bool) -> str:
    if is_tcp_opened:
        return 'Data Collection is started!'
    else:
        return 'Data Collection is NOT started!'


def get_tcp_collection_status_for_ui(is_tcp_opened: bool) -> str:
    if is_tcp_opened:
        return 'started'
    else:
        return 'stopped'


def was_button_clicked(request: HttpRequest) -> Tuple[bool, Optional[str]]:
    button_clicked = False
    click_time = None
    if request.method == 'POST' and 'action' in request.POST:
        action = request.POST['action']
        if action == 'click':
            button_clicked = True
            click_time = get_formatted_timestamp()
            clear_table()
            log_debug(data_ingress.__name__, f'button_clicked: {str(button_clicked)}')
    return button_clicked, click_time
