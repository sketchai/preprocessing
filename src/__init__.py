from sketchgraphs.data.sequence import EdgeOp, NodeOp
from sketch_data.primitive import Primitive
from sketch_data.constraint import Constraint
TYPE_OF_OP_FROM_NAME = {'edge': EdgeOp, 'node': NodeOp, 'primitive' : Primitive, 'constraint': Constraint}
OPS_ENCODING_TAG = 'ops_encoding'
SEQUENCE_ENCODING_TAG = 'sequence_encoding'
CLUSTER_DICT_TAG = 'cluster_dict'