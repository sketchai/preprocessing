import json
import sys

import logging
import unittest
import numpy as np
import os

from src.sinks.sink_weights import SinkWeights

from src.utils.logger import logger


class TestSinkWeights(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.output_path = 'tests/asset/out/test_sinkWeights_output.npy'
        self.output_path_json = 'tests/asset/out/test_sinkWeights_output.json'
        self.clean = True

    def tearDown(self):
        # Clean and remove created files
        if self.clean and os.path.exists(self.output_path):
            os.remove(self.output_path)
        if self.clean and os.path.exists(self.output_path_json):
            os.remove(self.output_path_json)
            
    def test_last_process(self):
        filter1 = SinkWeights({'output_path': self.output_path, 'output_path_json': self.output_path_json})
        indexes = [[0], [ 7, 8, 3, 4,], [1, 2], [5, 6, 9]]
        data = [[1.], [ 8., 9., 4., 5.,], [2., 3.], [6., 7., 10.]]
        l_clusters = [{'(0,0)':[0]},{'(1,0)':[0,3], '(2,0)':[1,2]},{'(3,0)':[0,1]},{'(4,0)':[0,1,2]}]

        for l_idx, weights, clusters in zip(indexes, data, l_clusters):
            message = {'weights': weights, 'list_of_indexes': l_idx, 'd_cluster': clusters}
            filter1.process(message)

        _ = filter1.last_process({})
        loaded_array = np.load(self.output_path, allow_pickle=False)
        self.assertIsNone(np.testing.assert_allclose(loaded_array, np.arange(10)+1))

        with open(self.output_path_json, 'r') as json_file:
            l_dicts = json.load(json_file)
            for d, expected_d in zip(l_dicts,l_clusters):
                self.assertDictEqual(d,expected_d)
