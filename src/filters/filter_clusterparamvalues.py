from typing import Dict
import numpy as np
from filtering_pipeline.filters.abstract_filter import AbstractFilter
from src import SEQUENCE_ENCODING_TAG, CLUSTER_DICT_TAG
from collections import Counter
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class FilterClusterParamValues(AbstractFilter):
    """
        A filter that clusters the sequences according to the params_array
    """

    def __init__(self, conf_filter: Dict={}):
        super().__init__(conf_filter)
        self.name = 'FilterClusterParamValues'

    def process(self,message: object) -> object: 
        sequence_list = message.get('list_of_sequences')
        if len(sequence_list) == 1:
            message['weights'] = [1.]
        else:
            d_cluster = message.get('d_cluster')
            weights = np.zeros((len(sequence_list),))
            n_clusters = len(list(d_cluster.keys()))
            for key, indexes in d_cluster.items():
                count_elts = len(d_cluster[key])
                weights[indexes] = 1./count_elts/n_clusters
            message['weights'] = weights

        return message