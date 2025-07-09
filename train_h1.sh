#!/bin/bash

source ~/.bashrc
source ~/miniconda3/etc/profile.d/conda.sh
conda activate env_isaaclab

HYDRA_FULL_ERROR=1 python scripts/rsl_rl/train.py --headless --task Unitree-H1-Velocity --max_iterations 30000

# python scripts/rsl_rl/play.py --livestream 1 --task Unitree-H1-Velocity --checkpoint logs/rsl_rl/unitree_h1_velocity/2025-07-07_17-35-21/model_19500.pt --num_envs 50
