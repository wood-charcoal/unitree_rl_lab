import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse


def plot_joint_angles(csv_file_path):
    """
    从 CSV 文件中读取并绘制机器人各关节角度随时间的变化。
    
    参数:
        csv_file_path (str): CSV 文件路径
        output_image (str, optional): 图像输出路径。如果未提供，则仅显示图像。
    """
    # 读取 CSV 文件
    df = pd.read_csv(csv_file_path)

    # 检查是否包含 timestamp 列
    if "timestamp" not in df.columns:
        raise ValueError("CSV 文件必须包含 'timestamp' 列")

    # 设置时间为索引
    df.set_index("timestamp", inplace=True)

    # 绘图设置
    plt.figure(figsize=(14, 8))
    for i, column in enumerate(df.columns):
        plt.plot(df.index, df[column], label=column)

    plt.title("Robot Joint Angles Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Joint Angle (radians)")
    plt.grid(True)
    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    plt.tight_layout()

    output_image = csv_file_path.replace(".csv", ".jpg")
    plt.savefig(output_image)
    print(f"[INFO] Plot saved to: {output_image}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot robot joint angles from CSV file.")
    parser.add_argument("--csv", type=str, required=True, help="Path to the CSV file with joint data.")

    args = parser.parse_args()

    plot_joint_angles(args.csv)