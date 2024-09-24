from django.urls import path
from data_ingress import views
from data_ingress.data_collection.data_collection_controller import data_collection_controller
from data_ingress.data_generation.data_generation_controller import data_generation_controller
from data_ingress.kafka_container_control.kafka_container_controller import kafka_container_controller

urlpatterns = [
    path('', views.DataIngressView.as_view(), name='data-ingress'),
    path('start_data_collection/', data_collection_controller.start_data_collection, name='start-data-collection'),
    path('stop_data_collection/', data_collection_controller.stop_data_collection, name='stop-data-collection'),
    path('start_kafka_container/', kafka_container_controller.start_kafka_container, name='start-kafka-container'),
    path('stop_kafka_container/', kafka_container_controller.stop_kafka_container, name='stop-kafka-container'),
    path('start_data_generation/', data_generation_controller.start_data_generation, name='start-data-generation'),
    path('stop_data_generation/', data_generation_controller.stop_data_generation, name='stop-data-generation'),
    path('clear_table/', views.DataIngressClearView.as_view(), name='clear-table'),
]
