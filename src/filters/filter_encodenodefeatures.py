from typing import Dict
import numpy as np
from filtering_pipeline.filters.abstract_filter import AbstractFilter
from filtering_pipeline import KO_FILTER_TAG
from sam.primitive import Primitive
from src.utils.maps import construct_node_map
from src.utils import discretization
from filtering_pipeline import KO_FILTER_TAG

from src.utils.logger import logger


class PrimitiveVoid(Primitive):
    """Void Primitive."""

    def __init__(self, status_construction: bool = False):
        type_ = lambda _:None
        type_.name = 'void'
        super(PrimitiveVoid, self).__init__(elt_type=type_, status_construction=status_construction)

    def __repr__(self):
        return f"Void"

    def point_belongs_to_primitive(self, point: object) -> bool:
        """Check if a point belongs to the line"""

    def _construct_mapp(self) -> None:
        pass

    def plot(self, ax, color='black', linewidth=1):
        pass


class FilterEncodeNodeFeatures(AbstractFilter):
    """
        A filter that encodes the features of all nodes
    """

    def __init__(self, conf_filter: Dict = {}):
        super().__init__(conf_filter)
        self.name = 'FilterEncodeOrder'
        n_bins = conf_filter.get('n_bins', 50)
        l_keep_node = conf_filter['l_keep_node']
        self.lMax = conf_filter.get('lMax',60)
        self.node_idx_map = construct_node_map(l_keep_node, encoding=True)
        self.params_node = discretization.create_params_node(n_bins)

    def process(self, message: object) -> object:
        sequence = message.get('sequence')
        node_ops = [op for op in sequence if isinstance(op, Primitive)]
        l = len(node_ops)
        node_ops += [PrimitiveVoid()]*(self.lMax-l)
        node_features = []
        for op in node_ops:
            if hasattr(op, 'subnode_type'):
                type_ = op.subnode_type
            else:
                type_ = op.type.name 
            node_features.append(self.node_idx_map[type_])
        node_features = np.array(node_features, dtype=np.int64)
        try:
            sparse_node_features = discretization.discretization_nodes(node_ops, self.params_node)
        except Exception:
            message[KO_FILTER_TAG] = self.name
            return message

        mask_attention = np.ones(self.lMax, dtype=bool)
        mask_attention[:l] = False
        message['node_ops'] = node_ops
        message['node_features'] = node_features
        message['sparse_node_features'] = sparse_node_features
        message['mask_attention'] = mask_attention
        message['length'] = l
        return message