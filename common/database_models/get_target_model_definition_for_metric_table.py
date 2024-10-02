from typing import Type

from django.db import models
from django.db.models import Model


def get_target_model_definition_for_metric_table(TargetModel: Type[models.Model], record: models.Model,
                                                 metric_name) -> Model:
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
