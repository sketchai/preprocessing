from typing import Dict

from ..filteringpipeline.src.filters.abstract_filter import AbstractFilter
from ..filteringpipeline.src.filters import KO_FILTER_TAG


class FilterCheckLabel(AbstractFilter):
    """
        A filter check is the label contained into a message is ok or not
    """

    def __init__(self, conf_filter: Dict = {}):
        super().__init__()
        self.label_list = conf_filter.get('label_list')
        self.name = 'FilterCheckLabel'

    def process(self, message: object) -> object:
        if message.get('status', False):
            return message
        else:
            op = message.get('op')
            if op.label not in self.label_list:
                message.update({KO_FILTER_TAG: self.name})
            return message
