from typing import Dict
import logging
import numpy as np

from filtering_pipeline.filters.abstract_filter import AbstractFilter
from sam.primitive import Primitive
from collections import OrderedDict, defaultdict

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class FilterParamsEncoding(AbstractFilter):
    """
        A filter that encodes the parameters of a list of sequences into a string
        then perform a clustering on identic keys
    """

    def __init__(self, conf_filter: Dict = {}):
        super().__init__()
        self.name = 'FilterClusterParamValues_new'
        self.nodes_parametrized = OrderedDict(conf_filter['nodes_parametrized'])
        self.max_cluster_size = conf_filter.get('max_cluster_size',10000)

    def process(self, message: object) -> object:
        list_of_sequences = message.get('list_of_sequences')
        d_cluster = defaultdict(list) 
        for i,seq in enumerate(list_of_sequences):
            key = self._encode_sequence(seq)
            d_cluster[key].append(i)

        message['d_cluster'] = d_cluster
        return message

    def _encode_sequence(self, seq):
        encoding = []
        for op in seq:
            if isinstance(op, Primitive):
                list_of_params = self.nodes_parametrized.get(type(op), [])
                for j, param in enumerate(list_of_params):
                    if param[-2:] in ['_x', '_y']:
                        racine, coord = param.split('_')
                        point = op.__dict__.get(racine)
                        value = point.__dict__.get(coord)
                    else :
                        value = op.__dict__.get(param)
                    encoding.append(int(round(value*4,0)))

        return str(encoding)