from typing import Dict

import torch
import numpy as np
from sam.constraint import ConstraintType
from filtering_pipeline.filters.abstract_filter import AbstractFilter
from src.utils.maps import construct_edge_map
from src.utils.logger import logger


class FilterEncodeGraphConnections(AbstractFilter):
    """
        A filter that encodes the incidences of all edges
    """

    def __init__(self, conf_filter: Dict = {}):
        super().__init__(conf_filter)
        self.name = 'FilterEncodeIncidences'

    def process(self, message: object) -> object:
        edge_ops = message.get('edge_ops')
        logger.debug(edge_ops)
        incidences = np.array([
            [op.references[0].node_index,
             op.references[-1].node_index] for op in edge_ops], dtype=np.int64)
        l = len(message['node_ops'])
        i_edges_given = []
        i_edges_possible = []
        for i, op in enumerate(edge_ops):
            if op.type.name == 'Subnode':
                i_edges_given.append(i)
            else:
                i_edges_possible.append(i)
        i_edges_given = np.array(i_edges_given, dtype=np.int64)
        i_edges_possible = np.array(i_edges_possible, dtype=np.int64)

        message['incidences']= incidences
        message['i_edges_given']= i_edges_given
        message['i_edges_possible']= i_edges_possible
        return message