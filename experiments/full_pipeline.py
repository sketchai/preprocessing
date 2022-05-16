import sys
import os
import logging

if __name__ == '__main__':
    # Add paths for packages
    sys.path.append('src/sketchgraphs/')
    sys.path.append('sam/')
    sys.path.append('src/filtering-pipeline/')
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, cur_path + "/..")
    logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.DEBUG)


import argparse
from experiments.experiment_coarse import ExperimentCoarse
from experiments.experiment_convert_sam import ExperimentConvertExchangeFormat
from experiments.experiment_normalization import ExperimentNormalization
from experiments.experiment_weight import ExperimentClusterOrder, ExperimentClusterParams
from experiments.experiment_encoding import ExperimentEncoding
from experiments.preprocessing_params import export_parameters

logger = logging.getLogger()

def main():
    parser = argparse.ArgumentParser(description='Run full pipeline')
    parser.add_argument('--dataset', help='train, validation or test')
    args = parser.parse_args()
    ExperimentCoarse(dataset=args.dataset).run_pipeline()
    ExperimentConvertExchangeFormat(dataset=args.dataset).run_pipeline()
    ExperimentNormalization(dataset=args.dataset).run_pipeline()
    ExperimentClusterOrder(dataset=args.dataset).run_pipeline()
    ExperimentClusterParams(dataset=args.dataset).run_pipeline()
    ExperimentEncoding(dataset=args.dataset).run_pipeline()
    export_parameters()

if __name__ == '__main__':
    main()