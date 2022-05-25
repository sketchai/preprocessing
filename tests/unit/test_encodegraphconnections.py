import sys

import numpy as np
import torch
import logging
import unittest
from sam.primitive import Primitive, PrimitiveType
from sam.constraint import Constraint, ConstraintType
from sam.catalog_primitive import Arc, Line, Circle, Point
from sam.catalog_constraint import *
from src.filters.filter_encodenodefeatures import PrimitiveVoid
from src.utils.logger import logger
from src.filters.filter_formatencoding import SubnodeConstraint
from src.filters.filter_encodegraphconnections import FilterEncodeGraphConnections

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestFilterEncodeGraphConnections(unittest.TestCase):

    def test_process(self):

        op_0 = Point(point=[0.,0.])
        op_1 = Circle(center=[0.,0.], radius=1.)
        op_2 = Point(point=[0.,0.])
        op_3 = SubnodeConstraint(references=[op_1,op_2])
        op_4 = Radius(radius=1, references=[op_1])
        mock_sequence_1 = [op_0, op_1, op_2, op_3, op_4]
        for i,op in enumerate([op_0,op_1,op_2]):
            op.node_index = i
        filter1 = FilterEncodeGraphConnections(conf_filter={})
        edge_ops = [op for op in mock_sequence_1 if isinstance(op, Constraint)]
        node_ops = [op for op in mock_sequence_1 if isinstance(op, Primitive)]
        message = {'sequence': mock_sequence_1, 'node_ops': node_ops, 'edge_ops': edge_ops}
        filter1.process(message)
        
        # check that 'incidences' contains all edges
        np.testing.assert_allclose(message['incidences'], [[1,2],[1,1]])

        # subnodes
        np.testing.assert_allclose(message['i_edges_given'], [0])
        
        # other edges
        np.testing.assert_allclose(message['i_edges_possible'], [1])