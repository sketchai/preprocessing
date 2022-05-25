import sys

import unittest
import numpy as np
from sam.catalog_primitive import Point,Line,Arc
from sam.catalog_constraint import Distance
from src.filters.filter_paramsencoding import FilterParamsEncoding
from src.utils.maps import NODES_PARAMETRIZED
from src.utils.logger import logger


class TestParamsEncoding(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.conf_filter = {'nodes_parametrized': NODES_PARAMETRIZED, 'max_cluster_size': 5}

    def test_process(self):
        # Test with n<=max_cluster_size
        filter1 = FilterParamsEncoding(self.conf_filter)
        message = {'list_of_sequences': [
            [Point(status_construction = True, point = [0.1, 0.3]), Distance(references=None, distance_min=1.)],
            [Point(status_construction = False, point = [0.3, 0.6]), Distance(references=None, distance_min=1.)],
            [Point(status_construction = False, point = [0.35, 0.6]), Distance(references=None, distance_min=1.)],
        ]}

        answer = filter1.process(message)

        result = answer['d_cluster']
        expected = {
            '[4, 0, 1]': [0],
            '[0, 1, 2]': [1,2]
        }
        

        self.assertDictEqual(result,expected)

    def test_encode_sequence(self):
        seq = [
            Point(status_construction=True, point=[0.1,0.2]),
            Distance(references=None, distance_min=1.),
            Line(status_construction=False, pnt1=[0.3,0.4], pnt2=[0.5,0.6]),
            Arc(status_construction=False, center=[0.3,0.4], radius=1., angles=[2*np.pi,0])
        ]
        filter1 = FilterParamsEncoding(self.conf_filter)
        encoding = filter1._encode_sequence(seq)

        expected = str([4,0,1,0,1,2,2,2,0,1,2,4,25,0])
        self.assertSequenceEqual(encoding, expected)
