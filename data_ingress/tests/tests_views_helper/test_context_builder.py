# from django.test import TestCase
#
# from data_ingress.views_helper.views_message_generator import *
#
#
# class TestUiMessage(TestCase):
#
#
#     def test_get_streaming_message_started(self):
#         status = 'started'
#         expected = 'Streaming is ongoing!'
#         result = get_data_generation_message(status)
#         self.assertEqual(result, expected)
#
#     def test_get_streaming_message_stopped(self):
#         status = 'stopped'
#         expected = 'Streaming is NOT started!'
#         result = get_data_generation_message(status)
#         self.assertEqual(result, expected)
#
#     def test_get_kafka_message_started(self):
#         is_kafka_running = True
#         expected = 'Kafka container is running!'
#         result = get_kafka_container_message(is_kafka_running)
#         self.assertEqual(result, expected)
#
#     def test_get_kafka_message_stopped(self):
#         is_kafka_running = False
#         expected = 'Kafka container is NOT running!'
#         result = get_kafka_container_message(is_kafka_running)
#         self.assertEqual(result, expected)
#
#     def test_get_tcp_message_started(self):
#         is_tcp_opened = True
#         expected = 'Data Collection is started!'
#         result = get_data_collection_message(is_tcp_opened)
#         self.assertEqual(result, expected)
#
#     def test_get_tcp_message_stopped(self):
#         is_tcp_opened = False
#         expected = 'Data Collection is NOT started!'
#         result = get_data_collection_message(is_tcp_opened)
#         self.assertEqual(result, expected)
#
