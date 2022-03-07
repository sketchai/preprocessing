from typing import Dict
import logging
from filtering_pipeline.filters.abstract_filter import AbstractFilter

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class FilterSequenceOrderEncoding(AbstractFilter):
    """
        A filter that takes a list of op-level encodings and converts it into a sequence-level encoding
    """

    def __init__(self, conf_filter: Dict = {}):
        super().__init__()
        self.name = 'FilterSequenceOrderEncoding'

    def process(self, message: object) -> object:
        sequence_encoding = message.get('sequence_encoding')
        message['str_sequence_encoding'] = str(sequence_encoding)
        return message
