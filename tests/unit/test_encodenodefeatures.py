import sys


import torch
import unittest
from sam.primitive import Primitive, PrimitiveType
from sam.catalog_primitive import Arc, Line, Circle, Point
from sam.catalog_constraint import *
from src.filters.filter_encodenodefeatures import FilterEncodeNodeFeatures, PrimitiveVoid
from src.filters.filter_formatencoding import format_for_encoding
from src.utils.logger import logger

class TestFilterEncodeNodeFeatures(unittest.TestCase):

    def test_process(self):
        n_bins = 50
        lMax = 6
        l_keep_node = [PrimitiveType.POINT, PrimitiveType.LINE,PrimitiveType.ARC]
        node_op_0 = Point(status_construction = False, point = [0., 1.]) 
        edge_op_1 = Length(references=node_op_0, length=1.)
        node_op_2 = Line(status_construction = False, pnt1 = [0.,0.], pnt2 = [1.,1.])
        mock_sequence_1 = [node_op_0, edge_op_1, node_op_2]
        conf_dict = {'l_keep_node': l_keep_node, 'n_bins': n_bins, 'lMax': lMax}
        filter1 = FilterEncodeNodeFeatures(conf_filter=conf_dict)
        mock_sequence_1 = format_for_encoding(mock_sequence_1)
        message = {'sequence': mock_sequence_1}
        message = filter1.process(message)

        # check that 'node_ops' is padded with 'void' nodes
        self.assertEqual(message['node_ops'][0], node_op_0)
        self.assertEqual(message['node_ops'][1], node_op_2)
        self.assertEqual(message['node_ops'][2].subnode_type, 'SN_pnt1')
        self.assertEqual(message['node_ops'][3].subnode_type, 'SN_pnt2')
        self.assertTrue(isinstance(message['node_ops'][4], PrimitiveVoid))
        self.assertTrue(isinstance(message['node_ops'][5], PrimitiveVoid))
        
        # check that the label is encoded with ints.
        # 'SN_pnt1' 'SN_pnt2' and 'void' should have encoding 3,4 and 6 resp.
        torch.testing.assert_allclose(message['node_features'], torch.tensor([0, 1, 3, 4, 6, 6]))

        # coords parameters are encoded from [-1,1] (float) to [0,n_bins-1] (int):
        # -1. -> 0
        #  0. -> n_bins // 2
        #  1. -> n_bins - 1

        # length parameters are encoded from [-srt(2),sqrt(2)] to [0,n_bins-1]
        expected_result = {
            'POINT' : { 'index': torch.tensor([0,2,3]),
                        'value': torch.tensor([ [0, n_bins//2,  n_bins-1],
                                                [0, n_bins//2,  n_bins//2],
                                                [0, n_bins-1,   n_bins-1],])
                        },
            'LINE': {'index': torch.tensor([1]), 'value': torch.tensor([[0]])},
            'CIRCLE': {'index': torch.tensor([], dtype=torch.int64), 'value': torch.zeros((0,2), dtype=torch.int64)},
            'ARC': {'index': torch.tensor([], dtype=torch.int64), 'value': torch.zeros((0,4), dtype=torch.int64)},
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

        # check mask with len(node_ops) = 4
        expected_mask = [False]*4 + [True]*(lMax-4)
        torch.testing.assert_allclose(message['mask_attention'], expected_mask)
