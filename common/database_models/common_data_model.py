from django.db import models


class CommonDataModels(models.Model):
    internal_unique_client_id = models.CharField(primary_key=True, max_length=255, default=None)
    unique_client_id = models.IntegerField(null=True, blank=True)
    date = models.CharField(max_length=255, default=None)
    time = models.CharField(max_length=255, default=None)
    message_number = models.IntegerField(null=True, blank=True)
    client_name = models.CharField(max_length=255, default=None)

    class Meta:
        abstract = True  # This makes it an abstract model
