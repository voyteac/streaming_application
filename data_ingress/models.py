from django.db import models


class DataBaseLoader(models.Model):
    internal_unique_client_id = models.CharField(primary_key=True, max_length=255, default=None)
    unique_client_id = models.IntegerField(null=True, blank=True)
    timestamp = models.FloatField(null=True, blank=True)
    message_number = models.IntegerField(null=True, blank=True)
    client_name = models.CharField(max_length=255, default=None)
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

    def __str__(self):
        return {self.unique_client_id}
