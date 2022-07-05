from typing import Dict
import numpy as np
from filtering_pipeline.filters.abstract_filter import AbstractFilter
from filtering_pipeline import KO_FILTER_TAG
from sam.primitive import Primitive
from src.utils.maps import construct_node_map
from src.utils import discretization_pyg

from src.utils.logger import logger

class FilterEncodeNodeFeatures(AbstractFilter):
    """
        A filter that encodes the features of all nodes
    """

    def __init__(self, conf_filter: Dict = {}):
        super().__init__(conf_filter)
        self.name = 'FilterEncodeOrder'
        n_bins = conf_filter.get('n_bins', 50)
        l_keep_node = conf_filter['l_keep_node']
        self.node_idx_map = construct_node_map(l_keep_node, encoding=True)
        self.params_node = discretization_pyg.create_params_node(n_bins)

    def process(self, message: object) -> object:
        sequence = message.get('sequence')
        node_ops = [op for op in sequence if isinstance(op, Primitive)]
        try:
            node_features = discretization_pyg.discretization_nodes(node_ops, self.params_node, self.node_idx_map)
        except Exception as e:
            message[KO_FILTER_TAG] = self.name
            return message
            
        message['node_ops'] = node_ops
        message['node_features'] = node_features
        return message