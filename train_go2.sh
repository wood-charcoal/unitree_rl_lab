#!/bin/bash

source ~/.bashrc
source ~/miniconda3/etc/profile.d/conda.sh
conda activate env_isaaclab

HYDRA_FULL_ERROR=1 python scripts/rsl_rl/train.py --headless --task Unitree-Go2-Velocity --max_iterations 10000
