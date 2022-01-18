from typing import List, Dict
import logging 

from src.filters.abstract_filter import AbstractFilter, SourceFilter
from src.filters import END_SOURCE_PIPELINE

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

class Pipeline(object):
    
    _filters : List = []
    _source : SourceFilter = None
    _sink : AbstractFilter = None 
    _pipeline_status : bool = False  

    def add_source(self, source : AbstractFilter) -> bool :
        if source is not None :
            self._source = source 
            self._pipeline_status = True 
            return True
        else :
            return False

    def add_sink(self, sink : AbstractFilter) -> bool :
        if sink is not None :
            self._sink = sink 
            return True
        else :
            return False

    def add_filter(self, filter: AbstractFilter) -> bool:
        if filter is not None :
            self._filters.append(filter)
            return True
        else :
            return False
    
    def execute(self) -> Dict :

        while self._pipeline_status:
            message = self._source.process()
            logger.debug(f'message: {message}')
            if END_SOURCE_PIPELINE in message : # No more data in the source
                self._pipeline_status = False     
            for filter in self._filters :
                message = filter.process(message)
            if self._sink is not None:
                self._sink.process(message)
        
        return self.generate_last_message()
    
    def generate_last_message(self, message : Dict = {}) -> Dict : 
        return message  