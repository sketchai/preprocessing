import sys
import os
import logging
import json

import numpy as np

if __name__ == '__main__':
    sys.path.append('sketch_data/')
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, cur_path + "/..")
    logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.DEBUG)

import pickle
from src.utils import flat_array
from src.utils.split import split_train_test_val, f_array_from_idxes, DEFAULT_SPLIT_MODE
from experiments import ENCODING_PATH, NORMALIZATION_PATH, INDEXES_PATH, WEIGHTS_PATH, SUBCLUSTERS_PATH

def split(
    encoded_dataset,
    cluster_path,
    weights_path,
    subcluster_path,
    test_ratio=0.05,
    val_ratio=0.05,
    ):
    
    with open(subcluster_path,'r') as json_file:
        indexes_subclusters = json.load(json_file)

    with open(cluster_path,'r') as json_file:
        d_clusters = json.load(json_file)

    mode = DEFAULT_SPLIT_MODE
    split_indexes = split_train_test_val(
        d_clusters,
        indexes_subclusters,
        test_ratio=test_ratio, val_ratio=val_ratio,
        mode=mode)

    f_array = flat_array.load_flat_array(encoded_dataset)
    encod_offsets, encod_data = f_array._offsets, f_array._pickle_data

    
    for split, seq_idxes in split_indexes.items():

        # save encoded sequences
        offsets, pickle_data = f_array_from_idxes(seq_idxes, encod_offsets, encod_data)
        pack = flat_array.pack_list_flat(offsets, pickle_data)
        path = encoded_dataset.split('.npy')[0] + f'_{split}.npy'
        np.save(path, pack, allow_pickle=False)
        
        if mode[split] == 'all':
            # save weights
            weights = np.load(weights_path)
            w_array = weights[seq_idxes]
            w_path = weights_path.split('.npy')[0] + f'_{split}.npy'
            np.save(w_path, w_array)


def main():
    encoded_dataset = ENCODING_PATH.format('merged')
    cluster_path = INDEXES_PATH.format('merged')
    weights_path = WEIGHTS_PATH.format('merged')
    subcluster_path = SUBCLUSTERS_PATH.format('merged')

    split(encoded_dataset,cluster_path,weights_path,subcluster_path)


if __name__ == '__main__':
    main()
