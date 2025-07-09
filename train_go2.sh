#!/bin/bash

source ~/.bashrc
source ~/miniconda3/etc/profile.d/conda.sh
conda activate env_isaaclab

HYDRA_FULL_ERROR=1 python scripts/rsl_rl/train.py --headless --task Unitree-Go2-Velocity --max_iterations 10000

# python scripts/rsl_rl/play.py --livestream 1 --task Unitree-Go2-Velocity --checkpoint logs/rsl_rl/unitree_go2_velocity/2025-07-06_15-28-16/model_26400.pt --num_envs 50

