import sys
sys.path.append('src/sketchgraphs/')
sys.path.append('src/filtering-pipeline/')

from sketch_data.catalog_primitive import Point
from sketch_data.catalog_constraint import Distance
from src.filters.filter_clusterparamvalues import FilterClusterParamValues
import unittest
import logging
import numpy as np

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestFilterClusterParamValues(unittest.TestCase):

    def test_process(self):
        array = np.array([
            [1., 0., 0.5],
            [0., 0.5, 1.],
            [0., 1., 0.]
        ])
        node_op_0 = Point(status_construction = True, point = [0.1, 0.1])
        node_op_1 = Point(status_construction = False, point = [0.3, 0.6])
        node_op_2 = Point(status_construction = False, point = [0.5, 0.4])
        mock_edge_op = Distance(distance_min=1.,references=None)
        message = {
            'list_of_sequences': [
                [node_op_0, mock_edge_op],
                ['this sequence should not be selected'],
                [node_op_1, mock_edge_op],
                [node_op_2, mock_edge_op]
            ],
            'params_array': array,
            'params_indexes': [0,2,3]
        }
        filter1 = FilterClusterParamValues()
        result = filter1.process(message)
        weights = result['weights']
        self.assertAlmostEqual(sum(weights), 1.)
        self.assertEqual(len(weights), 4)
        np.testing.assert_allclose(weights,[0.5, 0., 0.25, 0.25])
        logger.debug(weights)