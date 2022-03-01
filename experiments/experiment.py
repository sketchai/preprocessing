# Initialization
import sys
import os

## Add paths for packages
sys.path.append('src/sketchgraphs/')
sys.path.append('src/filteringpipeline/')
cur_path=os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, cur_path+"/..")

print(sys.path)

from sketchgraphs.data.sequence import ConstraintType, EntityType, SubnodeType
from sketchgraphs.data import flat_array
from filtering_pipeline.factory import pipeline_factory

from src.utils.to_dict import yaml_to_dict
from src.sources.source_fromflatarray import SourceFromFlatArray
from src.sources.source_fromlist import SourceList
from src.filters.filter_checklabel import FilterCheckLabel
from src.filters.filter_on_op import OpSubPipelineFilter
from src.filters.filter_checkparamsmetrics import FilterCheckParamsMetrics
from src.filters.filter_count import FilterCount
from src.filters.filter_constraintrefs import FilterConstraintRefs
from src.filters.sink_sequence import SinkSequence

catalog_filters = {'SourceFromFlatArray': SourceFromFlatArray,
                                'OpSubPipelineFilter': OpSubPipelineFilter,
                                'FilterCheckLabel': FilterCheckLabel,
                                'FilterCount': FilterCount,
                                'SourceList': SourceList,
                                'FilterConstraintRefs': FilterConstraintRefs,
                                'FilterCheckParamsMetrics': FilterCheckParamsMetrics,
                                'SinkSequence': SinkSequence,
                                }
########### Update conf 
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
d_conf['FilterCheckParamsMetrics_Length']['parms']['request'] = {
            ('edge', ConstraintType.Distance): {'length': ['.* METER']},
            ('edge', ConstraintType.Length): {'length': ['.* METER']},
            ('edge', ConstraintType.Diameter): {'length': ['.* METER']},
            ('edge', ConstraintType.Radius): {'length': ['.* METER']},
        }

d_conf['FilterCheckParamsMetrics_Angle']['parms']['request'] = {
            ('edge', ConstraintType.Angle): {'angle': ['.* DEGREE']},
        }
# Update some filters




# Launch pipeline
pipeline = pipeline_factory(conf=d_conf, catalog_filter=catalog_filters)
last_message = pipeline.execute()
