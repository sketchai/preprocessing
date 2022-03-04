import sys
sys.path.append('src/sketchgraphs/')
sys.path.append('src/filtering-pipeline/')

from sketchgraphs.data import flat_array
from sketchgraphs.data.sequence import ConstraintType, EntityType, SubnodeType
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
from filtering_pipeline.filters.catalog_filter.subpipeline_filter import SubPipelineFilter
import logging
import unittest


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestIntegrationCoarseGrainedPipeline(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.catalog_filters = {'SourceFromFlatArray': SourceFromFlatArray,
                                'OpSubPipelineFilter': OpSubPipelineFilter,
                                'FilterCheckLabel': FilterCheckLabel,
                                'FilterCount': FilterCount,
                                'SourceList': SourceList,
                                'FilterConstraintRefs': FilterConstraintRefs,
                                'FilterCheckParamsMetrics': FilterCheckParamsMetrics,
                                'SinkSequence': SinkSequence,
                                }
        self.d_conf = yaml_to_dict('config/conf_coarsegrainedpip.yml')
        self.d_conf['FilterCheckLabel']['parms']['edge_label_list'] = [
            ConstraintType.Coincident, ConstraintType.Distance, ConstraintType.Horizontal,
            ConstraintType.Parallel, ConstraintType.Vertical, ConstraintType.Tangent,
            ConstraintType.Length, ConstraintType.Perpendicular, ConstraintType.Midpoint,
            ConstraintType.Equal, ConstraintType.Diameter, ConstraintType.Radius,
            ConstraintType.Concentric, ConstraintType.Angle, ConstraintType.Subnode]

        self.d_conf['FilterCheckLabel']['parms']['node_label_list'] = [
            EntityType.Point, EntityType.Line,
            EntityType.Circle, EntityType.Arc,
            SubnodeType.SN_Start, SubnodeType.SN_End, SubnodeType.SN_Center,
            EntityType.External, EntityType.Stop]

        self.d_conf['FilterCheckParamsMetrics_Length']['parms']['request'] = {
            ('edge', ConstraintType.Distance): {'length': ['.* METER']},
            ('edge', ConstraintType.Length): {'length': ['.* METER']},
            ('edge', ConstraintType.Diameter): {'length': ['.* METER']},
            ('edge', ConstraintType.Radius): {'length': ['.* METER']},
        }

        self.d_conf['FilterCheckParamsMetrics_Angle']['parms']['request'] = {
            ('edge', ConstraintType.Angle): {'angle': ['.* DEGREE']},
        }
        # old label_list : [ConstraintType.Coincident, ConstraintType.Distance, ConstraintType.Horizontal, EntityType.Point, EntityType.Line]

    def test_pipeline(self):
        pipeline = pipeline_factory(conf=self.d_conf, catalog_filter=self.catalog_filters)
        last_message = pipeline.execute()

        logger.debug(f'Pipeline finished and returned {last_message}')

        input_path = self.d_conf['Source_A']['parms']['file_path']
        input_data = flat_array.load_dictionary_flat(input_path)['sequences']

        logger.info(f"Pipeline input is of length {len(input_data)}")

        output_path = self.d_conf['SinkSequence']['parms']['output_path']
        output_data = flat_array.load_flat_array(output_path)

        for sequence in output_data:
            self.assertIsInstance(sequence, list)

        logger.info(f"Pipeline output is of length {len(output_data)}")
