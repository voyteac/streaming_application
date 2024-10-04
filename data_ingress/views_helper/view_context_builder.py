from typing import Protocol, Dict

from common.logging_.to_log_file import log_debug


from django.http import HttpRequest
from data_ingress.common.tcp_operations.tcp_helper import TcpHelper
from data_ingress.container_control.common.docker_service_config_json_parser import DockerServiceConfigJsonParser
from data_ingress.container_control.kafka_docker_service_controller import kafka_docker_service_controller
from data_ingress.container_control.postgres_docker_service_controller import postgres_docker_service_controller
from data_ingress.container_control.elk_docker_service_controller import elk_docker_service_controller
from streaming_app.config import containers_config
from data_ingress.container_control.common import docker_service_config_json_parser


class TimestampGenerator(Protocol):
    def get_formatted_timestamp(self) -> str:
        """format timestamp"""


class ViewContextBuilder:
    def __init__(self, request: HttpRequest, timestamp_generator: TimestampGenerator):

        self.timestamp_generator = timestamp_generator
        self.tcp_helper = TcpHelper()

        data_collection_data = containers_config.data_collection
        data_generation_data = containers_config.data_generation
        kafka_docker_service_data = containers_config.kafka_service_data
        elk_docker_service_data = containers_config.elk_service_data
        postgres_docker_service_data = containers_config.postgres_service_data

        self.data_collection_config = docker_service_config_json_parser.DockerServiceConfigJsonParser(data_collection_data)
        self.data_generation_config = docker_service_config_json_parser.DockerServiceConfigJsonParser(data_generation_data)
        self.kafka_config = docker_service_config_json_parser.DockerServiceConfigJsonParser(kafka_docker_service_data)
        self.elk_config = docker_service_config_json_parser.DockerServiceConfigJsonParser(elk_docker_service_data)
        self.postgres_config = docker_service_config_json_parser.DockerServiceConfigJsonParser(postgres_docker_service_data)

        self.data_generation_status: bool = self.tcp_helper.check_TCP_port_data_generation_with_retries()
        self.data_collection_status: bool = self.tcp_helper.check_tcp_socket()
        self.kafka_docker_service_status: bool = kafka_docker_service_controller.get_kafka_docker_service_status()
        self.postgres_docker_service_status: bool = postgres_docker_service_controller.get_postgres_docker_service_status()
        self.elk_docker_service_status: bool = elk_docker_service_controller.get_elk_docker_service_status()

        self.kafka_containers_statuses: Dict[str, bool] = kafka_docker_service_controller.get_kafka_containers_statuses_for_service()
        self.postgres_containers_statuses: Dict[str, bool] = postgres_docker_service_controller.get_postgres_containers_statuses_for_service()
        self.elk_containers_statuses: Dict[str, bool] = elk_docker_service_controller.get_elk_containers_statuses_for_service()

        self.button_clicked_clean_all_tables = self.check_button_clean_all_tables_click(request)
        self.button_clicked_clean_metrics_tables = self.check_button_clean_metrics_tables_click(request)
        self.click_time = self.timestamp_generator.get_formatted_timestamp()


    def build_context(self) -> Dict:
        context_dict = {

            'data_generation_message': self.get_docker_service_message(self.data_generation_status, self.data_generation_config),
            'data_collection_message': self.get_docker_service_message(self.data_collection_status, self.data_collection_config),
            'kafka_docker_service_message': self.get_docker_service_message(self.kafka_docker_service_status, self.kafka_config),
            'postgres_docker_service_message': self.get_docker_service_message(self.postgres_docker_service_status, self.postgres_config),
            'elk_docker_service_message': self.get_docker_service_message(self.elk_docker_service_status, self.elk_config),

            'data_generation_status': self.get_session_value_for_service_status(self.data_generation_status, self.data_generation_config),
            'data_collection_status': self.get_session_value_for_service_status(self.data_collection_status, self.data_collection_config),
            'kafka_docker_service_status': self.get_session_value_for_service_status(self.kafka_docker_service_status, self.kafka_config),
            'postgres_docker_service_status': self.get_session_value_for_service_status(self.postgres_docker_service_status, self.postgres_config),
            'elk_docker_service_status': self.get_session_value_for_service_status(self.elk_docker_service_status, self.elk_config),

            'kafka_containers_statuses': self.kafka_containers_statuses,
            'postgres_containers_statuses': self.postgres_containers_statuses,
            'elk_containers_statuses': self.elk_containers_statuses,

            'button_clicked_all': self.button_clicked_clean_all_tables,
            'button_clicked_metrics': self.button_clicked_clean_metrics_tables,
            'click_time': self.click_time,  # to be improved

        }
        log_debug(self.build_context, f'context: {str(context_dict)}')

        return context_dict

    def get_session_value_for_service_status(self, status: bool, config: DockerServiceConfigJsonParser) -> str:
        return config.get_session_status_stopped() if not status else config.get_session_status_started()

    def get_docker_service_message(self, status: bool, config: DockerServiceConfigJsonParser) -> str:
        return config.get_ui_message_down() if not status else config.get_ui_message_up()

    def check_button_clean_all_tables_click(self, request: HttpRequest) -> bool:
        button_clicked = False
        if request.method == 'POST' and 'all' in request.POST:
            action = request.POST['all']
            if action == 'click':
                button_clicked = True
                log_debug(self.check_button_clean_all_tables_click, f'button_clicked: {str(button_clicked)}')
        return button_clicked

    def check_button_clean_metrics_tables_click(self, request: HttpRequest) -> bool:
        button_clicked = False
        if request.method == 'POST' and 'metrics' in request.POST:
            action = request.POST['metrics']
            if action == 'click':
                button_clicked = True
                log_debug(self.check_button_clean_all_tables_click, f'button_clicked: {str(button_clicked)}')
        return button_clicked






