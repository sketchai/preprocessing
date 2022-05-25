import sys

from sam.catalog_primitive import Point
from sam.catalog_constraint import Distance
from src.filters.filter_clusterparamvalues import FilterClusterParamValues
import unittest
import logging
import numpy as np

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestFilterClusterParamValues(unittest.TestCase):

    def test_process(self):
        node_op_0 = Point(status_construction = True, point = [0.1, 0.1])
        node_op_1 = Point(status_construction = False, point = [0.1, 0.1])
        node_op_2 = Point(status_construction = False, point = [0.1, 0.1])
        mock_edge_op = Distance(distance_min=1.,references=None)
        message = {
            'list_of_sequences': [
                [node_op_0, mock_edge_op],
                [node_op_1, mock_edge_op],
                [node_op_2, mock_edge_op]
            ],
            'd_cluster': {(1,0,0):[0], (0,0,0):[1,2]}
        }
        filter1 = FilterClusterParamValues()
        result = filter1.process(message)
        weights = result['weights']
        self.assertAlmostEqual(sum(weights), 1.)
        np.testing.assert_allclose(weights,[0.5, 0.25, 0.25])
        logger.debug(weights)