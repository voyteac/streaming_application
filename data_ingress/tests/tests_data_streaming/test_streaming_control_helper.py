# import unittest
# from unittest.mock import patch, MagicMock
#
# from data_ingress.data_collection.data_collection_controller_helper import start_thread, StartingThreadFailed
#
#
# class TestStartThread(unittest.TestCase):
#
#     @patch('threading.Thread')
#     def test_start_thread_success(self, mock_thread):
#         mock_target = MagicMock()
#         mock_thread_instance = MagicMock()
#         mock_thread.return_value = mock_thread_instance
#
#         args_tuple = (True, 1)
#         thread_name = "test-thread"
#
#         result = start_thread(mock_target, args_tuple, thread_name)
#
#         mock_thread.assert_called_once_with(target=mock_target, args=args_tuple)
#         mock_thread_instance.start.assert_called_once()
#         self.assertEqual(result, mock_thread_instance)
#
#     @patch('threading.Thread')
#     def test_start_thread_failure(self, mock_thread):
#
#         mock_target = MagicMock(side_effect=Exception("Thread error"))
#         mock_thread.side_effect = Exception("Thread creation error")
#         args_tuple = (1, 2)
#         thread_name = "test-thread-error"
#         with self.assertRaises(StartingThreadFailed) as mocker_error:
#             start_thread(mock_target, args_tuple, thread_name)
#
#         self.assertIn("Thread creation error", str(mocker_error.exception))