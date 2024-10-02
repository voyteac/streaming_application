from django.db import models
from django.db.models import Max, Min
from typing import Type

def get_number_of_generators(Model: Type[models.Model]) -> int:
    try:
        max_ = Model.objects.aggregate(Max('unique_client_id'))
        max_value = max_['unique_client_id__max']
        starting_from_zero = 1
        return max_value + starting_from_zero
    except TypeError:  # for empty db
        return 0