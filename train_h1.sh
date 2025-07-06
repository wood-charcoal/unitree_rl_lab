#!/bin/bash

source ~/.bashrc
source ~/miniconda3/etc/profile.d/conda.sh
conda activate env_isaaclab

python scripts/rsl_rl/train.py --headless --task Unitree-H1-Velocity
