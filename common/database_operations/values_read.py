from typing import Type, List, Tuple

import pandas as pd
from django.db import models


def get_kpi_values_for_generator_id(Model: Type[models.Model], generator_id: int) -> Tuple[List[float], List[float]]:
    data_for_generator_id = Model.objects.filter(unique_client_id=generator_id).order_by('message_number').values(
        'metric_value', 'message_number')
    df = pd.DataFrame(data_for_generator_id)
    kpi_values = df['metric_value']
    x_values = df['message_number']
    kpi_values = kpi_values.tolist()
    x_values = x_values.tolist()
    return kpi_values, x_values