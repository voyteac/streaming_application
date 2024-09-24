# from django.test import TestCase, RequestFactory
# from unittest.mock import patch, MagicMock
# from data_ingress.data_collection.streaming_controls import start_data_collection_view, stop_data_collection_view, data_collection_manager
#
#
#
# class TestDataCollectionController(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.request = self.factory.get('/data_ingress/')
#         self.request.session = {}
#
#     @patch('data_ingress.kafka_container_control.kafka_container_control.kafka_container_check')
#     @patch('data_ingress.data_collection.streaming_controls_helper.start_thread')
#     def test_start_data_collection_success(self, mock_start_thread, mock_kafka_container_check):
#         mock_kafka_container_check.return_value = True
#
#         response = start_data_collection_view(self.request)
#         session = self.client.session
#         session['start-tcp-server'] = 'started'
#         session.save()
#
#         response = self.client.get('/data_ingress/start_tcp_server/')
#         # session = self.client.session
#
#         expected_http_redirection_code = 302
#         result_http_redirection_code = response.status_code
#
#         self.assertEqual(result_http_redirection_code, expected_http_redirection_code)
#
#         expected_session_status = 'started'
#         result_session_status = self.request.session['tcp_server_status']
#
#         self.assertEqual(result_session_status, expected_session_status)
#
#         mock_start_thread.assert_called_once()
#
#
#     # @patch('data_ingress.kafka_container_control.kafka_container_control.kafka_container_check')
#     # @patch('data_ingress.logging_.to_log_file.log_warning')
#     # def test_start_data_collection_kafka_not_running(self, mock_log_warning, mock_kafka_container_check):
#     #     mock_kafka_container_check.return_value = False  # Simulate Kafka container not running
#     #
#     #     response = start_data_collection_view(self.request)
#     #
#     #     self.assertEqual(response.status_code, 302)  # Check for redirect
#     #     self.assertEqual(self.request.session['tcp_server_status'], 'stopped')  # Check session status
#     #     mock_log_warning.assert_called_once()  # Ensure log warning was called
#     #
#     # @patch('data_ingress.logging_.to_log_file.log_info')
#     # def test_stop_data_collection(self, mock_log_info):
#     #     # Simulate the streaming thread being alive
#     #     data_collection_manager.streaming_thread = MagicMock()
#     #     data_collection_manager.streaming_thread.is_alive.return_value = True
#     #
#     #     response = stop_data_collection_view(self.request)
#     #
#     #     self.assertEqual(response.status_code, 302)  # Check for redirect
#     #     self.assertEqual(self.request.session['tcp_server_status'], 'stopped')  # Check session status
#     #     data_collection_manager.streaming_thread.join.assert_called_once()  # Ensure join was called
#     #     mock_log_info.assert_any_call('stop_data_collection', 'Stopping data collection')
#     #     mock_log_info.assert_any_call('stop_data_collection', 'Data collection stopped')
#     #
#     # @patch('data_ingress.logging_.to_log_file.log_info')
#     # def test_stop_data_collection_no_active_thread(self, mock_log_info):
#     #     # Simulate no active streaming thread
#     #     data_collection_manager.streaming_thread = None
#     #
#     #     response = stop_data_collection_view(self.request)
#     #
#     #     self.assertEqual(response.status_code, 302)  # Check for redirect
#     #     self.assertEqual(self.request.session['tcp_server_status'], 'stopped')  # Check session status
#     #     mock_log_info.assert_any_call('stop_data_collection', 'Stopping data collection')
#     #     mock_log_info.assert_any_call('stop_data_collection', 'Data collection stopped')
