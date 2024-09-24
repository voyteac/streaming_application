from django.http import HttpResponse
from typing import Dict

from streaming_app.config import tcp_config
from data_ingress.tcp_operations.tcp_server import check_tcp_socket
from django.shortcuts import render
from data_ingress.kafka.kafka_container_control import kafka_container_check
from data_ingress.logging_.to_log_file import *
from data_ingress.views_helper.operation_status import *
from data_ingress.views_helper.ui_message import *


def data_ingress(request: HttpRequest) -> HttpResponse:
    log_info(data_ingress, 'START! / REFRESH!')

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
        'tcp_server_status': get_tcp_collection_status(is_tcp_opened),
        'button_clicked': button_clicked,
        'click_time': click_time,  # to be improved
    }
    log_debug(data_ingress, f'context: {str(context_dict)}')
    return context_dict



