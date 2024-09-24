from typing import Tuple, Dict, Optional

from django.http import HttpRequest

from data_ingress.common.dummy_data.timestamp_generator import TimestampGenerator
from data_ingress.common.logging_.to_log_file import log_debug
from data_ingress.common.windows_operations.windows_actions_handler import WindowsActionsHandler
from streaming_app.config.tcp_config import port


class ContextBuilder:
    def __init__(self):
        self.timestamp_utility = TimestampGenerator()
        self.windows_actions_handler = WindowsActionsHandler()

        self.tcp_port = port

    def build_context(self, data_generation_status: str, data_collection_status: bool, kafka_container_status: bool,
                      button_clicked: Optional[bool], click_time: Optional[str]) -> Dict:

        context_dict = {
            'data_generation_message': self.get_data_generation_message(data_generation_status),
            'data_generation_status': data_generation_status,
            'kafka_container_message': self.get_kafka_container_message(kafka_container_status),
            'kafka_container_status': self.get_kafka_container_status(kafka_container_status),
            'data_collection_message': self.get_data_collection_message(data_collection_status),
            'data_collection_status': self.get_data_collection_status(data_collection_status),
            'button_clicked': button_clicked,
            'click_time': click_time,  # to be improved
        }
        log_debug(self.build_context, f'context: {str(context_dict)}')
        return context_dict

    def get_data_generation_status(self) -> str:  # to improve
        is_data_generated = self.windows_actions_handler.check_TCP_port_data_generation_with_retries(self.tcp_port)
        return 'started' if is_data_generated else 'stopped'

    def get_kafka_container_status(self, is_kafka_container_running: bool) -> str:
        return 'started' if is_kafka_container_running == True else 'stopped'

    def get_data_collection_status(self, data_collection_status: bool) -> str:
        return 'started' if data_collection_status == True else 'stopped'

    def check_button_click(self, request: HttpRequest) -> Tuple[bool, Optional[str]]:
        button_clicked = False
        click_time = None
        if request.method == 'POST' and 'action' in request.POST:
            action = request.POST['action']
            if action == 'click':
                button_clicked = True
                click_time = self.timestamp_utility.get_formatted_timestamp()
                log_debug(self.check_button_click, f'button_clicked: {str(button_clicked)}')
        return button_clicked, click_time

    def get_data_generation_message(self, status: str) -> str:
        return 'Streaming is ongoing!' if status == 'started' else 'Streaming is NOT started!'

    def get_kafka_container_message(self, kafka_container_status: bool) -> str:
        return 'Kafka container is NOT running!' if kafka_container_status == False else 'Kafka container is running!'

    def get_data_collection_message(self, is_tcp_opened: bool) -> str:
        return 'Data Collection is NOT started!' if is_tcp_opened == False else 'Data Collection is started!'
