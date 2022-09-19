import argparse
import sys
import os
import logging

if __name__ == '__main__':
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, cur_path + "/..")
    logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.DEBUG)

from src.utils import flat_array
from sam.primitive import PrimitiveType
from sam.constraint import ConstraintType
from sam.catalog_primitive import Arc, Line, Circle, Point
from sam.catalog_constraint import *

from src.sinks.sink_weights import SinkWeights
from src.sinks.sink_dict import SinkDict

from src.sources.source_fromdict import SourceDict

from src.filters.filter_clusterparamvalues import FilterClusterParamValues
from src.filters.filter_paramsencoding import FilterParamsEncoding
from src.filters.filter_sequenceorderencoding import FilterSequenceOrderEncoding
from src.filters.filter_clustersequences import FilterClusterSequences
from src.filters.filter_encodeorder import FilterEncodeOrder
from src.sources.source_fromflatarray import SourceFromFlatArray
from src.filters.utils.filter_log import FilterLog
from src.utils.to_dict import yaml_to_dict
from filtering_pipeline.factory import pipeline_factory
from experiments import INDEXES_PATH, NORMALIZATION_PATH, SUBCLUSTERS_PATH, WEIGHTS_PATH, L_KEEP_EDGE, L_KEEP_NODE
import json
import numpy as np

logger = logging.getLogger()

class ExperimentClusterOrder():

    def __init__(self, dataset='merged'):
        self.catalog_filters = {
            'SourceFromFlatArray': SourceFromFlatArray,
            'SinkDict': SinkDict,
            'FilterSequenceOrderEncoding': FilterSequenceOrderEncoding,
            'FilterClusterSequences': FilterClusterSequences,
            'FilterEncodeOrder': FilterEncodeOrder,
            'FilterLog': FilterLog,
            }
        self.d_conf = yaml_to_dict('config/conf_clusterorder.yml')
        self.d_conf['FilterEncodeOrder']['parms']['l_keep_edge'] = L_KEEP_EDGE
        self.d_conf['FilterEncodeOrder']['parms']['l_keep_node'] = L_KEEP_NODE

        self.d_conf['SourceFromFlatArray']['parms']['file_path'] = NORMALIZATION_PATH.format(dataset)
        self.d_conf['SinkDict']['parms']['output_path'] = INDEXES_PATH.format(dataset)

    def run_pipeline(self):
        pipeline = pipeline_factory(conf=self.d_conf, catalog_filter=self.catalog_filters)
        last_message = pipeline.execute()

        logger.debug(f'Pipeline finished and returned {last_message}')

        input_path = self.d_conf['SourceFromFlatArray']['parms']['file_path']
        input_data = flat_array.load_flat_array(input_path)

        output_path = self.d_conf['SinkDict']['parms']['output_path']
        with open(output_path, 'r') as dict_file:
            output_data = json.load(dict_file)
        n_sequences = sum(len(cluster) for cluster in output_data.values())

        logger.info(f'Pipeline input is of length {len(input_data)}')
        logger.info(f'Number of sequences clustered : {n_sequences}')
        logger.info(f'Generated {len(output_data)} clusters')

        print(f'Pipeline input is of length {len(input_data)}')
        print((f'Generated {len(output_data)} clusters'))
        print(f'Number of sequences clustered : {n_sequences}')

class ExperimentClusterParams():

    def __init__(self, dataset='train'):
        self.catalog_filters = {
            'SourceDict': SourceDict,
            'FilterClusterParamValues': FilterClusterParamValues,
            'FilterParamsEncoding': FilterParamsEncoding,
            'FilterLog': FilterLog,
            'SinkWeights': SinkWeights,
            }
        self.d_conf = yaml_to_dict('config/conf_clusterparams.yml')

        self.d_conf['FilterParamsEncoding']['parms']['nodes_parametrized'] = {
            Point: ['status_construction', 'x', 'y'],
            Line: ['status_construction', 'pnt1_x', 'pnt1_y', 'pnt2_x', 'pnt2_y'],
            Circle: ['status_construction', 'center_x', 'center_y', 'radius'],
            Arc: ['status_construction', 'center_x', 'center_y', 'radius','angle_start', 'angle_end']
        }

        self.d_conf['SourceDict']['parms']['indexes'] = INDEXES_PATH.format(dataset)
        self.d_conf['SourceDict']['parms']['data'] = NORMALIZATION_PATH.format(dataset)
        self.d_conf['SinkWeights']['parms']['output_path'] = WEIGHTS_PATH.format(dataset)
        self.d_conf['SinkWeights']['parms']['output_path_json'] = SUBCLUSTERS_PATH.format(dataset)

        

    def run_pipeline(self):
        pipeline = pipeline_factory(conf=self.d_conf, catalog_filter=self.catalog_filters)
        last_message = pipeline.execute()

        logger.debug(f'Pipeline finished and returned {last_message}')

        input_path = self.d_conf['SourceDict']['parms']['data']
        input_data = flat_array.load_flat_array(input_path)

        output_path = self.d_conf['SinkWeights']['parms']['output_path']
        output_data = np.load(output_path)

        logger.info(f'Pipeline input is of length {len(input_data)}')
        logger.info(f'Pipeline output is of length {len(output_data)}')

        print(f'Pipeline input is of length {len(input_data)}')
        print(f'Pipeline output is of length {len(output_data)}')

def main():
    parser = argparse.ArgumentParser(description='Run Weights pipeline')
    parser.add_argument('--dataset', help='train, validation or test')
    args = parser.parse_args()
    ExperimentClusterOrder(dataset=args.dataset).run_pipeline()
    ExperimentClusterParams(dataset=args.dataset).run_pipeline()

if __name__ == '__main__':
    main()