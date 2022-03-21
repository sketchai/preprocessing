import sys
sys.path.append('src/sketchgraphs/')
sys.path.append('src/filtering-pipeline/')

from sketchgraphs.data.sequence import EdgeOp, NodeOp, EntityType, ConstraintType
from src.filters.filter_dof import FilterDof
import unittest
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestFilterDoF(unittest.TestCase):

    def test_process(self):
        # n <= max nodes, should not send KO
        self.mock_sequence_1 = [
            NodeOp(label=EntityType.Line),
            NodeOp(label=EntityType.Line),
            EdgeOp(label=ConstraintType.Vertical, references=(0,)),
            EdgeOp(label=ConstraintType.Vertical, references=(1,))
        ]
        expected_dof = 6
        filter1 = FilterDof()
        message = {'sequence': self.mock_sequence_1}
        res = filter1.process(message)
        self.assertEqual(res['dof'], expected_dof)
        answer = filter1.last_process(message)
