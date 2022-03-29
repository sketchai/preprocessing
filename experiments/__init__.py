from sketchgraphs.data.sequence import EntityType, ConstraintType, SubnodeType

## Paths
root = ''
SKETCHGRAPHS_PATH = root + 'data/sg_t16_{}.npy'
COARSE_PATH = root + 'out/coarse_grained_output_{}.npy'
NORMALIZATION_PATH = root + 'out/normalization_output_{}.npy'
INDEXES_PATH = root + 'out/indexes_cluster_order_{}.json'
WEIGHTS_PATH = root + 'out/weights_output_{}.npy'
ENCODING_PATH = root + 'out/encoding_output_{}.npy'

## Global params 
# (these params can be changed but should stay consistent through the pipeline steps)
L_KEEP_EDGE = [ConstraintType.Coincident, ConstraintType.Distance, ConstraintType.Horizontal,
               ConstraintType.Parallel, ConstraintType.Vertical, ConstraintType.Tangent,
               ConstraintType.Length, ConstraintType.Perpendicular, ConstraintType.Midpoint,
               ConstraintType.Equal, ConstraintType.Diameter, ConstraintType.Radius,
               ConstraintType.Concentric, ConstraintType.Angle, ConstraintType.Subnode]
L_KEEP_NODE = [EntityType.Point, EntityType.Line,
               EntityType.Circle, EntityType.Arc,
               SubnodeType.SN_Start, SubnodeType.SN_End, SubnodeType.SN_Center,
               EntityType.External, EntityType.Stop]
