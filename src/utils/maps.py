from typing import List, Dict

from sam.catalog_primitive import *
from sam.catalog_constraint import *

from src.utils.logger import logger

def construct_edge_map(l_keep_edge: List, encoding=False) -> Dict:
    edge_map = {}
    i = 0
    for t in l_keep_edge:
        edge_map[t.name] = i
        i += 1
    if encoding:
        edge_map['Subnode'] = len(edge_map)
    return edge_map


def construct_node_map(l_keep_node: List, encoding=False) -> Dict:
    node_map = {}
    i = 0
    for t in l_keep_node:
        node_map[t.name] = i
        i += 1
    if encoding:
        new_nodes = {
            'SN_pnt1':i,
            'SN_pnt2':i+1,
            'SN_center':i+2,
            'void':i+3}
        node_map.update(new_nodes)
    return node_map

NODES_PARAMETRIZED = {
    Point: ['status_construction', 'x', 'y'],
    Line: ['status_construction', 'pnt1_x', 'pnt1_y', 'pnt2_x', 'pnt2_y'],
    Circle: ['status_construction', 'center_x', 'center_y', 'radius'],
    Arc: ['status_construction', 'center_x', 'center_y', 'radius','angle_start', 'angle_end']
}

EDGES_PARAMETRIZED = {
    Angle: ['angle'],
    Length: ['length'],
    # datalib.ConstraintType.Distance: ['direction', 'halfSpace0', 'halfSpace1', 'length'],
    Radius: ['radius']
}
