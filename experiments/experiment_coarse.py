import sys
import os

# Add paths for packages
sys.path.append('src/sketchgraphs/')
sys.path.append('src/filtering-pipeline/')
cur_path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, cur_path + "/..")


import logging

logging.basicConfig(level=logging.WARNING)

print(sys.path)

# Initialization
from src.filters.sink_sequence import SinkSequence
from src.filters.filter_constraintrefs import FilterConstraintRefs
from src.filters.filter_count import FilterCount
from src.filters.filter_checkparamsmetrics import FilterCheckParamsMetrics
from src.filters.filter_on_op import OpSubPipelineFilter
from src.filters.filter_checklabel import FilterCheckLabel
from src.sources.source_fromlist import SourceList
from src.sources.source_fromflatarray import SourceFromFlatArray
from src.utils.to_dict import yaml_to_dict
from filtering_pipeline.factory import pipeline_factory
from sketchgraphs.data import flat_array
from sketchgraphs.data.sequence import ConstraintType, EntityType, SubnodeType



catalog_filters = {'SourceFromFlatArray': SourceFromFlatArray,
                   'OpSubPipelineFilter': OpSubPipelineFilter,
                   'FilterCheckLabel': FilterCheckLabel,
                   'FilterCount': FilterCount,
                   'SourceList': SourceList,
                   'FilterConstraintRefs': FilterConstraintRefs,
                   'FilterCheckParamsMetrics': FilterCheckParamsMetrics,
                   'SinkSequence': SinkSequence,
                   }
# Update conf
# the nodes and edges that are considered
l_keep_edge = [ConstraintType.Coincident, ConstraintType.Distance, ConstraintType.Horizontal,
               ConstraintType.Parallel, ConstraintType.Vertical, ConstraintType.Tangent,
               ConstraintType.Length, ConstraintType.Perpendicular, ConstraintType.Midpoint,
               ConstraintType.Equal, ConstraintType.Diameter, ConstraintType.Radius,
               ConstraintType.Concentric, ConstraintType.Angle, ConstraintType.Subnode]
l_keep_node = [EntityType.Point, EntityType.Line,
               EntityType.Circle, EntityType.Arc,
               SubnodeType.SN_Start, SubnodeType.SN_End, SubnodeType.SN_Center,
               EntityType.External, EntityType.Stop]

d_conf = yaml_to_dict('config/conf_coarsegrainedpip.yml')
d_conf['FilterCheckLabel']['parms']['edge_label_list'] = l_keep_edge
d_conf['FilterCheckLabel']['parms']['node_label_list'] = l_keep_node
length_format = {'length': r'[-+]?(?:\d*\.\d+|\d+) METER'}
d_conf['FilterCheckParamsMetrics_Length']['parms']['request'] = {
    ('edge', ConstraintType.Distance): length_format,
    ('edge', ConstraintType.Length): length_format,
    ('edge', ConstraintType.Diameter): length_format,
    ('edge', ConstraintType.Radius): length_format,
}

d_conf['FilterCheckParamsMetrics_Angle']['parms']['request'] = {
    ('edge', ConstraintType.Angle): {'angle': r'[-+]?(?:\d*\.\d+|\d+) DEGREE'},
}
# Update some filters

# Launch pipeline
pipeline = pipeline_factory(conf=d_conf, catalog_filter=catalog_filters)
last_message = pipeline.execute()

input_path = d_conf['Source_A']['parms']['file_path']
input_data = flat_array.load_dictionary_flat(input_path)['sequences']

print(f"Pipeline input is of length {len(input_data)}")

output_path = d_conf['SinkSequence']['parms']['output_path']
output_data = flat_array.load_flat_array(output_path)

print(f"Pipeline output is of length {len(output_data)}")
output_path = d_conf['SinkSequence']['parms']['output_path']
output_data = flat_array.load_flat_array(output_path)

