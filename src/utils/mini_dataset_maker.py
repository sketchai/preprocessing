from src.utils import flat_array
import numpy as np
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def save_mini_sequence_data(l_sequences, output_file):
    offsets, sequence_data = flat_array.raw_list_flat(l_sequences)
    flat_array_of_sequences = flat_array.pack_list_flat(offsets,sequence_data)

    result = flat_array.pack_dictionary_flat({
            'sequences': flat_array_of_sequences,
        })

    np.save(output_file, result, allow_pickle=False)