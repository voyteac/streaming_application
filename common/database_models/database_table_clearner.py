from typing import List, Callable
from django.db import transaction

from common.database_models.common_data_model import CommonDataModels
from common.database_models.get_list_of_models import get_metric_models_only, get_all_models
from data_ingress.common.logging_.to_log_file import log_error, log_info, log_error_traceback


class DbTableCleaner:

    def _clear_tables(self, models: List[CommonDataModels], method: Callable) -> None:
        for model in models:
            table_name = model._meta.db_table
            try:
                with transaction.atomic():  # Ensure data integrity
                    model.objects.all().delete()
                    if model.objects.count() == 0:
                        log_info(self._clear_tables, f'Table {table_name} has been truncated.')
                    else:
                        log_error(self._clear_tables, f'Table {table_name} was NOT cleaned.')
            except Exception as e:
                log_error_traceback(self._clear_tables)
                log_error(method, f'Error while clearing table {table_name}: {str(e)}')

    def clear_all_tables_in_db(self) -> None:
        all_models = get_all_models()
        self._clear_tables(all_models, self.clear_all_tables_in_db)

    def clear_metrics_tables_in_db(self) -> None:
        metric_models = get_metric_models_only()
        self._clear_tables(metric_models, self.clear_metrics_tables_in_db)

db_table_clearner = DbTableCleaner()
