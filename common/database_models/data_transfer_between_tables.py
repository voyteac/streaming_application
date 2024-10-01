from typing import Type, List, Tuple, Any
from django.db import models
from django.db import transaction
from django.db.models import Model


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
            target_model = get_target_model_definition(TargetModel, record, metric_name)
            target_records.append(target_model)
        else:
            records_to_update.append(record)
    return target_records, records_to_update


def update_missing_rows(records_to_update: list, TargetModel: Type[models.Model], metric_name: str) -> None:
    target_ids = set(TargetModel.objects.values_list('internal_unique_client_id', flat=True))
    target_records_to_add = []

    for record in records_to_update:
        if record.internal_unique_client_id not in target_ids:
            target_model = get_target_model_definition(TargetModel, record, metric_name)
            target_records_to_add.append(target_model)

    if target_records_to_add:
        TargetModel.objects.bulk_create(target_records_to_add)


def get_target_model_definition(TargetModel: Type[models.Model], record: models.Model, metric_name) -> Model:
    internal_unique_client_id = getattr(record, 'internal_unique_client_id')
    unique_client_id = getattr(record, 'unique_client_id')
    date = getattr(record, 'date')
    time = getattr(record, 'time')
    message_number = getattr(record, 'message_number')
    client_name = getattr(record, 'client_name')
    metric_value = getattr(record, metric_name)

    return TargetModel(
            internal_unique_client_id=internal_unique_client_id,
            unique_client_id=unique_client_id,
            date=date,
            time=time,
            message_number=message_number,
            client_name=client_name,
            metric_value=metric_value
        )

