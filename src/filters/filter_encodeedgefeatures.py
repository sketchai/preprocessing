from typing import Dict
import numpy as np
from filtering_pipeline.filters.abstract_filter import AbstractFilter
from filtering_pipeline import KO_FILTER_TAG
from sam.constraint import Constraint
from src.utils.maps import construct_edge_map, construct_edge_map
from src.utils import discretization
from src.utils.logger import logger


class FilterEncodeEdgeFeatures(AbstractFilter):
    """
        A filter that encodes the features of all edges
    """

    def __init__(self, conf_filter: Dict = {}):
        super().__init__(conf_filter)
        self.name = 'FilterEncodeEdgeFeatures'
        n_bins = conf_filter.get('n_bins', 50)
        l_keep_edge = conf_filter['l_keep_edge']
        self.edge_idx_map = construct_edge_map(l_keep_edge, encoding=True)
        self.params_edge = discretization.create_params_edge(n_bins)

    def process(self, message: object) -> object:
        sequence = message.get('sequence')
        edge_ops = [op for op in sequence if isinstance(op, Constraint)]
        edge_features = np.array([self.edge_idx_map[op.type.name] for op in edge_ops], dtype=np.int64)
        try:
            sparse_edge_features = discretization.discretization_edges(edge_ops, self.params_edge)
        except Exception:
            message[KO_FILTER_TAG] = self.name
            return message
            
        message['edge_ops'] = edge_ops
        message['edge_features'] = edge_features
        message['sparse_edge_features'] = sparse_edge_features
        return message