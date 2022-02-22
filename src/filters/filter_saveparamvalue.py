from typing import Dict
import re
import logging

from src.filters.filter_functiononparam import FilterFunctionOnParam
from ..filteringpipeline.src.filters import KO_FILTER_TAG
from src.sketchgraphs.sketchgraphs.data.sequence import EdgeOp, NodeOp

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class FilterSaveParamValue(FilterFunctionOnParam):
    """
        A filter that accesses the value of some parameter and stores it for later

        [this is an illustration of a FilterFunctionOnParam child]

        example:
            a filter that stores the length of Lines,
            and the radius of Circles

        conf_filter:
            request:
                (node, EntityType.Line):
                    parameter_name: 'length'

                (node, EntityType.Circle):
                    parameter_name: 'radius'

    """

    def __init__(self, conf_filter: Dict = {}):
        super().__init__(conf_filter)

        self.name = 'SaveParamValue'
        
        self.values = {}

    def apply_function(self, message: object, parameter_name: str) -> object:
        """
        This function saves the parameter value into a dict
        """
        op = message.get('op')
        param_value = op.parameters.get(parameter_name)

        if parameter_name in self.values.keys():
            self.values[parameter_name].append(param_value)
        else:
            self.values[parameter_name] = [param_value]

        return message


        

