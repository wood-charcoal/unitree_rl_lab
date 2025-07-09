#!/bin/bash

source ~/.bashrc
source ~/miniconda3/etc/profile.d/conda.sh
conda activate env_isaaclab

python scripts/rsl_rl/train.py --headless --task XHumanoid-Lite0430-Velocity --max_iterations 40000

# python scripts/rsl_rl/play.py --livestream 1 --task XHumanoid-Lite0430-Velocity --checkpoint logs/rsl_rl/xhumanoid_lite0430_velocity/2025-07-07_17-31-54/model_19999.pt --num_envs 50

