import numpy as np
import torch

from sketchgraphs.data import sequence, sketch as datalib
from src.utils.maps import NODES_PARAMETRIZED, EDGES_PARAMETRIZED

def create_params_node(n_bins=50):
    """
    Create dictionaries to discretize all the parameters of the primitives and the constraints.
    The values of the dictionaries are maps.
    The margin is used to take the floating point approx into account 
    so that -0.9999 gives 0 and 1.0001 give n_bins-1

    n_bins : int, number of bins to discretize angles, positions and lengths.
    """
    margin = 1e-3
    angle_map = np.linspace(0 - margin, 2*np.pi + margin, n_bins)  # values have been normalized first
    length_map = np.linspace(-2**.5 - margin, 2**.5 + margin, n_bins)# values have been normalized first
    coords_map = np.linspace(-1 - margin, 1 + margin, n_bins) # values have been normalized first
    
    params_node = dict([(datalib.EntityType.Point.name, dict([
                ('isConstruction', datalib.BooleanValue),
                ('x', coords_map),
                ('y', coords_map)])),
            (datalib.EntityType.Line.name, dict([
                ('isConstruction', datalib.BooleanValue),
                ('dirX', coords_map),
                ('dirY', coords_map),
                ('pntX', coords_map),
                ('pntY', coords_map),
                ('startParam', length_map),
                ('endParam', length_map)])),
            (datalib.EntityType.Circle.name, dict([
                ('isConstruction', datalib.BooleanValue),
                ('xCenter', coords_map),
                ('yCenter', coords_map),
                ('xDir', coords_map),
                ('yDir', coords_map),
                ('radius', length_map),
                ('clockwise', datalib.BooleanValue)])),
           (datalib.EntityType.Arc.name, dict([
                ('isConstruction', datalib.BooleanValue),
                ('xCenter', coords_map),
                ('yCenter', coords_map),
                ('xDir', coords_map),
                ('yDir', coords_map),
                ('radius', length_map),
                ('startParam', angle_map),
                ('endParam', angle_map),
                ('clockwise', datalib.BooleanValue)])) ])
    
    return params_node

def create_params_edge(n_bins=50):
    """
    Create dictionaries to discretize all the parameters of the primitives and the constraints. The values of the dictionaries are maps.
    n_bins : int, number of bins to discretize angles, positions and lengths.
    """
    margin = 1e-3
    angle_map = np.linspace(0 - margin, 2*np.pi + margin, n_bins)   # values have been normalized first
    length_map = np.linspace(-2**.5 - margin, 2**.5 + margin, n_bins)  # values have been normalized first

    params_edge = dict([(datalib.ConstraintType.Angle.name, dict([
                ('aligned', datalib.BooleanValue),
                ('clockwise', datalib.BooleanValue),
                ('angle', angle_map)])),
            (datalib.ConstraintType.Length.name, dict([
                ('direction', datalib.DirectionValue),
                ('length', length_map)])),
            (datalib.ConstraintType.Distance.name, dict([
                ('direction', datalib.DirectionValue),
                ('halfSpace0', datalib.HalfSpaceValue),
                ('halfSpace1', datalib.HalfSpaceValue),
                ('length', length_map)])),
            (datalib.ConstraintType.Diameter.name, dict([('length', length_map)])),
            (datalib.ConstraintType.Radius.name, dict([('length', length_map)]))])

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
        if op.label not in EDGES_PARAMETRIZED:
            continue
            
        num_feat = []
        for param, map_ in params_edge[op.label.name].items():
            if isinstance(map_, np.ndarray):
                value = np.searchsorted(map_, op.parameters[param])
                try:
                    assert value < len(map_)
                except Exception:
                    raise Exception(f'{(op.label.name,param)}')
            else:
                value = int(map_[op.parameters[param]])
            num_feat.append(value)
            
        edge_features[op.label.name]['index'].append(i)
        edge_features[op.label.name]['value'].append(num_feat)
        
    for k in edge_features.keys():
        edge_features[k]['index'] = torch.tensor(edge_features[k]['index'], dtype=torch.int64)
        if edge_features[k]['value']:
            edge_features[k]['value'] = torch.tensor(edge_features[k]['value'], dtype=torch.int64)
        else:
            edge_features[k]['value'] = torch.empty((0, len(params_edge[k])), dtype=torch.int64)
    return edge_features

def discretization_nodes(ops, params_node):
    """
    Apply the discretization to the nodes.
    ops : list of nodes;
    params_node : as returned by the function create_params.
    """
    node_features = {k: {'index': [], 'value':[]} for k in params_node.keys()}
    
    for i, op in enumerate(ops):
        if op.label not in NODES_PARAMETRIZED:
            continue
            
        num_feat = []
        for param, map_ in params_node[op.label.name].items():
            if isinstance(map_, np.ndarray):
                value = np.searchsorted(map_, op.parameters[param])
                try:
                    assert value < len(map_)
                except Exception:
                    raise Exception(f'{(op.label.name,param)}')
            else:
                value = int(map_[op.parameters[param]])
            num_feat.append(value)
            
        node_features[op.label.name]['index'].append(i)
        node_features[op.label.name]['value'].append(num_feat)
        
    for k in node_features.keys():
        node_features[k]['index'] = torch.tensor(node_features[k]['index'], dtype=torch.int64)
        if node_features[k]['value']:
            node_features[k]['value'] = torch.tensor(node_features[k]['value'], dtype=torch.int64)
        else:
            node_features[k]['value'] = torch.empty((0, len(params_node[k])), dtype=torch.int64)
    return node_features
    
