import sys

from sam.primitive import Primitive
from sam.constraint import Constraint
TYPE_OF_OP_FROM_NAME = {'primitive' : Primitive, 'constraint': Constraint}
try:
    from sketchgraphs.data.sequence import EdgeOp, NodeOp
    TYPE_OF_OP_FROM_NAME.update({'edge': EdgeOp, 'node': NodeOp})
except ModuleNotFoundError:
    pass

OPS_ENCODING_TAG = 'ops_encoding'
SEQUENCE_ENCODING_TAG = 'sequence_encoding'
CLUSTER_DICT_TAG = 'cluster_dict'