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

import pickle
from src.utils.slicing import merge_array_slices
from src.utils import flat_array
from experiments import SKETCHGRAPHS_PATH

def merge(path, pack_dict=False):
    paths = []
    for split in ('train','test','validation'):
        paths.append(path.format(split))
    array = merge_array_slices(slice_path_list=paths)
    merge_path = path.format('merged')
    if pack_dict:
        array = flat_array.pack_dictionary_flat({
            'sequences': array,
        })
    np.save(merge_path,array, allow_pickle=False)

if __name__ == '__main__':
    merge(path=SKETCHGRAPHS_PATH, pack_dict=True)