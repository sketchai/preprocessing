# Initialization
from ..sources.source_fromflatarray import SourceFromFlatArray
from ..filteringpipeline.src.filters.catalog_filter.pipeline_filter import PipelineFilter
from ..filteringpipeline.src.filters.factory import pipeline_factory

catalog_filters = {'SourceFromFlatArray': SourceFromFlatArray,
                                'PipelineFilter': PipelineFilter,
                                'CheckElementWiseFilter': CheckElementWiseFilter}
d_conf = yaml_to_dict('config/conf_coarsegrainedpip.yml')

# Update some filters
from sketchgraphs.data import sketch as datalib

# the nodes and edges that are considered
l_keep_edge = [datalib.ConstraintType.Coincident, datalib.ConstraintType.Distance, datalib.ConstraintType.Horizontal,
             datalib.ConstraintType.Parallel, datalib.ConstraintType.Vertical, datalib.ConstraintType.Tangent,
             datalib.ConstraintType.Length, datalib.ConstraintType.Perpendicular, datalib.ConstraintType.Midpoint,
             datalib.ConstraintType.Equal, datalib.ConstraintType.Diameter, datalib.ConstraintType.Radius,
             datalib.ConstraintType.Concentric, datalib.ConstraintType.Angle, datalib.ConstraintType.Subnode]
l_keep_node = [datalib.EntityType.Point, datalib.EntityType.Line,
             datalib.EntityType.Circle, datalib.EntityType.Arc,
             datalib.SubnodeType.SN_Start, datalib.SubnodeType.SN_End, datalib.SubnodeType.SN_Center,
             datalib.EntityType.External, datalib.EntityType.Stop]


# Launch pipeline
pipeline = pipeline_factory(conf=self.d_conf, catalog_filter=self.catalog_filters)
last_message = pipeline.execute()