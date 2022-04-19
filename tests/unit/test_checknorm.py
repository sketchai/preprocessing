import sys
sys.path.append('src/sketchgraphs/')
sys.path.append('src/filtering-pipeline/')

from src.filters.filter_checknorm import FilterCheckNorm
from filtering_pipeline import KO_FILTER_TAG
from sketchgraphs.data.sequence import NodeOp, EdgeOp, ConstraintType, EntityType
import logging
import unittest


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestFilterCheckNorm(unittest.TestCase):

    def test_process(self):
        filter1 = FilterCheckNorm()
        # Test msg with an incorrect edge param value
        message = {'sequence': [EdgeOp(label=ConstraintType.Distance, references=(0,1), parameters= {
            'direction': '%#-~@g', 'halfSpace0': 'LEFT', 'halfSpace1': 'RIGHT', 'length': 2**0.5})]}

        answer = filter1.process(message=message)
        self.assertEqual(filter1.name,answer[KO_FILTER_TAG])

        # Test msg with an incorrect edge param value
        message = {'sequence': [EdgeOp(label=ConstraintType.Distance, references=(0,1), parameters= {
            'direction': 'MINIMUM', 'halfSpace0': 'LEFT', 'halfSpace1': 'RIGHT', 'length': 2**0.5+0.1})]}

        answer = filter1.process(message=message)
        self.assertEqual(filter1.name,answer[KO_FILTER_TAG])

        # Test msg with correct edge param values
        message = {'sequence': [EdgeOp(label=ConstraintType.Distance, references=(0,1), parameters= {
            'direction': 'MINIMUM', 'halfSpace0': 'LEFT', 'halfSpace1': 'RIGHT', 'length': 2**0.5})]}

        answer = filter1.process(message=message)
        self.assertIsNone(answer.get(KO_FILTER_TAG))

        # Test msg with an incorrect node param value
        message = {'sequence': [NodeOp(label=EntityType.Point, parameters={'isConstruction':0, 'x':0.,'y':1.02})]}

        answer = filter1.process(message=message)
        self.assertEqual(filter1.name,answer[KO_FILTER_TAG])

        # Test msg with correct node param values
        message = {'sequence': [NodeOp(label=EntityType.Point, parameters={'isConstruction':0, 'x':0.,'y':1.})]}

        answer = filter1.process(message=message)
        self.assertIsNone(answer.get(KO_FILTER_TAG))