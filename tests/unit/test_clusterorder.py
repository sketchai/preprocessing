from src.filters.filter_clusterorder import FilterClusterOrder
import logging
import unittest
import sys
sys.path.append('src/sketchgraphs/')
sys.path.append('src/filtering-pipeline/')

from sketchgraphs.data.sequence import NodeOp, EdgeOp

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestFilterClusterOrder(unittest.TestCase):

    def test_process(self):
        filter1 = FilterClusterOrder()
        messages = [
            {
                'sequence': [NodeOp(0), EdgeOp(0,(0,)), NodeOp(1),],
                'str_sequence_encoding': '[0,10,20,1]'
            },
            {
                'sequence': [NodeOp(1), EdgeOp(0,(0,)), NodeOp(1),],
                'str_sequence_encoding': '[1,10,20,1]'
            },
            {
                'sequence': [NodeOp(0), EdgeOp(0,(0,)), NodeOp(1),],
                'str_sequence_encoding': '[0,10,20,1]'
            }
        ]
        for message in messages:
            filter1.process(message)
        self.assertEqual(len(filter1.dict['[0,10,20,1]']),2)
        self.assertEqual(len(filter1.dict['[1,10,20,1]']),1)
    
    def test_last_process(self):
        filter1 = FilterClusterOrder()
        mock_dict = {'k1': [], 'k2': []}
        filter1.dict = mock_dict
        message = {}
        answer = filter1.last_process(message)
        self.assertEqual(answer['order_clusters'], mock_dict)