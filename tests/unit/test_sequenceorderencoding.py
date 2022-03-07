from src.filters.filter_sequenceorderencoding import FilterSequenceOrderEncoding
import logging
import unittest
import sys
sys.path.append('src/sketchgraphs/')
sys.path.append('src/filtering-pipeline/')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestFilterSequenceOrderEncoding(unittest.TestCase):

    def test_process(self):
        filter1 = FilterSequenceOrderEncoding()
        message = {'sequence_encoding': [1, 0, 10, 100, 1, 0]}
        message = filter1.process(message)
        result = message['str_sequence_encoding']
        self.assertEqual(result, '[1, 0, 10, 100, 1, 0]')
