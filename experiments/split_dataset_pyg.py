import sys
import os
import logging
import json

import numpy as np

if __name__ == '__main__':
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, cur_path + "/..")
    logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.DEBUG)

from experiments.split_dataset import split
from experiments import ENCODING_PATH_PYG, INDEXES_PATH, WEIGHTS_PATH, SUBCLUSTERS_PATH

def main():
    encoded_dataset = ENCODING_PATH_PYG.format('merged')
    cluster_path = INDEXES_PATH.format('merged')
    weights_path = WEIGHTS_PATH.format('merged')
    subcluster_path = SUBCLUSTERS_PATH.format('merged')

    split(encoded_dataset,cluster_path,weights_path,subcluster_path)


if __name__ == '__main__':
    main()
