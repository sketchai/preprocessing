from typing import Dict
import re

from ..filteringpipeline.src.filters.abstract_filter import AbstractFilter
from ..filteringpipeline.src.filters import KO_FILTER_TAG
from src.sketchgraphs.sketchgraphs.data import sketch as datalib, sequence

CONSTRAINTS_WITH_A_LENGTH = [
    datalib.ConstraintType.Distance,
    datalib.ConstraintType.Length,
    datalib.ConstraintType.Diameter,
    datalib.ConstraintType.Radius,
]


class FilterMeasureUnit(AbstractFilter):
    """
        A filter that checks that a parameter is in the right unit (meters, rad etc.)

        conf_filter parameters:
            'angle_regex' : str, a regular expression that must match the angle value
            'length_regex' : str

        example :
            'length_regex' : '.* (METER)|(CENTIMETER)|(FEET)'
    """

    def __init__(self, conf_filter: Dict = {}):
        super().__init__()
        self.angle_regex = conf_filter.get('angle_regex')
        self.length_regex = conf_filter.get('length_regex')
        self.name = 'FilterMeasureUnit'

    def process(self, message: object) -> object:
        op = message.get('op')
        KO_flag = False
        if isinstance(op, sequence.EdgeOp):
            if self.angle_regex and op.label == datalib.ConstraintType.Angle:
                angle = op.parameters['angle']
                if not re.match(self.angle_regex, angle):
                    message.update({KO_FILTER_TAG: self.name})
                    return message

            if self.length_regex and op.label in CONSTRAINTS_WITH_A_LENGTH:
                length = op.parameters.get('length')
                if length is None:
                    KO_flag = True
                elif not re.match(self.length_regex, length):
                    KO_flag = True

                if KO_flag:
                    message.update({KO_FILTER_TAG: self.name})
        return message
