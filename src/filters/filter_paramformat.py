from typing import Dict
import re
import logging

from src.filters.filter_functiononparam import FilterFunctionOnParam
from ..filteringpipeline.src.filters import KO_FILTER_TAG
from src.sketchgraphs.sketchgraphs.data.sequence import EdgeOp, NodeOp

# a regex that should match all numbers in float notation or '' if no match
NUMBERS_REGEX = r'[-+]?(?:\d*\.\d+|\d+)|$'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class FilterParamFormat(FilterFunctionOnParam):
    """
        A filter that access the value of a parameter and format it

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
                        if None, the value is not converted and stays as a string

        example :
            {
                'type': 'edge'
                'label': ConstraintType.Angle
                'param': 'angle'
                'format_dict': {
                    'RAD': 1.
                    'DEGREE': 0.01745
                }

            }
    """

    def __init__(self, conf_filter: Dict = {}):
        super().__init__()

        self.name = 'FilterProcessParam'

        # Parse the conf_dict into a request dictionnary
        type_of_op = conf_filter.get('type')
        l_label = conf_filter.get('label')
        param = conf_filter.get('param')
        format_dict = conf_filter.get('format_dict')

        if param is None:
            raise Exception(f'Specifying a param for {self.name} is mandatory')

        if not isinstance(l_label, list):
            l_label = [l_label]

        self.request = {}

        # here the kwargs are constant
        function_kwargs = {'parameter_name': param, 'format_dict': format_dict}

        for label in l_label:
            self.request.update({
                (type_of_op, label): function_kwargs
            })

    def apply_function(self, message: object, parameter_name: str, format_dict: dict) -> object:
        """
        This function formats the given parameter using the format_dict.
        If it fails, a KO_FLAG is sent.
        """
        # read the value of the chosen parameter
        op = message.get('op')
        param_value = op.parameters.get(parameter_name)

        if not isinstance(param_value, str):
            message.update({KO_FILTER_TAG: self.name})
            return message

        # Check that it correctly matches one of the regex
        format_is_in_keys = False
        for regex, unit_format in format_dict.items():
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
            op.parameters.update({parameter_name: new_param_value})

        return message
