#!/bin/bash

#SBATCH --job-name=sketchgraphs_preprocessing
#SBATCH --output=output.out
#SBATCH --error=output.err
#SBATCH --qos=an_all_short
#SBATCH --partition=an
#SBATCH --time=01:00:00
#SBATCH --wckey="P11MM:SALOME"
set -x
srun hostname
. /home/f49681/anaconda3/etc/profile.d/conda.sh
now=$(date +"%m_%d_%Y_%H_%M_%S")
folder="scripts/coarse_$now"
mkdir $folder

conda activate sg_prep
srun python experiments/experiment_coarse.py

mv output.err $folder
mv output.out $folder