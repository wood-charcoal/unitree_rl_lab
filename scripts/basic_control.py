import argparse
from isaaclab.app import AppLauncher

# add argparse arguments
parser = argparse.ArgumentParser(description="This script demonstrates basic control of the Unitree H1 robot.")
parser.add_argument("--num_envs", type=int, default=1, help="Number of environments to spawn.")
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

# launch omniverse app
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

# import modules after launching app
import torch
import numpy as np
import isaaclab.sim as sim_utils
from isaaclab.assets import AssetBaseCfg, ArticulationCfg
from isaaclab.scene import InteractiveScene, InteractiveSceneCfg
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.utils import configclass


@configclass
class UnitreeArticulationCfg(ArticulationCfg):
    """Configuration for Unitree articulations."""

    joint_sdk_names: list[str] = None # type: ignore

UNITREE_MODEL_DIR = "/home/ubuntu/projects/robot_model"  # MISSING

UNITREE_H1_CFG = UnitreeArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{UNITREE_MODEL_DIR}/H1/h1/usd/h1.usd",
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            # enabled_self_collisions=False, solver_position_iteration_count=4, solver_velocity_iteration_count=4
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0, 0, 1.1),
        joint_vel={".*": 0.0},
    ),
    soft_joint_pos_limit_factor=0.9,
    actuators={
        # "legs": ImplicitActuatorCfg(
        #     joint_names_expr=[
        #         ".*_hip_yaw_joint",
        #         ".*_hip_roll_joint",
        #         ".*_hip_pitch_joint",
        #         ".*_knee_joint",
        #         "torso_joint",
        #     ],
        #     effort_limit_sim={
        #         ".*_hip_yaw_joint": 200.0,
        #         ".*_hip_roll_joint": 200.0,
        #         ".*_hip_pitch_joint": 200.0,
        #         ".*_knee_joint": 300.0,
        #         "torso_joint": 200.0,
        #     },
        #     velocity_limit_sim={
        #         ".*_hip_yaw_joint": 23.0,
        #         ".*_hip_roll_joint": 23.0,
        #         ".*_hip_pitch_joint": 23.0,
        #         ".*_knee_joint": 14.0,
        #         "torso_joint": 23.0,
        #     },
        #     stiffness={
        #         ".*_hip_.*_joint": 150.0,
        #         ".*_knee_joint": 200.0,
        #         "torso_joint": 300.0,
        #     },
        #     damping={
        #         ".*_hip_.*_joint": 2.0,
        #         ".*_knee_joint": 4.0,
        #         "torso_joint": 6.0,
        #     },
        # ),
        # "feet": ImplicitActuatorCfg(
        #     joint_names_expr=[".*_ankle_joint"],
        #     effort_limit_sim=40.0,
        #     velocity_limit_sim=9.0,
        #     stiffness=40.0,
        #     damping=2.0,
        # ),
        "arms": ImplicitActuatorCfg(
            joint_names_expr=[
                ".*_shoulder_pitch_joint",
                ".*_shoulder_roll_joint",
                ".*_shoulder_yaw_joint",
                ".*_elbow_joint",
            ],
            effort_limit_sim={
                ".*_shoulder_pitch_joint": 40.0,
                ".*_shoulder_roll_joint": 40.0,
                ".*_shoulder_yaw_joint": 18.0,
                ".*_elbow_joint": 18.0,
            },
            velocity_limit_sim={
                ".*_shoulder_pitch_joint": 9.0,
                ".*_shoulder_roll_joint": 9.0,
                ".*_shoulder_yaw_joint": 20.0,
                ".*_elbow_joint": 20.0,
            },
            stiffness={
                ".*_shoulder_pitch_joint": 100.0,
                ".*_shoulder_roll_joint": 50.0,
                ".*_shoulder_yaw_joint": 50.0,
                ".*_elbow_joint": 50.0,
            },
            damping={
                ".*_shoulder_pitch_joint": 2.0,
                ".*_shoulder_roll_joint": 2.0,
                ".*_shoulder_yaw_joint": 2.0,
                ".*_elbow_joint": 2.0,
            },
        ),
    },
    joint_sdk_names=[
        "right_hip_roll_joint",
        "right_hip_pitch_joint",
        "right_knee_joint",
        "left_hip_roll_joint",
        "left_hip_pitch_joint",
        "left_knee_joint",
        "torso_joint",
        "left_hip_yaw_joint",
        "right_hip_yaw_joint",
        "",
        "left_ankle_joint",
        "right_ankle_joint",
        "right_shoulder_pitch_joint",
        "right_shoulder_roll_joint",
        "right_shoulder_yaw_joint",
        "right_elbow_joint",
        "left_shoulder_pitch_joint",
        "left_shoulder_roll_joint",
        "left_shoulder_yaw_joint",
        "left_elbow_joint",
    ],
)

# ========================
# 自定义场景配置类
# ========================
class H1SceneCfg(InteractiveSceneCfg):
    """H1 场景配置"""
    ground = AssetBaseCfg(
        prim_path="/World/defaultGroundPlane",
        spawn=sim_utils.GroundPlaneCfg()
    )
    dome_light = AssetBaseCfg(
        prim_path="/World/Light",
        spawn=sim_utils.DomeLightCfg(intensity=3000.0, color=(0.75, 0.75, 0.75))
    )

    # 添加 H1 机器人
    h1 = UNITREE_H1_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

# ========================
# 控制逻辑函数
# ========================
def run_simulator(sim: sim_utils.SimulationContext, scene: InteractiveScene):
    sim_dt = sim.get_physics_dt()
    sim_time = 0.0
    count = 0

    while simulation_app.is_running():
        # 每 500 步重置一次
        if count % 1000 == 0:
            print("[INFO]: Resetting H1 robot...")
            root_state = scene["h1"].data.default_root_state.clone()
            root_state[:, :3] += scene.env_origins
            scene["h1"].write_root_pose_to_sim(root_state[:, :7])
            scene["h1"].write_root_velocity_to_sim(root_state[:, 7:])
            scene["h1"].write_joint_state_to_sim(
                scene["h1"].data.default_joint_pos.clone(),
                scene["h1"].data.default_joint_vel.clone()
            )
            scene.reset()
            sim.step()
            scene.update(sim_dt)

        wave_action = scene["h1"].data.default_joint_pos.clone()
        wave_action[:, scene["h1"].joint_names.index("left_shoulder_pitch_joint")] += 0.5 * np.sin(np.pi * sim_time)
        wave_action[:, scene["h1"].joint_names.index("right_shoulder_pitch_joint")] -= 0.5 * np.sin(np.pi * sim_time)
        scene["h1"].set_joint_position_target(wave_action)
        # efforts = torch.randn_like(scene["h1"].data.joint_pos) * 2.0
        # # -- apply action to the robot
        # scene["h1"].set_joint_effort_target(efforts)

        scene.write_data_to_sim()
        sim.step()
        sim_time += sim_dt
        count += 1
        scene.update(sim_dt)

# ========================
# 主函数
# ========================
def main():
    # 初始化仿真器
    sim_cfg = sim_utils.SimulationCfg(device=args_cli.device)
    sim = sim_utils.SimulationContext(sim_cfg)
    sim.set_camera_view([2.5, 0.0, 2.5], [0.0, 0.0, 0.5])

    # 构建场景
    scene_cfg = H1SceneCfg(num_envs=args_cli.num_envs, env_spacing=2.0)
    scene = InteractiveScene(scene_cfg)

    # Play the simulator
    sim.reset()

    print("[INFO]: Setup complete...")

    # 运行主循环
    run_simulator(sim, scene)

if __name__ == "__main__":
    main()
    simulation_app.close()