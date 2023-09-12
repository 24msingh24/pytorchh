#!/bin/bash
#SBATCH --job-name=test
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --partition=vgpu20
#SBATCH --gres=gpu:1

source activate /home/Student/s4823925/manan  

/home/Student/s4823925/manan/bin/python /home/Student/s4823925/pytorchh/task2.py
