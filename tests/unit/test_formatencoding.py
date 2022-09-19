import sys

import unittest
from sam.primitive import Primitive, PrimitiveType
from sam.catalog_primitive import Arc, Line, Circle, Point
from sam.catalog_constraint import Length, Distance
from src.filters.filter_formatencoding import format_for_encoding
from src.utils.logger import logger

class TestFormatEncoding(unittest.TestCase):
    def test_format_for_encoding(self):
        node_op_0 = Point(status_construction = False, point = [0., 1.]) 
        edge_op_1 = Length(references=[node_op_0], length = 6.)
        node_op_2 = Line(pnt1 = [8.,-8.], pnt2 = [9.,10.])
        edge_op_3 = Distance(references=[node_op_2.pnt1, node_op_0], distance_min= 1.)
        node_op_4 = Point(status_construction = False, point = [0., 1.]) 


        mock_sequence_1 = [node_op_0, edge_op_1, node_op_2, edge_op_3, node_op_4]
        new_seq = format_for_encoding(mock_sequence_1)
        logger.debug(new_seq)

        self.assertEqual(edge_op_3.references[1].node_index, node_op_0.node_index)
        self.assertEqual(edge_op_3.references[0].node_index, node_op_2.pnt1.node_index)
        node_indexes = [p.node_index for p in new_seq if isinstance(p,Primitive)]
        self.assertListEqual(node_indexes, [0,1,2,3,4])
        self.assertEqual(len(new_seq),1+1+5+1+1)