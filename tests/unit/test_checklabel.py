import unittest
import logging


from src.sketchgraphs.sketchgraphs.data.sequence import NodeOp, EdgeOp
from src.sketchgraphs.sketchgraphs.data import sketch as datalib

from src.filters.filter_checklabel import FilterCheckLabel

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestFilterCheckLabel(unittest.TestCase):

    def test_process(self):
        filter = FilterCheckLabel(conf_filter={'label_list': [datalib.ConstraintType.Coincident, datalib.ConstraintType.Distance, datalib.ConstraintType.Horizontal,
                                                              datalib.EntityType.Point, datalib.EntityType.Line, datalib.EntityType.Circle]})

        # Test 1 : the op fulfills the condition
        message_A = {'op': NodeOp(label=0)}
        message = filter.process(message_A)
        message_A['status'] = True
        self.assertDictEqual(message_A, message)

        message_A = {'op': EdgeOp(label=0, references=(1,))}
        message = filter.process(message_A)
        message_A['status'] = True
        self.assertDictEqual(message_A, message)

        # Test 2 : the op does not fulfill the condition
        message_A = {'op': NodeOp(label=12)}
        message = filter.process(message_A)
        message_A['status'] = False
        self.assertDictEqual(message_A, message)

        message_A = {'op': EdgeOp(label=12, references=(1,))}
        message = filter.process(message_A)
        message_A['status'] = False
        self.assertDictEqual(message_A, message)
