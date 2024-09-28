from typing import Dict

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View

from data_ingress.common.dummy_data.timestamp_generator import RealTimestampGenerator
from data_ingress.common.logging_.to_log_file import log_info
from data_ingress.database_handling.postgresql_operations import PostgresqlHandler
from data_ingress.views_helper.context_builder import ContextBuilder
from data_ingress.views_helper.view_exceptions import ClearingDatabaseFailed


class DataIngressView(View):
    def __init__(self):
        super().__init__()
        self.timestamp_generator: RealTimestampGenerator = RealTimestampGenerator()

    def get(self, request: HttpRequest) -> HttpResponse:
        log_info(self.get, 'START! / REFRESH!')
        context_builder = ContextBuilder(request, self.timestamp_generator)
        context: Dict = context_builder.build_context()
        return render(request, 'data_ingress_main.html', context)


class DataIngressClearView(View):
    def __init__(self):
        super().__init__()
        self.postgresql_handler = PostgresqlHandler()
        self.timestamp_generator: RealTimestampGenerator = RealTimestampGenerator()

    def post(self, request: HttpRequest) -> HttpResponse:
        log_info(self.post, 'Clear table')
        context_builder = ContextBuilder(request, self.timestamp_generator)

        try:
            if context_builder.check_button_click(request):
                self.postgresql_handler.clear_table()
            context: Dict = context_builder.build_context()
        except Exception as e:
            raise ClearingDatabaseFailed(str(e), self.post)

        return render(request, 'data_ingress_main.html', context)
