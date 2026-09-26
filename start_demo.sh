#!/bin/bash

echo "=================================================="
echo " Launching Autonomous Navigation Control Center"
echo "=================================================="

source /opt/ros/kilted/setup.bash
source ~/robust-visual-navigation/install/setup.bash

# 1. Launch Gazebo Simulation World
ros2 launch visual_navigation_robot gazebo.launch.py &
sleep 3

# 2. Launch Sensor Fusion Stack
ros2 launch visual_navigation_robot mapping.launch.py sensor_config:=s4 &
sleep 2

# 3. Start Waypoint Navigator Node
ros2 run visual_navigation_robot waypoint_navigator --ros-args -p use_sim_time:=true &

# 4. Start ROSBridge WebSocket Bridge (Port 9090)
ros2 launch rosbridge_server rosbridge_websocket_launch.xml address:=0.0.0.0 &

# 5. Start Web Video Server (Port 8080)
ros2 run web_video_server web_video_server &

echo "=================================================="
echo " Open Web Dashboard at: "
echo " file:///home/minat/robust-visual-navigation/src/visual_navigation_robot/web_ui/index.html"
echo "=================================================="

wait