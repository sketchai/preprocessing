import sys
sys.path.append('src/sketchgraphs/')
sys.path.append('src/filtering-pipeline/')


import unittest
import logging

from src.filters.filter_checkparamsmetrics import FilterCheckParamsMetrics
from sketchgraphs.data.sequence import EdgeOp, NodeOp, ConstraintType, EntityType
from filtering_pipeline import KO_FILTER_TAG

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestFilterCollectParamValue(unittest.TestCase):

    def test_process(self):

        # First Filter : Check if length is in one of the accepted units
        conf = {
            'request': {
                ('edge', ConstraintType.Distance): {'length': ['.* METER', '.* FEET']},
                ('edge', ConstraintType.Length): {'length': ['.* METER', '.* FEET']},
                ('edge', ConstraintType.Diameter): {'length': ['.* METER', '.* FEET']},
                ('edge', ConstraintType.Radius): {'length': ['.* METER', '.* FEET']},
            }
        }

        filter1 = FilterCheckParamsMetrics(conf=conf)

        # A message with the wrong type -> OK
        message_0 = {'op': NodeOp(
            label=1,
            parameters={}
        )
        }
        logger.debug('sending msg 0')
        answer = filter1.process(message_0)
        self.assertDictEqual(answer, message_0)
        self.assertIsNone(answer.get(KO_FILTER_TAG))

        # A message with a wrong label -> OK
        message_1 = {'op': EdgeOp(
            label=ConstraintType.Coincident,
            references=(17, 12),
            parameters={}
        )
        }
        logger.debug('sending msg 1')
        answer = filter1.process(message_1)
        self.assertDictEqual(answer, message_1)
        self.assertIsNone(answer.get(KO_FILTER_TAG))

        # A message with a length in the right unit -> OK
        message_2 = {'op': EdgeOp(
            label=ConstraintType.Diameter,
            references=(1,),
            parameters={'length': '0.008 METER'}
        )
        }
        logger.debug('sending msg 2')
        answer = filter1.process(message_2)
        self.assertDictEqual(answer, message_2)
        self.assertIsNone(answer.get(KO_FILTER_TAG))

        # A message with a length in another accepted unit -> OK
        message_3 = {'op': EdgeOp(
            label=ConstraintType.Diameter,
            references=(1,),
            parameters={'length': '12 FEET'}
        )
        }
        logger.debug('sending msg 3')
        answer = filter1.process(message_3)
        self.assertDictEqual(answer, message_3)
        self.assertIsNone(answer.get(KO_FILTER_TAG))

        # A message with a length in an unknown unit -> KO

        message_4 = {'op': EdgeOp(
            label=ConstraintType.Diameter,
            references=(1,),
            parameters={'length': '3'}
        )
        }
        logger.debug('sending msg 4')
        answer = filter1.process(message_4)
        self.assertIsNotNone(answer.get(KO_FILTER_TAG))

        # A constraint with no length -> KO

        message_5 = {'op': EdgeOp(
            label=ConstraintType.Diameter,
            references=(1,),
            parameters={}
        )
        }
        logger.debug('sending msg 5')
        answer = filter1.process(message_5)
        self.assertIsNotNone(answer.get(KO_FILTER_TAG))
