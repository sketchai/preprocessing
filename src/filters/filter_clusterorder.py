from typing import Dict

from filtering_pipeline.filters.abstract_filter import AbstractFilter
from collections import defaultdict

class FilterClusterOrder(AbstractFilter):
    """
        A filter that clusters the sequences based on their order encoding
    """

    def __init__(self, conf_filter: Dict = None):
        self.name = 'FilterClusterOrder'
        super().__init__()
        self.dict = defaultdict(list)

    def process(self,message: object) -> object:
        sequence = message.get('sequence')
        key = message.get('str_sequence_encoding')
        self.dict[key].append(sequence)
        return message

    def last_process(self, message: object) -> object:
        message['order_clusters'] = self.dict
        return message