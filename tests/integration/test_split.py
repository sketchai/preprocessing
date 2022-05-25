import sys
sys.path.append('src/sketch_data/')

import unittest
from experiments.split_dataset import split
from tests import MOCK_ENCODING_PATH, MOCK_NORMALIZATION_PATH, MOCK_INDEXES_PATH, MOCK_SUBCLUSTERS_PATH, MOCK_WEIGHTS_PATH
from src.utils.logger import logger


class TestSplit(unittest.TestCase):

    def test_split(self):
        normalized_dataset = MOCK_NORMALIZATION_PATH
        encoded_dataset = MOCK_ENCODING_PATH
        cluster_path = MOCK_INDEXES_PATH
        weights_path = MOCK_WEIGHTS_PATH
        subcluster_path = MOCK_SUBCLUSTERS_PATH
        split(encoded_dataset,cluster_path,weights_path,subcluster_path,test_ratio=0.2, val_ratio=0.2)
