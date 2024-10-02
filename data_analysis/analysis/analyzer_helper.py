from typing import Type, List

from django.db import models
from django.db.models import Max, Min


class AnalyzerHelper:

    def fill_in_margins_bound_values(self, bound_list, windows_size) -> List[float]:
        ### due to size window and list value = not predicted
        prefix = [0 for _ in range(windows_size)]
        postfix = [0 for _ in range(1)]
        data = list(bound_list)
        return prefix + data + postfix

    def get_min_value_from_column_for_generator_id(self, Model: Type[models.Model], column_name: str,
                                                   generator_id: int) -> int:
        max_ = Model.objects.filter(unique_client_id=generator_id).aggregate(Min(column_name))
        max_value = max_[f'{column_name}__min']
        return max_value

    def get_number_of_generators(self, Model: Type[models.Model]) -> int:
        try:
            max_ = Model.objects.aggregate(Max('unique_client_id'))
            max_value = max_['unique_client_id__max']
            starting_from_zero = 1
            return max_value + starting_from_zero
        except TypeError:  # for empty db
            return 0

    def get_button_range(self, number_of_generators: int) -> range:
        return range(number_of_generators)

    def get_max_value_from_column_for_generator_id(self, Model: Type[models.Model], column_name: str,
                                                   generator_id: int) -> int:
        max_ = Model.objects.filter(unique_client_id=generator_id).aggregate(Max(column_name))
        max_value = max_[f'{column_name}__max']
        return max_value

    def get_number_of_messages_for_generator_id(self, Model: Type[models.Model], generator_id: id) -> int:
        # last_message_number - first_message_number_in_db + 1
        return len(Model.objects.filter(unique_client_id=generator_id))


