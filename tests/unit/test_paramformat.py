import unittest
import logging


from src.filters.filter_paramformat import FilterParamFormat
from src.sketchgraphs.sketchgraphs.data.sequence import EdgeOp, NodeOp, ConstraintType
from src.filteringpipeline.src.filters import KO_FILTER_TAG


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestFilterParamFormat(unittest.TestCase):

    def test_length(self):

        l_constraints_with_a_length = [
            ConstraintType.Distance, ConstraintType.Length,
            ConstraintType.Diameter, ConstraintType.Radius,
        ]

        # First Filter : Check if length is in one of the accepted units
        conf_filter1 = {
            'type': 'edge',
            'label': l_constraints_with_a_length,
            'param': 'length',
            'format_dict': {
                '.* METER': None,
                '.* FEET': None,
            }
        }
        filter1 = FilterParamFormat(conf_filter=conf_filter1)

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

    def test_angle(self):

        # Second Filter : Check if angle is in one of the accepted units then convert it
        conf_filter1 = {
            'type': 'edge',
            'label': ConstraintType.Angle,
            'param': 'angle',
            'format_dict': {
                '.* RAD': 1.,
                '.* DEGREE': 0.01745,
            }
        }
        filter1 = FilterParamFormat(conf_filter=conf_filter1)

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

        # A message with an angle in the right unit -> convert
        message_2 = {'op': EdgeOp(
            label=ConstraintType.Angle,
            references=(1,),
            parameters={'angle': '180 DEGREE'}
        )
        }
        logger.debug('sending msg 2')
        answer = filter1.process(message_2)
        self.assertAlmostEqual(answer['op'].parameters['angle'], 3.1416, delta=1e-3)

        # A message with an angle in the right unit -> convert
        message_3 = {'op': EdgeOp(
            label=ConstraintType.Angle,
            references=(1,),
            parameters={'angle': '3.1416 RAD'}
        )
        }
        logger.debug('sending msg 3')
        answer = filter1.process(message_3)
        self.assertAlmostEqual(answer['op'].parameters['angle'], 3.1416, delta=1e-3)

        # A message with an angle in an unknown unit

        message_4 = {'op': EdgeOp(
            label=ConstraintType.Angle,
            references=(1,),
            parameters={'angle': '3 PI'}
        )
        }
        logger.debug('sending msg 4')
        answer = filter1.process(message_4)
        self.assertIsNotNone(answer.get(KO_FILTER_TAG))
