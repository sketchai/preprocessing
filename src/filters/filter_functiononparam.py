from typing import Dict
import re
import logging

from ..filteringpipeline.src.filters.abstract_filter import AbstractFilter
from ..filteringpipeline.src.filters import KO_FILTER_TAG
from src.sketchgraphs.sketchgraphs.data.sequence import EdgeOp, NodeOp


TYPE_OF_OP_FROM_NAME = {'edge' : EdgeOp, 'node' : NodeOp}

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class FilterFunctionOnParam(AbstractFilter):
    """
        A filter that check the operation and apply a function if it corresponds to the request

        The request and the function must be implemented for children filters

        The request can be directly written in the yml if it's simple enough :

            request:
                (type_A, label_A):
                    function_argument_1 : value
                    function_argument_2 : value

                (type_B, label_B):
                    function_argument_1 : value
                    function_argument_2 : value

        Otherwise, it should be overwritten in the children's __init__ method

    """

    def __init__(self, conf_filter: Dict = {}):
        super().__init__()

        self.name = 'FilterFunctionOnParam'
        
        self.request = conf_filter.get('request')

    @staticmethod
    def _check_couple(op, requested_type, requested_label) -> bool:
        """
        Test if the op type and label corresponds to the one tested by the filter
        """
        # Test the type of op
        if requested_type is not None:
            type_of_op = TYPE_OF_OP_FROM_NAME.get(requested_type)
            if not isinstance(op,type_of_op):
                return False

        # Test the op.label
        if requested_label is not None:
            if op.label == requested_label:
                return True
        
        return False

    def process(self, message : object) -> object:
        """
        If the operation corresponds to one of the requested couple (type, label), 
        apply a given function
        """
        op = message.get('op')

        for couple, function_kwargs in self.request.items():
            requested_type, requested_label = couple
            found_couple = self._check_couple(op, requested_type, requested_label)
            
            if found_couple:
                logger.debug(function_kwargs)
                message = self.apply_function(message,**function_kwargs)
                return message
        
        return message

    def apply_function(self, message, **kwargs):
        raise NotImplementedError()
