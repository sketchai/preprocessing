import numpy as np
import enum
import torch


from sam.primitive import PrimitiveType
from sam.constraint import ConstraintType
from src.utils.discretization import create_params_edge, create_params_node
from src.utils.logger import logger

BooleanValue = enum.IntEnum(
    'BooleanValue',
    [('FALSE', 0), ('TRUE', 1), ('False', 0), ('True', 1)]
)
BooleanValue._member_map_[False] = BooleanValue.FALSE
BooleanValue._member_map_[True] = BooleanValue.TRUE

MARGIN=1e-3


def feature_dims(params_node):
    """
    Returns the dimensions (i.e. the number of possible discrete values) of the parameters of the primitives
    params_edge, params_node : as returned by the function create_params.
    """
    node_feature_dimensions = {}
    for k, params in params_node.items():
        node_feature_dimensions[k] = {}
        for param, map_ in params.items():
            node_feature_dimensions[k][param] = len(map_)
    return node_feature_dimensions

def discretization_nodes(ops, params_node, node_idx_map):
    """
    Apply the discretization to the nodes.
    ops : list of nodes;
    params_node : as returned by the function create_params.
    node_idx_map:
    """
    # set padding idx to the max possible dim
    f_dims = feature_dims(params_node=params_node)
    padding_idx = 0
    n_max_params = max(len(params.values()) for params in f_dims.values())
    node_features = np.ones((len(ops),n_max_params + 1), dtype=np.int64)
    node_features *= padding_idx
    for i, op in enumerate(ops):
        if hasattr(op, 'subnode_type'):
            type_ = op.subnode_type
        else:
            type_ = op.type.name 
        logger.debug(f'{op.type}')
        logger.info(f'op: {op}, type {op.type.name}')
        offset = 1
        node_features[i, 0] = node_idx_map[type_]
        for param, map_ in params_node[op.type.name].items():
            if param[-2:] in ['_x', '_y']:
                racine, coord = param.split('_')
                point = op.__dict__.get(racine)
                op_parms = point.__dict__.get(coord)
            else :
                op_parms = op.__dict__.get(param)
            logger.info(f'param: {param}, op_param: {op_parms}')
            if isinstance(map_, np.ndarray):
                value = np.searchsorted(map_, op_parms-MARGIN)
                assert value < len(map_), f'{(value,op,param)}'
            else:
                value = int(map_[op_parms])
            node_features[i, offset] = value
            offset +=1
    return node_features