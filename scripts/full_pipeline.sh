#!/bin/bash

#SBATCH --job-name=sketchgraphs_preprocessing
#SBATCH --output=scripts/output_full_pipeline.out
#SBATCH --error=scripts/output_full_pipeline.err
#SBATCH --qos=an_all_long_rd
#SBATCH --partition=an
#SBATCH --nodes=1
#SBATCH --time=3-00:00:00
#SBATCH --wckey="P11MM:SALOME"
#SBATCH --exclusive
set -x
srun hostname
. /home/f49681/anaconda3/etc/profile.d/conda.sh
now=$(date +"%m_%d_%Y_%H_%M_%S")
folder="scripts/full_pipeline_$1_$now"
mkdir $folder
STARTTIME=$(date +%s)
dataset=$1

conda activate sg_prep
srun python experiments/full_pipeline.py --dataset $dataset

mv scripts/output_full_pipeline.err $folder
mv scripts/output_full_pipeline.out $folder

ENDTIME=$(date +%s)
echo "Time spent: $((($ENDTIME - $STARTTIME)/ 60)) minutes"
