#!/bin/bash
#SBATCH --job-name=test
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=8G
#SBATCH --partition=vgpu
#SBATCH --gres=gpu:1

source /home/Student/s4823925/miniconda3/bin/activate /home/Student/s4823925/manan
python task2.py

