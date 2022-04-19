from typing import Dict
import numpy as np

from filtering_pipeline.filters.abstract_filter import AbstractFilter
from src.utils.logger import logger


class FilterModuloAngle(AbstractFilter):
    """
        A filter that transposes radiant angles in [0;2pi].
    """

    def __init__(self, conf: Dict = {}):
        self.name = 'FilterModuloAngle'
        super().__init__(conf)
        self.request = conf.get('request')


    def apply_function(self, message: object, additional_parameters) -> object:
       
        op = message.get('op')
        if isinstance(additional_parameters, str):
            list_of_params = [additional_parameters]
        else:
            list_of_params = additional_parameters
        
        for parameter_name in list_of_params:
            value = op.__dict__.get(parameter_name) 
            value %= 2*np.pi
            op.update_parms({parameter_name: value})
        return message

    def process(self, message: object) -> object:
        """
        If the operation corresponds to one of the requested couple (type, label), apply function self.apply_function()
        """
        op = message.get('op')
        for couple, additional_parameters in self.request.items():
            if isinstance(op , couple) :
                message = self.apply_function(message, additional_parameters)
        return message