#!/bin/bash

source ~/.bashrc
source ~/miniconda3/etc/profile.d/conda.sh
conda activate env_isaaclab

python scripts/rsl_rl/train.py --headless --task XHumanoid-Lite0430-Velocity --max_iterations 20000
