import sys

sys.path.append('src/sketchgraphs/')
sys.path.append('src/filtering-pipeline')

import unittest
import logging
import numpy as np

from src.utils.bounding_box import compute_coords_of_entity
from src.filters.filter_boundingbox import FilterBoundingBox
from sketchgraphs.data.sequence import EdgeOp, NodeOp, EntityType, ConstraintType
from filtering_pipeline import KO_FILTER_TAG

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestFilterBoundingBox(unittest.TestCase):

    def test_last_process(self):
        sequence_1 = [
            NodeOp(label=EntityType.Point, parameters={'x': 1., 'y': 2.}),
            NodeOp(label=EntityType.Circle, parameters={'xCenter': 3., 'yCenter': 4., 'radius': 5.}),
            EdgeOp(label=ConstraintType.Distance, references=None, parameters={'length': 6.}),
            EdgeOp(label=ConstraintType.Length, references=None, parameters={'length': 6.}),
            EdgeOp(label=ConstraintType.Diameter, references=None, parameters={'length': 6.}),
            EdgeOp(label=ConstraintType.Radius, references=None, parameters={'length': 6.}),
            NodeOp(label=EntityType.Arc, parameters={'xCenter': 7., 'yCenter': -7., 'radius': 7., 'xDir': 0.,
             'yDir': 1., 'startParam': 0, 'endParam': np.pi, 'clockwise' : True}),
            NodeOp(label=EntityType.Line, parameters={'pntX': 8., 'pntY': -8., 'startParam': 9.,
             'endParam': 10., 'dirX': 0., 'dirY': 1.}),
        ]

        self.conf_filter = {
            'request': {
                ('node', EntityType.Point): ['x', 'y'],
                ('node', EntityType.Line): ['pntX', 'pntY', 'startParam', 'endParam'],
                ('node', EntityType.Circle): ['xCenter', 'yCenter', 'radius'],
                ('node', EntityType.Arc): ['xCenter', 'yCenter', 'radius'],
                ('edge', ConstraintType.Distance): 'length',
                ('edge', ConstraintType.Length): 'length',
                ('edge', ConstraintType.Diameter): 'length',
                ('edge', ConstraintType.Radius): 'length',
            }
        }

        filter1 = FilterBoundingBox(conf_filter=self.conf_filter)

        for op in sequence_1:
            message = {'op': op}
            message = filter1.process(message)

        message = filter1.last_process(message)

        # check that the NodeOps are in the box
        for op in sequence_1:
            x_coords, y_coords = compute_coords_of_entity(op)
            for coord in x_coords + y_coords:
                self.assertGreater(coord,-0.0001)
                self.assertLess(coord,1.0001)
        
        # check that EdgeOps are also normalized
        constraints_parameter = [
            sequence_1[2].parameters['length'],
            sequence_1[3].parameters['length'],
            sequence_1[4].parameters['length'],
            sequence_1[5].parameters['length'],
        ]
        for parameter in constraints_parameter:
            self.assertGreater(parameter,-2**0.5 + 1e-4)
            self.assertLess(parameter,2**0.5 + 1e-4)

