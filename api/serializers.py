from rest_framework import serializers
from data_ingress.models import MetricsDataModelsLoader
from data_analysis.models import Metric0

class MetricsDataModelsLoaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricsDataModelsLoader
        fields = '__all__'


class Metric0Serializer(serializers.ModelSerializer):
    class Meta:
        model = Metric0
        fields = '__all__'