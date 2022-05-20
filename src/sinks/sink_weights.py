import json
import sys

from typing import Dict
import logging
import numpy as np

from src.utils import flat_array
from filtering_pipeline.filters.abstract_filter import AbstractFilter

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class SinkWeights(AbstractFilter):
    """
        A sink filter that sorts the weights and saves them into a npy file
    """

    def __init__(self, conf_filter: Dict = {}):
        super().__init__()
        self.output_path: str = conf_filter.get('output_path')
        self.output_json = conf_filter.get('output_path_json')
        self.collect_data = []
        self.collect_indexes = []
        self.collect_subclusters = []
        self.name = 'SinkWeights'

    def process(self, message: Dict) -> Dict:
        self.collect_data.append(message.get('weights'))
        self.collect_indexes.append(message.get('list_of_indexes'))

        self.collect_subclusters.append(message.get('d_cluster'))
        return message

    def last_process(self, message: Dict) -> Dict:
        indexes = np.concatenate(self.collect_indexes)
        argsort=np.argsort(indexes)
        concat_data = np.concatenate(self.collect_data)
        weights = concat_data[argsort]
        logger.debug(f'Writing {len(weights)} weights to {self.output_path}')
        np.save(self.output_path, weights, allow_pickle=False)

        if self.output_json:
            with open(self.output_json, 'w') as output_file:
                json.dump(self.collect_subclusters, output_file, indent=2)
        return message
