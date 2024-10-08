# Generated by Django 5.1.1 on 2024-10-03 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MetricsDataModelsLoader',
            fields=[
                ('internal_unique_client_id', models.CharField(default=None, max_length=255, primary_key=True, serialize=False)),
                ('unique_client_id', models.IntegerField(blank=True, null=True)),
                ('date', models.CharField(default=None, max_length=255)),
                ('time', models.CharField(default=None, max_length=255)),
                ('message_number', models.IntegerField(blank=True, null=True)),
                ('client_name', models.CharField(default=None, max_length=255)),
                ('metric_0', models.FloatField(blank=True, null=True)),
                ('metric_1', models.FloatField(blank=True, null=True)),
                ('metric_2', models.FloatField(blank=True, null=True)),
                ('metric_3', models.FloatField(blank=True, null=True)),
                ('metric_4', models.FloatField(blank=True, null=True)),
                ('metric_5', models.FloatField(blank=True, null=True)),
                ('metric_6', models.FloatField(blank=True, null=True)),
                ('metric_7', models.FloatField(blank=True, null=True)),
                ('metric_8', models.FloatField(blank=True, null=True)),
                ('metric_9', models.FloatField(blank=True, null=True)),
                ('metric_10', models.FloatField(blank=True, null=True)),
                ('metric_11', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'data_ingress',
            },
        ),
    ]
