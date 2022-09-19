import argparse
import sys
import os
import logging

if __name__ == '__main__':
    # Add paths for packages
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, cur_path + "/..")
    logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.DEBUG)

from sam.catalog_primitive import *
from sam.catalog_constraint import *

from src.sources.source_fromlist import SourceList
from src.sources.source_fromflatarray import SourceFromFlatArray
from src.filters.on_exchangeformat.filter_boundingbox import FilterBoundingBox
from src.filters.filter_on_op import OpSubPipelineFilter
from src.filters.on_exchangeformat.filter_moduloangle import FilterModuloAngle
from src.filters.utils.filter_log import FilterLog
from src.sinks.sink_slices import SinkSlices
from src.utils.to_dict import yaml_to_dict
from src.utils.flat_array import load_flat_array

from filtering_pipeline.factory import pipeline_factory
from experiments import EXCHANGE_PATH, NORMALIZATION_PATH
import logging

logger = logging.getLogger()

class ExperimentNormalization():

    def __init__(self, dataset='merged'):
        self.catalog_filters = {'SourceFromFlatArray': SourceFromFlatArray,
                                'OpSubPipelineFilter': OpSubPipelineFilter,
                                'SourceList': SourceList,
                                'FilterModuloAngle': FilterModuloAngle,
                                'SinkSlices': SinkSlices,
                                'FilterLog': FilterLog,
                                'FilterBoundingBox': FilterBoundingBox,
                                }
        self.d_conf = yaml_to_dict('config/conf_normalizationpip.yml')
        self.d_conf['FilterBoundingBox']['parms'] ={
            'request_coord': {
                'POINT' : ['x', 'y'],
                'LINE' : ['pnt1', 'pnt2'],
                'ARC' : ['pnt1', 'pnt2','center'],
                'CIRCLE' : 'center',
            },
            'request_length': {
                'ARC' : 'radius',
                'CIRCLE' : 'radius',
                # 'DISTANCE': 'distance_min',
                'LENGTH': 'length',
                'RADIUS': 'radius',
            }}

        self.d_conf['FilterModuloAngle']['parms']['request'] = {
                'ARC': ["angle_start","angle_end"],
                'ANGLE': "angle"
        }

        self.d_conf['SourceFromFlatArray']['parms']['file_path'] = EXCHANGE_PATH.format(dataset)
        self.d_conf['SinkSlices']['parms']['output_path'] = NORMALIZATION_PATH.format(dataset)


    def run_pipeline(self):
        pipeline = pipeline_factory(conf=self.d_conf, catalog_filter=self.catalog_filters)
        last_message = pipeline.execute()

        input_path = self.d_conf['SourceFromFlatArray']['parms']['file_path']
        input_data = load_flat_array(input_path)
        output_path = self.d_conf['SinkSlices']['parms']['output_path']
        output_data = load_flat_array(output_path)

        logger.info(f"Pipeline input is of length {len(input_data)}")
        logger.info(f"Pipeline output is of length {len(output_data)}")

        print(f"Pipeline input is of length {len(input_data)}")
        print(f"Pipeline output is of length {len(output_data)}")

def main():
    parser = argparse.ArgumentParser(description='Run Coarse pipeline')
    parser.add_argument('--dataset', help='train, validation or test')
    args = parser.parse_args()
    ExperimentNormalization(dataset=args.dataset).run_pipeline()

if __name__ == '__main__':
    main()