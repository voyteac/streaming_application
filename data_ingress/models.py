from django.db import models
from common.database_models.common_data_model import CommonDataModels
from streaming_app.config import database

class MetricsDataModelsLoader(CommonDataModels):
    metric_0 = models.FloatField(null=True, blank=True)
    metric_1 = models.FloatField(null=True, blank=True)
    metric_2 = models.FloatField(null=True, blank=True)
    metric_3 = models.FloatField(null=True, blank=True)
    metric_4 = models.FloatField(null=True, blank=True)
    metric_5 = models.FloatField(null=True, blank=True)
    metric_6 = models.FloatField(null=True, blank=True)
    metric_7 = models.FloatField(null=True, blank=True)
    metric_8 = models.FloatField(null=True, blank=True)
    metric_9 = models.FloatField(null=True, blank=True)
    metric_10 = models.FloatField(null=True, blank=True)
    metric_11 = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = database.data_ingress_table_name


    def __str__(self):
        return {self.internal_unique_client_id}

