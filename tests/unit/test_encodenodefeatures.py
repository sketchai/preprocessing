import sys

sys.path.append('src/sketchgraphs/')
sys.path.append('sketch_data/')
sys.path.append('src/filtering-pipeline/')

import torch
import logging
import unittest
from sketch_data.primitive import Primitive, PrimitiveType
from sketch_data.catalog_primitive import Arc, Line, Circle, Point
from sketch_data.catalog_constraint import *
from src.filters.filter_encodenodefeatures import FilterEncodeNodeFeatures, PrimitiveVoid

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestFilterEncodeNodeFeatures(unittest.TestCase):

    def test_process(self):
        n_bins = 50
        lMax = 4
        l_keep_node = [PrimitiveType.POINT, PrimitiveType.LINE,PrimitiveType.ARC]
        node_op_0 = Point(status_construction = False, point = [0., 1.]) 
        edge_op_1 = Length(references=[10], length = 6.)
        node_op_2 = Line(pnt1 = [8.,-8.], pnt2 = [9.,10.])
        mock_sequence_1 = [node_op_0, edge_op_1, node_op_2]

        conf_dict = {'l_keep_node': l_keep_node, 'n_bins': n_bins, 'lMax': lMax}
        filter1 = FilterEncodeNodeFeatures(conf_filter=conf_dict)
        
        message = {'sequence': mock_sequence_1}
        message = filter1.process(message)

        # check that 'node_ops' is padded with 'void' nodes
        self.assertEqual(message['node_ops'][0], node_op_0)
        self.assertEqual(message['node_ops'][1], node_op_2)
        self.assertTrue(isinstance(message['node_ops'][2], PrimitiveVoid))
        self.assertTrue(isinstance(message['node_ops'][3], PrimitiveVoid))
        
        # check that the label is encoded with ints. 'void' is encoded by len(l_keep_node)
        torch.testing.assert_allclose(message['node_features'], torch.tensor([0, 1, len(l_keep_node), len(l_keep_node)]))

        # coords parameters are encoded from [-1,1] (float) to [0,n_bins-1] (int):
        # -1. -> 0
        #  0. -> n_bins // 2
        #  1. -> n_bins - 1

        # length parameters are encoded from [-srt(2),sqrt(2)] to [0,n_bins-1]
        expected_result = {
            'POINT' : { 'index': torch.tensor([0]), 'value': torch.tensor([[0, n_bins//2, n_bins-1]])},
            'LINE': {'index': torch.tensor([1]), 'value': torch.tensor([[0, n_bins//2, n_bins-1, n_bins//2, n_bins//2, n_bins//2, n_bins-1]])},
            'CIRCLE': {'index': torch.tensor([], dtype=torch.int64), 'value': torch.zeros((0,7), dtype=torch.int64)},
            'ARC': {'index': torch.tensor([], dtype=torch.int64), 'value': torch.zeros((0,9), dtype=torch.int64)},
            }
        
        x = message['sparse_node_features']
        logger.info(f'here {x}')
        # Check sparse node features
        for key, subdict in message['sparse_node_features'].items():
            
            logger.debug(f'key= {key}, subdict = {subdict}')
            index, value = subdict.values()
            exp_index, exp_value = expected_result[key].values()
            torch.testing.assert_allclose(index, exp_index)
            torch.testing.assert_allclose(value, exp_value)

        # check mask with len(node_ops) = 2
        expected_mask = [False]*2 + [True]*(lMax-2)
        torch.testing.assert_allclose(message['mask_attention'], expected_mask)

        # Test msg with an incorrect param value
        message = {'sequence': [NodeOp(label=EntityType.Point, parameters={'isConstruction':0, 'x':0.,'y':1.02})]}

        answer = filter1.process(message=message)
        self.assertEqual(filter1.name,answer[KO_FILTER_TAG])