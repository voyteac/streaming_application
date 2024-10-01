from common.database_models.common_data_model import CommonDataModels
from data_analysis.models import (Metric0, Metric1, Metric2, Metric3, Metric4, Metric5, Metric6, Metric7,
                                  Metric8, Metric9, Metric10, Metric11)

from data_ingress.models import MetricsDataModelsLoader
from typing import List, Tuple, Type


def get_all_models() -> List[CommonDataModels]:
    return [MetricsDataModelsLoader, Metric0, Metric1, Metric2, Metric3, Metric4, Metric5, Metric6, Metric7,
            Metric8, Metric9, Metric10, Metric11]

def get_metric_models_only() -> List[CommonDataModels]:
    return [Metric0, Metric1, Metric2, Metric3, Metric4, Metric5, Metric6, Metric7,
            Metric8, Metric9, Metric10, Metric11]

def get_metric_name_for_model() -> List[Tuple[Type[CommonDataModels], str]]:
    return [
        (Metric0, 'metric_0'),
        (Metric1, 'metric_1'),
        (Metric2, 'metric_2'),
        (Metric3, 'metric_3'),
        (Metric4, 'metric_4'),
        (Metric5, 'metric_5'),
        (Metric6, 'metric_6'),
        (Metric7, 'metric_7'),
        (Metric8, 'metric_8'),
        (Metric9, 'metric_9'),
        (Metric10, 'metric_10'),
        (Metric11, 'metric_11')
    ]