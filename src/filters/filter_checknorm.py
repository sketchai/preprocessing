import enum
from typing import Dict
import logging
import numpy as np

from sketchgraphs.data.sequence import EdgeOp, NodeOp, EntityType, ConstraintType
from src.filters.utils.filter_functiononparam import FilterFunctionOnParam
from filtering_pipeline import KO_FILTER_TAG
from src.utils.discretization import create_params_edge, create_params_node
from filtering_pipeline.filters.abstract_filter import AbstractFilter

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class FilterCheckNorm(AbstractFilter):
    """
        This filter checks the value of all node and edge parameters 
        to make sure its in the right format for discretization
    """

    def __init__(self, conf_filter: Dict = {}):
        super().__init__(conf_filter)
        self.name = 'FilterCheckNorm'
        n_bins = 2 # we only want min and max
        self.node_params = create_params_node(n_bins)
        self.edge_params = create_params_edge(n_bins)

    def process(self, message):
        op = message['op']
        label = op.label.name
        if isinstance(op,NodeOp):
            d_param_map_ = self.node_params.get(label)
        elif isinstance(op,EdgeOp):
            d_param_map_ = self.edge_params.get(label)
        if d_param_map_ is None:
            return message
        check = self.params_are_in_map_(
            op.parameters,
            d_param_map_)
        if not check:
            message[KO_FILTER_TAG] = self.name
        return message

    def params_are_in_map_(self,params,d_param_map_):
        for parameter, value in params.items():
            map_ = d_param_map_[parameter]
            if isinstance(map_,np.ndarray):
                min_value, max_value = map_
                if value < min_value or value > max_value:
                    logger.debug(f'not in array {value},{min_value},{max_value}')
                    return False
            elif issubclass(map_,enum.IntEnum):
                try:
                    int(map_[value])
                except Exception:
                    return False
        return True
