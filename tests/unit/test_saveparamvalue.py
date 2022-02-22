import unittest
import logging


from src.filters.filter_saveparamvalue import FilterSaveParamValue
from src.sketchgraphs.sketchgraphs.data.sequence import EdgeOp, NodeOp, EntityType
from src.filteringpipeline.src.filters import KO_FILTER_TAG

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestFilterSaveParamValue(unittest.TestCase):
    def test_length(self):
        conf_filter1 = {
            'request': {
                ('node', EntityType.Line): {'parameter_name': 'length'},
                ('node', EntityType.Circle): {'parameter_name': 'radius'}
            }
        }
        filter1 = FilterSaveParamValue(conf_filter=conf_filter1)
        logger.debug(filter1.request)
        self.mock_sequence_1 = [
            NodeOp(label=0, parameters={'radius': 0}),  # wrong label
            EdgeOp(label=0, references=(1, 2), parameters={'radius': 0}),  # wrong type
            NodeOp(label=2, parameters={'radius': 42}),  # a Circle
            NodeOp(label=3),
            NodeOp(label=1, parameters={'length': 1}),  # a Line
            NodeOp(label=2, parameters={'radius': -42}),  # another Circle
            EdgeOp(label=0, references=(1, 2)),
            NodeOp(label=12)
        ]

        for op in self.mock_sequence_1:
            message = {'op': op}
            filter1.process(message)

        self.assertEqual(filter1.values['radius'], [42, -42])
        self.assertEqual(filter1.values['length'], [1])
