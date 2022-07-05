import sys

import unittest
from tests import MOCK_ENCODING_PATH, MOCK_NORMALIZATION_PATH
from experiments.experiment_encoding_pyg import ExperimentEncoding
from src.utils.flat_array import load_flat_array
from src.utils.logger import logger

class TestExperimentEncoding(unittest.TestCase):

    def test_run_pipeline(self):
        experiment = ExperimentEncoding()
        experiment.d_conf['SourceFromFlatArray']['parms']['file_path'] = MOCK_NORMALIZATION_PATH
        experiment.d_conf['SinkDictFlat']['parms']['output_path'] = MOCK_ENCODING_PATH
        experiment.run_pipeline()

        # To see what is inside the dataset
        data = load_flat_array(MOCK_ENCODING_PATH)
        logger.info(f'data: {data}')
        for i,d in enumerate(data) :
            # logger.info(f'd= {d}')
            self.assertEqual(i, d.get('sequence_idx'))

