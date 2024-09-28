from django.urls import path
from data_ingress import views
from data_ingress.data_collection.data_collection_controller import data_collection_controller
from data_ingress.data_generation.data_generation_controller import data_generation_controller
from data_ingress.container_control.kafka_docker_service_controller import kafka_docker_service_controller
from data_ingress.container_control.elk_docker_service_controller import elk_docker_service_controller

urlpatterns = [
    path('', views.DataIngressView.as_view(), name='data-ingress'),
    path('start_data_collection/', data_collection_controller.start_data_collection, name='start-data-collection'),
    path('stop_data_collection/', data_collection_controller.stop_data_collection, name='stop-data-collection'),
    path('start_kafka_docker_service/', kafka_docker_service_controller.start_kafka_docker_service, name='start-kafka-docker-service'),
    path('stop_kafka_docker_service/', kafka_docker_service_controller.stop_kafka_docker_service, name='stop-kafka-docker-service'),
    path('start_elk_docker_service/', elk_docker_service_controller.start_elk_docker_service, name='start-elk-docker-service'),
    path('stop_elk_docker_service/', elk_docker_service_controller.stop_elk_docker_service, name='stop-elk-docker-service'),
    path('start_data_generation/', data_generation_controller.start_data_generation, name='start-data-generation'),
    path('stop_data_generation/', data_generation_controller.stop_data_generation, name='stop-data-generation'),
    path('clear_table/', views.DataIngressClearView.as_view(), name='clear-table'),
]
