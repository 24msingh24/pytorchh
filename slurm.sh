#!/bin/bash
#SBATCH --job-name=test
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=4G
#SBATCH --partition=vgpu20
#SBATCH --gres=gpu:1

source /home/Student/s4823925/miniconda3/bin/activate /home/Student/s4823925/manan
python task2.py

