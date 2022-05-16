import numpy as np
import enum
import torch


from sam.primitive import PrimitiveType
from sam.constraint import ConstraintType

from src.utils.maps import NODES_PARAMETRIZED, EDGES_PARAMETRIZED
from src.utils.logger import logger

BooleanValue = enum.IntEnum(
    'BooleanValue',
    [('FALSE', 0), ('TRUE', 1), ('False', 0), ('True', 1)]
)
BooleanValue._member_map_[False] = BooleanValue.FALSE
BooleanValue._member_map_[True] = BooleanValue.TRUE

MARGIN=1e-3

def create_params_node(n_bins=50):
    """
    Create dictionaries to discretize all the parameters of the primitives and the constraints.
    The values of the dictionaries are maps.
    The margin is used to take the float16 approx into account 
    so that -0.999 gives 0 and 1.001 give n_bins-1

    n_bins : int, number of bins to discretize angles, positions and lengths.
    """
    angle_map = np.linspace(0, 2*np.pi, n_bins) # values have been normalized first
    length_map = np.linspace(-2**.5, 2**.5, n_bins) # values have been normalized first
    coords_map = np.linspace(-1, 1, n_bins) # values have been normalized first
    
    params_node = dict([(PrimitiveType.POINT.name, dict([
                ('status_construction', BooleanValue),
                ('x', coords_map),
                ('y', coords_map)
                ])),
            (PrimitiveType.LINE.name, dict([
                ('status_construction', BooleanValue),
                # ('pnt1_x', coords_map),
                # ('pnt1_y', coords_map),
                # ('pnt2_x', coords_map),
                # ('pnt2_y', coords_map)
                ])),
            (PrimitiveType.CIRCLE.name, dict([
                ('status_construction', BooleanValue),
                # ('center_x', coords_map),
                # ('center_y', coords_map),
                ('radius', length_map)])),
           (PrimitiveType.ARC.name, dict([
                ('status_construction', BooleanValue),
                # ('center_x', coords_map),
                # ('center_y', coords_map),
                ('radius', length_map),
                ('angle_start', angle_map),
                ('angle_end', angle_map)])) ])
    
    return params_node

def create_params_edge(n_bins=50):
    """
    Create dictionaries to discretize all the parameters of the primitives and the constraints. The values of the dictionaries are maps.
    n_bins : int, number of bins to discretize angles, positions and lengths.
    """
    angle_map = np.linspace(0, 2*np.pi, n_bins) # values have been normalized first
    length_map = np.linspace(-2**.5, 2**.5, n_bins) # values have been normalized first

    params_edge = dict([(ConstraintType.ANGLE.name, dict([
                ('angle', angle_map)])),
            (ConstraintType.LENGTH.name, dict([
                ('length', length_map)])),
            # (ConstraintType.DISTANCE.name, dict([
            #    ('distance_min', length_map)])),
            (ConstraintType.RADIUS.name, dict([('radius', length_map)]))])

    return params_edge


def feature_dims(params_edge, params_node):
    """
    Returns the dimensions (i.e. the number of possible discrete values) of the parameters of the primitives and the constraints.
    params_edge, params_node : as returned by the function create_params.
    """
    edge_feature_dimensions = {}
    node_feature_dimensions = {}
    for k, params in params_edge.items():
        edge_feature_dimensions[k] = {}
        for param, map_ in params.items():
            edge_feature_dimensions[k][param] = len(map_)
    for k, params in params_node.items():
        node_feature_dimensions[k] = {}
        for param, map_ in params.items():
            node_feature_dimensions[k][param] = len(map_)
    return edge_feature_dimensions, node_feature_dimensions

def discretization_edges(ops, params_edge):
    """
    Apply the discretization to the constraints.
    ops : list of constraints;
    params_edge : as returned by the function create_params.
    """
    edge_features = {k: {'index': [], 'value':[]} for k in params_edge.keys()}
    for i, op in enumerate(ops):
        if type(op) not in EDGES_PARAMETRIZED:
            continue
            
        num_feat = []
        for param, map_ in params_edge[op.type.name].items():
            if isinstance(map_, np.ndarray):
                value = np.searchsorted(map_, op.__dict__[param]-MARGIN)
                assert value < len(map_), f'{map_}'
            else:
                value = int(map_[op.__dict__[param]])
            num_feat.append(value)
            
        edge_features[op.type.name]['index'].append(i)
        edge_features[op.type.name]['value'].append(num_feat)
        
    for k in edge_features.keys():
        edge_features[k]['index'] = np.array(edge_features[k]['index'], dtype=np.int64)
        if edge_features[k]['value']:
            edge_features[k]['value'] = np.array(edge_features[k]['value'], dtype=np.int64)
        else:
            edge_features[k]['value'] = np.empty((0, len(params_edge[k])), dtype=np.int64)
    return edge_features

def discretization_nodes(ops, params_node):
    """
    Apply the discretization to the nodes.
    ops : list of nodes;
    params_node : as returned by the function create_params.
    """
    node_features = {k: {'index': [], 'value':[]} for k in params_node.keys()}
    l_subnodes = []
    for i, op in enumerate(ops):
        if type(op) not in NODES_PARAMETRIZED:
            continue
        logger.debug(f'{op.type}')
        num_feat = []
        logger.info(f'op: {op}, type {op.type.name}')
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
            num_feat.append(value)
            
        node_features[op.type.name]['index'].append(i)
        node_features[op.type.name]['value'].append(num_feat)
        
    for k in node_features.keys():
        node_features[k]['index'] = np.array(node_features[k]['index'], dtype=np.int64)
        if node_features[k]['value']:
            node_features[k]['value'] = np.array(node_features[k]['value'], dtype=np.int64)
        else:
            node_features[k]['value'] = np.empty((0, len(params_node[k])), dtype=np.int64)
    return node_features