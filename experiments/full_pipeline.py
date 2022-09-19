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
    parser = argparse.ArgumentParser(description='Run full pipeline')
    parser.add_argument('--dataset', help='train, validation or test', default='merged')
    args = parser.parse_args()
    ExperimentCoarse(dataset=args.dataset).run_pipeline()
    ExperimentConvertSAM(dataset=args.dataset).run_pipeline()
    ExperimentNormalization(dataset=args.dataset).run_pipeline()
    ExperimentClusterOrder(dataset=args.dataset).run_pipeline()
    ExperimentClusterParams(dataset=args.dataset).run_pipeline()
    ExperimentEncoding(dataset=args.dataset).run_pipeline()
    if args.dataset=='merged':
        split_dataset()
    export_parameters()

if __name__ == '__main__':
    main()
