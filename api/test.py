import unittest
from api import _log as lg


class TestLogging(unittest.TestCase):
    def test_empty_param(self):
        """
        Test that logging doesn't break when nothing is passed
        """
        with self.assertLogs(level='INFO') as log:
            lg.log_info()
            self.assertEqual(len(log.output), 1)
            self.assertEqual(len(log.records), 1)
            self.assertIn('called with empty', log.output[0])

    def test_empty_string(self):
        """
        Test that logging doesn't break when empty string is passed
        """
        with self.assertLogs(level='INFO') as log:
            data = ""
            lg.log_info(data, logger='TEST')
            self.assertEqual(len(log.output), 1)
            self.assertEqual(len(log.records), 1)
            self.assertIn('called with empty', log.output[0])

    def test_log_msg(self):
        """
        Test that logging works for message (string)
        """
        with self.assertLogs(level='INFO') as log:
            data = "xxx1"
            lg.log_info(data, logger='TEST')
            self.assertEqual(len(log.output), 1)
            self.assertEqual(len(log.records), 1)
            self.assertEqual('INFO:TEST:xxx1', log.output[0])

    def test_log_dict(self):
        """
        Test that logging works for simple dicts with table_names
        """
        with self.assertLogs(level='INFO') as log:
            data = {'Test_Table': {
                'header_1': 1,
                'header_2': 2,
            }
            }
            lg.log_info(data, logger='TEST')
            self.assertEqual(len(log.output), 1)
            self.assertEqual(len(log.records), 1)
            self.assertIn('Test_table', log.output[0])
            self.assertIn('header_1', log.output[0])


if __name__ == '__main__':
    unittest.main()
