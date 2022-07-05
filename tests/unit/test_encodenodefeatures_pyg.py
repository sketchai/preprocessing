import sys
import numpy as np


import torch
import unittest
from sam.primitive import Primitive, PrimitiveType
from sam.catalog_primitive import Arc, Line, Circle, Point
from sam.catalog_constraint import *
from src.filters.filter_encodenodefeatures_pyg import FilterEncodeNodeFeatures
from src.filters.filter_formatencoding import format_for_encoding
from src.utils.logger import logger

class TestFilterEncodeNodeFeatures_pyg(unittest.TestCase):

    def test_process(self):
        n_bins = 50
        l_keep_node = [PrimitiveType.POINT, PrimitiveType.LINE,PrimitiveType.ARC]
        node_op_0 = Point(status_construction = False, point = [0., 1.]) 
        edge_op_1 = Length(references=node_op_0, length=1.)
        node_op_2 = Line(status_construction = False, pnt1 = [0.,0.], pnt2 = [1.,1.])
        mock_sequence_1 = [node_op_0, edge_op_1, node_op_2]
        conf_dict = {'l_keep_node': l_keep_node, 'n_bins': n_bins}
        filter1 = FilterEncodeNodeFeatures(conf_filter=conf_dict)
        mock_sequence_1 = format_for_encoding(mock_sequence_1)
        message = {'sequence': mock_sequence_1}
        message = filter1.process(message)

        self.assertEqual(message['node_ops'][0], node_op_0)
        self.assertEqual(message['node_ops'][1], node_op_2)
        self.assertEqual(message['node_ops'][2].subnode_type, 'SN_pnt1')
        self.assertEqual(message['node_ops'][3].subnode_type, 'SN_pnt2')
        
        # check that the label is encoded with ints.
        # 'SN_pnt1' 'SN_pnt2' should have encoding 3,4 resp.
        # coords parameters are encoded from [-1,1] (float) to [0,n_bins-1] (int):
        # -1. -> 0
        #  0. -> n_bins // 2
        #  1. -> n_bins - 1

        # length parameters are encoded from [-srt(2),sqrt(2)] to [0,n_bins-1]
        pad = 0
        expected_result = np.array([
            [0, 0, n_bins//2,  n_bins-1, pad],
            [1, 0, pad, pad, pad],
            [3, 0, n_bins//2,  n_bins//2, pad],
            [4, 0, n_bins-1,   n_bins-1, pad],
        ]
        )
        np.testing.assert_allclose(message['node_features'], expected_result)

        