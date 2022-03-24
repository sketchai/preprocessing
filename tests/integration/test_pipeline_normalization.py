import sys
sys.path.append('src/sketchgraphs/')
sys.path.append('src/filtering-pipeline/')

from sketchgraphs.data import flat_array
from sketchgraphs.data.sequence import ConstraintType, EntityType, SubnodeType
from src.filters.filter_recenterline import FilterRecenterLine
from src.filters.filter_convertmetrics import FilterConvertMetrics
from src.filters.filter_divbymax import FilterDivByMax
from src.filters.filter_barycenter import FilterBarycenter
from src.filters.sink_slices import SinkSlices
from src.filters.filter_on_op import OpSubPipelineFilter
from src.sources.source_fromlist import SourceList
from src.sources.source_fromflatarray import SourceFromFlatArray
from src.utils.to_dict import yaml_to_dict
from filtering_pipeline.factory import pipeline_factory
from filtering_pipeline.filters.catalog_filter.subpipeline_filter import SubPipelineFilter
import numpy as np
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestIntegrationNormalizationPipeline(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.catalog_filters = {'SourceFromFlatArray': SourceFromFlatArray,
                                'OpSubPipelineFilter': OpSubPipelineFilter,
                                'SourceList': SourceList,
                                'FilterBarycenter': FilterBarycenter,
                                'FilterDivByMax': FilterDivByMax,
                                'FilterConvertMetrics': FilterConvertMetrics,
                                'FilterRecenterLine': FilterRecenterLine,
                                'SinkSlices': SinkSlices,
                                }
        self.d_conf = yaml_to_dict('config/conf_normalizationpip.yml')
        self.d_conf['FilterBarycenter_X']['parms']['request'] = {
            ('node', EntityType.Line): 'pntX',
            ('node', EntityType.Point): 'x',
            ('node', EntityType.Circle): 'xCenter',
            ('node', EntityType.Arc): 'xCenter',
        }
        self.d_conf['FilterBarycenter_Y']['parms']['request'] = {
            ('node', EntityType.Line): 'pntY',
            ('node', EntityType.Point): 'y',
            ('node', EntityType.Circle): 'yCenter',
            ('node', EntityType.Arc): 'yCenter',
        }

        self.d_conf['FilterDivByMax']['parms']['request'] = {
            ('node', EntityType.Point): ['x', 'y'],
            ('node', EntityType.Line): ['pntX', 'pntY', 'startParam', 'endParam'],
            ('node', EntityType.Circle): ['xCenter', 'yCenter', 'radius'],
            ('node', EntityType.Arc): ['xCenter', 'yCenter', 'radius'],
            ('edge', ConstraintType.Distance): 'length',
            ('edge', ConstraintType.Length): 'length',
            ('edge', ConstraintType.Diameter): 'length',
            ('edge', ConstraintType.Radius): 'length',
        }

        NB_RGX = r'[-+]?(?:\d*\.\d+|\d+)'

        self.d_conf['FilterConvertMetrics']['parms']['request'] = {
            ('edge', ConstraintType.Distance): {'length': {f'{NB_RGX} METER': 1., }},
            ('edge', ConstraintType.Length): {'length': {f'{NB_RGX} METER': 1.}},
            ('edge', ConstraintType.Diameter): {'length': {f'{NB_RGX} METER': 1.}},
            ('edge', ConstraintType.Radius): {'length': {f'{NB_RGX} METER': 1.}},
            ('edge', ConstraintType.Angle): {'angle': {f'{NB_RGX} DEGREE': np.pi / 180}},
            ('edge', ConstraintType.Angle): {'angle': {f'{NB_RGX} DEGREE': np.pi / 180}},
        }

        self.d_conf['FilterModuloAngle']['parms']['request'] = {
            ('node', EntityType.Arc): ["startParam", "endParam"],
            ('edge', ConstraintType.Angle): "angle",
        }

        # change input and output for testing
        self.d_conf['Source_A']['parms']['file_path'] = 'tests/asset/out/coarse_grained_results.npy'
        self.d_conf['SinkSlices']['parms']['output_path'] = 'tests/asset/out/normalization_results.npy'

    def test_pipeline(self):
        pipeline = pipeline_factory(conf=self.d_conf, catalog_filter=self.catalog_filters)
        last_message = pipeline.execute()

        logger.debug(f'Pipeline finished and returned {last_message}')

        input_path = self.d_conf['Source_A']['parms']['file_path']
        input_data = flat_array.load_flat_array(input_path)

        logger.info(f"Pipeline input is of length {len(input_data)}")

        output_path = self.d_conf['SinkSlices']['parms']['output_path']
        output_data = flat_array.load_flat_array(output_path)

        for sequence in output_data:
            self.assertIsInstance(sequence, list)

        logger.info(f"Pipeline output is of length {len(output_data)}")
        logger.debug([s for s in output_data])
