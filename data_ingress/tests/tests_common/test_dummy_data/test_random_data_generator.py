# from django.test import TestCase
# from unittest.mock import patch
# import numpy as np
#
# from data_ingress.common.dummy_data.random_data_generator import RandomDataGenerator
#
#
# class RandomDataTest(TestCase):
#
#     @patch('numpy.random.uniform')
#     def test_get_metric_value(self, mock_uniform):
#         data_gen = RandomDataGenerator()
#         return_value = 0.123456
#         scale = 100
#         mock_uniform.return_value = return_value
#         expected = np.ceil(return_value * scale) / scale
#
#         result = data_gen.get_metric_value()
#
#         self.assertEqual(result, expected)
#
#     @patch('numpy.random.uniform')
#     def test_get_metric_value_scale_test(self, mock_uniform):
#         data_gen = RandomDataGenerator()
#
#         return_value = 0.123456
#         scale = 1000
#         mock_uniform.return_value = return_value
#
#         expected = np.ceil(return_value * scale) / scale
#
#         result = data_gen.get_metric_value(precision=3)
#         self.assertEqual(result, expected)
#
#     @patch('data_ingress.random_data_generator.random_data.Faker')
#     def test_get_client_name_id_positive(self, mock_faker):
#         data_gen = RandomDataGenerator()
#
#         mock_instance = mock_faker.return_value
#         mock_instance.city.side_effect = [
#             'Wroclaw',
#             'Sydney',
#             'New York',
#             'San Francisco',
#             'Beijing'
#         ]
#         # Test for 3 clients
#         result = data_gen.get_client_name_id(3)
#         result_length = len(result)
#         expected_length = 3
#         self.assertEqual(result_length, expected_length)
#         self.assertNotIn('San Francisco', result)
#         self.assertIn('Wroclaw', result)
#         self.assertIn('Sydney', result)
#         self.assertIn('Beijing', result)
#
#
#     @patch('random.sample')
#     def test_get_unique_client_id_list_2(self, mock_sample):
#         data_gen = RandomDataGenerator()
#
#         mock_sample.return_value = [0, 1, 2, 3, 4]
#         result = data_gen.get_unique_client_id_list(5)
#         expected = [0, 1, 2, 3, 4]
#         self.assertEqual(result, expected)
#         mock_sample.assert_called_once_with(range(5), 5)