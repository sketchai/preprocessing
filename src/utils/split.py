import io
import json
from src.utils import flat_array
import numpy as np
from src.utils import logger

DEFAULT_SPLIT_MODE = {
    'train': 'all',
    'val': 'subcluster',
    'test': 'subcluster',
}

def split_train_test_val(d_clusters, l_subclusters=None, test_ratio=0.05, val_ratio=0.05, mode=DEFAULT_SPLIT_MODE)->None:
    """
    Splits a list of sketches between train, test and validation without splitting clusters

    returns a dict of indexes
    """

    n_clusters = len(d_clusters)
    idx_cluster_val = int((1-val_ratio-test_ratio)*n_clusters)
    idx_cluster_test = int((1-test_ratio)*n_clusters)

    split_indexes = {}
    for split in ['train','val','test']:

        if split == 'train':
            seq_idxes = _select_indexes_from_cluster(
                d_clusters, mode=mode[split], l_subclusters=l_subclusters,
                idx_max=idx_cluster_val)

        elif split == 'val':
            seq_idxes = _select_indexes_from_cluster(
                d_clusters, mode=mode[split], l_subclusters=l_subclusters,
                idx_min=idx_cluster_val, idx_max=idx_cluster_test)
        
        elif split == 'test':
            seq_idxes = _select_indexes_from_cluster(
                d_clusters, mode=mode[split], l_subclusters=l_subclusters,
                idx_min=idx_cluster_test)

        split_indexes[split] = seq_idxes
        print(f'{split} : {len(seq_idxes)} elts')

    return split_indexes

def f_array_from_idxes(l_idx, offsets, pickle_data):
    """
    given a flat array represented by (offsets, pickle_data)
    l_idx is a list of indexes to extract

    returns new flat offsets and bytes indexed by l_idx
    """
    output_offsets = np.empty(len(l_idx) + 1, dtype=np.dtype('<i8'))
    output_offsets[0] = 0
    current_offset = 0
    l_pickle = []
    for i, idx in enumerate(l_idx):
        seq_pickle = pickle_data[offsets[idx]:offsets[idx+1]]
        l_pickle.append(seq_pickle)
        current_offset += len(seq_pickle)
        output_offsets[i + 1] = current_offset
    output_array = np.concatenate(l_pickle)
    return output_offsets, output_array


def _select_indexes_from_cluster(d_clusters: dict, mode = 'cluster', l_subclusters=None, idx_min=None, idx_max=None,):
    """
    returns a list of sequence indexes in the flat array depending on clusters

    modes: 
        'cluster': one element per cluster is picked
        'subcluster': one element per subcluster is picked
        'all': all elements are picked

    Args
        d_clusters: dict
        indexes_subcluster_path [optional]: str
        idx_min [optional]: int, idx of first cluster
        idx_max [optional]: int, idx of last cluster
                
    """
    
    idxes_to_keep = []

    keys = list(d_clusters)
    idx_min = idx_min or 0
    idx_max = idx_max or len(keys)

    if mode == 'subcluster':
        for i in range(idx_min, idx_max):
            # get the list of sequence indexes
            l_idx_cluster = d_clusters[keys[i]]
            subcluster = l_subclusters[i]
            for l_idx_sub in subcluster.values():
                # get only one element per sub cluster
                first_element = l_idx_sub[0]
                seq_idx = l_idx_cluster[first_element]
                idxes_to_keep.append(seq_idx)

    elif mode == 'cluster':
        for i in range(idx_min, idx_max):
            l_idx_cluster = d_clusters[keys[i]]
            # get only one element per cluster
            idxes_to_keep.append(l_idx_cluster[0])

    elif mode == 'all':
        for i in range(idx_min, idx_max):
            l_idx_cluster = d_clusters[keys[i]]
            # get all elements of cluster
            idxes_to_keep.extend(l_idx_cluster)

    return idxes_to_keep
        


def split_flat_array(array, idx_split)->tuple:
    """splits a flat array in two"""
    offsets, sequence_data = array._offsets, array._pickle_data
    data0, offsets0 = sequence_data[:idx_split], offsets[:idx_split]
    data1, offsets1 = sequence_data[idx_split:], offsets[idx_split:]
    offsets1 -= offsets1[0]
    split0 = flat_array.FlatSerializedArray(offsets=offsets0,pickle_data=data0)
    split1 = flat_array.FlatSerializedArray(offsets=offsets1,pickle_data=data1)
    return split0, split1
