from typing import Dict

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View

from data_ingress.common.dummy_data.timestamp_generator import TimestampGenerator
from data_ingress.common.logging_.to_log_file import log_info
from data_ingress.common.tcp_operations.tcp_helper import TcpHelper
from data_ingress.database_handling.postgresql_operations import PostgresqlHandler
from data_ingress.kafka_container_control.kafka_container_controller import kafka_container_controller
from data_ingress.views_helper.context_builder import ContextBuilder
from streaming_app.config import tcp_config



class DataIngressView(View):
    def __init__(self):
        super().__init__()
        self.tcp_helper = TcpHelper()
        timestamp_generator = TimestampGenerator()
        self.context_builder = ContextBuilder(timestamp_generator)
        self.server_host: str = tcp_config.server_host
        self.server_port: int = tcp_config.port

    def get(self, request: HttpRequest) -> HttpResponse:
        log_info(self.get, 'START! / REFRESH!')

        is_data_collection_started: bool = self.tcp_helper.check_tcp_socket(self.server_host, self.server_port)
        is_kafka_container_running: bool = kafka_container_controller.get_kafka_container_status()
        data_generation_status = self.context_builder.get_data_generation_status()

        button_clicked = self.context_builder.check_button_click(request)

        context: Dict = self.context_builder.build_context(data_generation_status, is_data_collection_started,
                                                           is_kafka_container_running, button_clicked)
        return render(request, 'data_ingress_main.html', context)


class DataIngressClearView(View):
    def __init__(self):
        super().__init__()
        self.tcp_helper = TcpHelper()
        timestamp_generator = TimestampGenerator()
        self.context_builder = ContextBuilder(timestamp_generator)
        self.postgresql_handler = PostgresqlHandler()
        self.server_host: str = tcp_config.server_host
        self.server_port: int = tcp_config.port

    def post(self, request: HttpRequest) -> HttpResponse:
        log_info(self.post, 'Clear table')

        button_clicked = self.context_builder.check_button_click(request)

        if button_clicked:
            self.postgresql_handler.clear_table()

        is_data_collection_started: bool = self.tcp_helper.check_tcp_socket(self.server_host, self.server_port)
        is_kafka_container_running: bool = kafka_container_controller.get_kafka_container_status()
        data_generation_status = self.context_builder.get_data_generation_status()

        context: Dict = self.context_builder.build_context(data_generation_status, is_data_collection_started,
                                                           is_kafka_container_running,
                                                           button_clicked)

        return render(request, 'data_ingress_main.html', context)
