import sys
import unittest
import logging

from experiments.experiment_convert_sam import ExperimentConvertSAM
from tests import MOCK_COARSE_PATH, MOCK_EXCHANGEFORMAT_PATH

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

class TestExperimentCoarse(unittest.TestCase):

    def test_run_pipeline(self):
        experiment = ExperimentConvertSAM()
        experiment.d_conf['SourceFromFlatArray']['parms']['file_path'] = MOCK_COARSE_PATH
        experiment.d_conf['SinkSlices']['parms']['output_path'] =  MOCK_EXCHANGEFORMAT_PATH

        experiment.run_pipeline()
