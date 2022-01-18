from abc import ABC, abstractmethod
from typing import Dict

from src.filters import END_SOURCE_PIPELINE

class AbstractFilter(ABC):

    @abstractmethod
    def process(self, message: Dict) -> Dict:
        raise NotImplementedError("process function must be implemented")



class SourceFilter(AbstractFilter):

    def __init__(self) :
        self.gen = self.generator()

    def generator(self) -> Dict :
        pass 
    
    def process(self) -> Dict :
        message = {}
        while True :
            try:
                return next(self.gen)
            except StopIteration:
                return {END_SOURCE_PIPELINE : 'True'}

