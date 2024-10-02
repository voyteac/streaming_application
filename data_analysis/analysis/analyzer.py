from typing import List, Type

from django.db import models


from data_analysis.analysis.detect_anomalies import detect_anomalies
from data_analysis.analysis.figure_plotter import plot_figure_to_buffer, create_placeholder_if_no_plots
from common.database_operations.insert_values_to_metrics_tables import insert_values_to_margin_column, insert_values_to_anomaly_column
from common.database_operations.values_read import get_kpi_values_for_generator_id

from data_ingress.models import MetricsDataModelsLoader
from .analyzer_helper import AnalyzerHelper


class AnomalyAnalyzer:
    def __init__(self, model: Type[models.Model]):
        self.window_size = 8
        self.prediction_error_margin = 4
        self.helper = AnalyzerHelper()
        self.number_of_generators = self.helper.get_number_of_generators(MetricsDataModelsLoader)
        self.button_range = self.helper.get_button_range(self.number_of_generators)
        self.model: Type[models.Model] = model

    def analyze_metric_0(self) -> List[str]:
        if self.number_of_generators != 0:
            plots = self.get_plots_for_Metric0()
        else:  # empty db
            plots = create_placeholder_if_no_plots()
        return plots

    def get_plots_for_Metric0(self) -> List[str]:
        plots = []
        for generator_id in range(0, self.number_of_generators):

            kpi_values, x_values = get_kpi_values_for_generator_id(self.model, generator_id)

            x_values_original, y_values_original, y_values, online_predictions, detected_anomalies = detect_anomalies(
                x_values, kpi_values, self.window_size, self.prediction_error_margin)

            image_uri, lower_bound_values, upper_bound_values = plot_figure_to_buffer(x_values_original,
                                                                                      y_values_original, y_values,
                                                                                      online_predictions,
                                                                                      self.prediction_error_margin,
                                                                                      self.window_size,
                                                                                      detected_anomalies)

            insert_values_to_margin_column(self.model, generator_id, upper_bound_values,'margin_upper', self.window_size)
            insert_values_to_margin_column(self.model, generator_id, lower_bound_values,'margin_lower', self.window_size)
            insert_values_to_anomaly_column(self.model, detected_anomalies)
            plots.append(image_uri)

        return plots

