import sys
sys.path.append('src/sketchgraphs/')
sys.path.append('src/filtering-pipeline')

import unittest
import logging

from experiments.experiment_weight import ExperimentClusterOrder, ExperimentClusterParams

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

# TODO: move into tests/__init__ (https://gitlab.pleiade.edf.fr/cao_ml/sketchgraphs_for_edf/preprocessing/-/issues/32)
MOCK_INDEXES_PATH = 'tests/asset/out/indexes_cluster_order.json'
MOCK_NORMALIZATION_PATH = 'tests/asset/out/normalization_results.npy'
MOCK_WEIGHTS_PATH = 'tests/asset/out/weights_results.npy'

class TestExperimentClusterOrder(unittest.TestCase):

    def test_run_pipeline(self):
        experiment = ExperimentClusterOrder()
        experiment.d_conf['SourceFromFlatArray']['parms']['file_path'] = MOCK_NORMALIZATION_PATH
        experiment.d_conf['SinkDict']['parms']['output_path'] = MOCK_INDEXES_PATH

        experiment.run_pipeline()

class TestExperimentClusterParams(unittest.TestCase):

    def test_run_pipeline(self):
        experiment = ExperimentClusterParams()
        experiment.d_conf['SourceDict']['parms']['indexes'] = MOCK_INDEXES_PATH
        experiment.d_conf['SourceDict']['parms']['data'] = MOCK_NORMALIZATION_PATH
        experiment.d_conf['SinkArray']['parms']['output_path'] = MOCK_WEIGHTS_PATH

        experiment.run_pipeline()