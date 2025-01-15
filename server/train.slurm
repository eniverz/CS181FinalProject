#!/bin/bash
#SBATCH -J train
#SBATCH -p CS172
#SBATCH --gres=gpu:1
#SBATCH --output=%j.out
#SBATCH --error=%j.err

source ~/.bashrc
conda activate 172a2
cd /public/home/CS172/tengzhh2022-cs172/CS181FinalProject/server
python train_dvi.py