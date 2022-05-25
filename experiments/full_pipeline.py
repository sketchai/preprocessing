import sys
import os
import logging

if __name__ == '__main__':
    # Add paths for packages
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, cur_path + "/..")
    logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.DEBUG)


import argparse
from experiments.experiment_coarse import ExperimentCoarse
from experiments.experiment_convert_sam import ExperimentConvertSAM
from experiments.experiment_normalization import ExperimentNormalization
from experiments.experiment_weight import ExperimentClusterOrder, ExperimentClusterParams
from experiments.experiment_encoding import ExperimentEncoding
from experiments.preprocessing_params import export_parameters
from experiments.split_dataset import main as split_dataset

logger = logging.getLogger()

def main():
    ExperimentCoarse(dataset='merged').run_pipeline()
    ExperimentConvertSAM(dataset='merged').run_pipeline()
    ExperimentNormalization(dataset='merged').run_pipeline()
    ExperimentClusterOrder(dataset='merged').run_pipeline()
    ExperimentClusterParams(dataset='merged').run_pipeline()
    ExperimentEncoding(dataset='merged').run_pipeline()
    split_dataset()
    export_parameters()

if __name__ == '__main__':
    main()