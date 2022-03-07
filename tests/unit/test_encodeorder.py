import logging
import unittest
import sys
sys.path.append('src/sketchgraphs/')
sys.path.append('src/filtering-pipeline/')

from sketchgraphs.data.sequence import EdgeOp, NodeOp, ConstraintType, EntityType, SubnodeType
from src.filters.filter_encodeorder import FilterEncodeOrder

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestFilterEncodeOrder(unittest.TestCase):

    def test_process(self):
        l_keep_edge = [ConstraintType.Coincident, ConstraintType.Distance, ConstraintType.Horizontal,
               ConstraintType.Parallel, ConstraintType.Vertical, ConstraintType.Tangent,
               ConstraintType.Length, ConstraintType.Perpendicular, ConstraintType.Midpoint,
               ConstraintType.Equal, ConstraintType.Diameter, ConstraintType.Radius,
               ConstraintType.Concentric, ConstraintType.Angle, ConstraintType.Subnode]
        l_keep_node = [EntityType.Point, EntityType.Line,
               EntityType.Circle, EntityType.Arc,
               SubnodeType.SN_Start, SubnodeType.SN_End, SubnodeType.SN_Center,
               EntityType.External, EntityType.Stop]

        mock_sequence_1 = [
            NodeOp(label=0),
            EdgeOp(label=3, references=(0,)),
            NodeOp(label=2),
            EdgeOp(label=0, references=(0,2)),
            NodeOp(label=6),
        ]
        conf_dict = {'l_keep_node': l_keep_node, 'l_keep_edge': l_keep_edge}
        filter1 = FilterEncodeOrder(conf_filter=conf_dict)
        message = {'sequence': mock_sequence_1}
        filter1.process(message)
        
        edge_offset = len(l_keep_node) + 1
        ref_offset = len(l_keep_node) + 1 + len(l_keep_edge)
        expected_encoding = [
            filter1.node_idx_map[0],
            filter1.edge_idx_map[3]+edge_offset,
            0+ref_offset,
            filter1.node_idx_map[2],
            filter1.edge_idx_map[0]+edge_offset,
            0+ref_offset,
            2+ref_offset,
            filter1.node_idx_map[6],
            ]
        self.assertEqual(message['encoded_sequence'], expected_encoding)