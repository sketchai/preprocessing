import sys
sys.path.append('src/sketchgraphs/')
sys.path.append('sketch_data/')
sys.path.append('src/filtering-pipeline/')

import unittest
from sketch_data.primitive import Primitive, PrimitiveType
from sketch_data.catalog_primitive import Arc, Line, Circle, Point
from sketch_data.catalog_constraint import Length, Distance
from src.filters.filter_formatencoding import format_for_encoding
from src.utils.logger import logger

class TestFormatEncoding(unittest.TestCase):
    def test_format_for_encoding(self):
        node_op_0 = Point(status_construction = False, point = [0., 1.]) 
        edge_op_1 = Length(references=[node_op_0], length = 6.)
        node_op_2 = Line(pnt1 = [8.,-8.], pnt2 = [9.,10.])
        edge_op_3 = Distance(references=[node_op_2.pnt1, node_op_0], distance_min= 1.)

        mock_sequence_1 = [node_op_0, edge_op_1, node_op_2, edge_op_3]
        new_seq = format_for_encoding(mock_sequence_1)
        logger.debug(new_seq)

        self.assertEqual(edge_op_3.references[1].node_index, node_op_0.node_index)
        self.assertEqual(edge_op_3.references[0].node_index, node_op_2.pnt1.node_index)
        self.assertEqual(len(new_seq),1+1+5+1)