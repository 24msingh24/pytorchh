#!/bin/bash 
#SBATCH --job-name=manann
#SBATCH --mail-type=All
#SBATCH --mail-user=manandeep.singh@uqconnect.edu.au
#SBATCH --partition=vgpu
#SBATCH --gres=gpu:1

python ~/pytorchh/task2.py