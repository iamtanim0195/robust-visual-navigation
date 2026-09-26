#!/bin/bash

echo "=================================================="
echo " Launching Nav2 Autonomous Navigation Dashboard"
echo "=================================================="

source /opt/ros/kilted/setup.bash
source ~/robust-visual-navigation/install/setup.bash

MAP_PATH="$(ros2 pkg prefix visual_navigation_robot)/share/visual_navigation_robot/config/building_map.yaml"

# 1. Launch Gazebo Simulation World
ros2 launch visual_navigation_robot gazebo.launch.py &
sleep 3

# 2. Launch Perception & Sensor Fusion Stack
ros2 launch visual_navigation_robot mapping.launch.py sensor_config:=s4 &
sleep 2

# 3. Launch Nav2 Stack (Costmaps + Global/Local Planners)
ros2 launch nav2_bringup bringup_launch.py use_sim_time:=true map:=$MAP_PATH &
sleep 3

# 4. Launch Nav2 Room Navigator Node
ros2 run visual_navigation_robot nav2_room_navigator --ros-args -p use_sim_time:=true &

# 5. Start ROSBridge WebSocket (Port 9090)
ros2 launch rosbridge_server rosbridge_websocket_launch.xml address:=0.0.0.0 &

# 6. Start Web Video Server (Port 8080)
ros2 run web_video_server web_video_server &

echo "=================================================="
echo " Open Web Dashboard at: "
echo " file:///home/minat/robust-visual-navigation/src/visual_navigation_robot/web_ui/index.html"
echo "=================================================="

wait