from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import MetricsDataModelsLoaderSerializer, Metric0Serializer
from common.database_operations.data_transfer_between_tables import copy_data_from_main_to_metric_table
from data_analysis.analysis.analyzer import AnomalyAnalyzer
from data_analysis.models import Metric0
from data_ingress.models import MetricsDataModelsLoader


@api_view(['GET', 'POST'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/ingress_data',
        'GET /api/analysis_data',
        'POST /api/trigger_analysis'
    ]
    return Response(routes)


@api_view(['POST'])
def trigger_analysis(request):
    try:
        analyzer_for_metric0 = AnomalyAnalyzer(Metric0)
        copy_data_from_main_to_metric_table()
        analyzer_for_metric0.analyze_metric_0()
        return Response({"message": "Analysis triggered successfully!"}, status=status.HTTP_200_OK)
    except Exception:
        return Response({"message": "Analysis triggered failed!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_ingress_data(request):
    data_ingress = MetricsDataModelsLoader.objects.all()
    serializer = MetricsDataModelsLoaderSerializer(data_ingress, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_analysis_data(request):
    data_analysis = Metric0.objects.all()
    serializer = Metric0Serializer(data_analysis, many=True)
    return Response(serializer.data)
