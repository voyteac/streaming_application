from django.urls import path
from . import views
from .tcp_operations import tcp_client
from .kafka import kafka_container_control
from .data_streaming import streaming_controls
from .database import postgresql_operations

urlpatterns = [
    path('', views.data_ingress, name='data-ingress'),
    path('start_data_collection/', streaming_controls.start_data_collection, name='start-tcp-server'),
    path('stop_data_collection/', streaming_controls.stop_data_collection, name='stop-tcp-server'),
    path('start_kafka_container/', kafka_container_control.start_kafka_container, name='start-kafka-container'),
    path('stop_kafka_container', kafka_container_control.stop_kafka_container, name='stop-kafka-container'),
    path('start_streaming/', tcp_client.start_streaming, name='start-streaming'),
    path('stop_streaming/', tcp_client.stop_streaming, name='stop-streaming'),
    path('clear_table/', views.data_ingress, name='clear-table')

]