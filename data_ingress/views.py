from typing import Dict

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View

from data_ingress.common.dummy_data.timestamp_generator import RealTimestampGenerator
from data_ingress.common.logging_.to_log_file import log_info, log_error, log_error_traceback
from common.database_models.database_table_clearner import DbTableCleaner
from data_ingress.views_helper.view_context_builder import ViewContextBuilder
from data_ingress.views_helper.view_exceptions import ClearingDatabaseFailed

class DataIngressView(View):
    def __init__(self):
        super().__init__()
        self.timestamp_generator: RealTimestampGenerator = RealTimestampGenerator()

    def get(self, request: HttpRequest) -> HttpResponse:
        log_info(self.get, 'START! / REFRESH!')
        context_builder = ViewContextBuilder(request, self.timestamp_generator)
        context: Dict = context_builder.build_context()
        return render(request, 'data_ingress_main.html', context)


class DataIngressClearView(View):
    def __init__(self):
        super().__init__()
        self.timestamp_generator: RealTimestampGenerator = RealTimestampGenerator()

    def post(self, request: HttpRequest) -> HttpResponse:
        log_info(self.post, 'Clear table')
        context_builder = ViewContextBuilder(request, self.timestamp_generator)
        db_table_clearner = DbTableCleaner()
        try:
            if context_builder.check_button_clean_all_tables_click(request):
                db_table_clearner.clear_all_tables_in_db()
            elif context_builder.check_button_clean_all_tables_click(request):
                db_table_clearner.clear_metrics_tables_in_db()
            else:
                log_error_traceback(DataIngressClearView)
                log_error(DataIngressClearView, 'Error during triggering the tables cleaning.')
            context: Dict = context_builder.build_context()

        except Exception as e:
                raise ClearingDatabaseFailed(str(e), self.post)

        return render(request, 'data_ingress_main.html', context)
