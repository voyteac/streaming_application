# Generated by Django 5.1.1 on 2024-10-03 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Metric0',
            fields=[
                ('internal_unique_client_id', models.CharField(default=None, max_length=255, primary_key=True, serialize=False)),
                ('unique_client_id', models.IntegerField(blank=True, null=True)),
                ('date', models.CharField(default=None, max_length=255)),
                ('time', models.CharField(default=None, max_length=255)),
                ('message_number', models.IntegerField(blank=True, null=True)),
                ('client_name', models.CharField(default=None, max_length=255)),
                ('metric_value', models.FloatField(blank=True, null=True)),
                ('is_anomaly', models.FloatField(blank=True, null=True)),
                ('margin_lower', models.FloatField(blank=True, null=True)),
                ('margin_upper', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'metric_0',
            },
        ),
        migrations.CreateModel(
            name='Metric1',
            fields=[
                ('internal_unique_client_id', models.CharField(default=None, max_length=255, primary_key=True, serialize=False)),
                ('unique_client_id', models.IntegerField(blank=True, null=True)),
                ('date', models.CharField(default=None, max_length=255)),
                ('time', models.CharField(default=None, max_length=255)),
                ('message_number', models.IntegerField(blank=True, null=True)),
                ('client_name', models.CharField(default=None, max_length=255)),
                ('metric_value', models.FloatField(blank=True, null=True)),
                ('is_anomaly', models.FloatField(blank=True, null=True)),
                ('margin_lower', models.FloatField(blank=True, null=True)),
                ('margin_upper', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'metric_1',
            },
        ),
        migrations.CreateModel(
            name='Metric10',
            fields=[
                ('internal_unique_client_id', models.CharField(default=None, max_length=255, primary_key=True, serialize=False)),
                ('unique_client_id', models.IntegerField(blank=True, null=True)),
                ('date', models.CharField(default=None, max_length=255)),
                ('time', models.CharField(default=None, max_length=255)),
                ('message_number', models.IntegerField(blank=True, null=True)),
                ('client_name', models.CharField(default=None, max_length=255)),
                ('metric_value', models.FloatField(blank=True, null=True)),
                ('is_anomaly', models.FloatField(blank=True, null=True)),
                ('margin_lower', models.FloatField(blank=True, null=True)),
                ('margin_upper', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'metric_10',
            },
        ),
        migrations.CreateModel(
            name='Metric11',
            fields=[
                ('internal_unique_client_id', models.CharField(default=None, max_length=255, primary_key=True, serialize=False)),
                ('unique_client_id', models.IntegerField(blank=True, null=True)),
                ('date', models.CharField(default=None, max_length=255)),
                ('time', models.CharField(default=None, max_length=255)),
                ('message_number', models.IntegerField(blank=True, null=True)),
                ('client_name', models.CharField(default=None, max_length=255)),
                ('metric_value', models.FloatField(blank=True, null=True)),
                ('is_anomaly', models.FloatField(blank=True, null=True)),
                ('margin_lower', models.FloatField(blank=True, null=True)),
                ('margin_upper', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'metric_11',
            },
        ),
        migrations.CreateModel(
            name='Metric2',
            fields=[
                ('internal_unique_client_id', models.CharField(default=None, max_length=255, primary_key=True, serialize=False)),
                ('unique_client_id', models.IntegerField(blank=True, null=True)),
                ('date', models.CharField(default=None, max_length=255)),
                ('time', models.CharField(default=None, max_length=255)),
                ('message_number', models.IntegerField(blank=True, null=True)),
                ('client_name', models.CharField(default=None, max_length=255)),
                ('metric_value', models.FloatField(blank=True, null=True)),
                ('is_anomaly', models.FloatField(blank=True, null=True)),
                ('margin_lower', models.FloatField(blank=True, null=True)),
                ('margin_upper', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'metric_2',
            },
        ),
        migrations.CreateModel(
            name='Metric3',
            fields=[
                ('internal_unique_client_id', models.CharField(default=None, max_length=255, primary_key=True, serialize=False)),
                ('unique_client_id', models.IntegerField(blank=True, null=True)),
                ('date', models.CharField(default=None, max_length=255)),
                ('time', models.CharField(default=None, max_length=255)),
                ('message_number', models.IntegerField(blank=True, null=True)),
                ('client_name', models.CharField(default=None, max_length=255)),
                ('metric_value', models.FloatField(blank=True, null=True)),
                ('is_anomaly', models.FloatField(blank=True, null=True)),
                ('margin_lower', models.FloatField(blank=True, null=True)),
                ('margin_upper', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'metric_3',
            },
        ),
        migrations.CreateModel(
            name='Metric4',
            fields=[
                ('internal_unique_client_id', models.CharField(default=None, max_length=255, primary_key=True, serialize=False)),
                ('unique_client_id', models.IntegerField(blank=True, null=True)),
                ('date', models.CharField(default=None, max_length=255)),
                ('time', models.CharField(default=None, max_length=255)),
                ('message_number', models.IntegerField(blank=True, null=True)),
                ('client_name', models.CharField(default=None, max_length=255)),
                ('metric_value', models.FloatField(blank=True, null=True)),
                ('is_anomaly', models.FloatField(blank=True, null=True)),
                ('margin_lower', models.FloatField(blank=True, null=True)),
                ('margin_upper', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'metric_4',
            },
        ),
        migrations.CreateModel(
            name='Metric5',
            fields=[
                ('internal_unique_client_id', models.CharField(default=None, max_length=255, primary_key=True, serialize=False)),
                ('unique_client_id', models.IntegerField(blank=True, null=True)),
                ('date', models.CharField(default=None, max_length=255)),
                ('time', models.CharField(default=None, max_length=255)),
                ('message_number', models.IntegerField(blank=True, null=True)),
                ('client_name', models.CharField(default=None, max_length=255)),
                ('metric_value', models.FloatField(blank=True, null=True)),
                ('is_anomaly', models.FloatField(blank=True, null=True)),
                ('margin_lower', models.FloatField(blank=True, null=True)),
                ('margin_upper', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'metric_5',
            },
        ),
        migrations.CreateModel(
            name='Metric6',
            fields=[
                ('internal_unique_client_id', models.CharField(default=None, max_length=255, primary_key=True, serialize=False)),
                ('unique_client_id', models.IntegerField(blank=True, null=True)),
                ('date', models.CharField(default=None, max_length=255)),
                ('time', models.CharField(default=None, max_length=255)),
                ('message_number', models.IntegerField(blank=True, null=True)),
                ('client_name', models.CharField(default=None, max_length=255)),
                ('metric_value', models.FloatField(blank=True, null=True)),
                ('is_anomaly', models.FloatField(blank=True, null=True)),
                ('margin_lower', models.FloatField(blank=True, null=True)),
                ('margin_upper', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'metric_6',
            },
        ),
        migrations.CreateModel(
            name='Metric7',
            fields=[
                ('internal_unique_client_id', models.CharField(default=None, max_length=255, primary_key=True, serialize=False)),
                ('unique_client_id', models.IntegerField(blank=True, null=True)),
                ('date', models.CharField(default=None, max_length=255)),
                ('time', models.CharField(default=None, max_length=255)),
                ('message_number', models.IntegerField(blank=True, null=True)),
                ('client_name', models.CharField(default=None, max_length=255)),
                ('metric_value', models.FloatField(blank=True, null=True)),
                ('is_anomaly', models.FloatField(blank=True, null=True)),
                ('margin_lower', models.FloatField(blank=True, null=True)),
                ('margin_upper', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'metric_7',
            },
        ),
        migrations.CreateModel(
            name='Metric8',
            fields=[
                ('internal_unique_client_id', models.CharField(default=None, max_length=255, primary_key=True, serialize=False)),
                ('unique_client_id', models.IntegerField(blank=True, null=True)),
                ('date', models.CharField(default=None, max_length=255)),
                ('time', models.CharField(default=None, max_length=255)),
                ('message_number', models.IntegerField(blank=True, null=True)),
                ('client_name', models.CharField(default=None, max_length=255)),
                ('metric_value', models.FloatField(blank=True, null=True)),
                ('is_anomaly', models.FloatField(blank=True, null=True)),
                ('margin_lower', models.FloatField(blank=True, null=True)),
                ('margin_upper', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'metric_8',
            },
        ),
        migrations.CreateModel(
            name='Metric9',
            fields=[
                ('internal_unique_client_id', models.CharField(default=None, max_length=255, primary_key=True, serialize=False)),
                ('unique_client_id', models.IntegerField(blank=True, null=True)),
                ('date', models.CharField(default=None, max_length=255)),
                ('time', models.CharField(default=None, max_length=255)),
                ('message_number', models.IntegerField(blank=True, null=True)),
                ('client_name', models.CharField(default=None, max_length=255)),
                ('metric_value', models.FloatField(blank=True, null=True)),
                ('is_anomaly', models.FloatField(blank=True, null=True)),
                ('margin_lower', models.FloatField(blank=True, null=True)),
                ('margin_upper', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'metric_9',
            },
        ),
    ]
