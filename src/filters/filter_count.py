from typing import Dict
import logging
from ..filteringpipeline.src.filters.abstract_filter import AbstractFilter
from src.filteringpipeline.src.filters import KO_FILTER_TAG

from src.sketchgraphs.sketchgraphs.data import sketch as datalib, sequence


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class FilterCount(AbstractFilter):
    """
        A filter that count operations

        conf_filter arguments :

            'min' : int or None, inclusive minimum number of op
            'max' : int or None, inclusive maximum number of op
            'type' : str, type of op to count

                'node' to count sequence.NodeOp or 
                'edge' to count sequence.EdgeOp 

        last_process_action :

            returns a KO_FILTER_TAG if not min <= count <= max
    """

    def __init__(self, conf_filter: Dict = {}):
        super().__init__()
        self.min : int = conf_filter.get('min')
        self.max : int = conf_filter.get('max')
        type_str = conf_filter.get('type')
        if type_str=='node':
            self.type = sequence.NodeOp
        elif type_str=='edge':
            self.type = sequence.EdgeOp
        else : raise Exception()
        self.count : int = 0
        self.name = 'CountFilter'

    def process(self, message: object) -> object:
        logger.debug(f'message received: {message}')
        op = message.get('op')
        if isinstance(op, self.type):
                self.count += 1
        return message

    def last_process(self, message: Dict) -> Dict:
        KO_flag = False
        if self.min is not None :
            if self.count < self.min :
                KO_flag = True
        if self.max is not None :
            if self.count > self.max:
                KO_flag = True
                
        if KO_flag : message.update({KO_FILTER_TAG: self.name})
        return message