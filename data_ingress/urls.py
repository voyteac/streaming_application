from django.urls import path
from . import views
from .tcp_operations import tcp_client
from .tcp_operations import tcp_server
from .kafka import kafka_container_control
from .data_streaming import streaming_controls

urlpatterns = [
    path('', views.control_panel, name='control-panel'),
    path('start_data_collection/', streaming_controls.start_data_collection, name='start-tcp-server'),
    path('stop_data_collection/', streaming_controls.stop_data_collection, name='stop-tcp-server'),
    path('start_kafka_container/', kafka_container_control.start_kafka_container, name='start-kafka-container'),
    path('stop_kafka_container', kafka_container_control.stop_kafka_container, name='stop-kafka-container'),
    path('start_streaming/', tcp_client.start_streaming, name='start-streaming'),
    path('stop_streaming/', tcp_client.stop_streaming, name='stop-streaming')
]