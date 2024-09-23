from django.test import TestCase
from unittest.mock import patch
from datetime import datetime

from data_ingress.data_generator.time_data import get_formatted_timestamp


class TimeDataTest(TestCase):

    @patch('data_ingress.data_generator.time_data.get_timestamp')
    def test_get_formatted_timestamp(self, mock_timestamp):
        timestamp = 1630454400
        mock_timestamp.return_value = 1630454400
        expected = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        result = get_formatted_timestamp()
        self.assertEqual(result, expected)
