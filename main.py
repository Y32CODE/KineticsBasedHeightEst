import os
import sys
import shlex
import subprocess
from pathlib import Path

os.environ.setdefault("ROS_LOCALHOST_ONLY", "1")

dir_path = Path(__file__).resolve().parent
sys.path.append(str(dir_path / ".."))

ros_ws = dir_path / "ros2_ws"
setup_bash = ros_ws / "install" / "setup.bash"

if not setup_bash.exists():
    subprocess.run(
        ["colcon", "build"],
        cwd=ros_ws,
        check=True
    )

if os.environ.get("BASIC_LOCOMOTION_ROS2_SOURCED") != "1":
    cmd = (
        f"source {shlex.quote(str(setup_bash))} && "
        "export BASIC_LOCOMOTION_ROS2_SOURCED=1 && "
        f"exec {shlex.quote(sys.executable)} "
        + " ".join(
            shlex.quote(arg)
            for arg in [
                str(Path(__file__).resolve()),
                *sys.argv[1:]
            ]
        )
    )

    os.execv(
        "/bin/bash",
        ["bash", "-c", cmd]
    )

import rclpy
from rclpy.node import Node

from dls2_interface.msg import (
    BaseState,
    BlindState,
    Imu,
    ControlSignal,
)

#################################

