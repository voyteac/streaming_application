from typing import Tuple
from typing import Optional

from data_ingress.logging_.to_log_file import log_debug
from django.http import HttpRequest

from data_ingress.data_generator.time_data import get_formatted_timestamp
from data_ingress.database.postgresql_operations import clear_table


def get_streaming_status(request: HttpRequest) -> str:  # to improve
    streaming_status: str = request.session.get('streaming_status', 'stopped')
    log_debug(get_streaming_status, f'streaming_status: {streaming_status}')
    return streaming_status


def get_kafka_container_status(is_kafka_running: bool) -> str:
    return 'started' if is_kafka_running == True else 'stopped'


def get_tcp_collection_status(is_tcp_opened: bool) -> str:
    return 'started' if is_tcp_opened == True else 'stopped'


def was_button_clicked(request: HttpRequest) -> Tuple[bool, Optional[str]]:
    button_clicked = False
    click_time = None
    if request.method == 'POST' and 'action' in request.POST:
        action = request.POST['action']
        if action == 'click':
            button_clicked = True
            click_time = get_formatted_timestamp()
            clear_table()
            log_debug(was_button_clicked, f'button_clicked: {str(button_clicked)}')
    return button_clicked, click_time
