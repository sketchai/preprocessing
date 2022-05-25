import argparse
import sys
import os
import logging
import numpy as np

if __name__ == '__main__':
                
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, cur_path + "/..")
    logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.DEBUG)


from src.sources.source_fromflatarray import SourceFromFlatArray
from src.filters.filter_convert_exchangeformat import FilterConvertSequence
from src.filters.filter_on_op import OpSubPipelineFilter
from src.sources.source_fromlist import SourceList
from src.filters.filter_convertmetrics import FilterConvertMetrics
from src.filters.utils.filter_log import FilterLog
from src.sinks.sink_slices import SinkSlices
from src.utils.to_dict import yaml_to_dict
from src.utils import flat_array

from filtering_pipeline.factory import pipeline_factory
from experiments import EXCHANGE_PATH, COARSE_PATH
from sketchgraphs.data.sequence import ConstraintType, EntityType

logger = logging.getLogger()

class ExperimentConvertSAM():

    def __init__(self, dataset='merged'):
        self.catalog_filters = {
            'SourceFromFlatArray': SourceFromFlatArray,
            'OpSubPipelineFilter': OpSubPipelineFilter,
            'SourceList': SourceList,
            'FilterConvertSequence': FilterConvertSequence,
            'FilterConvertMetrics': FilterConvertMetrics,
            'FilterLog': FilterLog,
            'SinkSlices': SinkSlices
            }
        self.d_conf = yaml_to_dict('config/conf_convert_sam.yml')


        self.d_conf['SourceFromFlatArray']['parms']['file_path'] = COARSE_PATH.format(dataset)
        self.d_conf['SinkSlices']['parms']['output_path'] = EXCHANGE_PATH.format(dataset)
        NB_RGX = r'[-+]?(?:\d*\.\d+|\d+)'

        self.d_conf['FilterConvertMetrics']['parms']['request'] = {
            ('edge', ConstraintType.Distance): {'length': {f'{NB_RGX} METER': 1., }},
            ('edge', ConstraintType.Length): {'length': {f'{NB_RGX} METER': 1.}},
            ('edge', ConstraintType.Diameter): {'length': {f'{NB_RGX} METER': 1.}},
            ('edge', ConstraintType.Radius): {'length': {f'{NB_RGX} METER': 1.}},
            ('edge', ConstraintType.Angle): {'angle': {f'{NB_RGX} DEGREE': np.pi / 180}},
            ('edge', ConstraintType.Angle): {'angle': {f'{NB_RGX} DEGREE': np.pi / 180}},
        }

    def run_pipeline(self):
        pipeline = pipeline_factory(conf=self.d_conf, catalog_filter=self.catalog_filters)
        last_message = pipeline.execute()

        x = self.d_conf['SourceFromFlatArray']['parms']['file_path']
        print(f'here = {x}')
        input_path = self.d_conf['SourceFromFlatArray']['parms']['file_path']
        input_data = flat_array.load_flat_array(input_path)
        output_path = self.d_conf['SinkSlices']['parms']['output_path']
        output_data = flat_array.load_flat_array(output_path)

        logger.info(f"Pipeline input is of length {len(input_data)}")
        logger.info(f"Pipeline output is of length {len(output_data)}")

        print(f"Pipeline input is of length {len(input_data)}")
        print(f"Pipeline output is of length {len(output_data)}")
        print(f"Data saved: {output_path}")



def main():
    parser = argparse.ArgumentParser(description='Run Weights pipeline')
    parser.add_argument('--dataset', help='train, validation or test')
    args = parser.parse_args()
    ExperimentConvertSAM(dataset=args.dataset).run_pipeline()

if __name__ == '__main__':
    main()