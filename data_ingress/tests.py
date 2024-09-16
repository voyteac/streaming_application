from django.test import TestCase, RequestFactory
from unittest.mock import patch
from data_ingress.views import control_panel, build_context


class ControlPanelViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('data_ingress.views.check_tcp_socket')
    @patch('data_ingress.views.kafka_container_check')
    def test_control_panel_view_streaming_stopped(self, mock_kafka_check, mock_tcp_check):
        mock_kafka_check.return_value = False
        mock_tcp_check.return_value = False

        request = self.factory.get('/control-panel/')
        request.session = {'streaming_status': 'stopped'}

        response = control_panel(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn('streaming_message', response.context_data)
        self.assertIn('kafka_message', response.context_data)
        self.assertIn('tcp_server_message', response.context_data)

        # Validate the content of context
        self.assertEqual(response.context_data['streaming_message'], 'Streaming is NOT started!')
        self.assertEqual(response.context_data['kafka_message'], 'Kafka container is NOT running')
        self.assertEqual(response.context_data['tcp_server_message'], 'Data Collection is NOT started!')

    @patch('data_ingress.views.check_tcp_socket')
    @patch('data_ingress.views.kafka_container_check')
    def test_control_panel_view_streaming_started(self, mock_kafka_check, mock_tcp_check):
        mock_kafka_check.return_value = True
        mock_tcp_check.return_value = True

        request = self.factory.get('/control-panel/')
        request.session = {'streaming_status': 'started'}

        response = control_panel(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['streaming_message'], 'Streaming is ongoing!')
        self.assertEqual(response.context_data['kafka_message'], 'Kafka container is running!')
        self.assertEqual(response.context_data['tcp_server_message'], 'Data Collection is started!')


class BuildContextTest(TestCase):
    def test_build_context_stopped(self):
        context = build_context('stopped', False, False)

        self.assertEqual(context['streaming_message'], 'Streaming is NOT started!')
        self.assertEqual(context['kafka_message'], 'Kafka container is NOT running')
        self.assertEqual(context['tcp_server_message'], 'Data Collection is NOT started!')
        self.assertEqual(context['streaming_status'], 'stopped')
        self.assertEqual(context['kafka_container_status'], 'stopped')
        self.assertEqual(context['tcp_server_status'], 'stopped')

    def test_build_context_started(self):
        context = build_context('started', True, True)

        self.assertEqual(context['streaming_message'], 'Streaming is ongoing!')
        self.assertEqual(context['kafka_message'], 'Kafka container is running!')
        self.assertEqual(context['tcp_server_message'], 'Data Collection is started!')
        self.assertEqual(context['streaming_status'], 'started')
        self.assertEqual(context['kafka_container_status'], 'started')
        self.assertEqual(context['tcp_server_status'], 'started')
