import unittest
import logging

from tests.asset.mock.mock_abstract_filter import MockFilter

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestAbstractFilter(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.mock_filter = MockFilter(conf_filter={})
        self.mock_message_1 = {'a': 1, 'b': 2}
        self.mock_message_2 = {'a': 1}

    def test_check(self):
        logger.debug('Test check')
        new_message = self.mock_filter.check(self.mock_message_1)
        self.assertDictEqual(new_message, {'a': 2, 'b': 2})

    def test_check_last(self):
        logger.debug('Test check last')
        last_message = self.mock_filter.check_last({})
        self.assertTrue(last_message, 'Is last')

    def test_update_wrong_ob(self):
        logger.debug('Test update wrong ob')
        self.assertEqual(self.mock_filter.wrong_ob_cnt, 0)

        new_message = self.mock_filter.check(self.mock_message_1)
        self.assertEqual(self.mock_filter.wrong_ob_cnt, 1)

        new_message = self.mock_filter.check(self.mock_message_2)
        self.assertEqual(self.mock_filter.wrong_ob_cnt, 1)
