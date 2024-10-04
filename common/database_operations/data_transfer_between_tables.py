from typing import Any, Type

from django.db import models
from django.db import transaction
from django.db.models import Model

from common.database_models.get_list_of_models import get_metric_name_for_model
from common.database_models.get_target_model_definition_for_metric_table import get_target_model_definition_for_metric_table
from data_ingress.models import MetricsDataModelsLoader


def copy_data_from_main_to_metric_table() -> None:
    metrics = get_metric_name_for_model()
    for metric_class, metric_name in metrics:
        update_analysis_tables(MetricsDataModelsLoader, metric_class, metric_name)


def update_analysis_tables(SourceModel: Type[models.Model], TargetModel: Type[models.Model],
                           metric_name: str) -> None:
    target_records, records_to_update = get_records_from_table(SourceModel, TargetModel, metric_name)

    try:
        if target_records:
            with transaction.atomic():
                TargetModel.objects.bulk_create(target_records)
        if records_to_update:
            update_missing_rows(records_to_update, TargetModel, metric_name)

    except Exception as e:
        print(f"An error occurred: {e}")


def get_records_from_table(SourceModel: Type[models.Model], TargetModel: Type[models.Model],
                           metric_name: str) -> [list[Model] | list[Any]]:
    target_records = []
    records_to_update = []

    existing_ids = set(TargetModel.objects.values_list('internal_unique_client_id', flat=True))
    source_records = SourceModel.objects.all()

    for record in source_records:
        if record.internal_unique_client_id not in existing_ids:
            target_model = get_target_model_definition_for_metric_table(TargetModel, record, metric_name)
            target_records.append(target_model)
        else:
            records_to_update.append(record)
    return target_records, records_to_update


def update_missing_rows(records_to_update: list, TargetModel: Type[models.Model], metric_name: str) -> None:
    target_ids = set(TargetModel.objects.values_list('internal_unique_client_id', flat=True))
    target_records_to_add = []

    for record in records_to_update:
        if record.internal_unique_client_id not in target_ids:
            target_model = get_target_model_definition_for_metric_table(TargetModel, record, metric_name)
            target_records_to_add.append(target_model)

    if target_records_to_add:
        TargetModel.objects.bulk_create(target_records_to_add)


# if __name__ == '__main__':
#     main()

