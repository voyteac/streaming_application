from typing import List
from data_ingress.common.dummy_data.random_data_generator import RandomDataGenerator

class MetricValuesGenerator:
    def __init__(self):
        self.random_data_generator = RandomDataGenerator()

    def get_metrics_values(self) -> List[float]:
        metric_values: List[float] = [
            self.random_data_generator.get_metric_value(0, 1, 2),  # metric_0
            self.random_data_generator.get_metric_value(-1, 1, 4),  # metric_1
            self.random_data_generator.get_metric_value(-10, 10, 3),  # metric_2
            self.random_data_generator.get_metric_value(-100, 100, 1),  # metric_3
            self.random_data_generator.get_metric_value(-1000, 1000, 0),  # metric_4
            self.random_data_generator.get_metric_value(-100, 0, 1),  # metric_5
            self.random_data_generator.get_metric_value(-1000, -500, 0),  # metric_6
            self.random_data_generator.get_metric_value(0, 1000, 0),  # metric_7
            self.random_data_generator.get_metric_value(0, 100, 2),  # metric_8
            self.random_data_generator.get_metric_value(0, 10000, 0),  # metric_9
            self.random_data_generator.get_metric_value(0, 100000, 0),  # metric_10
            self.random_data_generator.get_metric_value(-100000, 100000, 0)  # metric_11
        ]
        return metric_values
