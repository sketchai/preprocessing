from typing import Dict
import logging
from collections import defaultdict

from src.filters.utils.filter_functiononparam import FilterFunctionOnParam

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class FilterCollectParamValue(FilterFunctionOnParam):
    """
        A filter that accesses the value of some parameter and stores its location for later
        (e.g. the length of Lines and the radius of Circles)

        conf_filter:
            request:
                (node, EntityType.Line): 'length'
    """

    def __init__(self, conf: Dict = {}):
        super().__init__(conf)
        self.name = 'SaveParamValue'
        self.values = defaultdict(list)
        self.references = defaultdict(list)

    def apply_function(self, message: Dict, additional_parameters: Dict) -> Dict:
        """
        This function saves the parameter value and references into a dict
        """
        op = message.get('op')
        param_value = op.parameters.get(additional_parameters)
        self.values[additional_parameters].append(param_value)
        self.references[additional_parameters].append(op.parameters)
        return message
