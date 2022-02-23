from typing import Dict
import re
import logging

from src.filters.utils.filter_functiononparam import FilterFunctionOnParam
from ..filteringpipeline.src.filters import KO_FILTER_TAG


# a regex that should match all numbers in float notation or '' if no match
NUMBERS_REGEX = r'[-+]?(?:\d*\.\d+|\d+)|$'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def check_regex(l_regex, param_value):
    res = [re.match(regex, param_value) for regex in l_regex]
    return any(res)


class FilterCheckParamsMetrics(FilterFunctionOnParam):
    """
        A filter that checks if metrics are in the right format (e.g. angle are in degree, etc.)

        requests : {(type, label) : {parameter_name : regex}}
    """

    def __init__(self, conf: Dict = {}):
        super().__init__(conf)
        self.name = 'FilterProcessParam'

    def apply_function(self, message: Dict, additional_parameters: Dict) -> Dict:
        """
            Check if a parameter is in the right format
        """
        # read the value of the chosen parameter
        logger.debug(f'here {additional_parameters}')
        op = message.get('op')
        for parameter_name, l_regex in additional_parameters.items():
            param_value = op.parameters.get(parameter_name)
            if not isinstance(param_value, str):  # All the parameters values must be string
                message.update({KO_FILTER_TAG: self.name})
                return message
            else:
                if not check_regex(l_regex, param_value):
                    message.update({KO_FILTER_TAG: self.name})
                    return message

        return message
