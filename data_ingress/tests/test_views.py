from django.test import TestCase
from unittest.mock import patch
from streaming_app.config import tcp_config


class DataIngressViewTest(TestCase):

    @patch('data_ingress.views.check_tcp_socket')
    @patch('data_ingress.views.kafka_container_check')
    def test_data_ingress_view(self, mock_kafka_container_check, mock_check_tcp_socket):
        mock_check_tcp_socket.return_value = True
        mock_kafka_container_check.return_value = True

        session = self.client.session
        session['streaming_status'] = 'started'
        session.save()

        response = self.client.get('/data_ingress/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'data_ingress.html')


        expected_context = {
            'streaming_message': 'Streaming is ongoing!',
            'kafka_message': 'Kafka container is running!',
            'tcp_server_message': 'Data Collection is started!',
            'streaming_status': 'started',
            'kafka_container_status': 'started',
            'tcp_server_status': 'started'
        }
        for key, value in expected_context.items():
            self.assertIn(key, response.context)
            self.assertEqual(response.context[key], value)

        mock_check_tcp_socket.assert_called_once_with(tcp_config.server_host, tcp_config.port)
        mock_kafka_container_check.assert_called_once()

    @patch('data_ingress.views.check_tcp_socket')
    @patch('data_ingress.views.kafka_container_check')
    def test_data_ingress_view_with_streaming_stopped(self, mock_kafka_container_check, mock_check_tcp_socket):

        mock_check_tcp_socket.return_value = False
        mock_kafka_container_check.return_value = False

        session = self.client.session
        session['streaming_status'] = 'stopped'
        session.save()

        response = self.client.get('/data_ingress/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'data_ingress.html')

        expected_context = {
            'streaming_message': 'Streaming is NOT started!',
            'kafka_message': 'Kafka container is NOT running',
            'tcp_server_message': 'Data Collection is NOT started!',
            'streaming_status': 'stopped',
            'kafka_container_status': 'stopped',
            'tcp_server_status': 'stopped'
        }
        for key, value in expected_context.items():
            self.assertIn(key, response.context)
            self.assertEqual(response.context[key], value)

        mock_check_tcp_socket.assert_called_once_with(tcp_config.server_host, tcp_config.port)
        mock_kafka_container_check.assert_called_once()