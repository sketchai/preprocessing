import sys

import logging
import unittest
from sam.primitive import PrimitiveType
from sam.constraint import ConstraintType
from sam.catalog_primitive import *
from sam.catalog_constraint import *
from src.filters.filter_encodeorder import FilterEncodeOrder
from src import OPS_ENCODING_TAG

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestFilterEncodeOrder(unittest.TestCase):

    def test_process(self):
        l_keep_edge = [ConstraintType.COINCIDENT, ConstraintType.DISTANCE]
        l_keep_node = [PrimitiveType.POINT, PrimitiveType.CIRCLE,PrimitiveType.ARC]

        mock_sequence_1 = [
            Point(point = [1., 2.]),
            Distance(references=[1,2], distance_min = 6.),
            Arc(center = [7., -7.], radius = 7., angles = [45,90]),
        ]
        conf_dict = {'l_keep_node': l_keep_node, 'l_keep_edge': l_keep_edge}
        filter1 = FilterEncodeOrder(conf_filter=conf_dict)
        message = {'sequence': mock_sequence_1}
        filter1.process(message)
        
        edge_offset = len(l_keep_node) 
        ref_offset = len(l_keep_node) + len(l_keep_edge)
        expected_encoding = [ 0, 4 , 2 ]
        #     filter1.node_idx_map[0],
        #     filter1.edge_idx_map[3]+edge_offset,
        #     0+ref_offset,
        #     filter1.node_idx_map[2],
        # ]
        self.assertListEqual(message[OPS_ENCODING_TAG], expected_encoding)