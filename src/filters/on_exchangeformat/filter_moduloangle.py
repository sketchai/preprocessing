from typing import Dict
import numpy as np

from filtering_pipeline.filters.abstract_filter import AbstractFilter
from src.utils.logger import logger


class FilterModuloAngle(AbstractFilter):
    """
        A filter that transforms degrees into radiant angles in [0;2pi].
    """

    def __init__(self, conf: Dict = {}):
        self.name = 'FilterModuloAngle'
        super().__init__(conf)
        self.request = conf.get('request')


    def modify_angle(self, message: object, additional_parameters) -> object:
       
        op = message.get('op')
        if isinstance(additional_parameters, str):
            list_of_params = [additional_parameters]
        else:
            list_of_params = additional_parameters
        
        for parameter_name in list_of_params:
            value = op.__dict__.get(parameter_name)
            value *= np.pi/180
            value %= 2*np.pi
            op.update_parms({parameter_name: value})
        if op.type.name == 'ARC':
            op.radian = True
        return message

    def process(self, message: object) -> object:
        """
        If the operation corresponds to one of the requested couple (type, label), apply function self.apply_function()
        """
        op = message.get('op')
        for name, additional_parameters in self.request.items():
            if op.type.name == name :
                message = self.modify_angle(message, additional_parameters)
        return message