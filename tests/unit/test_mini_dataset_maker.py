import sys

from src.utils.mini_dataset_maker import save_mini_sequence_data
from sketchgraphs.data.sequence import NodeOp, EdgeOp
import logging
import unittest
import os
from sketchgraphs.data import flat_array

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class TestMiniDatasetMaker(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.output_path = 'tests/asset/out/mini_file.npy'
        self.clean = True
        sequence1 = [NodeOp(label=2), EdgeOp(label=2, references=None), NodeOp(label=1)]
        sequence2 = [NodeOp(label=2)]
        sequence3 = [EdgeOp(label=2, references=None)]
        self.list_of_seqs = [sequence1, sequence2, sequence3]

    def tearDown(self):
        # Clean and remove created files
        if self.clean and os.path.exists(self.output_path):
            os.remove(self.output_path)

    def test_save_mini_sequence_data(self):

        save_mini_sequence_data(self.list_of_seqs,output_file=self.output_path)

        saved_sequences = flat_array.load_dictionary_flat(self.output_path)['sequences']
        for og_seq, saved_seq in zip(self.list_of_seqs, saved_sequences):
            self.assertEqual(og_seq, saved_seq)
