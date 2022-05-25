import sys

from filtering_pipeline import KO_FILTER_TAG
from sketchgraphs.data.sequence import EdgeOp, NodeOp
from sam.catalog_primitive import Arc, Line, Circle, Point
from sam.catalog_constraint import *

from src.filters.filter_convert_exchangeformat import FilterConvertSequence
from src.utils.logger import logger
import unittest



class TestFilterCount(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.filter = FilterConvertSequence(conf= {'nb_nodes': None, 'nb_edges': 1})


    def test_two_circles(self):
        mock_sequence = [
            NodeOp(label=7), # External
            NodeOp(label=2, parameters = {'isConstruction': False, 'clockwise': False, 'xCenter': 0.0,  # Circle
                                            'yCenter': 0.0, 'xDir': 1.0, 'yDir': 0.0, 'radius': 0.07468157776994294}),
            NodeOp(label=103), # SubnodeType.SN_Center
            EdgeOp(label=101, references=[2,1]), # ConstraintType.Subnode
            EdgeOp(label=0, references=[2,0]), # Coincident
            NodeOp(label=2, parameters={'isConstruction': False, 'clockwise': False, 'xCenter': 0.0, 'yCenter': 0.0, 
                            'xDir': 1.0, 'yDir': 0.0, 'radius': 0.06665470513285787}), # Circle
            NodeOp(label=103), # SubnodeType.SN_Center
            EdgeOp(label=101, references=[4,3]), # ConstraintType.Subnode
            EdgeOp(label=0, references=[4,2]), # Coincident
            NodeOp(label=8), # Stop
        ]

        answer = self.filter.process({'sequence': mock_sequence})
        logger.debug(f'answer= {answer}')
        self.assertIsNone(answer.get(KO_FILTER_TAG))

        sketch = answer.get('sequence')
        self.assertEqual(len(sketch), 3)
        self.assertTrue(isinstance(sketch[0], Circle))
        self.assertTrue(isinstance(sketch[1], Circle))
        self.assertTrue(isinstance(sketch[2], Coincident))


        
