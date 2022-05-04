from typing import Dict
import logging
import numpy as np

from filtering_pipeline.filters.abstract_filter import AbstractFilter
from sketch_data.primitive import Primitive
from collections import OrderedDict

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class FilterParamsEncoding(AbstractFilter):
    """
        A filter that encodes the parameters of a list of sequences into a 2d-array
        conf : a Dict : { 'node_label': ['param1', 'param2'] }
    """

    def __init__(self, conf_filter: Dict = {}):
        super().__init__()
        self.name = 'FilterParamsEncoding'
        self.nodes_parametrized = OrderedDict(conf_filter['nodes_parametrized'])
        self.max_cluster_size = conf_filter.get('max_cluster_size',10000)

    def process(self, message: object) -> object:
        list_of_sequences = message.get('list_of_sequences')
        n_sequences = len(list_of_sequences)
        logger.debug(n_sequences)
        np.random.seed(0)
        if n_sequences<=self.max_cluster_size:
            indexes = range(n_sequences)
        else:
            indexes = np.random.choice(n_sequences,self.max_cluster_size)
            n_sequences = self.max_cluster_size

        l_params = 0

        # count the nb of param
        template_seq = list_of_sequences[0]
        for op in template_seq:
            if isinstance(op, Primitive):
                l_params += len(self.nodes_parametrized.get(type(op), []))

        # fill the params array with the values
        params = np.zeros((n_sequences, l_params))
        for i, index in enumerate(indexes):
            seq = list_of_sequences[index]
            params[i] = self._encode_sequence(seq, l_params)

        params = self._normalize(params)

        message['params_array'] = params
        message['params_indexes'] = indexes
        return message

    def _encode_sequence(self, seq, l_params):
        encoding = np.zeros((l_params,))
        offset = 0
        for op in seq:
            if isinstance(op, Primitive):
                list_of_params = self.nodes_parametrized.get(type(op), [])
                logger.debug(list_of_params)
                for j, param in enumerate(list_of_params):
                    if param[-2:] in ['_x', '_y']:
                        racine, coord = param.split('_')
                        point = op.__dict__.get(racine)
                        value = point.__dict__.get(coord)
                    else :
                        value = op.__dict__.get(param)
                    logger.info(f'param: {param}, op_param: {value}')
                    encoding[offset + j] = float(value)

                offset += len(list_of_params)

        return encoding

    @staticmethod
    def _normalize(array):
        """normalize columns in [0,1]"""
        array -= np.min(array, axis=0, keepdims=True)
        peek_to_peek = np.ptp(array, axis=0, keepdims=True)
        np.divide(array, peek_to_peek, where=peek_to_peek != 0., out=array)
        return array
