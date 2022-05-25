import math
import sys
from weakref import ref

import torch
import unittest
from sam.primitive import Primitive, PrimitiveType
from sam.constraint import Constraint, ConstraintType
from sam.catalog_primitive import Arc, Line, Circle, Point
from sam.catalog_constraint import *
from src.filters.filter_encodenodefeatures import PrimitiveVoid
from src.filters.filter_encodeedgefeatures import FilterEncodeEdgeFeatures
from src.utils.logger import logger
from src.filters.filter_formatencoding import SubnodeConstraint
from filtering_pipeline import KO_FILTER_TAG

class TestFilterEncodeEdgeFeatures(unittest.TestCase):

    def test_process(self):
        n_bins = 50
        l_keep_edge = [ConstraintType.HORIZONTAL, ConstraintType.VERTICAL, ConstraintType.LENGTH]
        
        node_op_0 = Line(status_construction=False, pnt1=[0.,0.], pnt2=[1.,1.])
        node_op_1 = Point(status_construction=False, point=[0., 0.])
        edge_op_2 = SubnodeConstraint(references=[node_op_0,node_op_1])
        node_op_3 = Point(status_construction=False, point=[0., 0.])
        edge_op_4 = SubnodeConstraint(references=[node_op_0,node_op_3])
        edge_op_5 = Horizontal(references=[node_op_0])
        edge_op_6 = Length(references=[node_op_0], length=math.sqrt(2))
        mock_sequence_1 = [node_op_0, node_op_1, edge_op_2, node_op_3, edge_op_4, edge_op_5, edge_op_6]
        conf_dict = {'l_keep_edge': l_keep_edge, 'n_bins': n_bins}
        filter1 = FilterEncodeEdgeFeatures(conf_filter=conf_dict)
        message = {'sequence': mock_sequence_1}
        filter1.process(message)
        
        # check that 'edge_ops' contains all edges
        self.assertListEqual(message['edge_ops'],[edge_op_2, edge_op_4, edge_op_5, edge_op_6])

        # check that the label is encoded with ints (according to l_keep_edge)
        logger.debug(filter1.edge_idx_map)
        len_edg = len(l_keep_edge)
        torch.testing.assert_allclose(
            message['edge_features'],
            torch.tensor([len_edg, len_edg, 0, 2]))

        # the length is encoded from [-1,1] (float) to [0,n_bins-1] (int):
        # -1. -> 0
        #  0. -> n_bins // 2
        #  1. -> n_bins - 1
        expected_result = {
            'LENGTH': { 
                'index': torch.tensor([3]),
                'value': torch.tensor([[n_bins-1]])},
                
            # the rest are empty tensors
            'ANGLE': {'index': torch.tensor([], dtype=torch.int64),
                'value': torch.zeros((0,1), dtype=torch.int64)},
            'RADIUS': {'index': torch.tensor([], dtype=torch.int64),
                'value': torch.zeros((0,1), dtype=torch.int64)},
            }
        for key, subdict in message['sparse_edge_features'].items():
            index, value = subdict.values()
            exp_index, exp_value = expected_result[key].values()
            logger.debug(f'{(index,value,exp_index,exp_value)}')

            torch.testing.assert_allclose(index, exp_index)
            torch.testing.assert_allclose(value, exp_value)

        # Test msg with an incorrect param value
        message = {'sequence': [Length(length = 2**0.5+0.1)]}

        answer = filter1.process(message=message)
        self.assertEqual(filter1.name,answer[KO_FILTER_TAG])
