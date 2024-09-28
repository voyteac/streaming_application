import pytest
from django.http import HttpRequest, HttpResponse

from data_ingress.views import DataIngressView


@pytest.mark.django_db
def test_get(monkeypatch):
    mock_request = HttpRequest()

    def mock_check_tcp_socket(self, server_host, server_port):
        return True

    def mock_kafka_container_status():
        return True

    class MockContextBuilder:
        def __init__(self, *args, **kwargs):
            pass

        def get_data_generation_status(self):
            return 'stopped'

        def get_data_collection_status(self):
            return 'stopped'

        def get_kafka_container_status(self):
            return 'started'

        def check_button_click(self, request):
            return False

        def build_context(self, data_generation_status, data_collection_status, kafka_container_status, button_clicked):
            context = {
                'data_generation_message': 'Streaming is NOT started!',
                'data_generation_status': data_generation_status,
                'kafka_container_message': 'Kafka container is running!',
                'kafka_service_status': data_collection_status,
                'data_collection_message': 'Data Collection is NOT started!',
                'data_collection_status': kafka_container_status,
                'button_click': button_clicked
            }
            print("Expected build_context output:", context)  # Print the expected context
            return context

    monkeypatch.setattr('data_ingress.views.ContextBuilder', MockContextBuilder)

    view = DataIngressView()
    response = view.get(mock_request)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 200
    assert b'Kafka container is running!' in response.content
    assert b'Data Collection is NOT started!' in response.content
    assert b'Streaming is NOT started!' in response.content

