from typing import List, Type

from django.db import models
from django.db.models import QuerySet
from data_analysis.analysis.analyzer_helper import AnalyzerHelper


helper = AnalyzerHelper()

def insert_values_to_anomaly_column(model: Type[models.Model], detected_anomalies: List) -> None:
    for anomaly in detected_anomalies:
        rows_to_update = model.objects.filter(**{"message_number": anomaly})
        for row in rows_to_update:
            value_to_copy = getattr(row, "metric_value")
            setattr(row, "is_anomaly", value_to_copy)
            row.save()


def insert_values_to_margin_column(Model: Type[models.Model], generator_id: int,
                                   value_list_to_insert: List[float], target_column_name: str, window_size: int) -> None:


    prepared_value_list_to_insert: List[float] = helper.fill_in_margins_bound_values(value_list_to_insert, window_size)

    metrics: QuerySet = Model.objects.filter(unique_client_id=generator_id)
    existing_count = len(metrics)
    if existing_count == 0:
        copy_values_to_column(Model, prepared_value_list_to_insert, generator_id, target_column_name)
        return
    else:
        # Model.objects.update(**{target_column_name: None})
        copy_values_to_column(Model, prepared_value_list_to_insert, generator_id, target_column_name)
    return


def copy_values_to_column(Model: Type[models.Model], value_list_to_insert: List[float], generator_id: int, target_column_name: str) -> None:
    first_message_number_in_db = helper.get_min_value_from_column_for_generator_id(Model, 'message_number', generator_id)
    for offset in range(len(value_list_to_insert)):
        message_number = first_message_number_in_db + offset
        Model.objects.filter(unique_client_id=generator_id, message_number=message_number).update(
            **{target_column_name: value_list_to_insert[offset]})
    return
