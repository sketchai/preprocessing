import unittest
import logging


from src.sources.source_fromflatarray import SourceFromFlatArray
from src.filters.filter_checklabel import FilterCheckLabel
from src.filters.filter_on_op import OpSubPipelineFilter
from src.filteringpipeline.src.filters.catalog_filter.subpipeline_filter import SubPipelineFilter
from src.sources.source_fromlist import SourceList
from src.filteringpipeline.src.filters.factory import pipeline_factory
from src.utils.to_dict import yaml_to_dict


from src.sketchgraphs.sketchgraphs.data import sketch as datalib

# For SketchGraphs
import sys
sys.path.append('src/sketchgraphs')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestIntegrationCoarseGrainedPipeline(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.catalog_filters = {'SourceFromFlatArray': SourceFromFlatArray,
                                'OpSubPipelineFilter': OpSubPipelineFilter,
                                'FilterCheckLabel': FilterCheckLabel,
                                'SourceList': SourceList}
        self.d_conf = yaml_to_dict('config/conf_coarsegrainedpip.yml')
        self.d_conf['FilterCheckLabel']['parms']['label_list'] = [datalib.ConstraintType.Coincident, datalib.ConstraintType.Distance, 
                                                                    datalib.ConstraintType.Horizontal,datalib.EntityType.Point, 
                                                                    datalib.EntityType.Line]

    def test_pipeline(self):
        pipeline = pipeline_factory(conf=self.d_conf, catalog_filter=self.catalog_filters)
        last_message = pipeline.execute()