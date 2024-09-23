import random
import numpy as np
from faker import Faker
from typing import List

from data_ingress.logging_.to_log_file import log_debug


def get_metric_value(minimum: int = 0, maximum: int = 1, precision: int = 2) -> np.float64:
    value: float = np.random.uniform(minimum, maximum)
    scale: int = 10 ** precision
    rounded_value: np.float64 = np.ceil(value * scale) / scale
    return rounded_value


def get_client_name_id(number_of_clients: int) -> List[str]:
    faker: Faker = Faker()
    name_list: List[str] = []
    while len(name_list) < number_of_clients:  ## infinite loop?
        city: str = faker.city()
        if ' ' not in city:
            name_list.append(city)
    log_debug(get_client_name_id.__name__, f'client_name_list: {name_list}')
    return name_list


def get_unique_client_id_list(number_of_clients: int) -> List[int]:
    unique_client_id_list = random.sample(range(number_of_clients), number_of_clients)
    log_debug(get_unique_client_id_list.__name__, f'unique_event_id_list: {unique_client_id_list}')
    log_debug(get_unique_client_id_list.__name__, f'type of unique_event_id_list: {type(unique_client_id_list)}')
    return unique_client_id_list
