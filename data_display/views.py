from django.shortcuts import render
from typing import List, Dict, Union
from data_ingress.models import DataBaseLoader


def display(request):
    column_headers: List[str] = get_column_name_from_db()
    table_content: List[Dict[str, Union[str, int, float]]] = get_table_content_from_db()
    context = {
        'table_content': table_content,
        'column_headers': column_headers,
        'number_columns': len(column_headers)
    }
    return render(request, "data_display_main.html", context)


def get_table_content_from_db() -> List[Dict[str, Union[str, int, float]]]:
    all_records = DataBaseLoader.objects.all()
    table_content = [
        {
            'internal_unique_client_id': record.internal_unique_client_id,
            'unique_client_id': record.unique_client_id,
            'timestamp': record.timestamp,
            'message_number': record.message_number,
            'client_name': record.client_name,
            'metric_0': record.metric_0,
            'metric_1': record.metric_1,
            'metric_2': record.metric_2,
            'metric_3': record.metric_3,
            'metric_4': record.metric_4,
            'metric_5': record.metric_5,
            'metric_6': record.metric_6,
            'metric_7': record.metric_7,
            'metric_8': record.metric_8,
            'metric_9': record.metric_9,
            'metric_10': record.metric_10,
            'metric_11': record.metric_11,
        }
        for record in all_records]
    return table_content

def get_column_name_from_db() -> List[str]:
    column_headers: List[str] = [field.name for field in DataBaseLoader._meta.get_fields()]
    return convert_column_headers_nice_format(column_headers)

def convert_column_headers_nice_format(column_headers: List[str]) -> List[str]:
    return [' '.join(word.capitalize() for word in column.split('_')) for column in column_headers]

