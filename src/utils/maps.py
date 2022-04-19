from typing import List, Dict

from sketch_data.catalog_primitive import *
from sketch_data.catalog_constraint import *

from src.utils.logger import logger

def construct_edge_map(l_keep_edge: List) -> Dict:
    edge_map = {}
    i = 0
    for t in l_keep_edge:
        edge_map[t.name] = i
        i += 1
    return edge_map


def construct_node_map(l_keep_node: List) -> Dict:
    node_map = {}
    i = 0
    for t in l_keep_node:

        node_map[t.name] = i
        i += 1
    node_map['void'] = len(node_map)
    return node_map

NODES_PARAMETRIZED = {
    Point: ['status_construction', 'x', 'y'],
    Line: ['status_construction', 'pnt1', 'pnt2'],
    Circle: ['status_construction', 'center', 'radius'],
    Arc: ['status_construction', 'center', 'radius','angle_start', 'angle_end']
}

EDGES_PARAMETRIZED = {
    Angle: ['angle'],
    Length: ['length'],
    # datalib.ConstraintType.Distance: ['direction', 'halfSpace0', 'halfSpace1', 'length'],
    Radius: ['radius']
}
