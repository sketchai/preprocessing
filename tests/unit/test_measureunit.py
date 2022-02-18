import unittest
import logging


from src.filters.filter_measureunit import FilterMeasureUnit
from src.sketchgraphs.sketchgraphs.data.sequence import EdgeOp, NodeOp, ConstraintType
from src.filteringpipeline.src.filters import KO_FILTER_TAG

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestFilterMeasureUnit(unittest.TestCase):

    def test_length(self):

        # First Filter : Check if length is in one of the accepted units
        conf_filter1 = {
            'angle_regex': None,
            'length_regex': '.* (METER)|(CENTIMETER)|(FEET)'
        }
        filter1 = FilterMeasureUnit(conf_filter=conf_filter1)

        # A message with nothing to check
        message_1 = {'op': EdgeOp(
            label=ConstraintType.Coincident,
            references=(17, 12),
            parameters={}
        )
        }
        answer = filter1.process(message_1)
        self.assertDictEqual(answer, message_1)

        # A message with a length in the right unit
        message_2 = {'op': EdgeOp(
            label=ConstraintType.Diameter,
            references=(1,),
            parameters={'length': '0.008 METER'}
        )
        }
        answer = filter1.process(message_2)
        self.assertDictEqual(answer, message_2)

        # A message with a length in another accepted unit
        message_3 = {'op': EdgeOp(
            label=ConstraintType.Diameter,
            references=(1,),
            parameters={'length': '12e-1 FEET'}
        )
        }
        answer = filter1.process(message_3)
        self.assertDictEqual(answer, message_3)

        # A message with a length in an unknown unit

        message_4 = {'op': EdgeOp(
            label=ConstraintType.Diameter,
            references=(1,),
            parameters={'length': '3'}
        )
        }
        answer = filter1.process(message_4)
        self.assertIsNotNone(answer.get(KO_FILTER_TAG))

        # A constraint with no length

        message_5 = {'op': EdgeOp(
            label=ConstraintType.Diameter,
            references=(1,),
            parameters={}
        )
        }

        answer = filter1.process(message_5)
        self.assertIsNotNone(answer.get(KO_FILTER_TAG))

    def test_angle(self):

        # Second Filter : Check if angle is in one of the accepted units
        conf_filter1 = {
            'angle_regex': '.* (RAD)|(DEGREES)'
        }
        filter1 = FilterMeasureUnit(conf_filter=conf_filter1)

        # A message with nothing to check
        message_1 = {'op': EdgeOp(
            label=ConstraintType.Coincident,
            references=(17, 12),
            parameters={}
        )
        }
        answer = filter1.process(message_1)
        self.assertDictEqual(answer, message_1)

        # A message with an angle in the right unit
        message_2 = {'op': EdgeOp(
            label=ConstraintType.Angle,
            references=(1,),
            parameters={'angle': '0.008 DEGREE'}
        )
        }
        answer = filter1.process(message_2)
        self.assertDictEqual(answer, message_2)

        # A message with an angle in an unknown unit

        message_3 = {'op': EdgeOp(
            label=ConstraintType.Angle,
            references=(1,),
            parameters={'angle': '3 PI'}
        )
        }
        answer = filter1.process(message_3)
        self.assertIsNotNone(answer.get(KO_FILTER_TAG))
