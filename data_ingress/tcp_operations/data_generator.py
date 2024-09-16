import time
import random
import numpy as np
from faker import Faker
import logging

logger = logging.getLogger('streaming_app')


def get_timestamp():
    timestamp = time.time()
    # logger.debug(f'{get_timestamp.__name__} -> Timestamp: {timestamp}')
    return timestamp


def get_metric_value(min=0, max=1, precision=2):
    value = np.random.uniform(min, max)
    scale = 10 ** precision
    rounded_value = np.ceil(value * scale) / scale
    # logger.debug(f'{get_metric_value.__name__} -> rounded_value: {rounded_value}')
    return rounded_value


def get_client_name_id(number_of_clients):
    faker = Faker()
    name_list = []
    while len(name_list) < number_of_clients:
        city = faker.city()
        if ' ' not in city:
            name_list.append(city)
    # logger.debug(f'{get_client_name_id.__name__} -> name_list: {name_list}')
    return name_list


def get_unique_client_id_list(number_of_clients):
    unique_client_id_list = random.sample(range(number_of_clients), number_of_clients)
    # unique_client_id_list = unique_client_id_list = np.random.permutation(number_of_clients)
    # logger.debug(f'{get_unique_client_id_list.__name__} -> unique_client_id_list: {unique_client_id_list}')
    return unique_client_id_list
