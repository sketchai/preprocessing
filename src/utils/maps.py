from typing import List 
from sketchgraphs.data import sketch as datalib

def construct_edge_map(l_keep_edge:List) -> Dict:
    edge_map = {}
    i = 0
    for t in datalib.ConstraintType:
        if t in l_keep_edge:
            edge_map[t] = i
            i += 1
    return edge_map

def construct_node_map(l_keep_node:List) -> Dict:
    node_map = {}
    i = 0
    for t in list(datalib.EntityType) + list(datalib.SubnodeType):
        if t in l_keep_node:
            node_map[t] = i
            i += 1
    node_map['void'] = len(node_map)
    return node_map 


