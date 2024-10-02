from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from common.database_operations.data_transfer_between_tables import copy_data_from_main_to_metric_table
from common.logging_.to_log_file import log_info
from data_analysis.analysis.analyzer import AnomalyAnalyzer
from data_analysis.models import Metric0


def analysis(request: HttpRequest) -> HttpResponse:

    log_info(analysis, "Start Analysis!")


    analyzer_for_metric0 = AnomalyAnalyzer(Metric0)
    copy_data_from_main_to_metric_table()
    plots = analyzer_for_metric0.analyze_metric_0()



    context = {
        'number_of_buttons': analyzer_for_metric0.number_of_generators,
        'button_range': analyzer_for_metric0.button_range,
        'plots': plots
    }

    return render(request, 'data_analysis_main.html', context)


