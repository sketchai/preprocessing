from typing import Dict
import re
import logging

from ..filteringpipeline.src.filters.abstract_filter import AbstractFilter
from ..filteringpipeline.src.filters import KO_FILTER_TAG
from src.sketchgraphs.sketchgraphs.data.sequence import EdgeOp, NodeOp

# a regex that should match all numbers in float notation or '' if no match
NUMBERS_REGEX = r'[-+]?(?:\d*\.\d+|\d+)|$'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class FilterParamFormat(AbstractFilter):
    """
        A filter that access the value of parameter and perform an action

        conf_filter:

            'type': str [optional]
                Type of op, must be 'node' or 'edge'.
                If None, both will be inspected

            'label': list(ConstraintType) [optional]
                A single label or a list of labels to inspect
                If None, all labels will be inspected

            'param': str
                Name of the param to inspect

            'format_dict': dict
                a dict that matches units to a format value
                key = a string used as a regex
                value = a float that is multiplied with the converted value

        example :
            {
                'type': 'edge'
                'param': 'angle'
                'format_dict': {
                    'RAD': 1.
                    'DEGREE': 0.01745
                }

            }
    """

    def __init__(self, conf_filter: Dict = {}):
        super().__init__()

        self.type_of_op = conf_filter.get('type')
        self.label = conf_filter.get('label')
        self.param = conf_filter.get('param')
        self.format_dict = conf_filter.get('format_dict')
        self.name = 'FilterProcessParam'

        if self.param is None:
            raise Exception(f'Specifying a param for {self.name} is mandatory')

        if isinstance(self.label, int):
            self.label = [self.label]

    def process(self, message: object) -> object:
        op = message.get('op')

        if self.type_of_op is not None:
            if isinstance(op, EdgeOp):
                type_of_op = 'edge'
            elif isinstance(op, NodeOp):
                type_of_op = 'node'

            if not type_of_op == self.type_of_op:
                return message

        if self.label is not None:
            if op.label not in self.label:
                return message

        param_value = op.parameters.get(self.param)

        if not isinstance(param_value, str):
            message.update({KO_FILTER_TAG: self.name})
            return message

        # Check that it correctly matches one of the regex
        format_is_in_keys = False
        for regex, unit_format in self.format_dict.items():
            if re.match(regex, param_value):
                format_is_in_keys = True
                logger.debug(f"{regex} correctly matches {param_value}")
                break

        if not format_is_in_keys:
            logger.debug(f"found no matches")
            message.update({KO_FILTER_TAG: self.name})
            return message

        # Convert it if needed
        if unit_format is not None:
            match = re.findall(NUMBERS_REGEX, param_value)[0]
            if match == '':
                logger.debug('no number found')
                message.update({KO_FILTER_TAG: self.name})
                return message

            logger.debug(f'found number {match} in {param_value}')
            new_param_value = float(match) * unit_format
            op.parameters.update({self.param: new_param_value})

        return message
